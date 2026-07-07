# JA Blog 全量检查 Prompt

## 使用方法

将以下 prompt 复制粘贴给 AI 助手，让它逐个检查所有日语博客页面的问题。

---

## Prompt 正文

```
你的任务：逐个检查所有日语博客页面（ja/blog/*.html，排除 _template），找出以下 5 类问题，最后输出一份结构化报告。

## 检查范围
- 目录：ja/blog/
- 文件：所有 *.html，排除 _template-ja.html
- 总量：约 111 个文件

## 检查项（5 大类）

### 1. 格式问题（Format）
- [ ] Markdown H1 残留：`<p># ` 开头的行（应为 <h1> 或删除）
- [ ] 空标题：`<h2></h2>` 或 `<h3></h3>` 后无内容
- [ ] Markdown 表格未转换：`| col1 | col2 |` 格式
- [ ] Markdown 粗体残留：`**text**` 未转为 `<strong>`
- [ ] Markdown 链接残留：`[text](url)` 未转为 `<a href>`
- [ ] Markdown 代码块残留：``` ``` 未转为 `<pre><code>`
- [ ] 分割线残留：`---` 未删除
- [ ] CSS 选择器损坏：`<em>, </em>::before` （应为 `*, *::before`）
- [ ] 重复 `</style>` 标签
- [ ] callout 旧格式：`border-left: 4px solid` （应为 `border-top: 5px solid`）

### 2. 字体/布局问题（Layout）
- [ ] stat-number 字号过大：`font-size: 2.8rem`（应为 1.8rem）
- [ ] nav 缺少语言特定规则：无 `html[lang="ja"] .nav-links { gap: 16px; }`
- [ ] nav 两行显示（gap 过大）
- [ ] takeaway-box 缺少 `!important`（圆点+勾同时显示）
- [ ] 移动端无响应式：缺少 `@media (max-width: 640px)`

### 3. 英语参杂问题（English Contamination）
- [ ] 分类标签未翻译：`>strategy</span>` / `>platform</span>` 等（应为 `戦略`/`プラットフォーム`）
- [ ] 日期格式：`2026-06-23`（应为 `2026年6月23日`）
- [ ] 作者署名：`Baidu PPC Pro Team`（应为 `Baidu PPC Pro チーム`）
- [ ] 阅读时间：`11 min`（应为 `約11分`）
- [ ] CTA 文字英文残留
- [ ] Footer 品牌描述英文残留
- [ ] 正文中的英文句子（非品牌名/术语）

### 4. 奇怪符号问题（Symbols）
- [ ] 损坏的 emoji 实体：`&#x1f1fa;&#x1f1f8;#x1f1ef;...`（应为 🇺🇸）
- [ ] 语言切换器链接损坏：`/ko/blog/SLUG`（{{SLUG}} 未替换）
- [ ] 硬编码 slug：`baidu-merchant-agent-human-handoff-setup` 出现在不相关页面
- [ ] 乱码字符：`â€` / `ï¼` / `ã` 等 UTF-8 编码错误
- [ ] 重复的 HTML 实体：`&amp;amp;` 等

### 5. 日语特有问题（JA-specific）
- [ ] 韩语残留：`좋습니다` / `자격로` / `캠페인` 等
- [ ] 中文残留：`与此同时` / `效果` / `発行` 等
- [ ] 俄语残留：`управления` 等
- [ ] 日语语法不自然（机器翻译痕迹）
- [ ] 敬语不一致（です/ます vs だ/である 混用）

## 输出格式

对每个有问题的文件，按以下格式输出：

```
### [文件名]
URL: https://www.baidumarketing.com/ja/blog/[slug]

| # | 类别 | 问题 | 具体位置 | 建议修复 |
|---|------|------|----------|----------|
| 1 | 格式 | Markdown H1 残留 | 第5行 `<p># 标题</p>` | 删除或转为 <h1> |
| 2 | 英语 | 标签未翻译 | article-meta `>strategy</span>` | → `戦略` |
```

最后输出汇总表：

```
## 汇总
| 类别 | 受影响文件数 | 总问题数 |
|------|-------------|----------|
| 格式 | X | Y |
| 字体 | X | Y |
| 英语 | X | Y |
| 符号 | X | Y |
| 日语特有 | X | Y |
| **合计** | **X** | **Y** |
```

## 执行方式

1. 先运行批量扫描脚本（Python），检测所有文件的机械性问题
2. 对可疑文件逐个读取确认
3. 输出完整报告，等待用户确认后再修复
4. 修复后 commit + push

## 注意事项
- 不要自动修复，只检查和报告
- 品牌名（Baidu PPC Pro / BPP）和英文术语（CPC/CTR/ROI/CPL）不算英语参杂
- 中文术语如「百度」「爱采购」在括号注释中是允许的
- emoji 在 callout/title 中是允许的
```

