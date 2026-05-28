"""批量清除全站内部链接的 .html 后缀（Vercel cleanUrls 环境）"""
import os, re, glob

ROOT = os.path.dirname(os.path.abspath(__file__))

def clean_path(path):
    """将 /xxx.html 或 /index.html#anchor 转为干净路径"""
    # /index.html → /
    path = re.sub(r'/index\.html(?=#|$)', '/', path)
    # /xxx.html → /xxx（保留 #anchor）
    path = re.sub(r'\.html(?=#|$)', '', path)
    return path

def fix_href(match):
    """替换 href='/xxx.html' 为 href='/xxx'"""
    full = match.group(0)
    quote = match.group(1)   # " 或 '
    path = match.group(2)    # 完整路径
    
    # 只处理内部链接（以 / 开头）
    if not path.startswith('/'):
        return full
    
    # 不处理 blog/ 子页面链接（这些是博客详情页，文件名本身就是 xxx.html）
    if '/blog/' in path and path.count('/') >= 3:
        # /blog/xxx.html 是博客详情页，不处理
        # 但 /blog.html 是博客列表页，需要处理
        if not path.startswith('/blog.html') and not path.startswith('/ja/blog.html') and not path.startswith('/ko/blog.html'):
            return full
    
    new_path = clean_path(path)
    if new_path != path:
        return f'href={quote}{new_path}{quote}'
    return full

def fix_meta_url(match):
    """替换 meta 标签中的 .html URL"""
    full = match.group(0)
    url = match.group(1)
    if 'baidumarketing.com' in url:
        new_url = clean_path(url)
        if new_url != url:
            return full.replace(url, new_url)
    return full

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. 修复所有 href="xxx" 中的内部 .html 链接
    content = re.sub(r'href=(["\'])(/[^"\']*?\.html[^"\']*?)\1', fix_href, content)
    
    # 2. 修复 canonical
    content = re.sub(r'<link rel="canonical" href="([^"]*)"', fix_meta_url, content)
    
    # 3. 修复 og:url
    content = re.sub(r'<meta property="og:url" content="([^"]*)"', fix_meta_url, content)
    
    # 4. 修复 hreflang
    content = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="([^"]*)"', fix_meta_url, content)
    
    # 5. 修复 x-default
    content = re.sub(r'<link rel="alternate" hreflang="x-default" href="([^"]*)"', fix_meta_url, content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# 收集所有 HTML 文件
files = []
for pattern in ['*.html', 'blog/*.html', 'ja/*.html', 'ja/blog/*.html', 'ko/*.html', 'ko/blog/*.html']:
    files.extend(glob.glob(os.path.join(ROOT, pattern)))

files.sort()
changed = []
for f in files:
    rel = os.path.relpath(f, ROOT)
    if process_file(f):
        changed.append(rel)
        print(f'  FIXED: {rel}')
    else:
        print(f'  OK:    {rel}')

print(f'\n总计修改 {len(changed)} 个文件')
if changed:
    print('修改文件:')
    for c in changed:
        print(f'  - {c}')
