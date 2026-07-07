# KO Blog 全量检查 Prompt

> 本 prompt 与 `ja_blog_check_prompt.md` 同源，问题分类（5 大类）完全参照日语博客检查，
> 所有「正确值」均按韩语(KO)语境重写。用途：**只找不改**，输出问题 + URL 清单。

## 使用方法

将下方 `Prompt 正文` 复制粘贴给 AI 助手（或运行配套脚本 `check_ko_blog.py`），让它逐个检查所有韩语博客页面的问题。

---

## Prompt 正文

```
你的任务：逐个检查所有韩语博客页面（ko/blog/*.html，排除 _template-ko.html），找出以下 5 类问题，最后输出一份结构化报告（只检查、不修改）。

## 检查范围
- 目录：ko/blog/
- 文件：所有 *.html，排除 _template-ko.html
- 总量：约 60 个文件

## 检查项（5 大类，参照日语博客检查）

### 1. 格式问题（Format）
- [ ] Markdown H1 残留：`<p># ` 开头的行
- [ ] 空标题：`<h2></h2>` / `<h3></h3>` 后无内容
- [ ] Markdown 表格/粗体/链接/代码块/分割线残留（`| col |` / `**x**` / `[x](url)` / ```` ``` ```` / `---`）
- [ ] CSS 选择器损坏：`<em>, </em>::before`
- [ ] 重复 `</style>` 标签
- [ ] callout 旧格式：`border-left: 4px solid` （KO 模板正确为 `border: 1px solid`）
- [ ] takeaway 类名错误：`takeaway-box-box` （应为 `takeaway-box`）
- [ ] footer-lang 残留（全局应移除，仅 nav 右上角国旗下拉即可）

### 2. 字体/布局问题（Layout）
- [ ] stat-number 字号过大：`font-size: 2.8rem`（KO 模板正确为 1.8rem）
- [ ] ¹3 CSS bug：`.takeaway-box ul li::before { content: '¹3'; }`（应为 `content: '\2713'` 即 ✓）
- [ ] nav 缺少韩语特定规则：无 `html[lang="ko"] .nav-links { gap: 12px; font-size: .8rem; }`

### 3. 英语/他语参杂问题（English / Other Contamination）
- [ ] 分类标签未翻译：`>strategy</span>` / `>platform</span>` 等英文标签（应为韩语：전략/플랫폼…）
- [ ] 日期格式：`2026-06-23`（应为 `2026년 6월 21일` 这类韩语格式）
- [ ] 作者署名：`Baidu PPC Pro Team`（应为 `Baidu PPC Pro 팀`）
- [ ] 阅读时间：`11 min`（应为 `약 11분`）
- [ ] CTA 文字 / Footer 品牌描述英文残留
- [ ] 正文中的英文句子（非品牌名/术语）

### 4. 符号问题（Symbols）
- [ ] 损坏的 emoji 实体：缺 `&` 的国旗实体，如 `#x1f1f0;`（应为 `&#x1f1f0;&#x1f1f7;` 🇰🇷）
- [ ] 语言切换器链接损坏：`/ko/blog/SLUG`（{{SLUG}} 未替换 → 死链）
- [ ] 硬编码 slug：`baidu-merchant-agent-human-handoff-setup` 出现在不相关页面
- [ ] 乱码字符：`â€` / `ï¼` / `ã` 等 UTF-8 编码错误
- [ ] 按钮旗错误：KO 页按钮应显示 🇰🇷（字面或 `&#x1f1f0;&#x1f1f7;`）；检查①损坏实体 ②缺失（无 🇰🇷）③重复 ④错放美旗🇺🇸/日旗🇯🇵

### 5. 外语残留问题（Foreign Residue）
- [ ] 日语残留：平假名（ぁ-ん）/ 片假名（ア-ヶ）出现在正文（强信号；排除片假名区块里的 `・` U+30FB 与 `ー` U+30FC，二者在韩语中合法使用）
- [ ] 中文残留：中文专属连词如 `与此同时` / `一方面` / `另一方面` / `换句话说` / `综上所述`（保守列表，避免 Hanja 误报）
- [ ] 俄语残留等

## 输出格式

对每个有问题的文件，按以下格式输出：

```
### [文件名]
URL: https://www.baidumarketing.com/ko/blog/[slug]

| # | 类别 | 问题 | 建议修复 |
|---|------|------|----------|
| 1 | 格式 | callout 旧格式 | border-left:4px solid → border:1px solid |
| 2 | 英语 | 日期格式 2026-06-23 | → 2026년 6월 21일 |
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
| 外语残留 | X | Y |
| **合计** | **X** | **Y** |
```

## 执行方式

1. 先运行批量扫描脚本（Python）检测机械性问题
2. 对可疑文件逐个读取确认（尤其「外语残留」「按钮旗」需人工核对）
3. 输出完整报告，等待用户确认后再修复
4. 修复后 commit + push

## 注意事项
- **只读，不自动修复**，只检查和报告
- 品牌名（Baidu PPC Pro / BPP）和英文术语（CPC/CTR/ROI/CPL）不算英语参杂
- 汉字(Hanja)在韩语中合法，不算中文残留；只有中文专属连词才计入
- `・`(U+30FB) 与 `ー`(U+30FC) 是韩语合法标点，不算片假名污染
- emoji 在 callout/title 中是允许的
```

---

## 配套扫描脚本

将 `check_ko_blog.py` 保存于项目根目录，运行后生成终端报告 + `ko_blog_issues.json`：

```bash
python check_ko_blog.py
```

脚本为**只读**，不会改动任何文件。它已内置上述全部检查逻辑，并排除了已知的误报
（韩语合法标点 `・`/`ー`、Hanja 不算中文、语言切换器菜单内的日文标签）。

## 已知问题清单（基于历史经验，与日语博客同源）

| 问题类型 | 典型示例 | 修复方式（待用户确认后） |
|----------|----------|----------|
| callout 旧格式 | `border-left: 4px solid` | → `border: 1px solid` |
| takeaway 类名 | `takeaway-box-box` | → `takeaway-box` |
| stat-number 过大 | `2.8rem` | → `1.8rem` |
| ¹3 CSS bug | `content: '¹3'` | → `content: '\2713'` |
| 日期格式 | `2026-06-23` | → `2026년 6월 21일` |
| 作者署名 | `Baidu PPC Pro Team` | → `Baidu PPC Pro 팀` |
| 按钮旗错放 | 显示 🇺🇸 | → 🇰🇷 |
| SLUG 未替换 | `/ko/blog/SLUG` | → 实际 slug |
| 外语残留 | `バイダ`(片假名) | → 韩语写法 |
| nav 缺 KO 规则 | 无 `html[lang="ko"]` | 添加 `gap:12px; font-size:.8rem` |
