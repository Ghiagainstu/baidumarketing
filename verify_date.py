import sys, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

for lang, slug in [("ja", "baidu-ppc-roi-calculator"), ("ko", "baidu-ppc-roi-calculator")]:
    p = Path(rf'C:\Users\HYE\WorkBuddy\20260411211839\{lang}\blog\{slug}.html')
    html = p.read_text(encoding='utf-8')
    meta = re.search(r'<div class="article-meta">(.*?)</div>', html, re.DOTALL).group(1)
    spans = re.findall(r'<span>(.*?)</span>', meta, re.DOTALL)
    date_text = re.sub(r'<[^>]*>', '', spans[0]).strip()
    print(f'{lang} date: {date_text}')
