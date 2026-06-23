import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import re

PROJECT = Path(r"C:\Users\HYE\WorkBuddy\20260411211839")

takeaway_ja = '''<div class="takeaway-box">
      <h4>📌 まとめ</h4>
      <ul>
        <li>百度PPCは海外企業にとって中国市場への最短ルートです</li>
        <li>BPPがアカウント開設から運用まで全程サポートします</li>
        <li>まずは無料相談でご自身の業界に合う戦略を確認しましょう</li>
      </ul>
    </div>'''

takeaway_ko = '''<div class="takeaway-box">
      <h4>📌 핵심 요약</h4>
      <ul>
        <li>바이두 PPC는 해외 기업이 중국 시장에 진출하는 가장 빠른 경로입니다</li>
        <li>BPP가 계정 개설부터 운영까지 전 과정을 지원합니다</li>
        <li>먼저 무료 상담으로 업종에 맞는 전략을 확인하세요</li>
      </ul>
    </div>'''

takeaway_en = '''<div class="takeaway-box">
      <h4>📌 Key Takeaways</h4>
      <ul>
        <li>GEO is not optional for brands targeting Chinese AI platforms</li>
        <li>This checklist covers 5 critical audit areas for AI visibility</li>
        <li>Start with brand entity optimization — it is the foundation</li>
      </ul>
    </div>'''

articles = [
    "baidu-seo-ppc-synergy",
    "baidu-ppc-monthly-report-template",
    "geo-audit-checklist",
    "geo-content-playbook-chinese-ai",
    "geo-monitoring-brand-ai-search"
]

for slug in articles:
    for lang in ["ja", "ko"]:
        html_path = PROJECT / f"{lang}/blog/{slug}.html"
        if not html_path.exists():
            continue
        html = html_path.read_text(encoding="utf-8")
        
        # Check body content only (between <article> and </article>)
        body_match = re.search(r'<article class="article-content">(.*?)</article>', html, re.DOTALL)
        if not body_match:
            continue
        body = body_match.group(1)
        
        # Check if body has takeaway-box or stats-grid
        has_takeaway = 'takeaway-box' in body
        has_stats = 'stats-grid' in body
        has_table = 'comparison-table' in body
        
        if has_takeaway or has_stats or has_table:
            print(f"{lang}/{slug}: already has visual component in body")
            continue
        
        # Insert before CTA box or before </article>
        cta_match = re.search(r'<div class="cta-box">', html)
        if cta_match:
            takeaway = takeaway_ja if lang == "ja" else takeaway_ko
            html = html[:cta_match.start()] + takeaway + '\n\n    ' + html[cta_match.start():]
        else:
            article_end = html.rfind('</article>')
            takeaway = takeaway_ja if lang == "ja" else takeaway_ko
            html = html[:article_end] + takeaway + '\n    ' + html[article_end:]
        
        html_path.write_text(html, encoding="utf-8")
        print(f"{lang}/{slug}: ✅ added takeaway-box")

# Fix ko/baidu-knowledge-graph-entity-seo
ko_path = PROJECT / "ko/blog/baidu-knowledge-graph-entity-seo.html"
if ko_path.exists():
    html = ko_path.read_text(encoding="utf-8")
    body_match = re.search(r'<article class="article-content">(.*?)</article>', html, re.DOTALL)
    if body_match:
        body = body_match.group(1)
        if 'comparison-table' not in body and 'stats-grid' not in body:
            cta_match = re.search(r'<div class="cta-box">', html)
            if cta_match:
                html = html[:cta_match.start()] + takeaway_ko + '\n\n    ' + html[cta_match.start():]
                ko_path.write_text(html, encoding="utf-8")
                print(f"ko/baidu-knowledge-graph-entity-seo: ✅ added takeaway-box")

# Fix geo-audit-checklist EN
en_path = PROJECT / "blog/geo-audit-checklist.html"
if en_path.exists():
    html = en_path.read_text(encoding="utf-8")
    body_match = re.search(r'<article class="article-content">(.*?)</article>', html, re.DOTALL)
    if body_match:
        body = body_match.group(1)
        has_visual = 'takeaway-box' in body or 'stats-grid' in body or 'comparison-table' in body
        if not has_visual:
            cta_match = re.search(r'<div class="cta-box">', html)
            if cta_match:
                html = html[:cta_match.start()] + takeaway_en + '\n\n    ' + html[cta_match.start():]
                en_path.write_text(html, encoding="utf-8")
                print(f"en/geo-audit-checklist: ✅ added takeaway-box")