---

## 配套扫描脚本

将以下脚本保存为 `check_ja_blog.py`，运行后生成 JSON 报告：

```python
"""JA Blog 全量检查脚本 — 输出结构化问题报告"""
import os, re, json, glob

# 日语博客目录
JA_DIR = 'ja/blog'

# 韩文字符（强信号）
HANGUL = re.compile(r'[\uAC00-\uD7AF]{2,}')
# 中文专用字符（非日文汉字）
CN_SPECIFIC = re.compile(r'[与此同时效果]')
# 损坏的 emoji 实体
BROKEN_EMOJI = re.compile(r'&#x1f1fa;&#x1f1f8;#x1f1ef;')
# 硬编码 slug
HARDCODED_SLUG = re.compile(r'baidu-merchant-agent-human-handoff-setup')
# 未替换的模板变量
UNREPLACED_SLUG = re.compile(r'/ko/blog/SLUG"|/ja/blog/SLUG"|/blog/SLUG"')

def check_file(path):
    issues = []
    try:
        c = open(path, encoding='utf-8', errors='replace').read()
    except:
        return [{'type': '读取失败', 'detail': 'encoding error'}]
    
    slug = os.path.basename(path).replace('.html', '')
    
    # === 1. 格式问题 ===
    # Markdown H1 残留
    for m in re.finditer(r'<p>#\s+(.+?)</p>', c):
        issues.append({'type': '格式', 'subtype': 'Markdown H1残留', 'detail': m.group(0)[:60]})
    
    # 空标题
    for m in re.finditer(r'<h[23]>\s*</h[23]>', c):
        issues.append({'type': '格式', 'subtype': '空标题', 'detail': m.group(0)})
    
    # Markdown 粗体残留
    for m in re.finditer(r'\*\*[^*]+\*\*', c):
        issues.append({'type': '格式', 'subtype': 'Markdown粗体残留', 'detail': m.group(0)[:40]})
    
    # Markdown 链接残留
    for m in re.finditer(r'\[[^\]]+\]\([^)]+\)', c):
        if not m.group(0).startswith('[http'):
            issues.append({'type': '格式', 'subtype': 'Markdown链接残留', 'detail': m.group(0)[:50]})
    
    # CSS 选择器损坏
    if '<em>, </em>::before' in c:
        issues.append({'type': '格式', 'subtype': 'CSS选择器损坏', 'detail': '<em>, </em>::before'})
    
    # 重复 </style>
    if c.count('</style>') > 1:
        issues.append({'type': '格式', 'subtype': '重复</style>', 'detail': f"count={c.count('</style>')}"})
    
    # callout 旧格式
    if 'border-left: 4px solid' in c:
        issues.append({'type': '格式', 'subtype': 'callout旧格式', 'detail': 'border-left: 4px solid'})
    
    # === 2. 字体/布局问题 ===
    # stat-number 过大
    if 'font-size: 2.8rem' in c:
        issues.append({'type': '字体', 'subtype': 'stat-number过大', 'detail': '2.8rem → 1.8rem'})
    
    # nav 缺少 JA 特定规则
    if 'html[lang="ja"] .nav-links' not in c:
        issues.append({'type': '字体', 'subtype': 'nav缺少JA规则', 'detail': '缺少 gap:16px'})
    
    # === 3. 英语参杂 ===
    # 标签未翻译
    for tag in ['>strategy</span>', '>platform</span>', '>Search Ads</span>', 
                '>Feed Ads</span>', '>Landing Page</span>', '>Pricing Models</span>',
                '>Market Insights</span>']:
        if tag in c:
            issues.append({'type': '英语', 'subtype': '标签未翻译', 'detail': tag})
    
    # 日期格式
    if re.search(r'>\d{4}-\d{2}-\d{2}</span>', c):
        issues.append({'type': '英语', 'subtype': '日期格式', 'detail': '应为 2026年X月X日'})
    
    # 作者署名
    if 'Baidu PPC Pro Team</span>' in c or 'By Baidu PPC Pro Team' in c:
        issues.append({'type': '英语', 'subtype': '作者署名', 'detail': '应为 Baidu PPC Pro チーム'})
    
    # 阅读时间
    if re.search(r'>\d+\s*min</span>', c):
        issues.append({'type': '英语', 'subtype': '阅读时间', 'detail': '应为 約X分'})
    
    # Footer 英文品牌描述
    if "We help international agencies and brands access China" in c:
        issues.append({'type': '英语', 'subtype': 'Footer品牌描述', 'detail': '英文未翻译'})
    
    # === 4. 奇怪符号 ===
    if BROKEN_EMOJI.search(c):
        issues.append({'type': '符号', 'subtype': 'emoji实体损坏', 'detail': '&#x1f1fa;...'})
    
    if UNREPLACED_SLUG.search(c):
        issues.append({'type': '符号', 'subtype': 'SLUG未替换', 'detail': '/ko/blog/SLUG'})
    
    if HARDCODED_SLUG.search(c) and slug != 'baidu-merchant-agent-human-handoff-setup':
        issues.append({'type': '符号', 'subtype': '硬编码slug', 'detail': 'baidu-merchant-agent-human-handoff-setup'})
    
    # 乱码字符
    for garbled in ['â€', 'ï¼', 'ã\x82', 'Â']:
        if garbled in c:
            issues.append({'type': '符号', 'subtype': '乱码', 'detail': garbled})
    
    # === 5. 日语特有 ===
    # 韩语残留
    for m in HANGUL.finditer(c):
        text = m.group(0)
        # 排除 CSS 中的韩语选择器 html[lang="ko"]
        if not re.search(r'lang=["\']ko', c[max(0,m.start()-20):m.end()+20]):
            issues.append({'type': '日语特有', 'subtype': '韩语残留', 'detail': text[:20]})
            break
    
    # 中文残留
    for cn in ['与此同时', '效果', '発行', '展开', '响应']:
        if cn in c:
            issues.append({'type': '日语特有', 'subtype': '中文残留', 'detail': cn})
    
    return issues

# 主程序
results = {}
total_issues = 0
files_with_issues = 0

for f in sorted(glob.glob(f'{JA_DIR}/*.html')):
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
print(f"总文件数: {len(glob.glob(f'{JA_DIR}/*.html')) - 1}")
print(f"有问题的文件: {files_with_issues}")
print(f"总问题数: {total_issues}")
print(f"{'='*70}\n")

# 按类别统计
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

# 逐文件输出
for slug, data in sorted(results.items()):
    print(f"\n### {slug}")
    print(f"URL: {data['url']}")
    print(f"{'#':<3} {'类别':<10} {'子类型':<20} {'详情'}")
    print("-" * 80)
    for i, issue in enumerate(data['issues'], 1):
        print(f"{i:<3} {issue['type']:<10} {issue['subtype']:<20} {issue['detail'][:50]}")

# 保存 JSON
with open('ja_blog_issues.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\n详细报告已保存: ja_blog_issues.json")
```

