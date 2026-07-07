# -*- coding: utf-8 -*-
"""KO Blog 全量检查脚本（只读，不修改） — 输出结构化问题报告。
问题分类参照 JA 版 check_ja_blog.py，全部对准韩语(KO)语境。
"""
import os, re, json, glob

KO_DIR = 'ko/blog'

# 日文字符（强信号：平假名/片假名在韩语中绝不会出现）
# 注意：U+30FB(・中点) 与 U+30FC(ー长音) 虽在片假名区块，但韩语中合法使用，须排除
HIRAGANA = re.compile(r'[\u3041-\u3096]')
KATAKANA = re.compile(r'[\u30A1-\u30F6]')
# 中文专属连词（在韩语中几乎不出现，保守列表，避免 Hanja 误报）
CN_SPECIFIC = ['与此同时', '一方面', '另一方面', '换句话说', '综上所述', '现如今']
# 损坏的 emoji 实体（缺失 &）
BROKEN_EMOJI = re.compile(r'(?<!\&)#x1f1[0-9a-f]+;')
# 未替换的模板变量
UNREPLACED = re.compile(r'/ko/blog/SLUG"|/ja/blog/SLUG"|/blog/SLUG"')
# 硬编码 slug（来自 JA 历史）
HARDCODED_SLUG = re.compile(r'baidu-merchant-agent-human-handoff-setup')
# 乱码字符
GARBLED = ['â€', 'ï¼', 'ã\x82', 'Â']
# 正确的 KO 国旗（字面或实体）
KO_FLAG_LIT = '\U0001F1F0\U0001F1F7'   # 🇰🇷
KO_FLAG_ENT = '&#x1f1f0;&#x1f1f7;'

def visible_date(c):
    i = c.find('x1="3" y1="10"')
    if i < 0:
        return None
    end = c.find('</span>', i)
    seg = c[i:end+7]
    m = re.search(r'</svg>\s*(.*?)\s*</span>', seg, re.DOTALL)
    return m.group(1).strip() if m else None

