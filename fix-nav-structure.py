import re

FILE = r"c:\Users\HYE\WorkBuddy\20260411211839\blog\baidu-brand-info-account-level.html"

with open(FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 修复 nav-links：添加 nav-mobile-theme 按钮，给 Blog 加 active 类
old_navlinks = '''      <div class="nav-links" id="navLinks">
        <a href="../why-baidu-ppc-pro">Why Baidu PPC Pro</a>
        <a href="../features">Services</a>
        <a href="../pricing">Pricing</a>
        <a href="../clients">Clients</a>
        <a href="../faq">FAQ</a>
        <a href="../about">About</a>
        <a href="../blog" class="active">Blog</a>
        <a href="../contact">Contact</a>
      </div>'''

new_navlinks = '''      <div class="nav-links" id="navLinks">
        <a href="../why-baidu-ppc-pro">Why Baidu PPC Pro</a>
        <a href="../features">Services</a>
        <a href="../pricing">Pricing</a>
        <a href="../clients">Clients</a>
        <a href="../faq">FAQ</a>
        <a href="../about">About</a>
        <a href="../blog" class="active">Blog</a>
        <a href="../contact">Contact</a>
        <button class="nav-mobile-theme" onclick="toggleTheme()">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
          Toggle Dark Mode
        </button>
      </div>'''

html = html.replace(old_navlinks, new_navlinks)

# 2. 修复 theme-toggle + nav-cta：添加 nav-right-group wrapper 和 lang-switch
old_right = '''      <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode" onclick="toggleTheme()">
        <svg class="icon-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
        <svg class="icon-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
      </button><a href="../contact" class="nav-cta">Get Started →</a>'''

new_right = '''      <div class="nav-right-group">
      <div class="lang-switch">
        <button class="lang-switch-btn" onclick="toggleLangMenu()" aria-label="Language">
          🇺🇸
          <svg width="10" height="6" viewBox="0 0 10 6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M1 1l4 4 4-4"/></svg>
        </button>
        <div class="lang-switch-menu" id="langSwitchMenu">
            <a href="../index" lang="en" class="lang-switch-item">🇺🇸 English</a>
            <a href="../ja/index" lang="ja" class="lang-switch-item">🇯🇵 日本語</a>
        </div>
      </div>
      <button class="theme-toggle" id="themeToggle" aria-label="Toggle dark mode" onclick="toggleTheme()">
        <svg class="icon-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        <svg class="icon-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
      </button>
      <a href="../contact" class="nav-cta">Get Started →</a>
      </div>'''

html = html.replace(old_right, new_right)

# 3. 修复 hamburger SVG：用 rect 替代 path
old_hamburger = '''      <button class="nav-mobile-toggle" id="navToggle" aria-label="Menu" onclick="toggleMobileNav()"><svg viewBox="0 0 24 24" width="24" height="24"><path d="M3 12h18M3 6h18M3 18h18" stroke="currentColor" stroke-width="2" stroke-linecap="round"></path></svg></button>'''

new_hamburger = '''      <button class="nav-mobile-toggle" id="navToggle" aria-label="Menu" onclick="toggleMobileNav()">
        <svg class="hamburger-icon" width="22" height="22" viewBox="0 0 22 22" fill="none"><rect y="4" width="22" height="2" rx="1" fill="#374151"/><rect y="10" width="22" height="2" rx="1" fill="#374151"/><rect y="16" width="22" height="2" rx="1" fill="#374151"/></svg>
        <svg class="close-icon" width="22" height="22" viewBox="0 0 22 22" fill="none" style="display:none"><line x1="4" y1="4" x2="18" y2="18" stroke="#374151" stroke-width="2" stroke-linecap="round"/><line x1="18" y1="4" x2="4" y2="18" stroke="#374151" stroke-width="2" stroke-linecap="round"/></svg>
      </button>'''

html = html.replace(old_hamburger, new_hamburger)

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Fixed nav structure:")
print("   - Added nav-mobile-theme button")
print("   - Added nav-right-group wrapper")
print("   - Added lang-switch language switcher")
print("   - Fixed hamburger SVG (rect instead of path)")
print("   - Added close-icon SVG")
