# BPP 日语博客翻译任务 #27

## 任务
翻译一篇英文博客为日语 HTML。

## 文件信息
- **源文件**: `blog/baidu-vs-google-ppc-differences.html`
- **输出文件**: `ja/blog/baidu-vs-google-ppc-differences.html`
- **在线 URL**: `https://baidumarketing.com/ja/blog/baidu-vs-google-ppc-differences`

## 操作步骤

### 1. 读取源文件
打开 `blog/baidu-vs-google-ppc-differences.html`，读取全部内容。

### 2. 进行翻译 + 输出到 `ja/blog/baidu-vs-google-ppc-differences.html`

**必须改动的内容：**

| 改什么 | 怎么改 |
|--------|--------|
| `<html lang="en">` | → `<html lang="ja">` |
| title / description | 翻译为日语 |
| 6 项 OG 标签 | 翻译 og:title, og:description |
| 4 项 Twitter Card | 翻译 twitter:title, twitter:description |
| canonical URL | `https://baidumarketing.com/ja/blog/baidu-vs-google-ppc-differences` |
| JSON-LD headline/description | 翻译为日语 |
| **所有链接 `../xxx`** | → **`../../ja/xxx`**（因为文件在 ja/blog/ 子目录） |
| nav/footer/CTA 文字 | 用下方指定日语文本 |
| 文章正文 | 翻译为自然日语（ですます調） |
| SVG 中的文本标签 | 翻译为日语 |

**链接前缀对照表：**

| 链接位置 | 英文博客 | **日语博客（ja/blog/slug）** |
|---------|---------|--------------------------|
| nav 菜单 | `../features` | `../../ja/features` |
| Footer | `../contact` | `../../ja/contact` |
| Logo | `../index` | `../../ja/index` |
| CTA 按钮 | `../contact` | `../../ja/contact` |
| 面包屑首页 | `../index` | `../../ja/index` |
| 面包屑博客 | `../blog` | `../../ja/blog` |
| 相关文章 | `../blog/slug` | `../../ja/blog/slug` |
| 语言切换 English | `../index` | `../../index` |
| 语言切换 Japanese | `../ja/index` | `../../ja/index` |

**nav 链接——日语文本（8 项，顺序固定）：**
```html
<a href="../../ja/why-baidu-ppc-pro">Baidu PPC Proとは</a>
<a href="../../ja/features">サービス</a>
<a href="../../ja/pricing">料金プラン</a>
<a href="../../ja/clients">実績</a>
<a href="../../ja/faq">よくある質問</a>
<a href="../../ja/about">会社概要</a>
<a href="../../ja/blog" class="active">ブログ</a>
<a href="../../ja/contact">お問い合わせ</a>
```

**nav-right-group（语言切换器 + theme-toggle + CTA）：**
```html
<div class="nav-right-group">
  <div class="lang-switch">
    <button class="lang-switch-btn" onclick="toggleLangMenu()" aria-label="言語">🇯🇵 ▼</button>
    <div class="lang-switch-menu">
      <a href="../../index" lang="en" class="lang-switch-item">🇺🇸 English</a>
      <a href="../../ja/index" lang="ja" class="lang-switch-item">🇯🇵 日本語</a>
    </div>
  </div>
  <button class="theme-toggle">…</button>
  <a href="../../ja/contact" class="nav-cta">今すぐ始める →</a>
</div>
```

**Footer 链接——日语文本：**
```html
<li><a href="../../ja/features">Baidu PPC運用代行</a></li>
<li><a href="../../ja/faq">よくある質問</a></li>
<li><a href="../../ja/about">会社概要</a></li>
<li><a href="../../ja/contact">お問い合わせ</a></li>
<li><a href="../../ja/privacy">プライバシーポリシー</a></li>
<li><a href="../../ja/terms">利用規約</a></li>
```

**CTA 按钮日语文本：**
- nav-cta / mobile-cta: `今すぐ始める →`
- 文中 CTA: `今すぐ無料相談 →`
- Hero CTA: `今すぐアカウントを開設`
- hero 第二个按钮: `料金プランを見る`

**面包屑：**
```html
<div class="breadcrumb">
  <a href="../../ja/index">ホーム</a> / <a href="../../ja/blog">ブログ</a> / 文章日語標題
</div>
```

### 3. 保留不变的内容
- 所有 CSS 样式代码
- 所有 JavaScript（theme toggle, mobile nav, counter 等）
- SVG 图表的视觉结构（只翻译 SVG 内的文本标签）
- 图片链接
- 品牌 Logo SVG
- 数字、数据、百分比

### 4. 每篇必须包含的 6 种视觉元素
（从英文版直接翻译内容文本，保留 HTML 结构）
1. 数据网格 (`.stats-grid`)
2. 对比表格 (`<table class="comparison-table">`)
3. 强调框 (`.callout`, `.tip-box`, `.warning-box`)
4. 要点总结 (`.takeaway-box`)
5. SVG 图表（只翻译文字标签）
6. 引用块 (`<blockquote>`)

### 5. 验证清单
完成后逐项确认：
- [ ] 文件输出到 `ja/blog/baidu-vs-google-ppc-differences.html`
- [ ] `<html lang="ja">`
- [ ] canonical: `https://baidumarketing.com/ja/blog/baidu-vs-google-ppc-differences`
- [ ] title 30-70字符，格式 `日语标题 — Baidu PPC Pro Blog`
- [ ] 所有 `../` 已改为 `../../ja/`（lang-switch English 用 `../../index`）
- [ ] nav 8 项链接 + 日语文本正确
- [ ] footer 链接正确
- [ ] 正文日语自然（ですます調），无 AI 味翻译痕迹
- [ ] 6 种视觉元素齐全
- [ ] dark mode 正常

---

完成后告诉我，我会接手更新 blog.html 卡片列表、sitemap.xml 和 git push。
