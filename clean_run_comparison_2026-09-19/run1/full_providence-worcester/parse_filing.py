import re, html, sys
from bs4 import BeautifulSoup

path = 'raw_filing/providence-worcester_2016-09-20_DEFM14A.htm'
raw = open(path, encoding='utf-8', errors='replace').read()

soup = BeautifulSoup(raw, 'html.parser')

# Remove scripts/styles
for t in soup(['script','style']):
    t.decompose()

body = soup.body or soup

# We'll walk the document and emit blocks, tracking page breaks from <hr> tags.
blocks = []
page = 1
def emit(text, tag):
    global page
    text = re.sub(r'\s+', ' ', text).strip()
    if text:
        blocks.append((tag, page, text))

from bs4 import NavigableString

# Walk children recursively in document order
def walk(node):
    global page
    for child in node.children:
        if isinstance(child, NavigableString):
            continue
        name = getattr(child, 'name', None)
        if name is None:
            continue
        if name == 'hr':
            page += 1
        elif name in ('p','div','table','h1','h2','h3','h4','h5','h6','tr','li','td','th'):
            # if contains block children, recurse; else emit text
            if child.find(['p','div','table','tr','li','hr']):
                walk(child)
            else:
                emit(child.get_text(' '), name)
        else:
            walk(child)

walk(body)

with open('/home/uctpiaj/work/filing_blocks.txt','w') as f:
    for i,(tag,p,t) in enumerate(blocks):
        f.write(f"[[{i}|{tag}|p{p}]] {t}\n")

print("blocks:", len(blocks))
print("last page:", page)
