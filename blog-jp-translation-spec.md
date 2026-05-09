# BPP 博客日语翻译 — Agent 交接文档

## 项目概述

- 网站：baidumarketing.com（Baidu PPC Pro）
- 任务：将 `blog/` 目录下 40 篇英文博客翻译为日语 HTML
- 输出目录：`ja/blog/<slug>.html`
- 在线 URL：`https://baidumarketing.com/ja/blog/<slug>`
- 技术栈：纯 HTML/CSS/JS，无框架

## 目录结构

```
baidumarketing.com/
├── blog/              ← 英文博客（源文件）
│   ├── can-i-do-baidu-ppc.html
│   └── ...（共 40 个 .html）
├── ja/                ← 日语版
│   ├── index.html     ← 日语首页（参考）
│   ├── contact.html   ← 日语联系页（参考）
│   └── blog/          ← 日语博客（新建，已创建空目录）
│       ├── can-i-do-baidu-ppc.html  ← 输出示例
│       └── ...
```

## 翻译规则

### 1. 语言
- 使用自然、正式（ですます調）的日语
- 避免 AI 味道的表达（中国語直訳調、不自然なビジネス敬語）
- BPP 品牌名保持 "Baidu PPC Pro" 不变
- 百度术语保留英文并在括号内标注日文，例：CPC（クリック単価）
- 数据、数字、百分比保持原样不翻译

### 2. 文件结构
每个日语博客 HTML 文件必须包含以下内容（参考 `ja/index.html` 的样式和结构）：

#### `<html>` 标签
```html
<html lang="ja">
```

#### `<head>` 部分
- **title**: `日语标题 — Baidu PPC Pro Blog`（30-70字符）
- **description**: 日语描述（100-160字符）
- **canonical**: `https://baidumarketing.com/ja/blog/<slug>`
- **OG 标签** 6 项（og:type=article, og:url, og:title, og:description, og:site_name="Baidu PPC Pro", og:image）
- **Twitter Card** 4 项（twitter:card=summary_large_image, twitter:title, twitter:description, twitter:image）
- **theme-color**: `#FFFFFF`
- **color-scheme**: `light dark`
- **favicon**: 与英文版相同的内联 SVG
- **preconnect**: Google Fonts 双标签
- **JSON-LD**: `@type: BlogPosting` Schema

#### `<style>` 部分
从英文博客直接复制完整 CSS（设计 token + dark mode + nav + footer + 博客专属样式），只需将 `lang="en"` 相关的选择器改为 `lang="ja"` 相关内容不需要改——CSS 不变。

#### `<nav>` 导航栏
与日语核心页面结构一致，但链接前缀不同：

| 项目 | 英文博客路径 | **日语博客路径** |
|------|-------------|-----------------|
| 相对 URL | `blog/slug` | `ja/blog/slug` |
| nav 链接前缀 | `../` | `../../ja/` |
| Footer 链接前缀 | `../` | `../../ja/` |
| Lang-switch English | `../index` | `../../index` |
| Lang-switch Japanese | `../ja/index` | `../../ja/index` |

**nav 链接示例：**
```html
<!-- 日语博客（从 ja/blog/slug 出发，../../ja/xxx → /ja/xxx） -->
<a href="../../ja/why-baidu-ppc-pro">Baidu PPC Proとは</a>
<a href="../../ja/features">サービス</a>
<a href="../../ja/pricing">料金プラン</a>
<a href="../../ja/clients">実績</a>
<a href="../../ja/faq">よくある質問</a>
<a href="../../ja/about">会社概要</a>
<a href="../../ja/blog" class="active">ブログ</a>
<a href="../../ja/contact">お問い合わせ</a>
```

**Footer 链接示例：**
```html
<li><a href="../../ja/features">Baidu PPC運用代行</a></li>
<li><a href="../../ja/faq">よくある質問</a></li>
<li><a href="../../ja/about">会社概要</a></li>
<li><a href="../../ja/contact">お問い合わせ</a></li>
<li><a href="../../ja/privacy">プライバシーポリシー</a></li>
<li><a href="../../ja/terms">利用規約</a></li>
```

**语言切换器：**
```html
<div class="lang-switch">
  <button class="lang-switch-btn" onclick="toggleLangMenu()" aria-label="言語">🇯🇵 ...</button>
  <div class="lang-switch-menu">
    <a href="../../index" lang="en" class="lang-switch-item">🇺🇸 English</a>
    <a href="../../ja/index" lang="ja" class="lang-switch-item">🇯🇵 日本語</a>
  </div>
</div>
```

**nav-right-group + theme-toggle + nav-cta：**
```html
<div class="nav-right-group">
  <div class="lang-switch">…</div>
  <button class="theme-toggle">…</button>
  <a href="../../ja/contact" class="nav-cta">今すぐ始める →</a>
</div>
```

