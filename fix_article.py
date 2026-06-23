import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import re

PROJECT = Path(r"C:\Users\HYE\WorkBuddy\20260411211839")
SLUG = sys.argv[1] if len(sys.argv) > 1 else "baidu-account-opening-foreign-companies"

# Read the JA/KO MD files for frontmatter
for lang in ["ja", "ko"]:
    template_path = PROJECT / f"{lang}/blog/_template-{lang}.html"
    output_path = PROJECT / f"{lang}/blog/{SLUG}.html"
    md_path = PROJECT / "blog-drafts" / SLUG / f"{SLUG}-{lang}.md"
    
    if not template_path.exists():
        print(f"Template not found: {template_path}")
        continue
    
    # Read template fresh (known-good encoding)
    template = template_path.read_text(encoding="utf-8")
    
    # Read MD for frontmatter
    md_text = md_path.read_text(encoding="utf-8-sig")
    fm_match = re.match(r'^---\s*\n(.*?)\n---', md_text, re.DOTALL)
    fm = {}
    if fm_match:
        for line in fm_match.group(1).split('\n'):
            m = re.match(r'^(\w+):\s*"?(.*?)"?\s*$', line)
            if m:
                fm[m.group(1)] = m.group(2)
    
    # Read the existing generated HTML to extract body content
    if output_path.exists():
        existing = output_path.read_text(encoding="utf-8")
        # Extract article-content body
        body_match = re.search(r'<article class="article-content">(.*?)</article>', existing, re.DOTALL)
        if body_match:
            body_html = body_match.group(1).strip()
            print(f"{lang}: extracted body ({len(body_html)} chars)")
        else:
            print(f"{lang}: no body found in existing HTML")
            body_html = ""
    else:
        print(f"{lang}: no existing HTML to extract body from")
        body_html = ""
    
    # Now build from template
    title = fm.get("title", "")
    description = fm.get("description", "")
    date = fm.get("date", "")
    reading_time = fm.get("reading_time", "")
    author = fm.get("author", "Baidu PPC Pro Team")
    
    canonical_prefix = f"https://www.baidumarketing.com/{lang}/blog/"
    
    html = template
    html = html.replace("{{SLUG}}", SLUG)
    html = html.replace("{{TITLE}}", title)
    # Format date per language
    from datetime import datetime
    try:
        dt = datetime.strptime(date, '%Y-%m-%d')
        if lang == 'ja':
            date_display = f'{dt.year}年{dt.month}月{dt.day}日'
        elif lang == 'ko':
            date_display = f'{dt.year}년 {dt.month}월 {dt.day}일'
        else:
            date_display = dt.strftime('%b %d, %Y')
    except ValueError:
        date_display = date
    html = html.replace("{{DATE}}", date_display)
    html = html.replace("{{READ_TIME}}", reading_time)
    html = html.replace("{{CATEGORY}}", fm.get("category", "strategy"))
    html = html.replace("{{AUTHOR}}", author)
    html = html.replace("{{BODY}}", body_html)
    
    # CTA
    if lang == "ja":
        html = html.replace("{{CTA_TITLE}}", "2026年に百度をブランドに活かす準備はできていますか？")
        html = html.replace("{{CTA_TEXT}}", "BPPのチームが、業界、予算、目標に合った現実的な選択肢をご案内します。高圧的ではなく、実直に。")
        html = html.replace("{{CTA_LINK}}", "/ja/contact")
        html = html.replace("{{CTA_BTN}}", "BPPに問い合わせる")
    else:
        html = html.replace("{{CTA_TITLE}}", "2026년 바이두를 브랜드에 활용할 준비가 되셨나요?")
        html = html.replace("{{CTA_TEXT}}", "BPP 팀이 업종, 예산, 목표에 맞는 현실적인 옵션을 안내해 드립니다. 강요 없이, 솔직하게.")
        html = html.replace("{{CTA_LINK}}", "/ko/contact")
        html = html.replace("{{CTA_BTN}}", "BPP에 문의하기")
    
    # Fix meta tags
    html = re.sub(r'<title>[^<]*</title>', f'<title>{title} \u2014 Baidu PPC Pro Blog</title>', html)
    html = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{description}">', html)
    html = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{title}">', html)
    html = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{description}">', html)
    html = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{canonical_prefix}{SLUG}">', html)
    html = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{title}">', html)
    html = re.sub(r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{description}">', html)
    html = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{canonical_prefix}{SLUG}">', html)
    
    # Fix hreflang
    html = re.sub(r'href="https://www\.baidumarketing\.com/blog/[^"]*"', f'href="https://www.baidumarketing.com/blog/{SLUG}"', html)
    html = re.sub(r'href="https://www\.baidumarketing\.com/ja/blog/[^"]*"', f'href="https://www.baidumarketing.com/ja/blog/{SLUG}"', html)
    html = re.sub(r'href="https://www\.baidumarketing\.com/ko/blog/[^"]*"', f'href="https://www.baidumarketing.com/ko/blog/{SLUG}"', html)
    
    # Fix JSON-LD
    html = re.sub(r'"headline":"[^"]*"', f'"headline":"{title}"', html)
    html = re.sub(r'"description":"[^"]*"', f'"description":"{description}"', html)
    html = re.sub(r'"datePublished":"[^"]*"', f'"datePublished":"{date}"', html)
    html = re.sub(r'"dateModified":"[^"]*"', f'"dateModified":"{date}"', html)
    html = re.sub(r'"@id":"https://www\.baidumarketing\.com/(?:ja/|ko/)?blog/[^"]*"', f'"@id":"{canonical_prefix}{SLUG}"', html)
    
    # Fix blog card links in lang-switch (they reference old slugs from template)
    html = re.sub(r'href="/blog/[^"]*" lang="en"', f'href="/blog/{SLUG}" lang="en"', html)
    html = re.sub(r'href="/ja/blog/[^"]*" lang="ja"', f'href="/ja/blog/{SLUG}" lang="ja"', html)
    html = re.sub(r'href="/ko/blog/[^"]*" lang="ko"', f'href="/ko/blog/{SLUG}" lang="ko"', html)
    
    # Write with explicit UTF-8 BOM-less encoding
    # Fix KO footer if needed
    if lang == "ko":
        html = html.replace('Baidu PPC Pro. All rights reserved.', 'Baidu PPC Pro. \ubb34\ub2e8\uc804\uc7ac\ub97c \uae08\uc9c0\ud569\ub2c8\ub2e4.')
    output_path.write_text(html, encoding="utf-8")
    
    # Verify
    verify = output_path.read_text(encoding="utf-8")
    has_service = "サービス" in verify if lang == "ja" else True
    has_nihongo = "日本語" in verify if lang == "ja" else "한국어" in verify
    print(f"{lang}: Written {len(html)} chars. Has correct text: service={has_service}, lang_name={has_nihongo}")
