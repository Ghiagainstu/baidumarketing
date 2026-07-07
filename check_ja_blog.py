"""JA Blog 全量检查脚本 — 输出结构化问题报告"""
import os, re, json, glob

JA_DIR = 'ja/blog'

HANGUL = re.compile(r'[\uAC00-\uD7AF]{2,}')
BROKEN_EMOJI = re.compile(r'(?<!\&)#x1f1[0-9a-f]+;')   # 缺少 & 的损坏国旗实体（合法应为 &#x1f1ef;）
HARDCODED_SLUG = re.compile(r'baidu-merchant-agent-human-handoff-setup')
UNREPLACED_SLUG = re.compile(r'/ko/blog/SLUG"|/ja/blog/SLUG"|/blog/SLUG"')

# 允许的英文术语（不算英语参杂）
ALLOWED_EN = {'CPC', 'CTR', 'ROI', 'CPL', 'CPA', 'ROAS', 'CPM', 'GEO', 'PPC', 'SEO',
              'Baidu', 'PPC', 'Pro', 'BPP', 'ERNIE', 'DeepSeek', 'Doubao', 'Douyin',
              'Kuaishou', 'TikTok', 'Aicgou', 'AiCaiGou', 'oCPC', 'OCPC', 'AI', 'B2B',
              'B2C', 'SaaS', 'MBA', 'EMBA', 'PMP', 'IELTS', 'TOEFL', 'KOL', 'GSC',
              'GA4', 'URL', 'ID', 'API', 'JSON', 'HTML', 'CSS', 'JS'}

