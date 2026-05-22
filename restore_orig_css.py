#!/usr/bin/env python3
"""
恢复原始博客 CSS + 添加 lang-switch CSS
从 git cae2d63 获取原始 CSS，加 lang-switch 块，替换当前合并后的 CSS
"""
import subprocess, glob

# 读取原始 EN 博客 CSS
def get_orig_css(filepath_in_git):
    result = subprocess.run(['git', 'show', f'cae2d63:{filepath_in_git}'],
                           capture_output=True, text=True, encoding='utf-8')
    html = result.stdout
    start = html.find('<style>')
    end = html.find('</style>')
    return html[start+7:end] if (start != -1 and end != -1) else ''

EN_ORIG = get_orig_css('blog/baidu-ad-billing-models-explained.html')
JA_ORIG = get_orig_css('ja/blog/baidu-ocpc-skip-data-accumulation.html')
print(f'EN 原始 CSS: {len(EN_ORIG)} chars')
print(f'JA 原始 CSS: {len(JA_ORIG)} chars')

# lang-switch CSS（从测试成功的 lang-test.html 提炼）
LANG_CSS = '''
    /* Language switcher */
    .nav-right-group { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
    .lang-switch { position: relative; }
    .lang-switch-btn { display: inline-flex; align-items: center; gap: 4px; padding: 4px 10px; border-radius: 8px; border: 1px solid var(--gray-200); background: transparent; cursor: pointer; font-size: .9rem; color: var(--gray-600); transition: all var(--transition-base); line-height: 1; }
    .lang-switch-btn:hover { border-color: var(--blue); color: var(--blue); }
    .lang-switch-menu { position: absolute; top: calc(100% + 6px); right: 0; background: #fff; border: 1px solid var(--gray-200); border-radius: 8px; box-shadow: var(--shadow-md); min-width: 150px; opacity: 0; pointer-events: none; transform: translateY(-4px); transition: opacity .2s ease, transform .2s ease; z-index: 200; }
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

# 应用到所有 EN 博客
en_count = 0
for path in sorted(glob.glob('blog/*.html')):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    start = html.find('<style>')
    end = html.find('</style>')
    if start == -1:
        continue
    new_css = LANG_CSS + '\n' + EN_ORIG
    html = html[:start+7] + new_css + html[end:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    en_count += 1

# 应用到所有 JA 博客
ja_count = 0
for path in sorted(glob.glob('ja/blog/*.html')):
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    start = html.find('<style>')
    end = html.find('</style>')
    if start == -1:
        continue
    new_css = LANG_CSS + '\n' + JA_ORIG
    html = html[:start+7] + new_css + html[end:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    ja_count += 1

print(f'EN: {en_count} files, JA: {ja_count} files')
print('Done')
