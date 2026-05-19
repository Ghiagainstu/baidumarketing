import re

FILE = r"c:\Users\HYE\WorkBuddy\20260411211839\blog\baidu-brand-info-account-level.html"

with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 添加 lang-switch CSS（在 .nav-mobile-toggle CSS 之后）
lang_switch_css = '''    .lang-switch { position: relative; }
    .lang-switch-btn {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 4px 10px;
      border-radius: 8px;
      border: 1px solid var(--gray-200);
      background: transparent;
      cursor: pointer;
      font-size: .9rem;
      color: var(--gray-600);
      transition: all var(--transition-base);
      line-height: 1;
    }
    .lang-switch-btn:hover {
      border-color: var(--blue);
      color: var(--blue);
    }
    .lang-switch-menu {
      position: absolute;
      top: calc(100% + 6px);
      right: 0;
      background: #fff;
      border: 1px solid var(--gray-200);
      border-radius: 8px;
      box-shadow: var(--shadow-md);
      min-width: 150px;
      opacity: 0;
      pointer-events: none;
      transform: translateY(-4px);
      transition: opacity .2s ease, transform .2s ease;
      z-index: 200;
    }
    .lang-switch-menu.open {
      opacity: 1;
      pointer-events: auto;
      transform: translateY(0);
    }
    .lang-switch-item {
      display: block;
      padding: 10px 16px;
      font-size: .9rem;
      color: var(--gray-700);
      transition: background .15s;
      white-space: nowrap;
    }
    .lang-switch-item:hover {
      background: var(--blue-light);
      color: var(--blue);
    }
    .lang-switch-item:first-child { border-radius: 7px 7px 0 0; }
    .lang-switch-item:last-child { border-radius: 0 0 7px 7px; }
    [data-theme="dark"] .lang-switch-btn {
      border-color: var(--gray-200);
      color: var(--gray-600);
    }
    [data-theme="dark"] .lang-switch-btn:hover {
      border-color: var(--blue);
      color: var(--blue);
    }
    [data-theme="dark"] .lang-switch-menu {
      background: #0B0F1A;
      border-color: var(--gray-200);
    }
    [data-theme="dark"] .lang-switch-item {
      color: var(--gray-700);
    }
    [data-theme="dark"] .lang-switch-item:hover {
      background: rgba(99,102,241,.12);
      color: var(--blue);
    }
'''

# 插入到 .nav-mobile-toggle CSS 之后
html = html.replace(
    '    .nav-mobile-toggle { display: none; background: none; border: none; cursor: pointer; }',
    '    .nav-mobile-toggle { display: none; background: none; border: none; cursor: pointer; }\n' + lang_switch_css
)

# 2. 添加 toggleLangMenu JS（在 toggleTheme 函数之后）
toggle_lang_js = '''
function toggleLangMenu() {
  const menu = document.getElementById('langSwitchMenu');
  if (menu) menu.classList.toggle('open');
}

document.addEventListener('click', function(e) {
  const sw = document.querySelector('.lang-switch');
  if (sw && !sw.contains(e.target)) {
    const menu = document.getElementById('langSwitchMenu');
    if (menu) menu.classList.remove('open');
  }
});
'''

# 查找 toggleTheme 函数并在其后添加
pattern = r'(function toggleTheme\(\)[^}]+\})'
match = re.search(pattern, html)
if match:
    insert_pos = match.end()
    html = html[:insert_pos] + '\n' + toggle_lang_js + html[insert_pos:]

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Added lang-switch CSS + toggleLangMenu JS")
