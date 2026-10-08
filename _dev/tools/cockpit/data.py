"""Read-only data layer for the ledger review cockpit.

Nothing here writes a file. Workbooks are read from an in-memory copy of their
bytes, filings are parsed in memory, and the mechanical checker runs in-process
with its report kept only in a cache. The cockpit never reads ``ref/``.

The quote locator reproduces both filing renderings that ``check_lean`` accepts
(``soup.get_text(" ")`` and ``soup.get_text("")``, each normalized with
``normalize_contiguous``) and maps every character of a match back to a position
in the displayed filing blocks, so a quote the checker accepts can be
highlighted.

NFC normalization runs per text node here but over the whole text in the
checker, so a combining mark that starts a new text node could compose
differently. None of the real filings hits this; the tests compare the two
renderings with the checker's directly.
"""

from __future__ import annotations

import bisect
import zipfile
from array import array
import csv
import datetime as dt
import io
import re
import sys
import threading
import unicodedata
from pathlib import Path
from typing import Any

TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import check_lean  # noqa: E402
import derive_analysis  # noqa: E402
import review_list  # noqa: E402
import openpyxl  # noqa: E402
from openpyxl.utils.exceptions import InvalidFileException  # noqa: E402
from bs4 import BeautifulSoup, CData, NavigableString, Tag  # noqa: E402

REPO_ROOT = TOOLS_DIR.parents[1]
SLUG_RE = re.compile(r"[a-z0-9][a-z0-9-]*")

LEDGER_SHEET = "Deal ledger"
ROUNDS_SHEET = "Rounds"
QUESTIONS_SHEET = "Questions"
FACTS_SHEET = "Deal facts"
QUOTE_COLUMN = "Quote and page"

# Elements that start a new display block. Text directly inside any other
# element (font, span, b, a, ...) flows inline with its neighbours.
BLOCK_TAGS = frozenset(
    "address article aside blockquote body caption center dd div dl dt figcaption figure footer "
    "form h1 h2 h3 h4 h5 h6 header html li main nav ol p pre section table tbody td tfoot th thead "
    "title tr ul".split()
)
HEADING_TAGS = frozenset("h1 h2 h3 h4 h5 h6".split())
CELL_TAGS = frozenset(("td", "th"))
TEXT_TYPES = (NavigableString, CData)  # exactly the types Tag.get_text() yields
TOKEN_RE = re.compile(r"\S+")
# Characters that print nothing. They stay in the text (the checker keeps
# them), but a block or table cell made only of them counts as empty.
INVISIBLE_RE = re.compile(r"[\s\u200b\u200c\u200d\u2060\ufeff]+")
# A list bullet or Q:/A: label that EDGAR puts in its own element, joined to
# the text that follows it.
LABEL_RE = re.compile(r"[\u2022\u25cf\u00b7\u25aa\u25a0\u25e6\u2219\u2023\u2043\u2013\u2014*-]|[QA]:")
# Table cells that belong to the neighbouring number: "$ | 159.8", "(40.9 | )".
GLUE_NEXT = frozenset(("$", "(", "($"))
GLUE_PREVIOUS = frozenset((")", "%", ")%"))
TOC_LINK_RE = re.compile(r"(?:back\s+to\s+)?table\s+of\s+contents", re.I)
BOLD_STYLE_RE = re.compile(r"font-weight:\s*(bold|[6-9]00)", re.I)
# A table row with this much text is a layout container, not a data row.
ROW_TEXT_LIMIT = 3000
# Printed page labels: 24, A-1, B-12, B-2-B, ii. See page_label() for the
# dashes and parentheses that may surround them.
PAGE_LABEL_RE = re.compile(
    r"(?:(?:Ex\.?|Annex)\s+)?(?:[A-Z]{1,2}\s?-\s?)?(?:\d{1,4}|[ivxlc]{1,7})(?:\s?-\s?[A-Z])?", re.I
)
ROMAN_IN_PARENS_RE = re.compile(r"\(\s*([ivxlc]{1,7})\s*\)", re.I)
BACKGROUND_RE = re.compile(
    r"^background\s+(?:of|to)\s+the\s+(?:proposed\s+)?(?:merger|mergers|offer|transaction|transactions|acquisition)\b",
    re.I,
)
PAGES_RELIABLE_SHARE = 0.9
MIN_MAIN_RUN = 10


class DealNotFound(LookupError):
    """Unknown or invalid deal slug."""


class DealUnavailable(LookupError):
    """A known deal whose workbook or filing cannot be read right now."""


def visible(text: str) -> str:
    """Return text without whitespace and zero-width characters."""

    return INVISIBLE_RE.sub("", text)


def page_label(text: str) -> str | None:
    """Return the printed page label a short line spells, or None.

    Accepts 24, A-1, B-2-B, ii, and the same wrapped in dashes (-ii-, - 7 -)
    or a roman numeral in parentheses ((ii)).
    """

    text = text.strip()
    if len(text) > 16:
        return None
    core = INVISIBLE_RE.sub(" ", text).strip(" -\u2013\u2014")
    roman = ROMAN_IN_PARENS_RE.fullmatch(core)
    if roman:
        core = roman.group(1)
    if core and PAGE_LABEL_RE.fullmatch(core):
        return re.sub(r"\s+", "", core)
    return None


