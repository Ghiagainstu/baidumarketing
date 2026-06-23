import sys
sys.stdout.reconfigure(encoding='utf-8')
import re
from pathlib import Path

PROJECT = Path(r"C:\Users\HYE\WorkBuddy\20260411211839")
DRAFTS = PROJECT / "blog-drafts"

def get_fm(slug, lang):
    md = (DRAFTS / slug / f"{slug}-{lang}.md").read_text(encoding="utf-8-sig")
    fm = {}
    m = re.match(r'^---\s*\n(.*?)\n---', md, re.DOTALL)
    if m:
        for line in m.group(1).split('\n'):
            kv = re.match(r'^(\w+):\s*"?(.*?)"?\s*$', line)
            if kv:
                fm[kv.group(1)] = kv.group(2)
    return fm

slug = sys.argv[1]
fm_en = get_fm(slug, "en")
fm_ja = get_fm(slug, "ja")
fm_ko = get_fm(slug, "ko")

print(f'--category {fm_en.get("category", "strategy")}')
print(f'--title-en "{fm_en["title"]}"')
print(f'--title-ja "{fm_ja["title"]}"')
print(f'--title-ko "{fm_ko["title"]}"')
print(f'--excerpt-en "{fm_en.get("description", "")}"')
print(f'--excerpt-ja "{fm_ja.get("description", "")}"')
print(f'--excerpt-ko "{fm_ko.get("description", "")}"')
print(f'--date "Jun 23, 2026"')
print(f'--date-ja "2026年6月23日"')
print(f'--date-ko "2026년 6월 23일"')
print(f'--read-time "{fm_en.get("reading_time", "7 min")}"')
print(f'--read-time-ja "{fm_ja.get("reading_time", "8 min")}"')
print(f'--read-time-ko "{fm_ko.get("reading_time", "8 min")}"')