## 使用步骤

1. **运行扫描脚本**：
   ```bash
   python check_ja_blog.py
   ```

2. **查看报告**：脚本会输出终端报告 + `ja_blog_issues.json` 详细文件

3. **用户确认**：将报告给用户审阅，确认哪些需要修复

4. **批量修复**：根据确认的问题列表，编写修复脚本

5. **Commit + Push**：修复后提交推送

## 已知问题清单（基于历史经验）

| 问题类型 | 典型示例 | 修复方式 |
|----------|----------|----------|
| Markdown H1 残留 | `<p># 标题</p>` | 删除或转 `<h1>` |
| CSS 选择器损坏 | `<em>, </em>::before` | → `*, *::before` |
| stat-number 过大 | `2.8rem` | → `1.8rem` |
| nav 缺 JA 规则 | 无 `html[lang="ja"]` | 添加 `gap:16px; font-size:.82rem` |
| 标签未翻译 | `>strategy</span>` | → `>戦略</span>` |
| 日期格式 | `2026-06-23` | → `2026年6月23日` |
| 作者署名 | `Baidu PPC Pro Team` | → `Baidu PPC Pro チーム` |
| 阅读时间 | `11 min` | → `約11分` |
| emoji 损坏 | `&#x1f1fa;...` | → `🇺🇸` |
| SLUG 未替换 | `/ko/blog/SLUG` | → `/ko/blog/{actual-slug}` |
| 硬编码 slug | `baidu-merchant-agent-...` | → `{{SLUG}}` 或实际 slug |
| 韩语残留 | `좋습니다` | → `良いです` |
| 中文残留 | `与此同时` | → `一方で` / `同時に` |
| Footer 英文 | `We help international...` | → 日文翻译 |