# ---------------------------------------------------------------------------
# Cell display


def display_value(value: Any) -> str:
    """Show a cell value: dates as YYYY-MM-DD, whole floats without .0, None as ""."""

    if value is None:
        return ""
    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"
    if isinstance(value, dt.datetime):
        return value.date().isoformat()
    if isinstance(value, dt.date):
        return value.isoformat()
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return repr(value)
    return str(value)


# ---------------------------------------------------------------------------
# Filing parsing


def _style_flags(tag: Tag) -> tuple[bool, bool]:
    style = re.sub(r"\s+", "", str(tag.get("style") or "")).lower()
    before = "page-break-before:always" in style or "break-before:page" in style
    after = "page-break-after:always" in style or "break-after:page" in style
    return before, after


def _after_subtree(tag: Tag) -> Any:
    last: Any = tag
    while isinstance(last, Tag) and last.contents:
        last = last.contents[-1]
    return last.next_element


class _Block:
    __slots__ = ("kind", "parts", "length", "segment", "bold")

    def __init__(self, kind: str, segment: int) -> None:
        self.kind = kind
        self.parts: list[str] = []
        self.length = 0
        self.segment = segment
        self.bold = True

    def append(self, text: str) -> int:
        offset = self.length
        self.parts.append(text)
        self.length += len(text)
        return offset

    @property
    def text(self) -> str:
        return "".join(self.parts)


class _Rendering:
    """One checker rendering, built token by token with a map to blocks."""

    __slots__ = ("parts", "length", "pending", "starts", "blocks", "offsets")

    def __init__(self) -> None:
        self.parts: list[str] = []
        self.length = 0
        self.pending = False
        self.starts: list[int] = []
        self.blocks: list[int] = []
        self.offsets: list[int] = []

    def token(self, token: str, block: int, offset: int) -> None:
        if self.pending and self.length:
            self.parts.append(" ")
            self.length += 1
        self.pending = False
        self.starts.append(self.length)
        self.blocks.append(block)
        self.offsets.append(offset)
        self.parts.append(token)
        self.length += len(token)

    def finish(self) -> tuple[str, array, array, array]:
        text = "".join(self.parts)
        self.parts = []
        return text, array("i", self.starts), array("i", self.blocks), array("i", self.offsets)


def _is_label_block(block: _Block) -> bool:
    return block.kind != "row" and block.length <= 12 and bool(LABEL_RE.fullmatch(visible(block.text)))


def is_toc_link(text: str) -> bool:
    """True for the "Table of Contents" back-link EDGAR repeats on every page."""

    return bool(TOC_LINK_RE.fullmatch(INVISIBLE_RE.sub(" ", text).strip()))


def _promotable(text: str) -> bool:
    """A short bold paragraph reads as a heading, but not a lone label or a
    page's "Table of Contents" back-link."""

    return 3 < len(visible(text)) and len(text) <= 150 and not is_toc_link(text)


