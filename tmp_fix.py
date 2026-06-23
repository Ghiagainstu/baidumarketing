import re
from pathlib import Path

SLUG = "b2b-manufacturer-baidu-case-study"
PROJECT = Path(r"C:\Users\HYE\WorkBuddy\20260411211839")

for lang, footer_text, home_text, blog_text, base_url in [
    ("ja", "無断転載を禁じます", "ホーム", "ブログ", "https://www.baidumarketing.com/ja/blog/"),
    ("ko", "무단전재를 금지합니다", "홈", "블로그", "https://www.baidumarketing.com/ko/blog/"),
]:
    path = PROJECT / lang / "blog" / f"{SLUG}.html"
    html = path.read_text(encoding="utf-8")
    
    # Fix footer
    html = re.sub(r'(class="footer-copy">).*?(</div>)', rf'\1© <script>document.write(new Date().getFullYear())</script> Baidu PPC Pro. {footer_text}\2', html, count=1)
    
    # Fix canonical
    html = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{base_url}{SLUG}" />', html)
    html = re.sub(r'property="og:url" content="[^"]*">', f'property="og:url" content="{base_url}{SLUG}">', html)
    
    # Fix breadcrumb
    html = re.sub(r'(class="breadcrumb">).*?(</div>)', rf'\1<a href="/{lang}/">{home_text}</a> / <a href="/{lang}/blog">{blog_text}</a>\2', html, count=1)
    
    # Fix garbled nav text
    replacements = {
        "ja": {"銈点兗銉撱偣": "サービス", "鏂欓噾": "料金", "灏庡叆浜嬩緥": "導入事例", "銈堛亸銇傘倠璩屽晱": "よくある質問", "浼氱ぞ姒傝": "会社概要", "銇婂晱銇勫悎銈忋仜": "お問い合わせ", "鐧惧害PPC Pro銇ㄣ伅": "百度PPC Proとは", "銉栥儹銈?": "ブログ", "浠娿仚銇愬銈併倠 鈫?": "今すぐ始める →", "銈炽兗銉?": "ホーム", "銉涖兗銉?": "ホーム"},
        "ko": {},
    }
    for old, new in replacements.get(lang, {}).items():
        html = html.replace(old, new)
    
    path.write_text(html, encoding="utf-8")
    print(f"✅ {lang} fixed")
