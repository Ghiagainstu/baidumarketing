# BPP Blog QClaw 工作流 — 双阶段全自动管道

> 两阶段流水线：
> **Phase 1: QClaw** → 撰写 Markdown 博客 → 保存到 Obsidian
> **Phase 2: WorkBuddy** → 读取 Obsidian → 生成完整 HTML → 部署到 Vercel

---

## 工作流总览

```
                                            Phase 1 (QClaw)
源内容（DOCX / 中文 / 翻译需求）
    ↓
QClaw 按规范创作博客正文（Markdown）
    ↓
保存到 Obsidian vault：E:/Obsidian/Baidu/{分类文件夹}/bpp-{序号}-{slug}.md
    ============================================
                                            Phase 2 (WorkBuddy)
WorkBuddy 扫描 Obsidian vault
    ↓
检测到新 Markdown 文件
    ↓
解析 frontmatter + 正文
    ↓
生成完整 HTML（套 nav/footer/CSS/SEO/JSON-LD/视觉元素）
    ↓
更新 blog.html 卡片
    ↓
更新 sitemap.xml
    ↓
git push → Vercel 自动部署
```

---

# Phase 1：QClaw 创作规范（输入给 QClaw 的 Prompt）

## QClaw 角色定位

你是 BPP（Baidu PPC Pro）的 SEO 内容撰稿人。你的任务是创作/翻译面向海外广告主的英文博客文章，输出到 Obsidian Markdown 格式。

## 源内容

[粘贴源内容：DOCX 文本 / 中文文章 / 翻译需求 / 创作主题]

## 内容规则

### 语气与风格
- 目标读者：海外广告主、品牌经理、营销代理商（非中国客户）
- 视角：first-person（we/our），有实战经验感
- 正式但有真实案例/数据支撑
- 去 AI 味：禁用 leverage / additionally / showcase / groundbreaking / moreover / indispensable / paramount / it is important to note / in order to / due to the fact that
- 全英文，禁止中文残留
- 数字/百分比/日期必须准确保留
- 结尾必须有 CTA 导流到 baidumarketing.com 联系页

### 文章结构
- 标题：抓眼球 + 包含核心关键词
- 摘要（description）：80-160 字符，包含核心卖点
- 引言：痛点 → 解决方案
- 正文：多个小节，用小标题分隔
- 结论：总结 + CTA

### 强制视觉元素（每篇至少包含 4 种）
在 Markdown 中嵌入以下 HTML 结构（只替换文本内容，保留标签和 class）：

```html
<!-- 1. Stats Grid — 3-4张统计卡片 -->
<div class="stats-grid">
  <div class="stat-card">
    <div class="stat-icon">📊</div>
    <div class="stat-number">85%</div>
    <div class="stat-label">Baidu search market share</div>
  </div>
</div>

<!-- 2. Comparison Table -->
<table class="comparison-table">
  <thead><tr><th>Feature</th><th>Baidu</th><th>Google</th></tr></thead>
  <tbody><tr><td>Minimum deposit</td><td>¥2,400</td><td>$10</td></tr></tbody>
</table>

<!-- 3. Callout Box -->
<div class="callout tip"><strong>💡 Pro Tip:</strong> Start with...</div>
<div class="callout warning"><strong>⚠️ Note:</strong> Account verification...</div>

<!-- 4. Takeaway Box -->
<div class="takeaway"><h4>🎯 Key Takeaways</h4><ul><li>✅ First item</li></ul></div>

<!-- 5. Blockquote -->
<blockquote class="blockquote-highlight">"...quote..." <cite>— Source</cite></blockquote>

<!-- 6. Platform Badge -->
<div class="platform-badge"><span class="pill baidu">Baidu</span> vs <span class="pill google">Google</span></div>
```

### SEO 要求
- Title：`文章标题（不含品牌后缀）`
- Description：100-160 字符
- Category 从以下选择：insights / search / feed / strategy / landing / platform
- Slug：全小写英文连字符

