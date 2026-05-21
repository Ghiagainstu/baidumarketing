import os
import glob

base = "C:/Users/HYE/WorkBuddy/20260411211839"

# 找所有包含问题的文件
pattern = os.path.join(base, "blog", "*.html")
ja_pattern = os.path.join(base, "ja", "blog", "*.html")

all_files = glob.glob(pattern) + glob.glob(ja_pattern)
print(f"扫描到 {len(all_files)} 个博客文件")

fixed = 0
for fpath in all_files:
    try:
        content = open(fpath, encoding='utf-8').read()
    except:
        continue

    old = 'href="https://baidumarketing.com/'
    if old not in content:
        continue

    new = 'href="https://www.baidumarketing.com/'
    count = content.count(old)
    new_content = content.replace(old, new)

    open(fpath, 'w', encoding='utf-8').write(new_content)
    fixed += 1
    rel = os.path.relpath(fpath, base)
    print(f"  ✅ {rel}：修复了 {count} 处")

print()
print(f"完成！共修复 {fixed} 个文件")