#### `<main>` 文章内容
- 使用 `<article class="article-content">` 包裹
- 文章标题用 `<h1 class="article-title">`
- 段落用 `<p>`
- 内部链接（引用其他博客）：使用 `../../ja/blog/<slug>` 指向日语博客版本
- CTA 按钮：`../../ja/contact`
- 面包屑：`<a href="../../ja/index">ホーム</a> / <a href="../../ja/blog">ブログ</a> / 当前文章日语标题`
- 相关文章区：链接到日语博客版本 `../../ja/blog/<slug>`
- 底部 CTA：`<a href="../../ja/contact" class="cta-button">今すぐ無料相談 →</a>`

### 3. 视觉元素（每篇博客必须包含）
每篇日语博客必须包含以下 6 种视觉元素（从英文版直接翻译内容，保留 HTML 结构）：

1. **数据网格** (`.stats-grid`)
2. **对比表格** (`<table class="comparison-table">`)
3. **强调框** (`.callout`, `.tip-box`, `.warning-box`)
4. **要点总结** (`.takeaway-box`)
5. **SVG 图表**（保留 SVG 代码，只翻译文字标签）
6. **引用块** (`<blockquote>`)

### 4. 不需要改动的内容
- 所有 CSS 样式代码（设计变量、dark mode、动画等）
- 所有 JavaScript 代码（theme toggle、mobile nav、counter 等）
- SVG 图表的视觉结构（只翻译其中的文本标签）
- 图片链接（如果有，保持原样）
- 品牌 Logo SVG

### 5. 生成流程
1. 读取 `blog/<slug>.html` 英文源文件
2. 保持完整 HTML 结构不变
3. 将 `<html lang="en">` → `<html lang="ja">`
4. 翻译 title, description, OG/Twitter 标签
5. 翻译 nav/footer/CTA 中所有日语文本（已在上方列出）
6. 调整所有链接路径（`../` → `../../ja/`）
7. 翻译文章正文内容
8. 输出到 `ja/blog/<slug>.html`

### 6. 验证清单
每完成一篇，确认：
- [ ] 文件在 `ja/blog/<slug>.html`
- [ ] `<html lang="ja">`
- [ ] canonical URL 正确
- [ ] title 30-70字符
- [ ] 所有链接使用 `../../ja/` 前缀
- [ ] 正文日语自然、无 AI 味
- [ ] 6 种视觉元素齐全
- [ ] dark mode 正常
- [ ] nav 导航栏 8 个链接顺序正确
- [ ] 语言切换器下拉菜单正常
- [ ] mobile nav 正常
- [ ] footer 链接正确

---

## 源文件列表（40篇）

```
blog/8-ways-lower-baidu-cpc.html
blog/ai-assistants-vs-baidu.html
blog/baidu-2025-earnings-geo.html
blog/baidu-ad-billing-models-explained.html
blog/baidu-ad-display-name-update.html
blog/baidu-ads-foreign-business.html
blog/baidu-app-ecosystem.html
blog/baidu-audience-targeting-guide.html
blog/baidu-brand-protection-guide.html
blog/baidu-brand-zone-generic-keywords.html
blog/baidu-ecosystem-numbers.html
blog/baidu-feed-account-structure.html
blog/baidu-feed-ads-explained.html
blog/baidu-invalid-click-protection.html
blog/baidu-keyword-match-types-guide.html
blog/baidu-mcc-account-guide.html
blog/baidu-paid-search-video-ads.html
blog/baidu-ppc-account-status-guide.html
blog/baidu-ppc-different-domain.html
blog/baidu-ppc-terms-explained.html
blog/baidu-pricing-models.html
blog/baidu-search-ad-video-format-guide.html
blog/baidu-shared-budget-guide.html
blog/baidu-url-wildcard-guide.html
blog/baidu-user-data-targeting.html
blog/baidu-v-sign-verification-guide.html
blog/baidu-vs-google-ppc-differences.html
blog/can-i-do-baidu-ppc.html
blog/china-internet-numbers-2025.html
blog/cpm-ocpm-ecpm-explained.html
blog/digital-consumer-9trillion.html
blog/digital-marketing-china.html
blog/feed-landing-page-optimization.html
blog/how-much-does-baidu-ppc-cost.html
blog/keyword-research-baidu.html
blog/landing-page-bounce-rate.html
blog/native-ads-vs-feed-ads.html
blog/ocpc-explained.html
blog/rising-cpm-bad-baidu.html
blog/search-vs-ai-usage.html
```

## 参考文件

- `ja/index.html` — 日语首页（nav/footer/语言切换器样式参考）
- `ja/contact.html` — 日语联系页（按钮/CTA 日语文本参考）
- 任一篇英文博客 `blog/*.html` — 结构模板
