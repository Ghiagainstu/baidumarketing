# -*- coding: utf-8 -*-
"""KO 可见日期二次修复：覆盖原检查器漏掉的英文月份格式 & 丢日问题。
规则：以 JSON-LD datePublished 为准生成 'YYYY년 M월 D일'；无 JSON-LD 时解析可见英文日期。
"""
import re, os
KO = 'ko/blog/'
MONTHS = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}

def parse_to_ko(text):
    text = text.strip()
    m = re.match(r'^(\d{4})-(\d{2})-(\d{2})$', text)
    if m: return f"{m.group(1)}년 {int(m.group(2))}월 {int(m.group(3))}일"
    m = re.match(r'^([A-Z][a-z]{2})\s+(\d{1,2}),\s*(\d{4})$', text)
    if m and m.group(1) in MONTHS:
        return f"{m.group(3)}년 {MONTHS[m.group(1)]}월 {int(m.group(2))}일"
    m = re.match(r'^(\d{4})-(\d{2})$', text)
    if m: return f"{m.group(1)}년 {int(m.group(2))}월"
    return None

def fix(c):
    i = c.find('x1="3" y1="10"')
    if i < 0: return c, 0
    e = c.find('</span>', i)
    seg = c[i:e+7]
    m = re.search(r'</svg>\s*(.*?)\s*</span>', seg, re.DOTALL)
    if not m: return c, 0
    vd = m.group(1).strip()
    if re.match(r'^\d{4}년 \d{1,2}월 \d{1,2}일$', vd):
        return c, 0  # 已正确
    jm = re.search(r'"datePublished"\s*:\s*"([^"]*)"', c)
    target = jm.group(1) if jm else vd
    ko = parse_to_ko(target)
    if not ko:
        return c, 0
    new_seg = seg[:m.start(1)] + ko + seg[m.end(1):]
    c = c[:i] + new_seg + c[e+7:]
    return c, 1

if __name__ == '__main__':
    import sys
    args = sys.argv[1:] or [os.path.basename(f)[:-5] for f in __import__('glob').glob(KO+'*.html') if '_template' not in f]
    for slug in args:
        f = KO + slug + '.html'
        if not os.path.exists(f): 
            print(slug, 'MISSING'); continue
        c = open(f, encoding='utf-8', errors='replace').read()
        c2, n = fix(c)
        if n:
            open(f, 'w', encoding='utf-8').write(c2)
        print(slug, '-> changed' if n else '-> ok(no change)')