class Filing:
    """Display blocks, printed pages and the two checker renderings of one filing."""

    def __init__(self, raw: bytes) -> None:
        soup = BeautifulSoup(raw, "html.parser")
        for element in soup(["script", "style", "noscript"]):
            element.decompose()
        self._row_ok: dict[int, bool] = {}
        self._build(soup)
        self._detect_pages()
        self.background_block = self._find_background()
        if self.background_block is not None:
            segment = self.blocks_raw[self.background_block].segment
            if not self._main_run[0] <= segment <= self._main_run[1]:
                self.pages_reliable = False

    # -- construction -----------------------------------------------------

    def _context(self, node: Any) -> tuple[Any, str, Any, Any, bool]:
        """Return (block key, kind, cell key, inner block key, bold) for a string."""

        inner = None
        cell = None
        bold = False
        heading = False
        for parent in node.parents:
            name = parent.name
            if name in ("b", "strong"):
                bold = True
            elif inner is None and parent.get("style") and BOLD_STYLE_RE.search(str(parent.get("style"))):
                bold = True
            if name in HEADING_TAGS and inner is None:
                heading = True
            if name in CELL_TAGS and cell is None:
                cell = parent
            if name == "tr":
                if self._row_is_data(parent):
                    return id(parent), "row", id(cell), id(inner), bold
                cell = None
            if name in BLOCK_TAGS and inner is None:
                inner = parent
                if parent.get("style") and BOLD_STYLE_RE.search(str(parent.get("style"))):
                    bold = True
        if inner is None:
            return None, "p", None, None, bold
        return id(inner), ("h" if heading else "p"), None, id(inner), bold

    def _row_is_data(self, tr: Tag) -> bool:
        key = id(tr)
        ok = self._row_ok.get(key)
        if ok is None:
            ok = len(tr.get_text()) <= ROW_TEXT_LIMIT
            self._row_ok[key] = ok
        return ok

    def _build(self, soup: BeautifulSoup) -> None:
        break_before: set[int] = set()
        break_after: set[int] = set()
        for tag in soup.find_all(style=True):
            before, after = _style_flags(tag)
            if before:
                break_before.add(id(tag))
            if after:
                marker = _after_subtree(tag)
                if marker is not None:
                    break_after.add(id(marker))
        if not break_before and not break_after:
            break_before = {id(tag) for tag in soup.find_all("hr")}
        breaks = break_before | break_after

        blocks: list[_Block] = []
        spaced = _Rendering()  # soup.get_text(" ")
        joined = _Rendering()  # soup.get_text("")
        segment = 0
        current: _Block | None = None
        current_key: Any = object()
        current_cell: Any = None  # the row cell that last added visible text
        cell_text = ""  # visible text of that cell so far
        current_inner: Any = None
        display_pending = False  # whitespace or a line break since the last token
        first_string = True

        for node in soup.descendants:
            if id(node) in breaks:
                segment += 1
                current = None
                current_key = object()
            if isinstance(node, Tag):
                if node.name == "br":
                    display_pending = True
                continue
            if type(node) not in TEXT_TYPES:
                continue
            text = unicodedata.normalize("NFC", str(node)).replace("\u00a0", " ")
            # get_text(" ") puts a separator between every pair of strings.
            if not first_string:
                spaced.pending = True
            first_string = False
            tokens = list(TOKEN_RE.finditer(text))
            if not tokens:
                if text:
                    joined.pending = True
                    display_pending = True
                continue
            if tokens[0].start() > 0:
                joined.pending = True
                display_pending = True
            key, kind, cell, inner, bold = self._context(node)
            shown = visible(text)
            # The separator only shapes the displayed text. It is chosen
            # before the tokens are appended, so every recorded offset
            # already includes it.
            if current is None or key != current_key or key is None:
                if current is not None and _is_label_block(current) and kind != "row":
                    # A bullet or Q:/A: label in its own element joins the
                    # text that follows it (zero-width filler is glued on).
                    separator = " " if shown else ""
                else:
                    current = _Block(kind, segment)
                    blocks.append(current)
                    separator = ""
                    current_cell = None
                    cell_text = ""
                current_key = key
                if kind == "row" and shown:
                    current_cell = cell
            elif kind == "row" and cell != current_cell:
                if not shown:
                    separator = ""  # a spacer cell of zero-width characters
                elif not visible(current.text):
                    separator = ""
                elif cell_text in GLUE_NEXT or shown in GLUE_PREVIOUS:
                    separator = ""
                elif LABEL_RE.fullmatch(cell_text):
                    separator = " "
                else:
                    separator = " | "
                if shown:
                    current_cell = cell
                    cell_text = ""
            elif display_pending or inner != current_inner:
                separator = " "
            else:
                separator = ""
            current_inner = inner
            if kind == "row" and cell == current_cell:
                cell_text += shown
            if separator and current.length:
                current.append(separator)
            index = len(blocks) - 1
            previous_end = None
            for match in tokens:
                if previous_end is not None:
                    current.append(" ")
                    joined.pending = True
                    spaced.pending = True
                word = match.group()
                offset = current.append(word)
                spaced.token(word, index, offset)
                joined.token(word, index, offset)
                previous_end = match.end()
            if shown:
                current.bold = current.bold and bold
            display_pending = False
            if previous_end is not None and previous_end < len(text):
                joined.pending = True
                display_pending = True

        self.blocks_raw = blocks
        self.texts = [block.text for block in blocks]
        self.kinds = []
        for block, text in zip(blocks, self.texts):
            block.parts = []  # the joined text is kept in self.texts
            kind = block.kind
            if kind == "h" and is_toc_link(text):
                kind = "p"  # a page's "Table of Contents" back-link, not a section
            elif kind == "p" and block.bold and _promotable(text):
                kind = "h"
            self.kinds.append(kind)
        self.renderings: dict[str, tuple[str, array, array, array]] = {
            sep: rendering.finish() for sep, rendering in ((" ", spaced), ("", joined))
        }

    def _detect_pages(self) -> None:
        """Label each page-break segment with the printed page number at its foot."""

        by_segment: dict[int, list[int]] = {}
        for index, block in enumerate(self.blocks_raw):
            by_segment.setdefault(block.segment, []).append(index)
        labels: dict[int, str] = {}
        for segment, indexes in by_segment.items():
            # EDGAR filers print the folio as the last short line of the page.
            for index in indexes[::-1][:3]:
                label = page_label(self.texts[index])
                if label is not None:
                    labels[segment] = label
                    break
        self.page_of_block: list[str | None] = [labels.get(block.segment) for block in self.blocks_raw]
        self.pages: list[dict[str, Any]] = [
            {"page": labels[segment], "block": by_segment[segment][0]}
            for segment in sorted(by_segment)
            if segment in labels
        ]

        # The longest run of consecutive segments numbered n, n+1, n+2, ...
        # is the proxy's main body; the narrative lives there.
        ordered = sorted(by_segment)
        best = (0, -1, -1)
        run_start = None
        previous: int | None = None
        for position, segment in enumerate(ordered):
            label = labels.get(segment, "")
            number = int(label) if label.isdigit() else None
            continues = number is not None and previous is not None and number == previous + 1
            if not (continues and run_start is not None):
                run_start = position if number is not None else None
            previous = number
            if run_start is not None and position - run_start + 1 > best[0]:
                best = (position - run_start + 1, ordered[run_start], segment)
        numbers = [int(labels[s]) for s in ordered if labels.get(s, "").isdigit()]
        steps = list(zip(numbers, numbers[1:]))
        unit_steps = sum(1 for a, b in steps if b == a + 1)
        self._main_run = (best[1], best[2])
        self.pages_reliable = bool(
            best[0] >= MIN_MAIN_RUN and steps and unit_steps >= PAGES_RELIABLE_SHARE * len(steps)
        )

    def _find_background(self) -> int | None:
        candidates = [
            index
            for index, (kind, text) in enumerate(zip(self.kinds, self.texts))
            if kind != "row" and len(text) <= 120 and BACKGROUND_RE.match(text.strip())
        ]
        if not candidates:
            return None
        # The table of contents and cross-references are short; the real
        # section is followed by the most narrative before the next heading.
        def narrative(index: int) -> int:
            total = 0
            for following in range(index + 1, min(index + 400, len(self.texts))):
                if self.kinds[following] == "h" and total > 2000:
                    break
                total += len(self.texts[following])
            return total

        headings = [index for index in candidates if self.kinds[index] == "h"] or candidates
        return max(headings, key=lambda index: (narrative(index), -index))

    # -- queries ----------------------------------------------------------

    def blocks_payload(self) -> list[dict[str, Any]]:
        """The /api/filing blocks: kind, displayed text and printed page."""

        return [
            {"kind": kind, "text": text, "page": page}
            for kind, text, page in zip(self.kinds, self.texts, self.page_of_block)
        ]

    def _position(self, sep: str, char: int) -> tuple[int, int]:
        _, starts, blocks, offsets = self.renderings[sep]
        token = bisect.bisect_right(starts, char) - 1
        return blocks[token], offsets[token] + (char - starts[token])

    def _pages_between(self, start_block: int, end_block: int) -> list[str]:
        pages: list[str] = []
        for index in range(start_block, end_block + 1):
            page = self.page_of_block[index]
            if page is not None and page not in pages:
                pages.append(page)
        return pages

    def locate(self, passage: str, cited_page: str | None) -> dict[str, Any]:
        """Locate a normalized passage exactly as the checker tests it."""

        result: dict[str, Any] = {
            "text": passage,
            "cited_page": cited_page,
            "located": False,
            "rendering": None,
            "start": None,
            "end": None,
            "found_page": None,
            "occurrences": 0,
        }
        if not passage:
            return result
        cited = cited_pages(cited_page)
        for sep in (" ", ""):
            text = self.renderings[sep][0]
            hits: list[int] = []
            at = text.find(passage)
            while at >= 0:
                hits.append(at)
                at = text.find(passage, at + 1)  # overlapping repeats count too
            if not hits:
                continue
            chosen = None
            for hit in hits:
                start = self._position(sep, hit)
                end_block, end_offset = self._position(sep, hit + len(passage) - 1)
                pages = self._pages_between(start[0], end_block)
                candidate = (start, (end_block, end_offset + 1), pages)
                if chosen is None:
                    chosen = candidate
                if cited and cited.intersection(pages):
                    chosen = candidate
                    break
            assert chosen is not None
            (start_block, start_offset), (end_block, end_offset), pages = chosen
            result.update(
                located=True,
                rendering=sep,
                start={"block": start_block, "offset": start_offset},
                end={"block": end_block, "offset": end_offset},
                found_page=("–".join((pages[0], pages[-1])) if len(pages) > 1 else (pages[0] if pages else None)),
                occurrences=len(hits),
                _pages=pages,
            )
            return result
        return result


