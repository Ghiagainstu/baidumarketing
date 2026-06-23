import re
f = 'ko/blog/baidu-account-opening-foreign-companies.html'
with open(f, 'r', encoding='utf-8') as fh:
    h = fh.read()

title = '?? ??? ??? PPC ??? ???? ??: ??? ???'
desc = '?? ??????? ?? ?? ??? ?? ??? ?? ?? ?? ??? ???. 2026? ?? ??.'

h = re.sub(r'<title>[^<]*</title>', '<title>' + title + ' \u2014 Baidu PPC Pro Blog</title>', h)
h = re.sub(r'<h1[^>]*>[^<]*</h1>', '<h1 class="article-title">' + title + '</h1>', h)
h = re.sub(r'og:title[^>]*content="[^"]*"', 'og:title" content="' + title + '"', h)
h = re.sub(r'og:description[^>]*content="[^"]*"', 'og:description" content="' + desc + '"', h)
h = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="' + desc + '"', h)
h = re.sub(r'"headline": "[^"]*"', '"headline": "' + title + '"', h)
h = re.sub(r'"description": "[^"]*"', '"description": "' + desc + '"', h)

with open(f, 'w', encoding='utf-8') as fh:
    fh.write(h)

with open(f, 'r', encoding='utf-8') as fh:
    verify = fh.read()
t = re.search(r'<title>(.*?)</title>', verify).group(1)
print('Verify title:', t[:80])
