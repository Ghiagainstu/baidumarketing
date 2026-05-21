import os
import re

base = "C:/Users/HYE/WorkBuddy/20260411211839"

# canonical 缺少 www 的页面
pages = [
    "blog/b2b-lead-generation-framework.html",
    "blog/baidu-2026-international-brands.html",
    "blog/chinese-consumers-decision-journey.html",
    "blog/why-b2b-baidu-search.html",
    "ja/blog/b2b-lead-generation-framework.html",
    "ja/blog/baidu-2026-international-brands.html",
]

print("修复 canonical URL（补 www）")
print("=" * 60)

for relpath in pages:
    fpath = os.path.join(base, relpath)
    content = open(fpath, encoding='utf-8').read()

    # 将 href="https://baidumarketing.com/ 替换为 href="https://www.baidumarketing.com/
    old = 'href="https://baidumarketing.com/'
    new = 'href="https://www.baidumarketing.com/'
    count = content.count(old)

    if count == 0:
        print(f"  跳过 {relpath}：未找到待修复的 canonical")
        continue

    new_content = content.replace(old, new)
    open(fpath, 'w', encoding='utf-8').write(new_content)
    print(f"  ✅ {relpath}：修复了 {count} 处 canonical URL")

print()
print("完成！")
