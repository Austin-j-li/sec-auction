"""Synthetic tests for the switchable human review queue."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import derive_analysis
import review_list
from test_derive_analysis import FACTS, bid, row, rounds_line, write


class ReviewListTests(unittest.TestCase):
    def test_every_category_is_generated_and_each_can_be_disabled(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rows = [
                row(1, "Alpha", "NDA signed", rnd=0, Type="Unknown", Count=1),
                bid(2, "Alpha", 10, formality="Formal", Type="Unknown", Note="Enterprise value €20m."),
                row(3, "Alpha", "Merger agreement signed", Count=1, Type="Unknown"),
                row(4, "Beta", "Other-scope bid", Type="Financial", Note="Partial assets only."),
                row(5, "Beta", "Withdrew", Count=1, Inferred="Y", **{"Exit reason": "Not stated"}),
                row(6, "Other financial and strategic bidders", "NDA signed", Type="Unknown",
                    Note="Count: at least 3, including one financial bidder."),
                row(7, "Target", "Round opened", rnd=2, day=1),
                row(8, "Target", "Process restarted", rnd=0, day=2, Process=2),
            ]
            rounds = [rounds_line(1, "Enforced"), rounds_line(2, "Passed without action")]
            path = write(Path(tmp) / "synthetic.xlsx", rows, rounds,
                         facts={**FACTS, "Currency and units of bid prices": "euro enterprise value"})
            ledger = derive_analysis.load(path)
            items = review_list.build_review_list(ledger)
            self.assertEqual({item["category"] for item in items}, set(review_list.CATEGORIES) - {"partial_only"})
            for category in review_list.CATEGORIES:
                with self.subTest(category=category):
                    switched = review_list.build_review_list(ledger, {category})
                    self.assertNotIn(category, {item["category"] for item in switched})
                    self.assertEqual([item for item in switched if item["category"] != category],
                                     [item for item in items if item["category"] != category])
            with self.assertRaisesRegex(ValueError, "unknown review categories"):
                review_list.build_review_list(ledger, {"not_a_category"})

    def test_partial_only_is_a_deal_level_review_item(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = write(Path(tmp) / "partial.xlsx",
                         [row(1, "Alpha", "Other-scope bid", **{"Price low": None, "Price high": None})], [],
                         facts={**FACTS, "Whole-company bids": "No; assets only"})
            items = review_list.build_review_list(derive_analysis.load(path))
            partial = [item for item in items if item["category"] == "partial_only"]
            self.assertEqual(len(partial), 1)
            self.assertEqual((partial[0]["sheet"], partial[0]["row"]), ("Deal facts", "Whole-company bids"))

    def test_formal_other_scope_unknown_and_qualified_fact_type_are_reviewed(self) -> None:
        ledger = {"ledger": [row(1, "Partial buyer", "Other-scope bid", Type="Unknown",
                                 Formality="Formal", Count=1),
                             row(2, "Other strategic and financial bidders", "NDA signed",
                                 Type="Unknown", Count=5, Note="Five signers.")],
                  "rounds": [], "facts": {**FACTS, "Acquirer type": "Unknown; buyer undisclosed"}}
        items = review_list.build_review_list(ledger)
        self.assertTrue(any(item["category"] == "unknown_type" and item["sheet"] == "Deal ledger"
                            and item["row"] == 1 for item in items))
        self.assertTrue(any(item["category"] == "unknown_type" and item["sheet"] == "Deal facts"
                            for item in items))
        self.assertTrue(any(item["category"] == "type_unsplit_count" and item["row"] == 2
                            for item in items))

    def test_currency_and_exchange_ratio_are_price_basis_review_items(self) -> None:
        for currency in ("CHF per share", "AUD per share", "Canadian dollars per share"):
            with self.subTest(currency=currency):
                ledger = {"ledger": [bid(1, "Alpha", 10)], "rounds": [],
                          "facts": {**FACTS, "Currency and units of bid prices": currency}}
                categories = {item["category"] for item in review_list.build_review_list(ledger)}
                self.assertIn("non_dollar_price", categories)
        ledger = {"ledger": [bid(1, "Alpha", None,
                                 Note="Exchange ratio 0.5 buyer shares per target share.")],
                  "rounds": [], "facts": FACTS}
        categories = {item["category"] for item in review_list.build_review_list(ledger)}
        self.assertIn("non_per_share_price", categories)


if __name__ == "__main__":
    unittest.main()
