import re

fpath = "C:/Users/HYE/WorkBuddy/20260411211839/sitemap.xml"
content = open(fpath, encoding='utf-8').read()

count_www = 0
count_html = 0

# 1. 补 www：href="https://baidumarketing.com/ → href="https://www.baidumarketing.com/
old1 = 'https://baidumarketing.com/'
new1 = 'https://www.baidumarketing.com/'
c1 = content.count(old1)
content = content.replace(old1, new1)
count_www = c1
print(f"补 www：替换了 {c1} 处")

# 2. 去掉 .html 后缀（仅 <loc> 和 <xhtml:link> 中的 URL）
# 匹配 <loc>...</loc> 中的 .html
def remove_html_in_loc(match):
    url = match.group(1)
    return '<loc>' + url.replace('.html', '') + '</loc>'

content_new = re.sub(r'<loc>(https?://[^<]*?)\.html</loc>', remove_html_in_loc, content)
count_html += content.count('.html</loc>') - content_new.count('.html</loc>')  # approximate
content = content_new

# 匹配 <xhtml:link ... href="...html" /> 中的 .html
def remove_html_in_href(match):
    return match.group(0).replace('.html', '')

content = re.sub(r'href="https://[^"]*?\.html"', remove_html_in_href, content)

# 统计最终结果
final_www = content.count('https://www.baidumarketing.com/')
final_nowww = content.count('https://baidumarketing.com/')
final_html = content.count('.html</loc>')

print(f"去掉 .html 后缀：完成")
print()
print(f"修复后统计：")
print(f"  带 www 的 URL：{final_www}")
print(f"  不带 www 的 URL：{final_nowww}")
print(f"  <loc> 中含 .html 的数量：{final_html}")

open(fpath, 'w', encoding='utf-8').write(content)
print()
print("sitemap.xml 修复完成！")
