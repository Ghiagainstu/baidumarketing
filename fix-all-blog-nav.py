import re, os

BLOG_DIR = r"c:\Users\HYE\WorkBuddy\20260411211839\blog"

# 需要添加的 ../ 前缀替换
REPLACEMENTS = [
    ('href="/why-baidu-ppc-pro"', 'href="../why-baidu-ppc-pro"'),
    ('href="/features">Services</a>', 'href="../features">Services</a>'),
    ('href="/pricing"', 'href="../pricing"'),
    ('href="/clients"', 'href="../clients"'),
    ('href="/faq"', 'href="../faq"'),
    ('href="/about"', 'href="../about"'),
    ('href="/blog">Blog</a>', 'href="../blog">Blog</a>'),
    ('href="/contact">Contact</a>', 'href="../contact">Contact</a>'),
    ('href="/contact" class="nav-cta"', 'href="../contact" class="nav-cta"'),
    ('href="/" class="nav-logo"', 'href="../index" class="nav-logo"'),
    ('class="mobile-nav-toggle"', 'class="nav-mobile-toggle"'),
]

def fix_blog_page(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    original = html
    for old, new in REPLACEMENTS:
        html = html.replace(old, new)
    
    if html != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return True
    return False

# 处理所有博客 HTML 文件
fixed = 0
for filename in os.listdir(BLOG_DIR):
    if filename.endswith('.html'):
        filepath = os.path.join(BLOG_DIR, filename)
        try:
            if fix_blog_page(filepath):
                print(f"✅ Fixed: {filename}")
                fixed += 1
            else:
                print(f"⏭️ No changes: {filename}")
        except Exception as e:
            print(f"❌ Error: {filename} - {e}")

print(f"\n总计修复: {fixed} 个文件")
