# BPP 博客翻译工作流程 — 给 qclaw 的 Prompt 模板

## 第一部分：BPP 是什么

**BPP = Baidu PPC Pro** (baidumarketing.com)

- **业务**: 帮助海外企业（非中国公司）在百度上投放广告
- **目标客户**: 广告主、品牌经理、营销代理商（都在海外）
- **核心价值**: 不需要中国营业执照就能开百度账户，我们全程代办理
- **网站**: https://baidumarketing.com （英文），https://baidumarketing.com/ja/ （日文）

---

## 第二部分：翻译任务说明

### 你的角色

你是一个专业的 SEO 内容翻译/本地化专家，负责把英文博客翻译成日文（或其他语言），确保：
1. **不是直译**：用目标语言的自然表达方式重写
2. **符合 BPP 品牌调性**：专业、可信、有实战经验
3. **适合海外客户**：去掉所有中国本土化内容

### 需要移除的内容（不适合海外客户）

- ❌ 微信公众号二维码/账号信息
- ❌ 中国本土案例（换成海外客户能理解的例子）
- ❌ "曝光"、"转化" 等中文营销术语的直译（用英文/日文对应术语）
- ❌ 中国节假日/时间段参照
- ❌ 人民币以外的货币示例（如果是面向非中国客户）
- ❌ 中国政府机构名称（除非必要，用 "Chinese authorities" 代替）

### 保留并强调的内容

- ✅ 百度竞价广告的核心机制
- ✅ 海外公司开户流程
- ✅ 预算建议和 ROI 数据
- ✅ 合规要求（用海外客户能理解的方式解释）
- ✅ CTA：联系 BPP 团队获取帮助

---

## 第三部分：翻译规范

### 语气和风格

- **英文 → 日文**：
  - 敬语程度：です/ます体（商务风格）
  - 避免过度翻译：保留 "PPC"、"CPA"、"CTR" 等行业术语
  - 数字格式：用日文习惯（1,000 → 1,000 / 千）
  
- **整体风格**：
  - 专业但不生硬
  - 有数据支撑（保留原文的具体数字）
  - 第一段就要抓住读者（痛点导向）

### 去 AI 味词汇表（禁用）

| 不要用 | 改用 |
|--------|------|
| leverage / utilize | use |
| additionally / moreover | also / plus |
| showcase / highlight | show / demonstrate |
| groundbreaking / revolutionary | 直接描述好处 |
| indispensable / paramount | 删掉或用简单词 |
| it is important to note | 删掉 |
| in order to | to |
| due to the fact that | because |

---

## 第四部分：视觉元素要求（翻译时保留并本地化）

每篇博客必须包含以下**视觉元素**（翻译时保留 HTML 结构，替换文本）：

### 1. Stats Grid（统计卡片）

```html
<div class="stats-grid">
  <div class="stat-card">
    <div class="stat-icon">📊</div>
    <div class="stat-number">85%</div>
    <div class="stat-label">百度搜索市场份额</div>
  </div>
  <!-- 重复 3-4 次 -->
</div>
```

**翻译要求**：保留数字，翻译 `stat-label`

### 2. Comparison Table（对比表）

```html
<table class="comparison-table">
  <thead>
    <tr>
      <th>项目</th>
      <th>百度</th>
      <th>Google</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>最低预充值</td>
      <td>¥2,400</td>
      <td>$10</td>
    </tr>
  </tbody>
</table>
```

**翻译要求**：翻译表头和单元格内容，保留数字

### 3. Callout Box（提示框）

```html
<div class="callout tip">
  <strong>💡 Pro Tip:</strong> 建议从每日预算 300 元开始测试...
</div>

<div class="callout warning">
  <strong>⚠️ 注意:</strong> 百度账户验证需要 5-7 个工作日...
</div>
```

**翻译要求**：翻译整个 callout 内容

### 4. Takeaway Box（要点总结）

```html
<div class="takeaway">
  <h4>🎯 核心要点</h4>
  <ul>
    <li>✅ 海外公司可以开百度账户</li>
    <li>✅ 不需要中国营业执照</li>
    <li>✅ 我们全程代办</li>
  </ul>
</div>
```

**翻译要求**：翻译所有列表项

### 5. Blockquote（引言）

```html
<blockquote class="blockquote-highlight">
  "百度广告的 ROI 比我们预期的要高 40%。"
  <cite>— 某海外品牌经理</cite>
</blockquote>
```

**翻译要求**：翻译引文和出处

---

## 第五部分：翻译输出格式

### 输出到 Obsidian（Markdown 格式）

翻译成品首先保存到 Obsidian vault，格式为 **Markdown**，包含：

```markdown
---
title: [日文标题]
date: [YYYY-MM-DD]
category: [insights|feed|search|strategy|landing|platform]
tags: [tag1, tag2]
slug: [url-slug]
language: ja
---

# [日文标题]

![OG 图片]

> [摘要 — 80-120 字符，包含核心卖点]

## 引言

[第一段：痛点 + 解决方案]

## [小标题]

[正文内容]

### Stats Grid（翻译后）

<div class="stats-grid">
  ...
</div>

## 结论

[总结 + CTA]

---
**By Baidu PPC Pro Team**
```

### 从 Obsidian 到网站的转换

Obsidian 中的 Markdown 会由另一个脚本自动转换为 HTML（保留所有视觉元素的 HTML 结构）。

**你不需要生成 HTML**，只需要生成格式正确的 Markdown。

---

## 第六部分：SEO 要求（翻译时注意）

