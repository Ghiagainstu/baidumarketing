#!/usr/bin/env python3
"""
fix_blog_ko_final2.py — 最终修复韩语博客详情页 v2
1. 替换整个导航为标准韩语导航（含语言切换器）
2. 修复所有链接为绝对路径
3. 修复日期、阅读时间、作者
"""
import re
import os
import glob

PROJECT = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(PROJECT, "ko", "blog")

# 标准韩语导航 HTML 模板
NAV_TEMPLATE = '''<nav class="nav" id="mainNav">
  <div class="nav-inner">
    <a href="/ko" class="nav-logo"><svg width="28" height="28" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#2932E1"/><text x="16" y="21.5" text-anchor="middle" fill="#fff" font-weight="800" font-size="13">BPP</text></svg> Baidu PPC Pro</a>
    <div class="nav-links" id="navLinks">
      <a href="/ko/why-baidu-ppc-pro">바이두 PPC Pro란</a><a href="/ko/features">서비스</a><a href="/ko/pricing">요금</a><a href="/ko/clients">도입 사례</a><a href="/ko/faq">자주 묻는 질문</a><a href="/ko/about">회사 소개</a><a href="/ko/blog" class="active">블로그</a><a href="/ko/contact">문의하기</a>
    </div>
    <div class="nav-right-group">
      <div class="lang-switch">
        <button class="lang-switch-btn" onclick="event.stopPropagation();toggleLangMenu()" aria-label="언어">🇰🇷<svg width="10" height="6" viewBox="0 0 10 6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M1 1l4 4 4-4"/></svg></button>
        <div class="lang-switch-menu" id="langSwitchMenu">
          <a href="/blog/{slug}" lang="en" class="lang-switch-item">🇺🇸 English</a>
          <a href="/ja/blog/{slug}" lang="ja" class="lang-switch-item">🇯🇵 日本語</a>
          <a href="/ko/blog/{slug}" lang="ko" class="lang-switch-item">🇰🇷 한국어</a>
        </div>
      </div>
      <a href="/ko/contact" class="nav-cta">지금 시작하기 →</a>
    </div>
    <button class="nav-mobile-toggle" onclick="toggleMobileNav()" aria-label="Menu"><svg class="hamburger-icon" width="22" height="22" viewBox="0 0 22 22" fill="none"><rect y="4" width="22" height="2" rx="1" fill="#374151"/><rect y="10" width="22" height="2" rx="1" fill="#374151"/><rect y="16" width="22" height="2" rx="1" fill="#374151"/></svg><svg class="close-icon" width="22" height="22" viewBox="0 0 22 22" fill="none" style="display:none"><line x1="4" y1="4" x2="18" y2="18" stroke="#374151" stroke-width="2" stroke-linecap="round"/><line x1="18" y1="4" x2="4" y2="18" stroke="#374151" stroke-width="2" stroke-linecap="round"/></svg></button>
  </div>
</nav>
<div class="nav-overlay" id="navOverlay" onclick="toggleMobileNav()" aria-hidden="true"></div>'''

# 语言切换器 CSS
LANG_SWITCH_CSS = '''    /* Language switcher */
    .lang-switch { position: relative; z-index: 9999 !important; }
    .lang-switch-btn { display: inline-flex; align-items: center; gap: 4px; padding: 4px 10px; border-radius: 8px; border: 1px solid var(--gray-200); background: transparent; cursor: pointer; font-size: .9rem; color: var(--gray-600); transition: all var(--transition-base); line-height: 1; }
    .lang-switch-btn:hover { border-color: var(--blue); color: var(--blue); }
    .lang-switch-btn:hover svg { transform: rotate(180deg); }
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
    .nav-right-group { display: flex; align-items: center; gap: 8px; }
'''

# 日期映射
MONTH_MAP = {
    'Jan': '1월', 'Feb': '2월', 'Mar': '3월', 'Apr': '4월',
    'May': '5월', 'Jun': '6월', 'Jul': '7월', 'Aug': '8월',
    'Sep': '9월', 'Oct': '10월', 'Nov': '11월', 'Dec': '12월',
}


def fix_file(filepath):
    """修复单个文件"""
    basename = os.path.basename(filepath)
    if basename.startswith("_"):
        return False
    
    slug = basename.replace(".html", "")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # ========== 1. 替换导航 ==========
    # 匹配两种格式: <nav class="nav"...> 和 <nav>...
    nav_pattern = r'<nav[^>]*>.*?</nav>\s*<div[^>]*class="nav-overlay"[^>]*></div>'
    new_nav = NAV_TEMPLATE.format(slug=slug)
    content = re.sub(nav_pattern, new_nav, content, flags=re.DOTALL)
    
    # ========== 2. 添加语言切换器 CSS ==========
    if 'lang-switch-btn' not in content:
        content = content.replace('</style>', LANG_SWITCH_CSS + '\n  </style>')
    
    # ========== 3. 修复 HTML entities → emoji ==========
    content = content.replace('&#x1f1f0;&#x1f1f7;', '🇰🇷')
    content = content.replace('&#x1f1fa;&#x1f1f8;', '🇺🇸')
    content = content.replace('&#x1f1ef;&#x1f1f5;', '🇯🇵')
    
    # ========== 4. 修复日期格式 ==========
    def replace_date(m):
        month_en, day, year = m.group(1), m.group(2).lstrip('0'), m.group(3)
        month_ko = MONTH_MAP.get(month_en, month_en)
        return f'>{year}년 {month_ko} {day}일<'
    content = re.sub(r'>(\w{3}) (\d{1,2}), (\d{4})<', replace_date, content)
    
    # ========== 5. 修复阅读时间 ==========
    content = re.sub(r'>(\d+) min<', r'>\1분 읽기<', content)
    
    # ========== 6. 修复作者 ==========
    content = content.replace('By Baidu PPC Pro Team', 'Baidu PPC Pro 팀')
    
    # ========== 7. 修复 footer 中的相对链接 ==========
    content = content.replace('href="../contact"', 'href="/ko/contact"')
    content = content.replace('href="../index"', 'href="/ko"')
    content = content.replace('href="../features"', 'href="/ko/features"')
    content = content.replace('href="../pricing"', 'href="/ko/pricing"')
    content = content.replace('href="../clients"', 'href="/ko/clients"')
    content = content.replace('href="../faq"', 'href="/ko/faq"')
    content = content.replace('href="../about"', 'href="/ko/about"')
    content = content.replace('href="../blog"', 'href="/ko/blog"')
    content = content.replace('href="../why-baidu-ppc-pro"', 'href="/ko/why-baidu-ppc-pro"')
    content = content.replace('href="../privacy"', 'href="/ko/privacy"')
    content = content.replace('href="../terms"', 'href="/ko/terms"')
    
    # ========== 8. 修复 &rarr; → → ==========
    content = content.replace('&rarr;', '→')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    print("=" * 60)
    print("🇰🇷 最终修复韩语博客详情页 v2")
    print("=" * 60)
    
    files = glob.glob(os.path.join(BLOG_DIR, "*.html"))
    files = [f for f in files if "_template" not in os.path.basename(f)]
    
    fixed = 0
    for filepath in sorted(files):
        basename = os.path.basename(filepath)
        if fix_file(filepath):
            print(f"  ✓ Fixed: {basename}")
            fixed += 1
        else:
            print(f"  - No changes: {basename}")
    
    print("=" * 60)
    print(f"✅ 完成: {fixed}/{len(files)} 个文件已修复")
    print("=" * 60)


if __name__ == "__main__":
    main()
