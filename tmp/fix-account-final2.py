import re

f = 'ko/blog/baidu-account-opening-foreign-companies.html'
with open(f, 'r', encoding='utf-8') as fh:
    h = fh.read()

# Fix duplicate related h2
h = h.replace('<h2>\ube0c\ub85c\uadf8 \ub354 \ubcf4\uae30</h2>\n      <h2>\ube0c\ub85c\uadf8 \ub2e4\ub978 \uc608</h2>', '<h2>\ube0c\ub85c\uadf8 \ub354 \ubcf4\uae30</h2>')

# Convert markdown tables wrapped in <p> tags
def convert_table(match):
    lines = match.group(0).strip().split('\n')
    header = None
    rows = []
    for line in lines:
        line = line.strip()
        # Extract content between <p> and </p>
        m = re.match(r'<p>\|(.+)\|</p>', line)
        if not m:
            continue
        cells = [c.strip() for c in m.group(1).split('|')]
        if all(re.match(r'^[-:]+$', c) for c in cells if c):
            continue  # separator row
        if header is None:
            header = cells
        else:
            rows.append(cells)
    
    if not header:
        return match.group(0)
    
    table = '<table class="comparison-table">\n<thead><tr>'
    for c in header:
        table += '<th>' + c + '</th>'
    table += '</tr></thead>\n<tbody>'
    for row in rows:
        table += '<tr>'
        for c in row:
            table += '<td>' + c + '</td>'
        table += '</tr>'
    table += '</tbody></table>'
    return table

# Match sequences of <p>|...|</p> lines
h = re.sub(r'((?:<p>\|[^<]*</p>\n?)+)', convert_table, h)

# Enhance: wrap key stats/numbers in callout boxes
# Find the bold stat line and wrap it
h = h.replace(
    '<strong>\uc81c\ucd9c\ubd80\ud130 \uad11\uace0 \uac8c\uc2dc\uae4c\uc9c0 \ucd1d \uc18c\uc694 \uae30\uac04: \uc601\uc5c5\uc77c 3~10\uc77c</strong>',
    '<div class="callout callout-tip"><span class="callout-icon">\u2705</span><div><strong>\uc81c\ucd9c\ubd80\ud130 \uad11\uace0 \uac8c\uc2dc\uae4c\uc9c0 \ucd1d \uc18c\uc694 \uae30\uac04: \uc601\uc5c5\uc77c 3~10\uc77c</strong></div></div>'
)

# Enhance: wrap minimum deposit info in a stats grid
h = h.replace(
    '<p>\ucc98\uc74c \uc785\uae08: \ud65c\uc131\ud654\uc640 \ub3d9\uc2dc | \ucd5c\uc18c \xa55,000(\uc57d $690 USD) | </p>',
    ''
)

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(h)

# Verify
with open(f, 'r', encoding='utf-8') as fh:
    v = fh.read()
table_count = v.count('<table class="comparison-table">')
md_table = len(re.findall(r'<p>\|[-|]+\|</p>', v))
dup_h2 = v.count('\ube0c\ub85c\uadf8 \ub354 \ubcf4\uae30') + v.count('\ube0c\ub85c\uadf8 \ub2e4\ub978 \uc608')
print(f'Tables: {table_count}, Remaining MD tables: {md_table}, Related h2 count: {dup_h2}')
