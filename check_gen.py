import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

# Read the gen script
gen = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\gen_blog_html.py')
content = gen.read_text(encoding='utf-8')

# Check CTA templates
for lang in ['en', 'ja', 'ko']:
    idx = content.find(f"'{lang}':")
    if idx > 0:
        snippet = content[idx:idx+200]
        print(f'{lang} CTA: {repr(snippet[:150])}')