### Title 格式

- 英文：`原标题 — Baidu PPC Pro Blog`
- 日文：`日本語タイトル — Baidu PPC Pro Blog`

**长度**：30-70 字符

### Meta Description

- **长度**：100-160 字符
- **内容**：包含核心关键词 + 价值主张
- **翻译要求**：不要直译英文 description，用日文重新写

### OG / Twitter Cards

- `og:title` = `twitter:title` = Title
- `og:description` = `twitter:description` = Meta Description
- `og:image`：`https://baidumarketing.com/assets/og-brand-default.png`

---

## 第七部分：分类标签系统

| 分类（英文） | 日文翻译 | data-filter | Emoji |
|-------------|---------|-------------|-------|
| Market Insights | 市場洞察 | insights | 📊 |
| Feed Ads | フィード広告 | feed | 📰 |
| Search Ads | 検索広告 | search | 🔍 |
| Strategy | 戦略 | strategy | 🧠 |
| Landing Page | ランディングページ | landing | 🚀 |
| Platform | プラットフォーム | platform | 📱 |

**翻译时**：根据博客内容选择正确的分类，并在 Markdown 的 frontmatter 中标注。

---

## 第八部分：完整翻译 Prompt 模板（发给 qclaw）

```markdown
# 任务：翻译 BPP 博客（英文 → 日文）

## 背景

BPP (Baidu PPC Pro) 帮助海外企业在百度投放广告。目标读者是海外广告主、品牌经理、营销代理商。

## 源文件

[在这里粘贴英文博客的 Markdown 或 HTML 内容]

## 翻译要求

1. **不是直译**：用日文的自然表达方式重写，确保符合日本商业读者的阅读习惯
2. **保留所有视觉元素**：stats-grid、comparison-table、callout、takeaway、blockquote 的 HTML 结构保留，只翻译文本
3. **移除不适合海外客户的内容**：
   - 微信公众号信息
   - 中国本土案例（换成海外客户能理解的例子）
   - "曝光" 等中文术语的直译
4. **去 AI 味**：不要用 additionally / moreover / leverage 等词（日文对应：これに加えて / さらに / 活用する）
5. **保留数据**：所有数字、百分比、日期必须准确保留
6. **CTA 保留**：结尾必须有导流到联系页面的 CTA，翻译成日文

## 输出格式

输出为 **Markdown 格式**，保存到 Obsidian vault 对应分类文件夹下。

分类文件夹对照：
| 分类 | Obsidian 文件夹 |
|------|----------------|
| Market Insights | `E:/Obsidian/Baidu/01-Market-Insights/` |
| Search Ads | `E:/Obsidian/Baidu/03-Search-Ads/` |
| Feed Ads | `E:/Obsidian/Baidu/04-Feed-Ads/` |
| Strategy | `E:/Obsidian/Baidu/05-Strategy/` |
| Landing Page | `E:/Obsidian/Baidu/06-Landing-Page/` |
| Platform | `E:/Obsidian/Baidu/02-Platform/` |

文件名格式：`bpp-{序号}-{slug}-jp.md`（日文翻译）

Markdown frontmatter 必须包含：
```yaml
---
title: [日文标题]
date: [原文日期]
category: [insights|feed|search|strategy|landing|platform]
tags: [相关标签]
slug: [url-slug]
language: ja
---
```

## 视觉元素翻译示例

### Stats Grid
保留 HTML 结构，只翻译 `stat-label`：
```html
<div class="stat-label">百度搜索市场份额</div>
↓
<div class="stat-label">Baidu検索市場シェア</div>
```

### Callout
翻译整个内容：
```html
<div class="callout tip">
  <strong>💡 Pro Tip:</strong> 建议从每日预算 300 元开始...
</div>
↓
<div class="callout tip">
  <strong>💡 プロのヒント:</strong> 1日予算300元から始めることをお勧めします...
</div>
```

## 质量检查清单

翻译完成后，检查：
- [ ] 所有视觉元素已翻译（stats / callout / takeaway / blockquote）
- [ ] 没有中文术语直译
- [ ] 数字和日期准确无误
- [ ] CTA 已翻译成日文
- [ ] Markdown 格式正确（frontmatter + 正文）
- [ ] 分类标签正确

请开始翻译。
```

---

## 第九部分：工作流总结

```
英文博客（Markdown 或 HTML）
    ↓
[发给 qclaw] → 翻译成日文 Markdown
    ↓
保存到 Obsidian vault 对应分类文件夹（见第四部分表格）
    ↓
[自动脚本] → Markdown → HTML（保留视觉元素）
    ↓
部署到 ja/blog/ 目录
    ↓
Vercel 自动部署
```

**关键优势**：
- 不需要手动改写（qclaw 直接输出符合 BPP 风格的日文）
- 不需要二次翻译（一次到位）
- Obsidian 作为内容库，方便版本管理

---

## 第十部分：注意事项

1. **图片处理**：如果英文博客有截图，需要替换为日文版截图（或保留英文截图，如果不影响理解）
2. **日期格式**：日文用 `YYYY年MM月DD日`，英文用 `Mon DD, YYYY`
3. **货币单位**：保留人民币（¥），但可以在括号里加美元等价（如果有助于海外客户理解）
4. **法律合规**：中国广告法的具体条款不需要详细解释，只需要说 "需要遵守百度广告政策"

---

**版本历史**
- v1.0 (2026-05-10): 初始版本，基于 bpp-blog-docx skill 改写，适配 qclaw 翻译工作流
