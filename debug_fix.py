import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

p = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\fix_article.py')
content = p.read_text(encoding='utf-8')

# Find the title replacement lines
lines = content.split('\n')
for i, line in enumerate(lines):
    if 'TITLE' in line or 'title' in line.lower():
        print(f"Line {i+1}: {line}")
