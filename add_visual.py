import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import re

PROJECT = Path(r"C:\Users\HYE\WorkBuddy\20260411211839")

# Articles that need visual components
articles = [
    "baidu-seo-ppc-synergy",
    "baidu-ppc-monthly-report-template",
    "baidu-knowledge-graph-entity-seo",
    "geo-audit-checklist",
    "geo-content-playbook-chinese-ai",
    "geo-monitoring-brand-ai-search"
]

# JA and KO takeaway-box content
takeaway_ja = '''
<div class="takeaway-box">
  <h4>📌 まとめ</h4>
  <ul>
    <li>百度PPCは海外企業にとって中国市場への最短ルートです</li>
    <li>BPPがアカウント開設から運用まで全程サポートします</li>
    <li>まずは無料相談でご自身の業界に合う戦略を確認しましょう</li>
  </ul>
</div>
'''

takeaway_ko = '''
<div class="takeaway-box">
  <h4>📌 핵심 요약</h4>
  <ul>
    <li>바이두 PPC는 해외 기업이 중국 시장에 진출하는 가장 빠른 경로입니다</li>
    <li>BPP가 계정 개설부터 운영까지 전 과정을 지원합니다</li>
    <li>먼저 무료 상담으로 업종에 맞는 전략을 확인하세요</li>
  </ul>
</div>
'''

for slug in articles:
    for lang in ["ja", "ko"]:
        html_path = PROJECT / f"{lang}/blog/{slug}.html"
        if not html_path.exists():
            continue
        
        html = html_path.read_text(encoding="utf-8")
        
        # Check if already has takeaway-box
        if 'takeaway-box' in html or 'stats-grid' in html:
            print(f"{lang}/{slug}: already has visual components")
            continue
        
        # Find the CTA box and insert takeaway-box before it
        cta_match = re.search(r'<div class="cta-box">', html)
        if cta_match:
            takeaway = takeaway_ja if lang == "ja" else takeaway_ko
            html = html[:cta_match.start()] + takeaway + '\n    ' + html[cta_match.start():]
            html_path.write_text(html, encoding="utf-8")
            print(f"{lang}/{slug}: added takeaway-box")
        else:
            # Try inserting before closing </article>
            article_end = html.rfind('</article>')
            if article_end > 0:
                takeaway = takeaway_ja if lang == "ja" else takeaway_ko
                html = html[:article_end] + takeaway + '\n    ' + html[article_end:]
                html_path.write_text(html, encoding="utf-8")
                print(f"{lang}/{slug}: added takeaway-box before </article>")
            else:
                print(f"{lang}/{slug}: could not find insertion point")

# Also fix geo-audit-checklist EN if it only has cta-box
en_path = PROJECT / "blog/geo-audit-checklist.html"
if en_path.exists():
    html = en_path.read_text(encoding="utf-8")
    if 'takeaway-box' not in html and 'stats-grid' not in html:
        cta_match = re.search(r'<div class="cta-box">', html)
        if cta_match:
            takeaway_en = '''
<div class="takeaway-box">
  <h4>📌 Key Takeaways</h4>
  <ul>
    <li>GEO is not optional for brands targeting Chinese AI platforms</li>
    <li>This checklist covers 5 critical audit areas for AI visibility</li>
    <li>Start with brand entity optimization — it is the foundation</li>
  </ul>
</div>
'''
            html = html[:cta_match.start()] + takeaway_en + '\n    ' + html[cta_match.start():]
            en_path.write_text(html, encoding="utf-8")
            print(f"en/geo-audit-checklist: added takeaway-box")
