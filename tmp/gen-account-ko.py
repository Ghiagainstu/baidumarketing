import re

md_path = r'E:\Obsidian\Baidu\05-Strategy\baidu-account-opening-foreign-companies\baidu-account-opening-foreign-companies-ko.md'
html_path = 'ko/blog/baidu-account-opening-foreign-companies.html'

with open(md_path, 'r', encoding='utf-8-sig') as fh:
    md = fh.read()

with open(html_path, 'r', encoding='utf-8') as fh:
    html = fh.read()

fm_match = re.match(r'^---\s*\n(.*?)\n---', md, re.DOTALL)
fm = {}
if fm_match:
    for line in fm_match.group(1).split('\n'):
        m = re.match(r'^(\w+):\s*(.+)', line)
        if m:
            fm[m.group(1)] = m.group(2).strip('"')

body = re.sub(r'^---[\s\S]*?---\n*', '', md, count=1)
body = re.sub(r'^#\s+.*\n*', '', body, count=1)
body = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', body, flags=re.MULTILINE)
body = re.sub(r'^### (.+)$', r'<h3>\1</h3>', body, flags=re.MULTILINE)
body = re.sub(r'^## (.+)$', r'<h2>\1</h2>', body, flags=re.MULTILINE)
body = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', body)
body = re.sub(r'- (.+)$', r'<li>\1</li>', body, flags=re.MULTILINE)
body = re.sub(r'(\d+)\. (.+)$', r'<li>\2</li>', body, flags=re.MULTILINE)

body = re.sub(r'((?:<li>.*</li>\s*)+)', r'<ul>\n\1</ul>', body)

lines = body.split('\n')
result = []
for line in lines:
    t = line.strip()
    if not t:
        continue
    if t.startswith('<'):
        result.append(line)
    else:
        result.append('<p>' + t + '</p>')
body = '\n'.join(result)

start_tag = '<article class="article-content">'
start_idx = html.find(start_tag)
if start_idx == -1:
    start_tag = '<div class="article-content">'
    start_idx = html.find(start_tag)

if 'article' in start_tag:
    end_tag = '</article>'
else:
    end_tag = '</div>'
end_idx = html.find(end_tag, start_idx)

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + start_tag + '\n' + body + '\n    ' + end_tag + html[end_idx + len(end_tag):]

title = fm.get('title', 'Blog Post')
desc = fm.get('description', '')

html = re.sub(r'<title>[^<]*</title>', '<title>' + title + ' \u2014 Baidu PPC Pro Blog</title>', html)
html = re.sub(r'<h1[^>]*>[^<]*</h1>', '<h1 class="article-title">' + title + '</h1>', html)
html = re.sub(r'og:title[^>]*content="[^"]*"', 'og:title" content="' + title + '"', html)
html = re.sub(r'og:description[^>]*content="[^"]*"', 'og:description" content="' + desc + '"', html)
html = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="' + desc + '"', html)
html = re.sub(r'"headline": "[^"]*"', '"headline": "' + title + '"', html)
html = re.sub(r'"description": "[^"]*"', '"description": "' + desc + '"', html)

with open(html_path, 'w', encoding='utf-8') as fh:
    fh.write(html)

with open(html_path, 'r', encoding='utf-8') as fh:
    v = fh.read()
t = re.search(r'<title>(.*?)</title>', v).group(1)
print('Title:', t[:80])
print('Size:', len(v))