## 输出格式（Markdown + frontmatter）

```yaml
---
title: The article title
description: Meta description 100-160 chars
date: YYYY-MM-DD
category: insights|search|feed|strategy|landing|platform
tags: [keyword1, keyword2]
slug: article-url-slug
language: en
reading_time: 5 min
---
```

正文从这里开始，包含视觉 HTML 元素...

---

# Phase 2：WorkBuddy 执行规范（Agent 自动执行）

## 输入

从 Obsidian vault 检测新的 Markdown 文件：
- 路径：`E:/Obsidian/Baidu/{分类文件夹}/bpp-{序号}-{slug}.md`
- 或根目录：`E:/Obsidian/Baidu/bpp-{slug}.md`

## 输出

完整的 blog HTML 文件，包含：

### 1. HTML 页面结构
- 套用 `bpp-template-ultimate` 模板
- `<html lang="en">`
- `<main>` 包裹主体
- `<article class="article-content">` 包裹博客正文
- 从 Markdown 转换为完整的视觉效果（stats-grid / comparison-table / callout / takeaway / blockquote）

### 2. Nav（blog/ 子目录规则）
- 所有 href 加 `../` 前缀
- 顺序：Why Baidu PPC Pro → Services → Pricing → Clients → FAQ → About → Blog → Contact
- 当前页 `<a class="active">`
- **禁止** `nav-mobile-cta`
- nav-inner 带 `container` 类
- 语言切换器（English + Japanese）

### 3. Footer
- `background: var(--gray-800); color: #D1D5DB`
- `.footer-social` 邮箱信封图标
- Copyright 动态：`document.write(new Date().getFullYear())`
- 品牌描述含 "$100B+"

### 4. SEO
- Title：`标题 — Baidu PPC Pro Blog`（30-70 字符）
- OG 6 项 + Twitter Card 4 项
- Canonical https 绝对 URL
- JSON-LD BlogPosting
- theme-color + color-scheme
- Preconnect 双标签
- Favicon 内联 SVG（全单引号）

### 5. JS
- toggleTheme + localStorage 持久化
- toggleMobileNav + overlay 关闭
- back-to-top scroll 监听

### 6. Blog Meta（日期 / 阅读时间 / 作者）
```html
<div class="article-meta">
  <span><svg>...</svg> Mon DD, YYYY</span>
  <span><svg>...</svg> N min read</span>
  <span><svg>...</svg> By Baidu PPC Pro Team</span>
</div>
```

### 7. 附带更新
- blog.html 插入卡片（按分类分组）
- sitemap.xml 添加新 URL
- git add → git commit → git push（自动）

## 验证清单

完成后验证：
- [ ] `.nav-mobile-cta,.nav-mobile-theme{display:none}` CSS 存在
- [ ] 仅 1 个 `</style>` 标签
- [ ] Favicon 全单引号
- [ ] nav-overlay 含 `aria-hidden="true"`
- [ ] 视觉元素已从 Markdown HTML 正确保留
- [ ] Article meta 三元素齐全
- [ ] JSON-LD author 使用 Organization
- [ ] Copyright 动态非硬编码

---

## 分类与文件夹对照表

| Category | Obsidian Subfolder | Blog filter |
|----------|-------------------|-------------|
| Market Insights | `01-Market-Insights/` | insights |
| Search Ads | `02-Platform/` | platform |
| Feed Ads | `03-Search-Ads/` | search |
| Strategy | `04-Feed-Ads/` | feed |
| Landing Page | `05-Strategy/` | strategy |
| Platform | `06-Landing-Page/` | landing |

Obsidian 文件名格式：`bpp-{序号}-{slug}.md`
多语言后缀：`bpp-{序号}-{slug}-jp.md` / `bpp-{序号}-{slug}-ko.md`

---

**版本历史**
- v1.0 (2026-05-14)：初始版本，双阶段 QClaw + WorkBuddy 工作流