def check_file(path):
    issues = []
    try:
        c = open(path, encoding='utf-8', errors='replace').read()
    except Exception:
        return [{'type': '读取失败', 'detail': 'encoding error'}]
    slug = os.path.basename(path).replace('.html', '')

    # === 1. 格式问题 ===
    for m in re.finditer(r'<p>#\s+(.+?)</p>', c):
        issues.append({'type': '格式', 'subtype': 'Markdown H1残留', 'detail': m.group(0)[:60]})
    for m in re.finditer(r'<h[23]>\s*</h[23]>', c):
        issues.append({'type': '格式', 'subtype': '空标题', 'detail': m.group(0)})
    for m in re.finditer(r'\*\*[^*]+\*\*', c):
        issues.append({'type': '格式', 'subtype': 'Markdown粗体残留', 'detail': m.group(0)[:40]})
    for m in re.finditer(r'\[[^\]]+\]\([^)]+\)', c):
        if not m.group(0).startswith('[http'):
            issues.append({'type': '格式', 'subtype': 'Markdown链接残留', 'detail': m.group(0)[:50]})
    if '<em>, </em>::before' in c:
        issues.append({'type': '格式', 'subtype': 'CSS选择器损坏', 'detail': '<em>, </em>::before'})
    if c.count('</style>') > 1:
        issues.append({'type': '格式', 'subtype': '重复</style>', 'detail': f"count={c.count('</style>')}"})
    if 'border-left: 4px solid' in c:
        issues.append({'type': '格式', 'subtype': 'callout旧格式', 'detail': 'border-left: 4px solid → border:1px solid'})
    if 'takeaway-box-box' in c:
        issues.append({'type': '格式', 'subtype': 'takeaway类名错误', 'detail': 'takeaway-box-box → takeaway-box'})
    if 'footer-lang' in c:
        issues.append({'type': '格式', 'subtype': 'footer-lang残留', 'detail': '应全局移除'})

    # === 2. 字体/布局 ===
    # 仅当 2.8rem 出现在 stat-number 上下文才算问题；
    # .article-title 等合法的 2.8rem 不应被误报
    if re.search(r'stat-number\s*\{[^}]*font-size:\s*2\.8rem', c):
        issues.append({'type': '字体', 'subtype': 'stat-number过大', 'detail': '2.8rem → 1.8rem'})
    if "content: '¹3'" in c or 'content: "¹3"' in c:
        issues.append({'type': '字体', 'subtype': '¹3 CSS bug', 'detail': "content:'¹3' → content:'\\2713'"})
    if 'html[lang="ko"] .nav-links' not in c:
        issues.append({'type': '字体', 'subtype': 'nav缺少KO规则', 'detail': '缺少 html[lang="ko"] .nav-links'})

    # === 3. 英语/他语参杂 ===
    for tag in ['>strategy</span>', '>platform</span>', '>Search Ads</span>',
                '>Feed Ads</span>', '>Landing Page</span>', '>Pricing Models</span>',
                '>Market Insights</span>']:
        if tag in c:
            issues.append({'type': '英语', 'subtype': '标签未翻译', 'detail': tag})
    vd = visible_date(c)
    # 可见日期必须是韩式 YYYY년 M월 D일；ISO(2026-06-23) 与英文(Apr 20, 2026) 均不合规
    if vd and not re.match(r'^\d{4}년 \d{1,2}월 \d{1,2}일$', vd.strip()):
        issues.append({'type': '英语', 'subtype': '日期格式', 'detail': f'{vd} → YYYY년 M월 D일 형식'})
    if 'Baidu PPC Pro Team' in c:
        issues.append({'type': '英语', 'subtype': '作者署名', 'detail': 'Baidu PPC Pro Team → Baidu PPC Pro 팀'})
    if re.search(r'>\d+\s*min</span>', c):
        issues.append({'type': '英语', 'subtype': '阅读时间', 'detail': '应为 약X분'})
    if "We help international agencies and brands access China" in c:
        issues.append({'type': '英语', 'subtype': 'Footer品牌描述', 'detail': '英文未翻译'})

    # === 4. 符号问题 ===
    if BROKEN_EMOJI.search(c):
        issues.append({'type': '符号', 'subtype': 'emoji实体损坏', 'detail': '缺 & 的国旗实体'})
    if UNREPLACED.search(c):
        issues.append({'type': '符号', 'subtype': 'SLUG未替换', 'detail': '/ko/blog/SLUG'})
    if HARDCODED_SLUG.search(c) and slug != 'baidu-merchant-agent-human-handoff-setup':
        issues.append({'type': '符号', 'subtype': '硬编码slug', 'detail': 'baidu-merchant-agent-human-handoff-setup'})
    for g in GARBLED:
        if g in c:
            issues.append({'type': '符号', 'subtype': '乱码', 'detail': g})
    # 按钮旗：KO 页应含一个韩国旗（字面或实体）
    mb = re.search(r'lang-switch-btn"[^>]*>(.*?)<svg', c, re.DOTALL)
    btn = mb.group(1) if mb else ''
    if KO_FLAG_LIT not in btn and KO_FLAG_ENT not in btn:
        # 可能损坏或缺失
        if BROKEN_EMOJI.search(btn):
            issues.append({'type': '符号', 'subtype': '按钮旗损坏', 'detail': '韩国旗实体损坏'})
        else:
            issues.append({'type': '符号', 'subtype': '按钮旗缺失/错误', 'detail': '按钮无 🇰🇷'})
    elif btn.count(KO_FLAG_LIT) + btn.count(KO_FLAG_ENT) > 1:
        issues.append({'type': '符号', 'subtype': '按钮旗重复', 'detail': '重复韩国旗'})

    # === 5. 外语残留（韩语页不该出现的日语/中文）===
    # 日语：平假名/片假名（排除语言切换器菜单块）
    menu = re.search(r'lang-switch-menu.*?</div>', c, re.DOTALL)
    body_ex_menu = c if not menu else (c[:menu.start()] + c[menu.end():])
    for m in HIRAGANA.finditer(body_ex_menu):
        issues.append({'type': '外语残留', 'subtype': '日语(平假名)', 'detail': body_ex_menu[m.start():m.start()+10]})
        break
    if not any(i['subtype'] == '日语(平假名)' for i in issues):
        for m in KATAKANA.finditer(body_ex_menu):
            issues.append({'type': '外语残留', 'subtype': '日语(片假名)', 'detail': body_ex_menu[m.start():m.start()+10]})
            break
    # 中文专属连词（保守，避免 Hanja 误报）
    for cn in CN_SPECIFIC:
        if cn in body_ex_menu:
            issues.append({'type': '外语残留', 'subtype': '中文残留', 'detail': cn})
            break

    return issues

# 主程序
results = {}
total_issues = 0
files_with_issues = 0

for f in sorted(glob.glob(f'{KO_DIR}/*.html')):
    if '_template' in f:
        continue
    issues = check_file(f)
    if issues:
        slug = os.path.basename(f).replace('.html', '')
        results[slug] = {
            'url': f'https://www.baidumarketing.com/ko/blog/{slug}',
            'issues': issues
        }
        total_issues += len(issues)
        files_with_issues += 1

print(f"{'='*70}")
print(f"KO Blog 检查报告（只读）")
print(f"{'='*70}")
print(f"总文件数: {len(glob.glob(f'{KO_DIR}/*.html')) - 1}")
print(f"有问题的文件: {files_with_issues}")
print(f"总问题数: {total_issues}")
print(f"{'='*70}\n")

categories = {}
for slug, data in results.items():
    for issue in data['issues']:
        cat = issue['type']
        categories.setdefault(cat, {'files': set(), 'count': 0})
        categories[cat]['files'].add(slug)
        categories[cat]['count'] += 1

print("汇总：")
print(f"{'类别':<12} {'受影响文件':<10} {'问题数':<8}")
print("-" * 35)
for cat, data in sorted(categories.items()):
    print(f"{cat:<12} {len(data['files']):<10} {data['count']:<8}")
print("-" * 35)
print(f"{'合计':<12} {files_with_issues:<10} {total_issues:<8}\n")

for slug, data in sorted(results.items()):
    print(f"\n### {slug}")
    print(f"URL: {data['url']}")
    print(f"{'#':<3} {'类别':<10} {'子类型':<20} {'详情'}")
    print("-" * 80)
    for i, issue in enumerate(data['issues'], 1):
        print(f"{i:<3} {issue['type']:<10} {issue['subtype']:<20} {issue['detail'][:50]}")

with open('ko_blog_issues.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\n详细报告已保存: ko_blog_issues.json")
