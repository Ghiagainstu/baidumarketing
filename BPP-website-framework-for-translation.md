# BPP Website Framework — Context for QClaw Translation & Multi-Language Sites

> Save to Obsidian vault (`E:/Obsidian/Baidu/`) as a permanent reference.
> Use this as context when sending translation tasks to QClaw or any AI agent.
> **Purpose**: One complete document that prevents truncated output, broken links, missing CSS, and all known bugs.

---

## 1. Website Identity

```
Brand:           Baidu PPC Pro
Domain:          https://baidumarketing.com
Niche:           B2B — Help overseas companies run Baidu (China) ads
Target audience: Advertisers, brand managers, marketing agencies — all outside China
USP:             No Chinese business license needed; we handle everything
```

## 2. Technical Stack

```
Stack:      Pure HTML/CSS/JS (no framework, no CMS)
Build:      build.mjs (Node.js) — generates nav/footer HTML, syncs across languages
Hosting:    Vercel (auto-deploy from GitHub main branch)
Domain:     Cloudflare (DNS + SSL)
Clean URLs: Enabled via vercel.json (no .html suffix in browser)
Git:        Private repo at github.com/Ghiagainstu/baidumarketing.git
Proxy:      git config http.proxy http://127.0.0.1:10808 (for SSL issues)
```

### Key Build Commands

```bash
node build.mjs sync all          # Sync nav/footer across ALL languages
node build.mjs sync ja           # Sync nav/footer for Japanese only
node build.mjs ls                # List all page statuses
node build.mjs site              # Regenerate sitemap.xml
```

## 3. Directory Structure

```
baidumarketing.com/
├── index.html               ← English Home
├── about.html               ← About Us
├── blog.html                ← Blog listing page
├── china-geo.html           ← China Geo-targeting
├── clients.html             ← Our Clients
├── contact.html             ← Contact form
├── faq.html                 ← FAQ page
├── features.html            ← Services (Why Baidu PPC Pro)
├── pricing.html             ← Pricing plans
├── privacy.html             ← Privacy Policy
├── terms.html               ← Terms of Service
├── why-baidu-ppc-pro.html   ← Why Baidu PPC Pro
│
├── blog/                    ← 41 English blog articles
│   ├── 8-ways-lower-baidu-cpc.html
│   ├── ai-assistants-vs-baidu.html
│   ├── ...(41 .html files total)
│   └── search-vs-ai-usage.html
│
├── ja/                      ← Japanese version (sub-directory)
│   ├── index.html
│   ├── about.html
│   ├── blog.html
│   ├── clients.html
│   ├── contact.html
│   ├── faq.html
│   ├── features.html
│   ├── pricing.html
│   ├── privacy.html
│   ├── terms.html
│   ├── why-baidu-ppc-pro.html
│   └── blog/               ← Japanese blog articles
│       ├── 8-ways-lower-baidu-cpc.html
│       └── ...(41 .html files)
│
├── locales/                 ← JSON translation files
│   ├── languages.json       ← Available languages list
│   ├── nav-en.json          ← English nav text
│   ├── nav-ja.json          ← Japanese nav text
│   ├── footer-en.json       ← English footer text
│   └── footer-ja.json       ← Japanese footer text
│
├── assets/                  ← Static assets (images, OG images)
├── sitemap.xml              ← Auto-generated
├── robots.txt               ← SEO crawl rules
└── build.mjs                ← Build script
```

## 4. Navigation (CRITICAL — Link Path Rules)

### 4.1. Desktop Nav — 8 Links (Fixed Order)

```
[LOGO] → index
Why Baidu PPC Pro → why-baidu-ppc-pro
Services → features
Pricing → pricing
Clients → clients
FAQ → faq
About → about
Blog → blog
Contact → contact [Get Started button]
```

### 4.2. Link Path Rules by Page Level

**Core pages (root level):** `<a href="contact">` — relative, no prefix

