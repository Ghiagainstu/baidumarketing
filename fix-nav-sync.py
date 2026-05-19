import re

ROOT = r"c:\Users\HYE\WorkBuddy\20260411211839"

# 所有根目录 HTML 文件（排除 index.html 因为它可以保留 nav-mobile-cta）
PAGES = [
    "about.html",
    "blog.html",
    "china-geo.html",
    "clients.html",
    "contact.html",
    "faq.html",
    "features.html",
    "pricing.html",
    "privacy.html",
    "terms.html",
    "why-baidu-ppc-pro.html",
]

def fix_page(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    original = html
    
    # 1. 移除 nav-mobile-cta（非 index 页面）
    html = re.sub(
        r'\s*<a href="contact" class="nav-mobile-cta">Get Started →</a>\n',
        '\n',
        html
    )
    
    # 2. 修复 lang-switch 链接（根目录页面用相对路径）
    html = html.replace('href="/" lang="en"', 'href="index" lang="en"')
    html = html.replace('href="ja/" lang="ja"', 'href="ja/index" lang="ja"')
    
    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False

for page in PAGES:
    filepath = f"{ROOT}/{page}"
    try:
        changed = fix_page(filepath)
        status = "✅ Fixed" if changed else "⏭️ No changes"
        print(f"{status}: {page}")
    except Exception as e:
        print(f"❌ Error: {page} - {e}")

# 单独处理 index.html（只修复 lang-switch，保留 nav-mobile-cta）
print("\n--- Fixing index.html lang-switch only ---")
try:
    filepath = f"{ROOT}/index.html"
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    original = html
    html = html.replace('href="/" lang="en" class="lang-switch-item"', 'href="index" lang="en" class="lang-switch-item"')
    html = html.replace('href="ja/" lang="ja"', 'href="ja/index" lang="ja"')
    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print("✅ Fixed: index.html lang-switch")
    else:
        print("⏭️ No changes: index.html")
except Exception as e:
    print(f"❌ Error: index.html - {e}")