def check_file(path):
    issues = []
    try:
        c = open(path, encoding='utf-8', errors='replace').read()
    except:
        return [{'type': '格式', 'subtype': '读取失败', 'detail': 'encoding error'}]

    slug = os.path.basename(path).replace('.html', '')

    # === 1. 格式问题 ===
    for m in re.finditer(r'<p>#\s+(.+?)</p>', c):
        issues.append({'type': '格式', 'subtype': 'Markdown H1残留', 'detail': m.group(0)[:60]})

    for m in re.finditer(r'<h[23]>\s*</h[23]>', c):
        issues.append({'type': '格式', 'subtype': '空标题', 'detail': m.group(0)})

    article_match = re.search(r'<article class="article-content">(.*?)</article>', c, re.DOTALL)
    article = article_match.group(1) if article_match else ''

    for m in re.finditer(r'\*\*[^*]{2,}\*\*', article):
        issues.append({'type': '格式', 'subtype': 'Markdown粗体残留', 'detail': m.group(0)[:40]})

    for m in re.finditer(r'(?<!\!)\[[^\]]+\]\([^)]+\)', article):
        if not m.group(0).startswith('[http') and 'mailto' not in m.group(0):
            issues.append({'type': '格式', 'subtype': 'Markdown链接残留', 'detail': m.group(0)[:50]})

    if re.search(r'```', article):
        issues.append({'type': '格式', 'subtype': 'Markdown代码块残留', 'detail': '```'})

    if re.search(r'^---$', article, re.MULTILINE):
        issues.append({'type': '格式', 'subtype': '分割线残留', 'detail': '---'})

    if '<em>, </em>::before' in c:
        issues.append({'type': '格式', 'subtype': 'CSS选择器损坏', 'detail': '<em>, </em>::before'})

    if c.count('</style>') > 1:
        issues.append({'type': '格式', 'subtype': '重复</style>', 'detail': f"count={c.count('</style>')}"})

    if 'border-left: 4px solid' in c:
        issues.append({'type': '格式', 'subtype': 'callout旧格式', 'detail': 'border-left: 4px solid'})

    # === 2. 字体/布局 ===
    if 'font-size: 2.8rem' in c:
        issues.append({'type': '字体', 'subtype': 'stat-number过大', 'detail': '2.8rem → 1.8rem'})

    if 'html[lang="ja"] .nav-links' not in c:
        issues.append({'type': '字体', 'subtype': 'nav缺少JA规则', 'detail': '缺少 gap:16px'})

    # === 3. 英语参杂 ===
    en_tags = ['>strategy</span>', '>platform</span>', '>Search Ads</span>',
               '>Feed Ads</span>', '>Landing Page</span>', '>Pricing Models</span>',
               '>Market Insights</span>']
    for tag in en_tags:
        if tag in c:
            issues.append({'type': '英语', 'subtype': '标签未翻译', 'detail': tag})

    # 可见日期须为日式格式（YYYY年M月D日）；ISO 格式 YYYY-MM-DD 算误报
    # 真实标记：<svg...></svg> 2026-06-23</span>
    if re.search(r'</svg>\s*\d{4}-\d{2}-\d{2}\s*</span>', c):
        issues.append({'type': '英语', 'subtype': '日期格式', 'detail': '应为 2026年X月X日'})

    if 'Baidu PPC Pro Team</span>' in c or 'By Baidu PPC Pro Team' in c:
        issues.append({'type': '英语', 'subtype': '作者署名', 'detail': '应为 チーム'})

    if re.search(r'>\d+\s*min</span>', c):
        issues.append({'type': '英语', 'subtype': '阅读时间', 'detail': '应为 約X分'})

    if "We help international agencies and brands access China" in c:
        issues.append({'type': '英语', 'subtype': 'Footer品牌描述', 'detail': '英文未翻译'})

    # === 4. 奇怪符号 ===
    # 仅检测正文中的损坏国旗实体；语言切换器按钮内的旗标属菜单 UI，不计为误报
    for bem in BROKEN_EMOJI.finditer(c):
        s = bem.start()
        ctx = c[max(0, s-150):s+60]
        if 'lang-switch' in ctx or 'aria-label="Language"' in ctx or 'aria-label="언어"' in ctx:
            continue
        issues.append({'type': '符号', 'subtype': 'emoji实体损坏', 'detail': '&#x1f1fa;...'})
        break

    if UNREPLACED_SLUG.search(c):
        issues.append({'type': '符号', 'subtype': 'SLUG未替换', 'detail': '/ko/blog/SLUG'})

    if HARDCODED_SLUG.search(c) and slug != 'baidu-merchant-agent-human-handoff-setup':
        issues.append({'type': '符号', 'subtype': '硬编码slug', 'detail': 'baidu-merchant-agent-...'})

    for garbled in ['â€', 'ï¼', 'Â']:
        if garbled in c:
            issues.append({'type': '符号', 'subtype': '乱码', 'detail': garbled})
            break

    # === 5. 日语特有 ===
    # 韩语残留 — 仅检测正文；导航/语言切换器等"菜单"区域的韩语为合法 UI 文本，不计为误报
    # 品牌名 바이두（韩语"Baidu"）也视为合法
    MENU_MARKERS = ('nav-links', 'lang-switch', 'lang-switch-item', 'lang-switch-btn',
                    'aria-label="Language"', 'aria-label="언어"', 'lang="ko"')
    for m in HANGUL.finditer(c):
        text = m.group(0)
        if text in ('한국어', '바이두'):   # 菜单标签 / 品牌名，合法
            continue
        ctx_before = c[max(0, m.start()-150):m.start()]
        ctx_after = c[m.end():m.end()+150]
        if any(k in ctx_before or k in ctx_after for k in MENU_MARKERS):
            continue
        issues.append({'type': '日语特有', 'subtype': '韩语残留', 'detail': text[:20]})
        break

    for cn in ['与此同时', '展开', '响应']:
        if cn in article:
            issues.append({'type': '日语特有', 'subtype': '中文残留', 'detail': cn})

    return issues

# 主程序
results = {}
total_issues = 0
files_with_issues = 0
all_files = sorted(glob.glob(f'{JA_DIR}/*.html'))

for f in all_files:
    if '_template' in f:
        continue
    issues = check_file(f)
    if issues:
        slug = os.path.basename(f).replace('.html', '')
        results[slug] = {
            'url': f'https://www.baidumarketing.com/ja/blog/{slug}',
            'issues': issues
        }
        total_issues += len(issues)
        files_with_issues += 1

# 输出报告
print(f"{'='*70}")
print(f"JA Blog 检查报告")
print(f"{'='*70}")
print(f"总文件数: {len(all_files) - 1}")
print(f"有问题的文件: {files_with_issues}")
print(f"总问题数: {total_issues}")
print(f"{'='*70}\n")

categories = {}
for slug, data in results.items():
    for issue in data['issues']:
        cat = issue['type']
        if cat not in categories:
            categories[cat] = {'files': set(), 'count': 0}
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

with open('ja_blog_issues.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\n详细报告已保存: ja_blog_issues.json")
