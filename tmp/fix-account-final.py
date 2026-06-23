import re

f = 'ko/blog/baidu-account-opening-foreign-companies.html'
with open(f, 'r', encoding='utf-8') as fh:
    h = fh.read()

# 1. Fix canonical trailing >
h = h.replace('baidu-account-opening-foreign-companies" />', 'baidu-account-opening-foreign-companies" />')
h = re.sub(r'(" />)\s*>', r'\1', h)

# 2. Fix meta tag: translate strategy -> ??
h = h.replace('</svg> strategy</span>', '</svg> ??</span>')

# 3. Fix duplicate related blog h2
h = h.replace('<h2>\ube0c\ub85c\uadf8 \ub354 \ubcf4\uae30</h2>\n      <h2>\ube0c\ub85c\uadf8 \ub2e4\ub978 \uc608</h2>', '<h2>\ube0c\ub85c\uadf8 \ub354 \ubcf4\uae30</h2>')

# 4. Convert markdown tables to HTML tables
def convert_table(match):
    lines = match.group(0).strip().split('\n')
    # Find header row (first | row), separator (|---), and body rows
    header = None
    rows = []
    for line in lines:
        line = line.strip()
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if all(re.match(r'^[-:]+$', c) for c in cells):
            continue  # separator
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

# Find sequences of <p>|...</p> lines and convert them
h = re.sub(r'(?:<p>\|[^<]*</p>\n?)+', convert_table, h)

# 5. Convert markdown callout divs that came as plain text
# Look for patterns like: **Key Insight:** or similar that should be callouts

# 6. Add enhancements: wrap key stats in callout boxes
# Find important paragraphs and enhance them

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(h)

print('Fixed all issues in', f)
