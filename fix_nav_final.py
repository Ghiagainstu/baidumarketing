#!/usr/bin/env python3
"""彻底修复所有博客文件的 nav 链接和 nav-cta"""
import glob, re

EN_NAV_TEMPLATE = '''<nav><div class="container nav-inner">
<a href="/index.html" class="nav-logo"><svg width="32" height="32" viewBox="0 0 32 32" fill="none"><defs><linearGradient id="l" x1="0" y1="0" x2="32" y2="32"><stop offset="0%" stop-color="#2932E1"/><stop offset="100%" stop-color="#4F46E5"/></linearGradient></defs><rect width="32" height="32" rx="8" fill="url(#l)"/><path d="M9.5 11.5c0-1.1.9-2 2-2h9c1.1 0 2 .9 2 2v9c0 1.1-.9 2-2 2h-9c-1.1 0-2-.9-2-2v-9z" stroke="white" stroke-width="1.2" fill="none" opacity=".35"/><text x="16" y="21" text-anchor="middle" font-family="Inter,system-ui,sans-serif" font-size="12" font-weight="800" fill="white" letter-spacing=".3">BPP</text></svg>Baidu PPC Pro</a>
<div class="nav-links" id="navLinks">
<a href="/why-baidu-ppc-pro.html">Why Baidu PPC Pro</a><a href="/features.html">Services</a><a href="/pricing.html">Pricing</a><a href="/clients.html">Clients</a><a href="/faq.html">FAQ</a><a href="/about.html">About</a><a href="/blog.html" class="active">Blog</a><a href="/contact.html">Contact</a>
</div>
      <div class="nav-right-group">
      <div class="lang-switch">
        <button class="lang-switch-btn" onclick="toggleLangMenu()" aria-label="Language">&#x1f1fa;&#x1f1f8;<svg width="10" height="6" viewBox="0 0 10 6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M1 1l4 4 4-4"/></svg></button>
        <div class="lang-switch-menu" id="langSwitchMenu">
            <a href="/blog/SLUG" lang="en" class="lang-switch-item">&#x1f1fa;&#x1f1f8; English</a>
            <a href="/ja/blog/SLUG" lang="ja" class="lang-switch-item">&#x1f1ef;&#x1f1f5; 日本語</a>
        </div>
      </div>
      <a href="/contact.html" class="nav-cta">Get Started &rarr;</a>
      </div>
<button class="nav-mobile-toggle" onclick="toggleMobileNav()" aria-label="Menu"><svg class="hamburger-icon" width="22" height="22" viewBox="0 0 22 22" fill="none"><rect y="4" width="22" height="2" rx="1" fill="#374151"/><rect y="10" width="22" height="2" rx="1" fill="#374151"/><rect y="16" width="22" height="2" rx="1" fill="#374151"/></svg><svg class="close-icon" width="22" height="22" viewBox="0 0 22 22" fill="none" style="display:none"><line x1="4" y1="4" x2="18" y2="18" stroke="#374151" stroke-width="2" stroke-linecap="round"/><line x1="18" y1="4" x2="4" y2="18" stroke="#374151" stroke-width="2" stroke-linecap="round"/></svg></button>
</div></nav>'''

JA_NAV_TEMPLATE = '''<nav><div class="container nav-inner">
<a href="/ja/index.html" class="nav-logo"><svg width="32" height="32" viewBox="0 0 32 32" fill="none"><defs><linearGradient id="l" x1="0" y1="0" x2="32" y2="32"><stop offset="0%" stop-color="#2932E1"/><stop offset="100%" stop-color="#4F46E5"/></linearGradient></defs><rect width="32" height="32" rx="8" fill="url(#l)"/><path d="M9.5 11.5c0-1.1.9-2 2-2h9c1.1 0 2 .9 2 2v9c0 1.1-.9 2-2 2h-9c-1.1 0-2-.9-2-2v-9z" stroke="white" stroke-width="1.2" fill="none" opacity=".35"/><text x="16" y="21" text-anchor="middle" font-family="Inter,system-ui,sans-serif" font-size="12" font-weight="800" fill="white" letter-spacing=".3">BPP</text></svg>Baidu PPC Pro</a>
<div class="nav-links" id="navLinks">
<a href="/ja/why-baidu-ppc-pro.html">選ばれる理由</a><a href="/ja/features.html">サービス</a><a href="/ja/pricing.html">料金プラン</a><a href="/ja/clients.html">実績</a><a href="/ja/faq.html">よくある質問</a><a href="/ja/about.html">会社概要</a><a href="/ja/blog.html" class="active">ブログ</a><a href="/ja/contact.html">お問い合わせ</a>
</div>
      <div class="nav-right-group">
      <div class="lang-switch">
        <button class="lang-switch-btn" onclick="toggleLangMenu()" aria-label="言語">&#x1f1ef;&#x1f1f5;<svg width="10" height="6" viewBox="0 0 10 6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M1 1l4 4 4-4"/></svg></button>
        <div class="lang-switch-menu" id="langSwitchMenu">
            <a href="/blog/SLUG" lang="en" class="lang-switch-item">&#x1f1fa;&#x1f1f8; English</a>
            <a href="/ja/blog/SLUG" lang="ja" class="lang-switch-item">&#x1f1ef;&#x1f1f5; 日本語</a>
        </div>
      </div>
      <a href="/ja/contact.html" class="nav-cta">今すぐ始める →</a>
      </div>
<button class="nav-mobile-toggle" onclick="toggleMobileNav()" aria-label="Menu"><svg class="hamburger-icon" width="22" height="22" viewBox="0 0 22 22" fill="none"><rect y="4" width="22" height="2" rx="1" fill="#374151"/><rect y="10" width="22" height="2" rx="1" fill="#374151"/><rect y="16" width="22" height="2" rx="1" fill="#374151"/></svg><svg class="close-icon" width="22" height="22" viewBox="0 0 22 22" fill="none" style="display:none"><line x1="4" y1="4" x2="18" y2="18" stroke="#374151" stroke-width="2" stroke-linecap="round"/><line x1="18" y1="4" x2="4" y2="18" stroke="#374151" stroke-width="2" stroke-linecap="round"/></svg></button>
</div></nav>'''

def fix_blog_files(pattern, template, lang):
    count = 0
    for path in sorted(glob.glob(pattern)):
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
        slug = path.replace('\\', '/').split('/')[-1].replace('.html', '')
        old_nav_s = html.find('<nav')
        old_nav_e = html.find('</nav>') + len('</nav>')
        if old_nav_s == -1:
            continue
        new_nav = template.replace('SLUG', slug)
        html = html[:old_nav_s] + new_nav + html[old_nav_e:]
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        count += 1
        print(f'  ✅ {path.split("/")[-1]}')
    return count

en = fix_blog_files('blog/*.html', EN_NAV_TEMPLATE, 'en')
ja = fix_blog_files('ja/blog/*.html', JA_NAV_TEMPLATE, 'ja')
print(f'\n结果: EN={en}, JA={ja}')
