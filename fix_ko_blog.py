# -*- coding: utf-8 -*-
"""KO Blog 逐篇修复脚本（质量优先，精确范围保护）。
修复类型：
  1) 可见日期 ISO -> 韩语 YYYY년 M월 D일（JSON-LD 的 ISO 不动）
  2) stat-number 上下文 2.8rem -> 1.8rem（.article-title 的 2.8rem 不动）
  3) callout 旧格式 border-left:4px solid -> border:1px solid
  4) takeaway-box-box -> takeaway-box（选择器 + class）
  5) 按钮旗缺失/错误 -> 补/改韩国旗 🇰🇷（仅改 lang-switch-btn 内）
  6) SLUG 死链 /blog/SLUG -> 真实 slug
  7) 片假名混入（バイダ -> 바이두）等外语残留
  8) nav 缺 KO 规则 -> 在 .nav-links 桌面规则后插入 html[lang="ko"] .nav-links
所有替换均对干净文件为 no-op，可安全全量运行。
"""
import os, re, glob, sys

KO = 'ko/blog/'
KR_FLAG = '\U0001F1F0\U0001F1F7'      # 🇰🇷
US_FLAG = '\U0001F1FA\U0001F1F8'      # 🇺🇸
JP_FLAG = '\U0001F1EF\U0001F1F5'      # 🇯🇵

def fix_date(c):
    # 仅转换可见日期 span（</svg> ISO </span>），不碰 JSON-LD
    new, n = re.subn(
        r'(</svg>\s*)(\d{4})-(\d{2})-(\d{2})(\s*</span>)',
        lambda m: m.group(1) + f"{m.group(2)}년 {int(m.group(3))}월 {int(m.group(4))}일" + m.group(5),
        c)
    return new, n

def fix_stat(c):
    # 仅 stat-number 上下文的 2.8rem -> 1.8rem
    new, n = re.subn(r'(stat-number\s*\{\s*font-size:\s*)2\.8rem', r'\g<1>1.8rem', c)
    return new, n

def fix_callout(c):
    n = c.count('border-left: 4px solid')
    new = c.replace('border-left: 4px solid', 'border: 1px solid')
    return new, n

def fix_takeaway(c):
    n = c.count('takeaway-box-box')
    new = c.replace('takeaway-box-box', 'takeaway-box')
    return new, n

def fix_button(c):
    mb = re.search(r'lang-switch-btn"[^>]*>(.*?)<svg', c, re.DOTALL)
    if not mb:
        return c, 0
    btn = mb.group(1)
    if KR_FLAG in btn or '&#x1f1f0;&#x1f1f7;' in btn:
        return c, 0  # 已有韩国旗
    # 将按钮内的其他旗（美/日/损坏实体）替换为韩国旗
    new_btn = re.sub(
        r'\U0001F1FA\U0001F1F8|\U0001F1EF\U0001F1F5|&#x1f1fa;[^;]*;|&#x1f1ef;[^;]*;',
        KR_FLAG, btn)
    if new_btn == btn:
        return c, 0
    new = c[:mb.start(1)] + new_btn + c[mb.end(1):]
    return new, 1

def fix_slug(c, slug):
    n = 0
    for pat in ('/blog/SLUG', '/ko/blog/SLUG', '/ja/blog/SLUG'):
        repl = pat.replace('/SLUG', '/' + slug)
        if pat in c:
            c = c.replace(pat, repl)
            n += 1
    return c, n

def fix_katakana(c):
    # 已知片假名污染：バイ (片假名) + 더 (韩文) -> 바이두（Baidu 的韩语正确写法）
    # 注：原串是「バイ더」(バイ=片假名, 더=韩文)，不是「バイダ」
    reps = [('バイ더', '바이두')]
    n = 0
    for bad, good in reps:
        if bad in c:
            c = c.replace(bad, good)
            n += 1
    return c, n

def fix_nav(c):
    if 'html[lang="ko"] .nav-links' in c:
        return c, 0
    rule = ('\n'
            'html[lang="ko"] .nav-links { gap: 12px; font-size: .8rem; }\n'
            'html[lang="ko"] .nav-links a { white-space: nowrap; }\n')
    m = re.search(r'\.nav-links\s*\{\s*display:\s*flex;', c)
    if m:
        brace = c.find('{', m.start())
        depth = 0; i = brace
        while i < len(c):
            if c[i] == '{':
                depth += 1
            elif c[i] == '}':
                depth -= 1
                if depth == 0:
                    break
            i += 1
        insert_at = i + 1
        c = c[:insert_at] + rule + c[insert_at:]
        return c, 1
    # 兜底：插在 </style> 前
    idx = c.rfind('</style>')
    if idx >= 0:
        c = c[:idx] + rule + c[idx:]
        return c, 1
    return c, 0

def fix_file(path):
    slug = os.path.basename(path).replace('.html', '')
    c = open(path, encoding='utf-8', errors='replace').read()
    orig = c
    log = []
    c, n = fix_date(c);           log.append(('date', n)) if n else None
    c, n = fix_stat(c);           log.append(('stat', n)) if n else None
    c, n = fix_callout(c);        log.append(('callout', n)) if n else None
    c, n = fix_takeaway(c);       log.append(('takeaway', n)) if n else None
    c, n = fix_button(c);         log.append(('button', n)) if n else None
    c, n = fix_slug(c, slug);     log.append(('slug', n)) if n else None
    c, n = fix_katakana(c);       log.append(('katakana', n)) if n else None
    c, n = fix_nav(c);            log.append(('nav', n)) if n else None
    if c != orig:
        open(path, 'w', encoding='utf-8').write(c)
    return log

if __name__ == '__main__':
    # 默认全量；若命令行给了 slug 则只处理样本
    args = sys.argv[1:]
    if args:
        targets = [KO + a + '.html' for a in args]
    else:
        targets = sorted(glob.glob(KO + '*.html'))
        targets = [f for f in targets if '_template' not in f]
    for t in targets:
        log = fix_file(t)
        if log:
            print(os.path.basename(t).replace('.html',''), '->', log)
    print('DONE')
