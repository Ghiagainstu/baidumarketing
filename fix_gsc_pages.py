import os
import re

base = "C:/Users/HYE/WorkBuddy/20260411211839"

# 需要加 hreflang + x-default 的 EN 页面（缺失这俩标签）
hreflang_pages = [
    "blog/b2b-lead-generation-framework.html",
    "blog/baidu-2026-international-brands.html",
    "blog/chinese-consumers-decision-journey.html",
    "blog/why-b2b-baidu-search.html",
]

# 需要加 canonical 的页面（缺失 canonical）
canonical_pages = [
    "blog/baidu-ads-campaign-upgrade-2025.html",
    "blog/baidu-custom-form-retirement.html",
    "blog/faq-international-brands.html",
]

def slug_from_path(relpath):
    """从路径提取 slug，如 blog/foo.html -> blog/foo"""
    return relpath.replace('.html', '')

def fix_hreflang(filepath, slug):
    """在 <title> 标签后插入 hreflang + x-default"""
    content = open(filepath, encoding='utf-8').read()
    if 'hreflang="en"' in content:
        print(f"  跳过 {slug}：已有 hreflang")
        return False

    # 在 </title> 行后插入 hreflang 标签
    # 格式参照 baidu-ads-campaign-upgrade-2025.html
    insert_block = (
        '\n'
        f'  <link rel="alternate" hreflang="en" href="https://www.baidumarketing.com/{slug}">\n'
        f'  <link rel="alternate" hreflang="x-default" href="https://www.baidumarketing.com/{slug}">\n'
    )

    # 在 </title> 行后面插入
    new_content = content.replace('</title>', '</title>' + insert_block, 1)
    if new_content == content:
        print(f"  警告：{slug} 插入 hreflang 失败（未找到 </title>）")
        return False

    open(filepath, 'w', encoding='utf-8').write(new_content)
    print(f"  ✅ {slug}：已添加 hreflang + x-default")
    return True

def fix_canonical(filepath, slug):
    """添加 canonical 标签（在 <title> 后）"""
    content = open(filepath, encoding='utf-8').read()
    if 'rel="canonical"' in content:
        print(f"  跳过 {slug}：已有 canonical")
        return False

    insert_block = (
        '\n'
        f'  <link rel="canonical" href="https://www.baidumarketing.com/{slug}">\n'
    )

    new_content = content.replace('</title>', '</title>' + insert_block, 1)
    if new_content == content:
        print(f"  警告：{slug} 插入 canonical 失败")
        return False

    open(filepath, 'w', encoding='utf-8').write(new_content)
    print(f"  ✅ {slug}：已添加 canonical")
    return True

# ── 修复 hreflang ──────────────────────────────────────────────
print("=" * 60)
print("修复 hreflang + x-default（4个 EN 页面）")
print("=" * 60)
for relpath in hreflang_pages:
    slug = slug_from_path(relpath)
    fpath = os.path.join(base, relpath)
    print(f"处理：{relpath}")
    fix_hreflang(fpath, slug)

# ── 修复 canonical ─────────────────────────────────────────────
print()
print("=" * 60)
print("修复 canonical（3个页面）")
print("=" * 60)
for relpath in canonical_pages:
    slug = slug_from_path(relpath)
    fpath = os.path.join(base, relpath)
    print(f"处理：{relpath}")
    fix_canonical(fpath, slug)

print()
print("完成！")
