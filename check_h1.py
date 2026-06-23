import sys, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
p = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\ja\blog\geo-audit-checklist.html')
html = p.read_text(encoding='utf-8')
h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html)
print(f"H1: [{h1.group(1)[:100] if h1 else 'NOT FOUND'}]")
