import re
from pathlib import Path
md = (Path(r'C:\Users\HYE\WorkBuddy\20260411211839\blog-drafts') / 'baidu-vs-douyin-ads-china' / 'baidu-vs-douyin-ads-china-en.md').read_text(encoding='utf-8')
m = re.match(r'^---\s*\n(.*?)\n---', md, re.DOTALL)
if m:
    for line in m.group(1).split('\n'):
        kv = re.match(r'^(\w+):\s*"?(.*?)"?\s*$', line)
        if kv:
            print(f'{kv.group(1)} = {kv.group(2)[:60]}')
        else:
            print(f'NO MATCH: {line[:80]}')
