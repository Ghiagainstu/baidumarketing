"""修复博客页面 footer 链接（全部指向 / 的 bug）"""
import os, glob

ROOT = os.path.dirname(os.path.abspath(__file__))

# 正确的 footer 链接映射
REPLACEMENTS = [
    ('<a href="/">Services</a>', '<a href="/features">Services</a>'),
    ('<a href="/">Pricing</a>', '<a href="/pricing">Pricing</a>'),
    ('<a href="/">About Us</a>', '<a href="/about">About Us</a>'),
    ('<a href="/">FAQ</a>', '<a href="/faq">FAQ</a>'),
    ('<a href="/">Blog</a>', '<a href="/blog">Blog</a>'),
    ('<a href="/">Submit a Request</a>', '<a href="/contact">Submit a Request</a>'),
    ('<a href="/">Privacy Policy</a>', '<a href="/privacy">Privacy Policy</a>'),
    ('<a href="/">Terms of Service</a>', '<a href="/terms">Terms of Service</a>'),
]

blog_dir = os.path.join(ROOT, 'blog')
files = sorted(glob.glob(os.path.join(blog_dir, '*.html')))
changed = []

for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    original = content
    for old, new in REPLACEMENTS:
        content = content.replace(old, new)
    
    if content != original:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        rel = os.path.relpath(f, ROOT)
        changed.append(rel)
        print(f'  FIXED: {rel}')

print(f'\n总计修改 {len(changed)} 个文件')
