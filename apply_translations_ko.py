#!/usr/bin/env python3
"""
apply_translations_ko.py — 应用翻译文件到页面
用法：python apply_translations_ko.py <slug>
输入：translated_texts_<slug>.txt（格式：序号|原文|译文）
"""
import re
import os
import sys

PROJECT = os.path.dirname(os.path.abspath(__file__))

def load_translations(filepath):
    """加载翻译文件"""
    translations = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('|')
            if len(parts) >= 3:
                original = parts[1].strip()
                translated = parts[2].strip()
                if original and translated:
                    translations[original] = translated
    return translations


def apply_translations(html, translations):
    """应用翻译到 HTML"""
    for original, translated in translations.items():
        # 转义特殊字符
        escaped = re.escape(original)
        # 替换标签之间的文本
        html = re.sub(r'>' + escaped + r'<', '>' + translated + '<', html)
    return html


def fix_language_switcher(html):
    """修复语言切换器"""
    # 修复按钮
    html = re.sub(
        r'<button class="lang-switch-btn"[^>]*>.*?</button>',
        '<button class="lang-switch-btn" onclick="toggleLangMenu()" aria-label="Language">🇰🇷 <svg width="10" height="6" viewBox="0 0 10 6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M1 1l4 4 4-4"/></svg></button>',
        html,
        flags=re.DOTALL
    )
    
    # 修复菜单
    html = re.sub(
        r'<div class="lang-switch-menu"[^>]*>.*?</div>',
        '''<div class="lang-switch-menu" id="langSwitchMenu">
          <a href="/" lang="en" class="lang-switch-item">🇺🇸 English</a>
          <a href="/ja" lang="ja" class="lang-switch-item">🇯🇵 日本語</a>
          <a href="/ko" lang="ko" class="lang-switch-item">🇰🇷 한국어</a>
        </div>''',
        html,
        flags=re.DOTALL
    )
    
    return html


def update_links(html, slug):
    """更新链接为韩语路径"""
    # 更新导航链接
    html = re.sub(r'href="/about"', 'href="/ko/about"', html)
    html = re.sub(r'href="/features"', 'href="/ko/features"', html)
    html = re.sub(r'href="/pricing"', 'href="/ko/pricing"', html)
    html = re.sub(r'href="/clients"', 'href="/ko/clients"', html)
    html = re.sub(r'href="/faq"', 'href="/ko/faq"', html)
    html = re.sub(r'href="/contact"', 'href="/ko/contact"', html)
    html = re.sub(r'href="/blog"', 'href="/ko/blog"', html)
    html = re.sub(r'href="/why-baidu-ppc-pro"', 'href="/ko/why-baidu-ppc-pro"', html)
    html = re.sub(r'href="/privacy"', 'href="/ko/privacy"', html)
    html = re.sub(r'href="/terms"', 'href="/ko/terms"', html)
    html = re.sub(r'href="/china-geo"', 'href="/ko/china-geo"', html)
    
    # 更新 canonical
    html = re.sub(r'href="https://www\.baidumarketing\.com/' + slug + '"', 
                  f'href="https://www.baidumarketing.com/ko/{slug}"', html)
    
    # 更新 OG URL
    html = re.sub(r'content="https://www\.baidumarketing\.com/' + slug + '"', 
                  f'content="https://www.baidumarketing.com/ko/{slug}"', html)
    
    return html


def main():
    if len(sys.argv) < 2:
        print("用法: python apply_translations_ko.py <slug>")
        sys.exit(1)
    
    slug = sys.argv[1]
    en_path = os.path.join(PROJECT, f"{slug}.html")
    ko_path = os.path.join(PROJECT, "ko", f"{slug}.html")
    trans_path = os.path.join(PROJECT, f"translated_texts_{slug}.txt")
    
    if not os.path.exists(en_path):
        print(f"✗ EN 文件不存在: {en_path}")
        sys.exit(1)
    
    if not os.path.exists(trans_path):
        print(f"✗ 翻译文件不存在: {trans_path}")
        print(f"  请先运行: python translate_page_ko.py {slug}")
        sys.exit(1)
    
    # 加载翻译
    translations = load_translations(trans_path)
    print(f"📖 加载翻译: {len(translations)} 条")
    
    # 读取 EN 页面
    with open(en_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 更新 lang 属性
    html = html.replace('lang="en"', 'lang="ko"')
    
    # 应用翻译
    html = apply_translations(html, translations)
    
    # 修复语言切换器
    html = fix_language_switcher(html)
    
    # 更新链接
    html = update_links(html, slug)
    
    # 写入文件
    os.makedirs(os.path.dirname(ko_path), exist_ok=True)
    with open(ko_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 翻译应用完成: ko/{slug}.html ({len(html)} bytes)")


if __name__ == "__main__":
    main()
