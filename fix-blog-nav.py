import re

FILE = r"c:\Users\HYE\WorkBuddy\20260411211839\blog\baidu-brand-info-account-level.html"

with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 修复 logo 链接
html = html.replace('href="/" class="nav-logo"', 'href="../index" class="nav-logo"')

# 2. 修复 nav-links（添加 ../ 前缀）
replacements = [
    ('href="/why-baidu-ppc-pro"', 'href="../why-baidu-ppc-pro"'),
    ('href="/features">Services</a>', 'href="../features">Services</a>'),
    ('href="/pricing"', 'href="../pricing"'),
    ('href="/clients"', 'href="../clients"'),
    ('href="/faq"', 'href="../faq"'),
    ('href="/about"', 'href="../about"'),
    ('href="/blog">Blog</a>', 'href="../blog" class="active">Blog</a>'),
    ('href="/contact">Contact</a>', 'href="../contact">Contact</a>'),
]

for old, new in replacements:
    html = html.replace(old, new)

# 3. 修复 nav-cta 链接
html = html.replace('href="/contact" class="nav-cta"', 'href="../contact" class="nav-cta"')

# 4. 修复移动端按钮类名
html = html.replace('class="mobile-nav-toggle"', 'class="nav-mobile-toggle"')

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Fixed: baidu-brand-info-account-level.html")
print("   - Added ../ prefix to nav links")
print("   - Fixed logo link")
print("   - Fixed nav-cta link")
print("   - Fixed mobile nav toggle class")
