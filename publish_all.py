import sys
sys.stdout.reconfigure(encoding='utf-8')
import subprocess
from pathlib import Path

PROJECT = Path(r"C:\Users\HYE\WorkBuddy\20260411211839")
PYTHON = r"C:\Users\HYE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

# Articles to publish (slug, category, date_en, date_ja, date_ko)
articles = [
    ("baidu-ppc-education-industry", "strategy", "Jun 23, 2026", "2026年6月23日", "2026년 6월 23일"),
    ("how-to-choose-baidu-ppc-agency", "strategy", "Jun 23, 2026", "2026年6月23日", "2026년 6월 23일"),
    ("baidu-seo-ppc-synergy", "strategy", "Jun 23, 2026", "2026年6月23日", "2026년 6월 23일"),
    ("baidu-ppc-monthly-report-template", "platform", "Jun 23, 2026", "2026年6月23日", "2026년 6월 23일"),
    ("geo-get-brand-cited-by-chinese-ai", "strategy", "Jun 23, 2026", "2026年6月23日", "2026년 6월 23일"),
    ("geo-vs-ppc-budget-allocation", "strategy", "Jun 23, 2026", "2026年6月23日", "2026년 6월 23일"),
    ("baidu-knowledge-graph-entity-seo", "platform", "Jun 23, 2026", "2026年6月23日", "2026년 6월 23일"),
    ("geo-audit-checklist", "strategy", "Jun 23, 2026", "2026年6月23日", "2026년 6월 23일"),
    ("geo-content-playbook-chinese-ai", "strategy", "Jun 23, 2026", "2026年6月23日", "2026년 6월 23일"),
    ("geo-monitoring-brand-ai-search", "strategy", "Jun 23, 2026", "2026年6月23日", "2026년 6월 23일"),
]

import re

def get_fm(slug, lang):
    md_path = PROJECT / "blog-drafts" / slug / f"{slug}-{lang}.md"
    md = md_path.read_text(encoding="utf-8-sig")
    fm = {}
    m = re.match(r'^---\s*\n(.*?)\n---', md, re.DOTALL)
    if m:
        for line in m.group(1).split('\n'):
            kv = re.match(r'^(\w+):\s*"?(.*?)"?\s*$', line)
            if kv:
                fm[kv.group(1)] = kv.group(2)
    return fm

for slug, category, date_en, date_ja, date_ko in articles:
    print(f"\n{'='*60}")
    print(f"Publishing: {slug}")
    print(f"{'='*60}")
    
    fm_en = get_fm(slug, "en")
    fm_ja = get_fm(slug, "ja")
    fm_ko = get_fm(slug, "ko")
    
    args = [
        PYTHON, str(PROJECT / "blog_publish.py"), slug,
        "--category", category,
        "--title-en", fm_en.get("title", ""),
        "--title-ja", fm_ja.get("title", ""),
        "--title-ko", fm_ko.get("title", ""),
        "--excerpt-en", fm_en.get("description", ""),
        "--excerpt-ja", fm_ja.get("description", ""),
        "--excerpt-ko", fm_ko.get("description", ""),
        "--date", date_en,
        "--date-ja", date_ja,
        "--date-ko", date_ko,
        "--read-time", fm_en.get("reading_time", "7 min"),
        "--read-time-ja", fm_ja.get("reading_time", "8 min"),
        "--read-time-ko", fm_ko.get("reading_time", "8 min"),
    ]
    
    result = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    output = result.stdout + result.stderr
    
    # Check for success
    if "git commit 完成" in output:
        print(f"✅ {slug} published and committed")
    elif "卡片已插入" in output:
        print(f"⚠️ {slug} cards inserted but commit may have issues")
    else:
        print(f"❌ {slug} failed")
        # Show last few lines of output
        lines = output.strip().split('\n')
        for line in lines[-10:]:
            print(f"  {line}")
