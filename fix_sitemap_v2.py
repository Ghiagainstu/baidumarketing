import re

fpath = "C:/Users/HYE/WorkBuddy/20260411211839/sitemap.xml"
content = open(fpath, encoding='utf-8').read()

# ── 修复1：所有 baidumarketing.com（无 www）补 www ──────────
old = 'https://baidumarketing.com/'
new = 'https://www.baidumarketing.com/'
c1 = content.count(old)
content = content.replace(old, new)
print(f"✅ 补 www：替换了 {c1} 处")

# ── 修复2：去掉 <loc> 标签中的 .html 后缀 ─────────────────────
def fix_loc(match):
    url = match.group(1)   # URL 部分
    return '<loc>' + url.replace('.html', '') + '</loc>'

content = re.sub(r'<loc>(https?://[^<]+?)\.html</loc>', fix_loc, content)
c2 = content.count('.html</loc>')
print(f"✅ 去掉 <loc> 中的 .html 后缀（剩余 {c2} 处含 .html）</loc>")

# ── 修复3：去掉 <xhtml:link> 中的 .html 后缀 ─────────────────
def fix_xhtml(match):
    return match.group(0).replace('.html"', '"').replace('.html\'', '\'')

content = re.sub(r'<xhtml:link[^>]+href="[^"]*?\.html"[^>]*/\s*>', fix_xhtml, content)

# 简单方式：直接全文替换 href="...html" → href="..."（在 xhtml:link 标签内）
# 更安全的做法：只处理 xhtml:link 行
lines = content.split('\n')
new_lines = []
for line in lines:
    if '<xhtml:link' in line and '.html' in line:
        line = line.replace('.html"', '"').replace('.html\'', '\'')
    new_lines.append(line)
content = '\n'.join(new_lines)
print("✅ 去掉 <xhtml:link> 中的 .html 后缀")

# ── 最终检查 ──────────────────────────────────────────────────
final_nowww = content.count('https://baidumarketing.com/') - content.count('https://www.baidumarketing.com/')
final_html_loc = content.count('.html</loc>')
final_html_xhtml = sum(1 for l in content.split('\n') if '<xhtml:link' in l and '.html' in l)

print()
print("=" * 50)
print("最终检查：")
print(f"  残留 无www URL：{final_nowww}")
print(f"  残留 <loc> .html：{final_html_loc}")
print(f"  残留 <xhtml:link> .html：{final_html_xhtml}")

if final_nowww == 0 and final_html_loc == 0 and final_html_xhtml == 0:
    print("\n🎉 全部修复完成！")
    open(fpath, 'w', encoding='utf-8').write(content)
else:
    print("\n⚠️ 仍有残留问题，请手动检查")
