# BPP 网站全站审计发现（2026-07-08）

审计范围：500 个 HTML 文件（根目录 15 页 + blog/ 113 + ja/blog/ 113 + ko/blog/ 62 + 其他）。
约定参考：canonical/og:url 用带 `www` 的干净 URL，hreflang 含 en/ja/ko/x-default。

---

## 🔴 高优先级：部署垃圾 / 重复内容（会被 Vercel 原样上线）

Vercel `vercel.json` 的 `outputDirectory` 为 `.`，因此仓库根目录下所有文件都会部署。以下目录/文件均为**应删除的陈旧或测试内容**，且部分带有**冲突的 SEO 标签**（重复内容 + 错误 canonical/og），会稀释主站 SEO。

| 路径 | 被跟踪文件数 | 问题 |
|---|---|---|
| `codex audit/` | 186 | 整套站点陈旧副本：JA 博客 og:url 指向 EN `/blog/`、takeaway `✓` 乱码成 `â¬?`、残留旧 `¹3` bug。重复内容 + 错误 canonical |
| `tmp/` | 27 | 临时/草稿 |
| `temp_domain/` | 13 | 临时 |
| `temp_vs/` | 13 | 临时 |
| `temp_sb/` | 11 | 临时 |
| `public/` | 1 | 疑似残留 |
| `lang-test.html` | 1 | 测试页 |

合计约 **252 个文件**应移出仓库（建议 `git rm` + 加入 `.gitignore`，或放入未部署的 `drafts/` 目录）。

---

## 🟠 中高优先级：SEO 标签错误（影响搜索/社交分享）

1. **JA 博客 og:url 指向 EN 地址（4 处）** — social 分享时 OG URL 落到英文页，JA 页 canonical 与 og 不一致：
   - `ja/blog/baidu-brand-info-account-level.html`
   - `ja/blog/baidu-click-fraud-ipv4-blocking.html`
   - `ja/blog/baidu-conversion-tracking-dedup.html`
   - `ja/blog/faq-international-brands.html`
   - 修复：og:url 改为对应的 `https://www.baidumarketing.com/ja/blog/<slug>`

2. **og:url 缺 `www`（1 处）** — `blog/baidu-search-ads-1-1-desktop-images.html`：
   - canonical = `https://www.baidumarketing.com/...`，og:url = `https://baidumarketing.com/...`（无 www），两者不一致。

3. **JSON-LD `url` 字段为空（20 处真实文件，另 10 处在 codex 垃圾目录）** — 以下 10 篇文章的 EN + KO 版 Article/BlogPosting JSON-LD 中 `"url": ""`：
   - baidu-ad-performance-diagnostic-tool / baidu-click-fraud-ipv4-blocking / baidu-conversion-tracking-dedup / baidu-feed-ads-history-operation-records-upgrade / baidu-inactive-keyword-cleanup-2025 / baidu-landing-page-audit-rejection-reasons / baidu-landing-page-report / baidu-ocpc-skip-data-accumulation / baidu-search-device-bid-coefficient-retirement / faq-international-brands
   - 修复：填入对应 canonical URL。

4. **og:image 资源缺失（2 处）** — 以下两张图被引用但文件不存在，社交分享无图：
   - `assets/blog-search-usage-chart.jpg`（被 `blog/search-vs-ai-usage.html`、`ja/blog/search-vs-ai-usage.html` 引用）
   - `assets/blog-digital-consumer-infographic.jpg`（被 `blog/digital-consumer-9trillion.html`、`ja/blog/digital-consumer-9trillion.html` 引用）
   - 修复：补图或改指向 `assets/og-brand-default.png`。

5. **<title> 被截断成 `...`（54 处 EN 博客）** — 标题被硬截断到约 60 字符并加 `...`，部分**断在单词中间**（如 "Good N..."、"Why I..."、"Manag..."、"Structur..."、"Safegua..."、"Diagn..."、"Fe..."）。`og:title` 通常是完整版，说明只是 `<title>` 标签被裁剪。浏览器标签与 SERP 会显示残缺标题。
   - 修复：取消 `<title>` 截断（或重写自然长度内的标题）。

---

## 🟡 中优先级：链接与内容语言

6. **真·断链 1 处** — `blog/baidu-creative-url-retirement-migration.html` 的关联卡片链接到 `/blog/baidu-advertiser-consultation`，该文章未发布（无此文件）。修复：改为已存在的页面（如 `/contact` 或 `/blog/can-i-do-baidu-ppc`）或补发目标文。

7. **KO/JA 页面残留英文 CTA 块（7 处）** — 转化块未翻译，例如：
   - KO：`baidu-brand-info-account-level`、`baidu-creative-url-retirement-migration`、`baidu-ernie-5-1-release`、`baidu-service-direct-lead-ads`
   - JA：`baidu-qingge-search-feed-unified`、`baidu-service-direct-lead-ads`
   - 文本："Talk to the BPP team about your China marketing strategy."（及 KO 的 "BPP manages brand information..."）
   - 与之前发现的 `Need Help With Baidu Account Setup?` 英文块属同一类，建议统一译韩/译日。

---

## 🟢 低优先级 / 信息项

8. **KO 博客覆盖缺口** — EN 113 / JA 113 / KO 62（去掉模板后实约 112 / 112 / 61）。**51 篇** EN/JA 文章无 KO 版本（KO 覆盖约 54%）。
   - 副作用：这些 EN 文章的韩语语言切换器链接到 `/ko/blog/<slug>` 会 **404**。属于内容缺口，非代码 bug；补齐 KO 翻译后自动解决。

9. **模板占位符误报（非问题）** — `_template-*.html` 中 `/blog/{{SLUG}}`、`{{CTA_LINK}}` 等是模板变量，不是真实页面，审计中已排除。

10. **已验证正常项** — sitemap.xml 324 条全部可解析（0 失效）；所有主页与博客均含 hreflang（0 缺失）；所有 canonical/og:url 均不含 `.html` 后缀。

---

## 建议处理顺序
1. 删除 `codex audit/`、`tmp/`、`temp_*/`、`public/`、`lang-test.html`（最大 SEO 风险，且是纯清理）。
2. 修复 5 处 og:url（4 JA + 1 缺 www）。
3. 填充 20 处 JSON-LD 空 url。
4. 补 2 张缺失 og:image 或改默认图。
5. 取消 54 处 `<title>` 截断。
6. 修 1 处断链 + 译 7 处 KO/JA 英文 CTA。
7. （长期）补齐 51 篇 KO 翻译以消除语言切换 404。
