#!/usr/bin/env python3
"""恢复原始博客 CSS + 只加 lang-switch——去掉合并的 index.html 所有 CSS"""
import glob

# 从 lang-test.html 提炼的最小化 lang-switch CSS 块
LANG_CSS = '''
    /* Language switcher in nav */
    .nav-right-group { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
    .lang-switch { position: relative; z-index: 9999; }
    .lang-switch-btn { display: inline-flex; align-items: center; gap: 4px; padding: 4px 10px; border-radius: 8px; border: 1px solid var(--gray-200); background: transparent; cursor: pointer; font-size: .9rem; color: var(--gray-600); transition: all var(--transition-base); line-height: 1; position: relative; z-index: 9999; }
    .lang-switch-btn:hover { border-color: var(--blue); color: var(--blue); }
    .lang-switch-menu { position: absolute; top: calc(100% + 6px); right: 0; background: #fff; border: 1px solid var(--gray-200); border-radius: 8px; box-shadow: var(--shadow-md); min-width: 150px; opacity: 0; pointer-events: none; transform: translateY(-4px); transition: opacity .2s ease, transform .2s ease; z-index: 9999; }
    .lang-switch-menu.open { opacity: 1; pointer-events: auto; transform: translateY(0); }
    .lang-switch-item { display: block; padding: 10px 16px; font-size: .9rem; color: var(--gray-700); transition: background .15s; white-space: nowrap; text-decoration: none; }
    .lang-switch-item:hover { background: var(--blue-light); color: var(--blue); }
    .lang-switch-item:first-child { border-radius: 7px 7px 0 0; }
    .lang-switch-item:last-child { border-radius: 0 0 7px 7px; }
    [data-theme="dark"] .lang-switch-btn { border-color: var(--gray-200); color: var(--gray-600); }
    [data-theme="dark"] .lang-switch-btn:hover { border-color: var(--blue); color: var(--blue); }
    [data-theme="dark"] .lang-switch-menu { background: #0B0F1A; border-color: var(--gray-200); }
    [data-theme="dark"] .lang-switch-item { color: var(--gray-700); }
    [data-theme="dark"] .lang-switch-item:hover { background: rgba(99,102,241,.12); color: var(--blue); }
    @media (max-width: 900px) { .lang-switch { display: none; } }
'''

def get_blog_specific_css(full_css):
    """从合并后的 CSS 中提取博客特定的 CSS（去掉 index.html 的 CSS）"""
    # 合并 CSS 的格式: [index.css]\n\n[blog.css]
    # 博客 CSS 通常从 @media 规则或 blog-specific 规则开始
    # 查找 blog.css 的特征：以 @media 或 .article- 等开头
    lines = full_css.split('\n')
    for i, line in enumerate(lines):
        if '.article-' in line or '.breadcrumb' in line or '.blog-' in line:
            return '\n'.join(lines[i:])
    # fallback: 返回后半部分
    return '\n'.join(lines[len(lines)//2:])

for pattern in ['blog/*.html', 'ja/blog/*.html']:
    for path in sorted(glob.glob(pattern)):
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        
        # 提取当前合并后的 CSS
        start = html.find('<style>')
        end = html.find('</style>')
        if start == -1 or end == -1:
            continue
        
        full_css = html[start+7:end]
        blog_css = get_blog_specific_css(full_css)
        
        # 构建新的 CSS: lang_css + blog_css
        new_css = LANG_CSS + '\n' + blog_css
        
        # 替换
        html = html[:start+7] + new_css + html[end:]
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        slug = path.replace('\\', '/').split('/')[-1]
        print(f'  ✅ {slug}: {len(new_css)} chars')

print('Done')