def cited_pages(value: str | None) -> set[str]:
    """Expand a cited page reference such as ``24``, ``30-31`` or ``30, 32``."""

    pages: set[str] = set()
    if not value:
        return pages
    for part in re.split(r"\s*,\s*", value):
        bounds = [piece.strip() for piece in re.split(r"\s*[-–—]\s*", part) if piece.strip()]
        if len(bounds) == 2 and bounds[0].isdigit() and bounds[1].isdigit():
            low, high = int(bounds[0]), int(bounds[1])
            if high < low and len(bounds[1]) < len(bounds[0]):  # 130-31
                high = int(bounds[0][: len(bounds[0]) - len(bounds[1])] + bounds[1])
            if 0 <= high - low <= 50:
                pages.update(str(page) for page in range(low, high + 1))
                continue
        if bounds:
            # A-1 style labels contain a hyphen that is not a range.
            pages.add(re.sub(r"\s+", "", part))
            pages.update(bounds)
    return pages


# ---------------------------------------------------------------------------
# Workbook reading


def _sheet_table(wb: Any, name: str) -> tuple[list[str], list[tuple[int, list[Any]]]]:
    if name not in wb.sheetnames:
        return [], []
    ws = wb[name]
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return [], []
    header = list(rows[0])
    while header and check_lean.is_blank(header[-1]):
        header.pop()
    columns = [display_value(value) for value in header]
    body: list[tuple[int, list[Any]]] = []
    for number, values in enumerate(rows[1:], start=2):
        values = list(values)
        if all(check_lean.is_blank(value) for value in values):
            continue
        values = (values + [None] * len(columns))[: len(columns)]
        body.append((number, values))
    return columns, body


