import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import re

PROJECT = Path(r"C:\Users\HYE\WorkBuddy\20260411211839")
articles = [
    "baidu-seo-ppc-synergy",
    "baidu-ppc-monthly-report-template",
    "baidu-knowledge-graph-entity-seo",
    "geo-audit-checklist",
    "geo-content-playbook-chinese-ai",
    "geo-monitoring-brand-ai-search"
]

for slug in articles:
    for lang in ["ja", "ko"]:
        html_path = PROJECT / f"{lang}/blog/{slug}.html"
        html = html_path.read_text(encoding="utf-8")
        # Check for each visual component type
        components = {
            "stats-grid": len(re.findall(r'class="stats-grid"', html)),
            "callout": len(re.findall(r'class="callout', html)),
            "takeaway-box": len(re.findall(r'class="takeaway-box"', html)),
            "comparison-table": len(re.findall(r'class="comparison-table"', html)),
            "cta-box": len(re.findall(r'class="cta-box"', html)),
        }
        count = sum(1 for v in components.values() if v > 0)
        detail = ", ".join(f"{k}:{v}" for k, v in components.items() if v > 0)
        status = "✅" if count >= 2 else "❌"
        print(f"{status} {lang}/{slug}: {count} types ({detail})")
