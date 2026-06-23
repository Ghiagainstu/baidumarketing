import sys
sys.stdout.reconfigure(encoding='utf-8')
import subprocess
import re
from pathlib import Path

PROJECT = Path(r"C:\Users\HYE\WorkBuddy\20260411211839")
PYTHON = r"C:\Users\HYE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"

articles = [
    "b2b-manufacturer-baidu-case-study",
    "baidu-ppc-roi-calculator",
    "baidu-vs-douyin-ads-china",
    "baidu-ppc-education-industry",
    "how-to-choose-baidu-ppc-agency",
    "baidu-seo-ppc-synergy",
    "baidu-ppc-monthly-report-template",
    "geo-get-brand-cited-by-chinese-ai",
    "geo-vs-ppc-budget-allocation",
    "baidu-knowledge-graph-entity-seo",
    "geo-audit-checklist",
    "geo-content-playbook-chinese-ai",
    "geo-monitoring-brand-ai-search",
]

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

for slug in articles:
    print(f"\n{'='*60}")
    print(f"Publishing: {slug}")
    print(f"{'='*60}")
    
    fm_en = get_fm(slug, "en")
    fm_ja = get_fm(slug, "ja")
    fm_ko = get_fm(slug, "ko")
    category = fm_en.get("category", "strategy")
    
    args = [
        PYTHON, str(PROJECT / "blog_publish.py"), slug,
        "--category", category,
        "--title-en", fm_en.get("title", ""),
        "--title-ja", fm_ja.get("title", ""),
        "--title-ko", fm_ko.get("title", ""),
        "--excerpt-en", fm_en.get("description", ""),
        "--excerpt-ja", fm_ja.get("description", ""),
        "--excerpt-ko", fm_ko.get("description", ""),
        "--date", "Jun 23, 2026",
        "--date-ja", "2026年6月23日",
        "--date-ko", "2026년 6월 23일",
        "--read-time", fm_en.get("reading_time", "7 min"),
        "--read-time-ja", fm_ja.get("reading_time", "8 min"),
        "--read-time-ko", fm_ko.get("reading_time", "8 min"),
    ]
    
    try:
        result = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        output = result.stdout + result.stderr
        
        if "git commit 完成" in output:
            print(f"✅ {slug} published and committed")
        elif "卡片已存在" in output:
            print(f"⚠️ {slug} card already exists (skipped)")
        else:
            print(f"❌ {slug} failed")
            lines = output.strip().split('\n')
            for line in lines[-5:]:
                print(f"  {line}")
    except subprocess.TimeoutExpired:
        print(f"⏰ {slug} timed out (push failed but commit may have succeeded)")
    except Exception as e:
        print(f"❌ {slug} error: {e}")