def read_workbook(path: Path) -> dict[str, tuple[list[str], list[tuple[int, list[Any]]]]]:
    """Read every sheet from an in-memory copy; the file is never opened for writing."""

    data = path.read_bytes()
    wb = openpyxl.load_workbook(io.BytesIO(data), read_only=True, data_only=True)
    try:
        return {name: _sheet_table(wb, name) for name in (LEDGER_SHEET, ROUNDS_SHEET, QUESTIONS_SHEET, FACTS_SHEET)}
    finally:
        wb.close()


# ---------------------------------------------------------------------------
# Repository access with caches


def _stat_key(path: Path) -> tuple[int, int]:
    stat = path.stat()
    return stat.st_mtime_ns, stat.st_size


def _reason(exc: BaseException) -> str:
    """A short, path-free description of why a file could not be read."""

    if isinstance(exc, OSError):
        return f"{type(exc).__name__}: {exc.strerror or 'cannot read file'}"
    message = str(exc)
    for text in (str(REPO_ROOT), str(Path.home())):
        message = message.replace(text, ".")
    return f"{type(exc).__name__}: {message}"[:200]


# What a missing, unreadable or corrupt input raises while it is loaded.
READ_ERRORS = (OSError, zipfile.BadZipFile, InvalidFileException, KeyError, ValueError, EOFError)