**Blog subdirectory (blog/*.html):** `<a href="../contact">` — prepend `../` to all nav/CTA/logo links

**Japanese core pages (ja/*.html):**
```html
<a href="blog">    → /ja/blog          ← same directory
```

**Japanese blog pages (ja/blog/*.html):**
```html
<a href="../../ja/why-baidu-ppc-pro">  → /ja/why-baidu-ppc-pro  ← WRONG fixed later
<a href="/ja/why-baidu-ppc-pro.html">  → /ja/why-baidu-ppc-pro  ← CORRECT (absolute path)
```

**WARNING**: Japanese blog pages had all nav links using `../../ja/xxx`. These were fixed to absolute paths `/ja/xxx.html` in a batch fix. New JA blog pages MUST use absolute paths starting with `/ja/`.

### 4.3. Path Rules Cheatsheet

| Page location | nav href prefix | logo href | CTA href |
|---------------|-----------------|-----------|----------|
| Root (index.html) | `xxx` | `index` | `contact` |
| blog/*.html | `../xxx` | `../index` | `../contact` |
| ja/*.html | `xxx` | `index` | `contact` |
| ja/blog/*.html | `/ja/xxx.html` | `/ja/index` | `/ja/contact.html` |

### 4.4. Langauge Switcher (nav-right-group)

```html
<div class="nav-right-group">
  <div class="lang-switch">
    <button class="lang-switch-btn" onclick="toggleLangMenu()" aria-label="Language">🇬🇧 EN</button>
    <div class="lang-switch-menu" id="langMenu">
      <a href="/" lang="en" class="lang-switch-item">🇺🇸 English</a>
      <a href="/ja/index" lang="ja" class="lang-switch-item">🇯🇵 日本語</a>
    </div>
  </div>
  <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle theme">...</button>
  <a href="contact" class="nav-cta">Get Started →</a>
</div>
```

**For JA pages**: English link → `../../index` or `/`, Japanese link → `../../ja/index` or `/ja/`

### 4.5. Mobile Nav Rules

- **Only index.html** has `.nav-mobile-cta` (Get Started button in the mobile menu)
- **All other pages** must NOT have `.nav-mobile-cta` — the mobile menu's last link is Contact
- CSS `@media (max-width: 900px)` must contain:
  ```css
  .nav-mobile-cta { display: block; margin: 12px 24px 20px; ... }
  .nav-mobile-theme { display: flex; align-items: center; gap: 8px; ... }
  ```
- **Critical bug history**: These selectors were accidentally deleted across ALL pages in May 2026, causing mobile nav to crash. Always verify they exist.

## 5. Footer Rules

- **Background**: `var(--gray-800)` (dark) — DO NOT use `var(--gray-50)` (light)
- **Color**: `color: #D1D5DB`
- **4-column layout**: Brand / Quick Links / Contact / Legal
- **About link**: Home page → `#whyus`, all other pages → `about`
- **Social**: ONLY Baidu SVG icon in footer-link section. Do NOT add WeChat, Douyin/TikTok, Xiaohongshu, Bilibili
- **Copyright**: Dynamic only: `&copy; <script>document.write(new Date().getFullYear())</script> Baidu PPC Pro` (NEVER hardcoded year)

```html
<footer>
  <div class="footer-top">...4 columns...</div>
  <div class="footer-bottom">
    <div class="footer-copy">&copy; <script>document.write(new Date().getFullYear())</script> Baidu PPC Pro</div>
    <div class="footer-links">
      <a href="#">Baidu</a>
      <!-- NO other social platforms -->
    </div>
  </div>
</footer>
```

## 6. Blog Metadata Format (CRITICAL)

Every blog article must have this in `<article class="article-content">`:

```html
<div class="article-meta">
  <span class="article-date">
    <svg class="meta-icon" viewBox="0 0 24 24" width="16" height="16"><!-- calendar icon --></svg>
    May 10, 2026
  </span>
  <span class="article-read-time">
    <svg class="meta-icon" viewBox="0 0 24 24" width="16" height="16"><!-- clock icon --></svg>
    8 min read
  </span>
  <span class="article-author">
    <svg class="meta-icon" viewBox="0 0 24 24" width="16" height="16"><!-- person icon --></svg>
    By Baidu PPC Pro Team
  </span>
</div>
```

**Mandatory**: Date + Read Time + Author (3 elements, with SVG icons, always present).

## 7. Multi-Language Architecture

```
Site structure:
  baidumarketing.com/    → English (default)
  baidumarketing.com/ja/ → Japanese (Phase 1 — LIVE)
  baidumarketing.com/zh/ → Chinese (Phase 2 — planned)
  baidumarketing.com/ko/ → Korean (Phase 3 — planned)
  baidumarketing.com/de/ → German (Phase 3 — planned)
```

### 7.1. Language Switcher CSS/JS

When adding a new language page, always add:
- **CSS**: `.nav-right-group {}`, `.lang-switch {}`, `.lang-switch-btn {}`, `.lang-switch-menu {}`, `.lang-switch-item {}`, dark mode overrides
- **JS**: `toggleLangMenu()` function + click-outside-close handler

### 7.2. Translation Workflow

```
Source (English blog HTML)
  ↓
QClaw / AI Agent → translates to target language Markdown
  ↓
Save to Obsidian vault (E:/Obsidian/Baidu/)
  ↓
Convert Markdown → HTML (with build.mjs or manual process)
  ↓
Place in ja/blog/<slug>.html (with correct nav/footer/CSS)
  ↓
Update sitemap.xml (add new URL)
  ↓
git push → Vercel auto-deploy
```

## 8. CSS & Design System (Essential for Translations)

### 8.1. CSS Variables

```css
:root {
  --blue: #2932E1; --blue-dark: #1E25AF; --blue-deep: #151B8A;
  --blue-light: #EEF0FF; --blue-glow: #D4D8FF; --blue-subtle: #F5F6FF;
  --gray-50: #F9FAFB; --gray-100: #F3F4F6; --gray-200: #E5E7EB;
  --gray-300: #D1D5DB; --gray-400: #9CA3AF; --gray-600: #4B5563;
  --gray-700: #374151; --gray-800: #1F2937; --gray-900: #111827;
  --radius: 12px; --radius-lg: 16px; --radius-xl: 24px;
  --shadow-sm: ...; --shadow-md: ...; --shadow-lg: ...; --shadow-blue: ...;
  --gradient-brand: linear-gradient(135deg, #2932E1 0%, #4F46E5 50%, #7C3AED 100%);
  --gradient-hero: ...;
  --font-display: 'Inter', system-ui, -apple-system, sans-serif;
  --transition-base: 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-smooth: 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
```

### 8.2. Dark Mode

```css
[data-theme="dark"] {
  --blue: #6366F1; --blue-dark: #818CF8; --blue-deep: #4F46E5;
  /* ...all other vars swap... */
  background-color: #0B0F1A; color: #E5E7EB;
}
```

### 8.3. Mandatory Visual Elements in Blog Posts

Every blog MUST include at least 4 of these 6 visual elements:

1. **Stats Grid** (`.stats-grid` with `.stat-card`s)
2. **Comparison Table** (`<table class="comparison-table">`)
3. **Callout/Notice Boxes** (`.callout.tip`, `.callout.warning`)
4. **Takeaway/Key Takeaways** (`.takeaway` with checklist items)
5. **Highlighted Blockquote** (`<blockquote class="blockquote-highlight">`)
6. **Platform Badges** (Baidu vs Google/other badges)

Visual element icons MUST use emoji: 📊 💡 ⚠️ 🎯 ✅

### 8.4. Theme Toggle CSS

```css
.theme-toggle svg { width: 18px; height: 18px; }  /* ← Required, otherwise icon is too big */
.theme-toggle:hover { border-color: var(--blue); color: var(--blue); transform: rotate(15deg); }
```

## 9. SEO Requirements (for Translation)

### 9.1. Page Title

```
English core page:  Title — Baidu PPC Pro           (30-70 chars)
English blog:       Title — Baidu PPC Pro Blog       (30-70 chars)
Japanese core page: 日本語タイトル — Baidu PPC Pro   (16-35 chars Japanese)
Japanese blog:      日本語タイトル — Baidu PPC Pro Blog
```

### 9.2. OG / Twitter Tags

```html
<meta property="og:type" content="article" />
<meta property="og:url" content="https://baidumarketing.com/ja/blog/<slug>" />
<meta property="og:title" content="[Translated Title]" />
<meta property="og:description" content="[Translated Description 100-160 chars]" />
<meta property="og:site_name" content="Baidu PPC Pro" />
<meta property="og:image" content="https://baidumarketing.com/assets/og-brand-default.png" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="[Translated Title]" />
<meta name="twitter:description" content="[Translated Description]" />
<meta name="twitter:image" content="https://baidumarketing.com/assets/og-brand-default.png" />
```

**WARNING**: `og:title` and `twitter:title` must EXACTLY match the HTML `<title>`. 
Blog OG/twitter title includes brand suffix (`— Baidu PPC Pro Blog`).

### 9.3. JSON-LD Schema

- **Home page**: WebSite + Organization
- **Blog articles**: BlogPosting
- **FAQ page**: FAQPage (with all 45 Q&A items)
- **Other pages**: WebPage

### 9.4. Canonical URL

```html
<link rel="canonical" href="https://baidumarketing.com/ja/blog/<slug>" />
```
Must use **https** (not http), absolute URL, no `.html` suffix.

### 9.5. hreflang Tags

```html
<link rel="alternate" hreflang="en" href="https://baidumarketing.com/blog/<slug>" />
<link rel="alternate" hreflang="ja" href="https://baidumarketing.com/ja/blog/<slug>" />
<link rel="alternate" hreflang="x-default" href="https://baidumarketing.com/blog/<slug>" />
```

## 10. Translation Guardrails (Known Pitfalls)

### 10.1. Output Truncation / Cropping

**Problem**: AI agents may truncate long output, especially for large HTML files.
**Solution**: 
- Always request output in **Markdown** (not HTML) for QClaw translations — Markdown is ~40% smaller
- Split very long articles (>3000 words) into 2 parts
- Frontmatter YAML must be the FIRST thing in the output, no blank line before `---`

### 10.2. Chinese Characters in Japanese Pages

**Problem**: AI translations sometimes insert random Chinese characters (e.g., `扔` U+6254) into Japanese HTML files.
**Solution**: After translation, grep for any CJK characters that are NOT Japanese (Kanji that are not common in Japanese). Run a script to detect.

**Preventive rule**: "When translating English → Japanese, NEVER output Chinese characters. If uncertain about a Kanji character, verify it first."

### 10.3. Broken Link Paths

**Problem**: JA blog pages can have `../../ja/xxx` paths that break when pages move.
**Solution**: Use absolute paths with `/ja/` prefix:
```html
<!-- CORRECT for ja/blog/*.html -->
<a href="/ja/why-baidu-ppc-pro.html">...</a>
<a href="/ja/contact.html">...</a>
```

### 10.4. Nav / Language Switcher Missing CSS

**Problem**: `node build.mjs sync ja` only syncs nav/footer HTML, not CSS.
**Solution**: After sync, verify CSS/JS present:
```bash
grep -c '\.lang-switch' ja/<page>.html    # Should be ≥ 15 matches
grep -c 'toggleLangMenu' ja/<page>.html   # Should be ≥ 1 match
```

### 10.5. Missing Mobile Nav Selectors

**Problem**: `.nav-mobile-cta {` and `.nav-mobile-theme {` can be accidentally deleted during edits.
**Solution**: Verify after any CSS edit:
```bash
grep -A1 "Mobile CTA inside menu" ja/blog/<page>.html
# Output must show .nav-mobile-cta { on the line after the comment
```

### 10.6. Light Footer Background

**Problem**: Footer can accidentally use `--gray-50` (light) instead of `--gray-800` (dark).
**Solution**: Footer CSS must be:
```css
footer { background: var(--gray-800); color: #D1D5DB; }
```

## 11. Revised QClaw Translation Prompt

```markdown
# Task: Translate BPP Blog (English → Japanese)

## Context: The Website

BPP (Baidu PPC Pro) at https://baidumarketing.com helps overseas companies run Baidu ads in China.
- Target audience: Advertisers, brand managers, marketing agencies (all outside China)
- Technical: Pure HTML/CSS/JS, hosted on Vercel, clean URLs (no .html in browser)
- Japanese version at https://baidumarketing.com/ja/ (sub-directory structure)

## Source File

[Paste English blog HTML or Markdown content here]

## Translation Rules

1. **Natural Japanese, not literal translation**: Use です/ます体 (keigo business style). Rewrite naturally for Japanese business readers.
2. **DO NOT output Chinese characters**: This is critical. Every character must be valid Japanese (hiragana, katakana, standard kanji). If unsure, use the katakana equivalent.
3. **Keep ALL data intact**: Numbers, percentages, dates must be preserved exactly.
4. **Keep ALL visual element HTML structures**: stats-grid, comparison-table, callout, takeaway, blockquote — only translate the text inside them, never the HTML tags or class names.
5. **Remove China-specific content**: No WeChat references, no China-local case studies (replace with international examples), no direct translations of Chinese marketing terms.
6. **Remove AI-voice phrases**: Never use さらに、これに加えて、活用する — keep it direct and simple.
7. **Keep BPP branding**: "Baidu PPC Pro" stays in English. Industry terms like PPC, CPA, CTR stay in English (or add Japanese in parentheses on first use).
8. **CTA preservation**: Must end with a call-to-action directing to contact page, translated to Japanese.
9. **No truncation**: If content is very long (>3000 words), output in full — do not cut off.

## Output Format

### First: Markdown for Obsidian vault

```markdown
---
title: [Japanese title — with brand suffix if in OG tags]
date: YYYY-MM-DD
category: [insights|search|feed|strategy|landing|platform]
tags: [relevant tags]
slug: [url-slug]
language: ja
---

# [Japanese title]

![OG Image](https://baidumarketing.com/assets/og-brand-default.png)

> [Abstract — 80-120 chars, include core value proposition]

## Introduction

[Pain point + solution]

## [Section heading]

[Body content — keep all stats-grid / comparison-table / callout / takeaway / blockquote HTML]

## Conclusion

[Summary + CTA in Japanese]
```

### Then: QA Checklist

- [ ] All text is Japanese (no Chinese characters, no English except brand names)
- [ ] Visual elements preserved (stats-grid, comparison-table, callout, takeaway, blockquote)
- [ ] Numbers and data intact
- [ ] CTA present and localized
- [ ] Title length 30-70 chars (Japanese)
- [ ] Description 100-160 chars (Japanese)
- [ ] Category matches English original
```

## 12. Skill System (For AI Agents)

BPP uses a skill-based system at `~/.workbuddy/skills/`:

| Skill | Purpose |
|-------|---------|
| `bpp-template-ultimate` | Ultimate page template with all known bugs prevented |
| `bpp-blog-docx` | Blog creation pipeline (DOCX → HTML → sitemap → git push) |
| `blog-enhance` | Blog visual enhancement (stats-grid, callout, takeaway, etc.) |
| `nav-sync` | Sync nav/footer across all languages |
| `bpp-新语言-nav` | Add nav/language switcher when creating new language site |

## 13. Deployment Quick Reference

```bash
# After creating/editing pages:
git add <files>
git commit -m "description"
git config http.proxy http://127.0.0.1:10808   # Only if SSL error
git push origin main
# Vercel auto-deploys from GitHub main branch
```

---

**Version History**
- v1.0 (2026-05-14): Initial comprehensive framework for QClaw translation context