class Cockpit:
    """Deals under one repository root, with caches keyed on file mtime and size."""

    def __init__(self, repo_root: Path = REPO_ROOT) -> None:
        self.repo_root = Path(repo_root)
        self.extraction_dir = self.repo_root / "extraction"
        self.filing_dir = self.repo_root / "raw_filing"
        self._lock = threading.Lock()
        self._path_locks: dict[str, threading.Lock] = {}
        self._filings: dict[Path, tuple[tuple[int, int], Filing]] = {}
        self._workbooks: dict[Path, tuple[tuple[int, int], Any]] = {}
        self._checks: dict[tuple[Any, ...], dict[str, Any]] = {}
        self._payloads: dict[str, tuple[tuple[Any, ...], dict[str, Any]]] = {}
        from cockpit.workspace import Workspace
        self.workspace = Workspace(self)
        from cockpit.trace import Trace  # imported here: trace builds on the workspace module
        self.trace = Trace(self.workspace)
        from cockpit.runs import Runs
        self.runs = Runs(self.workspace)
        from cockpit.deals import Deals
        self.deals = Deals(self.workspace)
        from cockpit.instructions import Instructions
        self.instructions = Instructions(self.workspace)

    def _path_lock(self, key: str) -> threading.Lock:
        with self._lock:
            return self._path_locks.setdefault(key, threading.Lock())

    # -- inputs -----------------------------------------------------------

    def manifest(self) -> dict[str, dict[str, str]]:
        path = self.filing_dir / "MANIFEST.csv"
        if not path.is_file():
            return {}
        entries: dict[str, dict[str, str]] = {}
        with path.open(newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                deal = (row.get("deal") or "").strip()
                name = (row.get("file") or "").strip()
                if not SLUG_RE.fullmatch(deal) or not name or "/" in name or "\\" in name or name.startswith("."):
                    continue
                if (self.filing_dir / name).is_file():
                    entries[deal] = row
        if self.workspace.available:  # deals added in the cockpit keep their filings in the state folder
            for row in self.deals.added():
                path = self.deals.filing_path(row)
                if row["slug"] not in entries and path.is_file():
                    entries[row["slug"]] = {**{key: str(row[key]) for key in ("file", "form_type", "date_filed", "source_url", "document", "fetched_utc", "bytes", "sha256")},
                                            "deal": row["slug"], "path": str(path)}
        return entries

    def catalog_deals(self) -> dict[str, dict[str, Any]]:
        """The deals catalog.json lists; none without a readable catalog (the workspace reports that)."""

        from cockpit.workspace import WorkspaceError  # imported here: the workspace builds on this module
        if not self.workspace.available:
            return {}
        try:
            deals = self.workspace.catalog()["deals"]
        except WorkspaceError:
            return {}
        return {slug: item for slug, item in deals.items() if SLUG_RE.fullmatch(slug) and isinstance(item, dict)}

    def catalog_workbook(self, item: dict[str, Any]) -> Path | None:
        """A catalog deal's workbook: the path of its starting base, wherever the catalog keeps it."""

        from cockpit.workspace import WorkspaceError
        base = next((v for v in item.get("versions") or [] if isinstance(v, dict) and v.get("id") == item.get("default_base")), None)
        try:
            return self.workspace._path(base.get("path")) if base else None
        except WorkspaceError:
            return None

    def slugs(self) -> list[str]:
        """Catalog deals, found from catalog.json, and any other deal with a workbook in extraction/."""

        manifest = self.manifest()
        found = {slug for slug in self.catalog_deals() if slug in manifest}
        if self.extraction_dir.is_dir():
            found |= {
                path.stem
                for path in self.extraction_dir.glob("*.xlsx")
                if path.is_file() and SLUG_RE.fullmatch(path.stem) and path.stem in manifest
            }
        return sorted(found)

    def resolve(
        self, slug: str, manifest: dict[str, dict[str, str]] | None = None
    ) -> tuple[Path, Path, dict[str, str]]:
        """Return (workbook, filing, manifest row) for a valid slug, else DealNotFound."""

        if not isinstance(slug, str) or not SLUG_RE.fullmatch(slug):
            raise DealNotFound(f"unknown deal {slug!r}")
        if manifest is None:
            manifest = self.manifest()
        workbook = self.extraction_dir / f"{slug}.xlsx"
        entry = manifest.get(slug)
        if entry and entry.get("path"):  # an added deal: its workbooks are imported versions, read through the workspace
            return None, Path(entry["path"]), entry
        item = self.catalog_deals().get(slug)
        if entry is not None and item is not None:
            # A catalog deal is found from the catalog, not from extraction/<slug>.xlsx; the workspace
            # checks its workbook's hash when it reads it.
            return self.catalog_workbook(item) or workbook, self.filing_dir / entry["file"], entry
        if entry is None or not workbook.is_file():
            raise DealNotFound(f"unknown deal {slug!r}")
        return workbook, self.filing_dir / entry["file"], entry

    def filing(self, path: Path) -> Filing:
        with self._path_lock(str(path)):
            key = _stat_key(path)
            cached = self._filings.get(path)
            if cached and cached[0] == key:
                return cached[1]
            filing = Filing(path.read_bytes())
            self._filings[path] = (key, filing)
            return filing

    def workbook(self, path: Path) -> Any:
        with self._path_lock(str(path)):
            key = _stat_key(path)
            cached = self._workbooks.get(path)
            if cached and cached[0] == key:
                return cached[1]
            tables = read_workbook(path)
            self._workbooks[path] = (key, tables)
            return tables

    def check(self, workbook_path: Path, filing_path: Path) -> dict[str, Any]:
        """The current checker's report, cached per file state."""
        with self._path_lock("check:" + str(workbook_path)):
            key = (str(workbook_path), _stat_key(workbook_path), str(filing_path), _stat_key(filing_path), check_lean.CHECKER_VERSION)
            cached = self._checks.get(key)
            if cached is None:
                cached = check_lean.LeanChecker(workbook_path, filing_path).run()
                with self._lock:
                    for old in [k for k in self._checks if k[0] == key[0]]:
                        del self._checks[old]
                    self._checks[key] = cached
            return cached

    # -- payloads ---------------------------------------------------------

    def deal(self, slug: str, manifest: dict[str, dict[str, str]] | None = None, version: str = "working") -> dict[str, Any]:
        """The /api/deal payload (without the reader). DealUnavailable if an input cannot be read."""

        if self.workspace.available:
            return self.workspace.deal(slug, version)

        workbook_path, filing_path, entry = self.resolve(slug, manifest)
        try:
            filing = self.filing(filing_path)
        except READ_ERRORS as exc:
            raise DealUnavailable(f"{slug}: the filing could not be read ({_reason(exc)})") from exc
        try:
            tables = self.workbook(workbook_path)
            report = self.check(workbook_path, filing_path)
            key = (_stat_key(workbook_path), _stat_key(filing_path), id(filing), id(tables), id(report))
        except READ_ERRORS as exc:
            raise DealUnavailable(f"{slug}: the workbook could not be read ({_reason(exc)})") from exc
        with self._lock:
            cached = self._payloads.get(slug)
        if cached and cached[0] == key:
            return cached[1]
        payload = build_deal_payload(slug, entry, tables, filing, report)
        with self._lock:
            self._payloads[slug] = (key, payload)
        return payload

    def filing_payload(self, slug: str) -> dict[str, Any]:
        """The /api/filing payload: display blocks and page starts."""

        _, filing_path, _ = self.resolve(slug)
        try:
            filing = self.filing(filing_path)
        except READ_ERRORS as exc:
            raise DealUnavailable(f"{slug}: the filing could not be read ({_reason(exc)})") from exc
        return {"blocks": filing.blocks_payload(), "pages": filing.pages}

    def list_deals(self) -> list[dict[str, Any]]:
        """The /api/deals summary. A deal that cannot be read is listed as unreadable."""

        deals = []
        manifest = self.manifest()
        added = self.deals.added() if self.workspace.available else []
        slugs = self.slugs()
        slugs += [row["slug"] for row in added if row["slug"] not in slugs and row["slug"] in manifest]
        pending = {}
        if self.workspace.available:
            for slug in slugs:
                if slug in self.catalog_deals() or any(row["slug"] == slug for row in added):
                    item = self.workspace.item(slug)
                    if item.get("pending"):
                        pending[slug] = item
        for slug in slugs:
            if slug in pending:
                item = pending[slug]
                filing_entry = item.get("added") or item.get("filing") or manifest.get(slug, {})
                deals.append({"slug": slug, "target": item["name"], "name": item["name"], "pending": True, "filing": filing_entry.get("file", ""),
                              "form_type": filing_entry.get("form_type", ""), "date_filed": filing_entry.get("date_filed", ""), "rows": None, "rounds": None, "questions": None,
                              "check": None, "quotes_located": None, "quotes_total": None,
                              "added_by": item.get("added", {}).get("added_by") if item.get("added") else None,
                              "review_status": "no extraction yet"})
                continue
            try:
                payload = self.deal(slug, manifest)
            except DealNotFound:
                continue
            except Exception as exc:  # one bad workbook must not hide the others
                entry = manifest.get(slug, {})
                deals.append(
                    {
                        "slug": slug,
                        "target": slug,
                        "filing": entry.get("file", ""),
                        "form_type": entry.get("form_type", ""),
                        "date_filed": entry.get("date_filed", ""),
                        "rows": 0,
                        "rounds": 0,
                        "questions": 0,
                        "check": {"status": "unreadable", "errors": 0, "warnings": 0},
                        "quotes_located": 0,
                        "quotes_total": 0,
                        "error": str(exc) if isinstance(exc, DealUnavailable) else f"{slug}: {_reason(exc)}",
                    }
                )
                continue
            ledger_rows = payload["ledger"]["rows"]
            quotes = [row["quote"] for row in ledger_rows if row["quote"] is not None]
            facts = {fact["field"]: fact["value"] for fact in payload["facts"]}
            summary = payload["check"]["summary"]
            deals.append(
                {
                    "slug": slug,
                    "target": facts.get("Target") or slug,
                    "filing": payload["filing"]["file"],
                    "form_type": payload["filing"]["form_type"],
                    "date_filed": payload["filing"]["date_filed"],
                    "rows": len(ledger_rows),
                    "rounds": len(payload["rounds"]["rows"]),
                    "questions": len(payload["questions"]["rows"]),
                    "check": {
                        "status": payload["check"]["status"],
                        "errors": summary.get("errors", 0),
                        "warnings": summary.get("warnings", 0),
                        "checker_version": payload["check"].get("checker_version"),
                        "ledger_schema": payload.get("ledger_schema"),
                    },
                    "quotes_located": sum(1 for quote in quotes if quote["located"]),
                    "quotes_total": len(quotes),
                    "name": self.workspace.item(slug).get("name", slug) if self.workspace.available else slug,
                    "instruction_version": next((v.get("instruction_version") for v in payload.get("versions", []) if v.get("id") == payload.get("workspace", {}).get("base_version")), None),
                    "review_status": next((v.get("review_status") for v in payload.get("versions", []) if v.get("id") == payload.get("workspace", {}).get("base_version")), None),
                    "working_revision": payload.get("workspace", {}).get("revision", 0),
                    "base_label": next((v.get("label") for v in payload.get("versions", []) if v.get("id") == payload.get("workspace", {}).get("base_version")), None),
                }
            )
        hidden = self.deals.hidden() if self.workspace.available else {}
        for entry in deals:
            entry.update(self.deals.visibility_of(entry["slug"], hidden))
        return deals


def _issue_view(issue: dict[str, Any]) -> dict[str, Any]:
    return {
        "severity": issue.get("severity"),
        "code": issue.get("code"),
        "column": issue.get("column"),
        "message": issue.get("message"),
    }


def _row_id(value: Any) -> Any:
    if isinstance(value, bool):
        return display_value(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return display_value(value)


def page_hint(quote: dict[str, Any] | None, filing: Filing) -> str | None:
    """A cockpit hint when a located quote sits on a page other than the one cited."""

    if not quote or not quote.get("located") or not filing.pages_reliable:
        return None
    cited = cited_pages(quote.get("cited_page"))
    found = quote.get("_pages") or []
    if not cited or not found or cited.intersection(found):
        return None
    return f"page hint: quote found on p. {quote['found_page']}, cited p. {quote['cited_page']}"


def report_schema(report: dict[str, Any]) -> str:
    """The only supported ledger schema, including after a fatal workbook check."""
    return report.get("ledger_schema") or check_lean.CHECKER_VERSION


def build_deal_payload(
    slug: str,
    entry: dict[str, str],
    tables: dict[str, tuple[list[str], list[tuple[int, list[Any]]]]],
    filing: Filing,
    report: dict[str, Any],
) -> dict[str, Any]:
    """Assemble the /api/deal payload and attach checker issues to their rows."""

    issues_by_row: dict[tuple[str, int], list[dict[str, Any]]] = {}
    for issue in report.get("issues", []):
        if issue.get("sheet") and isinstance(issue.get("row"), int):
            issues_by_row.setdefault((issue["sheet"], issue["row"]), []).append(issue)
    attached: set[int] = set()

    def row_issues(sheet: str, excel_row: int) -> list[dict[str, Any]]:
        found = issues_by_row.get((sheet, excel_row), [])
        attached.update(id(issue) for issue in found)
        return [_issue_view(issue) for issue in found]

    def cells_of(columns: list[str], values: list[Any]) -> dict[str, str]:
        return {column: display_value(value) for column, value in zip(columns, values) if column}

    ledger_columns, ledger_body = tables[LEDGER_SHEET]
    ledger_rows = []
    for excel_row, values in ledger_body:
        record = dict(zip(ledger_columns, values))
        quote = None
        raw_quote = record.get(QUOTE_COLUMN)
        if not check_lean.is_blank(raw_quote):
            parsed = check_lean.parse_quote_and_page(raw_quote)
            if parsed is None:
                quote = filing.locate("", None)
                quote["text"] = check_lean.normalize_contiguous(raw_quote)
            else:
                quote = filing.locate(*parsed)
        hint = page_hint(quote, filing)
        if quote is not None:
            quote = {k: v for k, v in quote.items() if not k.startswith("_")}
        ledger_rows.append(
            {
                "excel_row": excel_row,
                "id": _row_id(record.get("#")),
                "cells": cells_of(ledger_columns, values),
                "quote": quote,
                "issues": row_issues(LEDGER_SHEET, excel_row),
                "page_hint": hint,
            }
        )

    round_columns, round_body = tables[ROUNDS_SHEET]
    round_rows = [
        {"excel_row": excel_row, "cells": cells_of(round_columns, values), "issues": row_issues(ROUNDS_SHEET, excel_row)}
        for excel_row, values in round_body
    ]

    question_columns, question_body = tables[QUESTIONS_SHEET]
    question_rows = []
    for excel_row, values in question_body:
        record = dict(zip(question_columns, values))
        question_rows.append(
            {
                "excel_row": excel_row,
                "id": _row_id(record.get("Q")),
                "cells": cells_of(question_columns, values),
                "issues": row_issues(QUESTIONS_SHEET, excel_row),
            }
        )

    fact_columns, fact_body = tables[FACTS_SHEET]
    field_index = fact_columns.index("Field") if "Field" in fact_columns else 0
    value_index = fact_columns.index("Value") if "Value" in fact_columns else 1
    facts = [
        {
            "field": display_value(values[field_index]) if field_index < len(values) else "",
            "value": display_value(values[value_index]) if value_index < len(values) else "",
        }
        for _, values in fact_body
    ]

    other = [issue for issue in report.get("issues", []) if id(issue) not in attached]
    return {
        "slug": slug,
        "ledger_schema": report_schema(report),
        "filing": {
            "file": entry.get("file", ""),
            "form_type": entry.get("form_type", ""),
            "date_filed": entry.get("date_filed", ""),
            "source_url": entry.get("source_url", ""),
        },
        "facts": facts,
        "ledger": {"columns": ledger_columns, "rows": ledger_rows},
        "rounds": {"columns": round_columns, "rows": round_rows},
        "questions": {"columns": question_columns, "rows": question_rows},
        "check": {
            "status": report.get("status"),
            "summary": report.get("summary", {}),
            "scope_note": report.get("scope_note", ""),
            "checker_version": report.get("checker_version"),
            "other_issues": other,
        },
        "background_block": filing.background_block,
        "pages_reliable": filing.pages_reliable,
        "review_queue": review_queue(tables),
    }


def review_queue(tables: dict[str, tuple[list[str], list[tuple[int, list[Any]]]]]) -> dict[str, Any]:
    """Alex's must-flag list for the workbook as shown: review_list.py's queue, read from the cells."""

    def records(sheet: str) -> list[dict[str, Any]]:
        columns, body = tables.get(sheet, ([], []))
        return [{column: value for column, value in zip(columns, values) if column} for _, values in body]

    facts = {derive_analysis.text(record.get("Field")): record.get("Value") for record in records(FACTS_SHEET)}
    try:
        items = review_list.build_review_list({"ledger": records(LEDGER_SHEET), "rounds": records(ROUNDS_SHEET), "facts": facts})
    except Exception as exc:  # a review aid never blocks the deal page; the panel shows why it is empty
        return {"categories": list(review_list.CATEGORIES), "items": [], "error": _reason(exc)}
    return {"categories": list(review_list.CATEGORIES), "items": items, "error": None}


_DEFAULT: Cockpit | None = None


def default() -> Cockpit:
    global _DEFAULT
    if _DEFAULT is None:
        _DEFAULT = Cockpit()
    return _DEFAULT
