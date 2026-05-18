#!/usr/bin/env node
/**
 * Obsidian Markdown → 完整 HTML 博客文章
 * 用法：node scripts/obsidian-to-html.mjs <obsidian-md-file>
 */

import fs from 'fs';
import path from 'path';

const MD_FILE = process.argv[2];
if (!MD_FILE) {
  console.error('Usage: node obsidian-to-html.mjs <obsidian-md-file>');
  process.exit(1);
}

// 读取文件，处理 BOM
let content = fs.readFileSync(MD_FILE, 'utf8');
if (content.charCodeAt(0) === 0xFEFF) content = content.slice(1);

// 解析 frontmatter（处理 \r\n 和 \n）
const delim = '\r\n---\r\n';
const parts = content.split(delim);

let frontmatterRaw, bodyRaw;
if (parts.length >= 3) {
  frontmatterRaw = parts[1];
  bodyRaw = parts.slice(2).join(delim).trim();
} else {
  // 尝试 \n 分隔符
  const parts2 = content.split('\n---\n');
  if (parts2.length >= 3) {
    frontmatterRaw = parts2[1];
    bodyRaw = parts2.slice(2).join('\n---\n').trim();
  } else {
    console.error('ERROR: Cannot parse frontmatter from', MD_FILE);
    process.exit(1);
  }
}

// 提取 frontmatter 字段
function getFM(field) {
  const m = frontmatterRaw.match(new RegExp(field + '\\s*:\\s*(.+)'));
  if (!m) return '';
  return m[1].trim().replace(/^["']|["']$/g, '');
}

const title    = getFM('title');
const date     = getFM('date');
const category = getFM('category');
const slug     = getFM('slug');
const language = getFM('language') || 'en';
const author   = getFM('author') || 'Baidu PPC Pro Team';

// 计算 reading time（简单估算：每 200 字 = 1 min）
const wordCount = bodyRaw.replace(/<[^>]+>/g, '').split(/\s+/).length;
const readingTime = Math.max(1, Math.ceil(wordCount / 200));

// Markdown → HTML（保留已有的 HTML 标签）
function mdToHtml(md) {
  let html = md;
  // 标题
  html = html.replace(/^#### (.+)$/gm, '<h4>$1</h4>');
  html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
  html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
  // 粗体 / 斜体
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
  // 链接
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
  // 有序列表
  html = html.replace(/^(\d+)\. (.+)$/gm, '<li>$2</li>');
  // 无序列表
  html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
  // 段落（连续非空行）
  html = html.replace(/^(?!<[uo]l>|<li>|<h[1-4]>|<div|<hr|<p)(.+)$/gm, '<p>$1</p>');
  // 包装相邻 <li> 到 <ul> 或 <ol>
  html = html.replace(/(<li>[\s\S]*?<\/li>\n?)+/g, (match) => {
    const isOl = match.includes('1. ');
    const tag = isOl ? 'ol' : 'ul';
    return `<${tag}>\n${match}</${tag}>\n`;
  });
  return html;
}

const bodyHtml = mdToHtml(bodyRaw);

// 日期格式化
function fmtDate(d) {
  if (!d) return '';
  const dateObj = new Date(d + 'T00:00:00Z');
  return dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric', timeZone: 'UTC' });
}

const formattedDate = fmtDate(date);

// 分类样式映射
const catClass = {
  insights: 'insights', search: 'search', feed: 'feed',
  platform: 'platform', strategy: 'strategy', landing: 'landing'
};
const catLabel = {
  insights: 'Market Insights', search: 'Search Ads', feed: 'Feed Ads',
  platform: 'Platform', strategy: 'Strategy', landing: 'Landing Page'
};
const cls = catClass[category] || 'search';
const label = catLabel[category] || category;

// 构建 HTML
const htmlFile = `<!DOCTYPE html>
<html lang="${language}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#FFFFFF">
  <meta name="color-scheme" content="light dark">
  <title>${title} — Baidu PPC Pro Blog</title>
  <meta name="description" content="${title}. ${bodyRaw.substring(0, 120).replace(/[#*\n\r]/g, ' ')}">
  <link rel="canonical" href="https://baidumarketing.com/blog/${slug}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="https://baidumarketing.com/blog/${slug}" />
  <meta property="og:title" content="${title}" />
  <meta property="og:description" content="${title}. ${bodyRaw.substring(0, 120).replace(/[#*\n\r]/g, ' ')}" />
  <meta property="og:site_name" content="Baidu PPC Pro" />
  <meta property="og:image" content="https://baidumarketing.com/assets/og-brand-default.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="${title}" />
  <meta name="twitter:description" content="${title}. ${bodyRaw.substring(0, 120).replace(/[#*\n\r]/g, ' ')}" />
  <meta name="twitter:image" content="https://baidumarketing.com/assets/og-brand-default.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop offset='0%25' stop-color='%232932E1'/><stop offset='100%25' stop-color='%234F46E5'/></linearGradient></defs><rect width='32' height='32' rx='8' fill='url(%23g)'/><path d='M9 11c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2v10c0 1.1-.9 2-2 2H11c-1.1 0-2-.9-2-2V11z' fill='none' stroke='white' stroke-width='1.5' opacity='.3'/><text x='16' y='21.5' text-anchor='middle' font-family='system-ui' font-size='13' font-weight='800' fill='white' letter-spacing='.5'>BPP</text></svg>" />
<style>
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body { font-family: 'Inter', system-ui, -apple-system, sans-serif; color: #111827; background: #ffffff; line-height: 1.6; -webkit-font-smoothing: antialiased; }
a { color: inherit; text-decoration: none; }
.container { max-width: 1140px; margin: 0 auto; padding: 0 24px; }
section { padding: 96px 0; }
/* Nav */
nav { position: sticky; top: 0; z-index: 100; background: rgba(255,255,255,.92); backdrop-filter: blur(12px); border-bottom: 1px solid #E5E7EB; }
.nav-inner { display: flex; align-items: center; justify-content: space-between; height: 64px; }
.nav-logo { display: flex; align-items: center; gap: 10px; font-weight: 700; font-size: 1.1rem; color: #1F2937; transition: color .2s; }
.nav-logo:hover { color: #2932E1; }
.nav-links { display: flex; gap: 28px; font-size: .9rem; color: #4B5563; }
.nav-links a { position: relative; transition: color .2s; }
.nav-links a::after { content: ''; position: absolute; bottom: -4px; left: 50%; width: 0; height: 2px; background: #2932E1; border-radius: 1px; transition: width .4s cubic-bezier(.16,1,.3,1), left .4s cubic-bezier(.16,1,.3,1); }
.nav-links a:hover { color: #2932E1; }
.nav-links a:hover::after { width: 100%; left: 0; }
.nav-links a.active { color: #2932E1; font-weight: 600; }
.nav-links a.active::after { width: 100%; left: 0; }
.nav-mobile-cta, .nav-mobile-theme { display: none; }
.nav-cta { background: linear-gradient(135deg, #2932E1 0%, #4F46E5 50%, #7C3AED 100%); color: #fff; padding: 10px 22px; border-radius: 8px; font-size: .9rem; font-weight: 600; transition: transform .2s, box-shadow .2s; position: relative; overflow: hidden; }
.nav-cta:hover { transform: translateY(-1px); box-shadow: 0 4px 16px rgba(41,50,225,.35); }
.nav-mobile-toggle { display: none; background: none; border: none; cursor: pointer; }
.nav-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.4); backdrop-filter: blur(2px); z-index: 99; opacity: 0; pointer-events: none; transition: opacity .3s; }
.nav-overlay.active { opacity: 1; pointer-events: auto; }
@media (max-width: 900px) { .nav-links { display: none; } .nav-mobile-toggle { display: block; } }
/* Hero */
.article-hero { padding: 120px 0 60px; background: linear-gradient(160deg, #ffffff 30%, #EEF0FF 60%, #E0E7FF 100%); }
.article-title { font-size: 2.8rem; font-weight: 800; line-height: 1.2; color: #111827; margin-bottom: 16px; }
.article-meta { display: flex; gap: 20px; font-size: .85rem; color: #6B7280; }
.article-meta span { display: inline-flex; align-items: center; gap: 6px; }
/* Content */
.article-section { padding: 60px 0 96px; }
.article-content { max-width: 750px; margin: 0 auto; font-size: 1.05rem; line-height: 1.8; color: #374151; }
.article-content h2 { font-size: 1.6rem; font-weight: 700; margin: 48px 0 20px; color: #111827; }
.article-content h3 { font-size: 1.3rem; font-weight: 600; margin: 32px 0 16px; color: #1F2937; }
.article-content p { margin-bottom: 20px; }
.article-content ul, .article-content ol { margin: 0 0 20px 24px; }
.article-content li { margin-bottom: 10px; }
.article-content a { color: #2932E1; border-bottom: 1px solid rgba(41,50,225,.3); transition: border-color .2s; }
.article-content a:hover { border-color: #2932E1; }
.callout { padding: 20px 24px; border-radius: 10px; margin: 28px 0; font-size: .95rem; line-height: 1.7; }
.callout.tip { background: #EEF0FF; border-left: 4px solid #2932E1; }
.callout.warning { background: #FEF3C7; border-left: 4px solid #F59E0B; }
.takeaway { background: #F0FDF4; border: 1px solid #86EFAC; border-radius: 10px; padding: 20px 24px; margin: 28px 0; }
.takeaway h4 { font-size: 1rem; margin-bottom: 12px; }
.takeaway ul { margin: 0 0 0 20px; }
/* Footer */
footer { background: #1F2937; color: #D1D5DB; padding: 56px 0 24px; }
.footer-top { display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 40px; padding-bottom: 40px; border-bottom: 1px solid rgba(255,255,255,.1); }
.footer-brand h3 { color: #fff; font-size: 1.1rem; font-weight: 700; margin-bottom: 12px; display: flex; align-items: center; gap: 10px; }
.footer-brand p { font-size: .85rem; line-height: 1.7; color: #9CA3AF; max-width: 280px; }
.footer-col h4 { color: #fff; font-size: .85rem; font-weight: 600; margin-bottom: 14px; }
.footer-col ul { list-style: none; display: flex; flex-direction: column; gap: 8px; }
.footer-col ul li a { font-size: .85rem; color: #9CA3AF; transition: color .2s; }
.footer-col ul li a:hover { color: #fff; }
.footer-bottom { display: flex; justify-content: space-between; align-items: center; padding-top: 24px; flex-wrap: wrap; gap: 12px; }
.footer-copy { font-size: .82rem; color: #6B7280; }
.footer-social { display: flex; gap: 14px; align-items: center; }
.footer-social a { width: 36px; height: 36px; border-radius: 8px; background: rgba(255,255,255,.08); display: grid; place-items: center; transition: background .2s, transform .2s; }
.footer-social a:hover { background: #2932E1; transform: translateY(-2px); }
/* Dark Mode */
[data-theme="dark"] body { background: #0B0F1A; color: #E5E7EB; }
[data-theme="dark"] nav { background: rgba(11,15,26,.85); border-bottom-color: #1F2937; }
[data-theme="dark"] .nav-links { color: #9CA3AF; }
[data-theme="dark"] .article-hero { background: linear-gradient(160deg, #0F172A 30%, #131C38 60%, #1E1B4B 100%); }
[data-theme="dark"] .article-title { color: #F9FAFB; }
[data-theme="dark"] .article-content { color: #D1D5DB; }
[data-theme="dark"] footer { background: #070B14; }
</style>
</head>
<body>
<nav>
  <div class="container nav-inner">
    <a href="../index" class="nav-logo">
      <svg width="32" height="32" viewBox="0 0 32 32" fill="none"><defs><linearGradient id="logoGrad" x1="0" y1="0" x2="32" y2="32"><stop offset="0%" stop-color="#2932E1"/><stop offset="100%" stop-color="#4F46E5"/></linearGradient></defs><rect width="32" height="32" rx="8" fill="url(#logoGrad)"/><text x="16" y="21" text-anchor="middle" font-family="Inter,system-ui,sans-serif" font-size="12" font-weight="800" fill="white" letter-spacing=".3">BPP</text></svg>
      Baidu PPC Pro
    </a>
    <div class="nav-links" id="navLinks">
      <a href="../why-baidu-ppc-pro">Why Baidu PPC Pro</a>
      <a href="../features">Services</a>
      <a href="../pricing">Pricing</a>
      <a href="../clients">Clients</a>
      <a href="../faq">FAQ</a>
      <a href="../about">About</a>
      <a href="../blog" class="active">Blog</a>
      <a href="../contact">Contact</a>
    </div>
    <a href="../contact" class="nav-cta">Get Started &rarr;</a>
    <button class="nav-mobile-toggle" onclick="toggleMobileNav()" aria-label="Menu">
      <svg class="hamburger-icon" width="22" height="22" viewBox="0 0 22 22" fill="none"><rect y="4" width="22" height="2" rx="1" fill="#374151"/><rect y="10" width="22" height="2" rx="1" fill="#374151"/><rect y="16" width="22" height="2" rx="1" fill="#374151"/></svg>
    </button>
  </div>
</nav>
<div class="nav-overlay" id="navOverlay" onclick="toggleMobileNav()"></div>

<main>
  <section class="article-hero">
    <div class="container">
      <h1 class="article-title">${title}</h1>
      <div class="article-meta">
        <span>📅 ${formattedDate}</span>
        <span>⏱️ ${readingTime} min read</span>
        <span>✍️ By ${author}</span>
      </div>
    </div>
  </section>
</main>

<section class="article-section">
  <div class="container">
    <article class="article-content">
      ${bodyHtml}
    </article>
  </div>
</section>

<footer>
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        <h3><svg width="28" height="28" viewBox="0 0 32 32" fill="none"><defs><linearGradient id="fLogo" x1="0" y1="0" x2="32" y2="32"><stop offset="0%" stop-color="#2932E1"/><stop offset="100%" stop-color="#4F46E5"/></linearGradient></defs><rect width="32" height="32" rx="8" fill="url(#fLogo)"/><text x="16" y="21" text-anchor="middle" font-family="Inter,system-ui,sans-serif" font-size="12" font-weight="800" fill="white">BPP</text></svg> Baidu PPC Pro</h3>
        <p>We help international agencies and brands access China's digital advertising market with compliance, clarity, and zero guesswork.</p>
      </div>
      <div class="footer-col">
        <h4>Quick Links</h4>
        <ul>
          <li><a href="../why-baidu-ppc-pro">Why Baidu PPC Pro</a></li>
          <li><a href="../features">Services</a></li>
          <li><a href="../pricing">Pricing</a></li>
          <li><a href="../about">About</a></li>
          <li><a href="../faq">FAQ</a></li>
          <li><a href="../blog">Blog</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Contact</h4>
        <ul>
          <li><a href="#" class="obf-email-link" data-u="baidu" data-d="baidumarketing.com"></a></li>
          <li><a href="../contact">Submit a Request</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Legal</h4>
        <ul>
          <li><a href="../privacy">Privacy Policy</a></li>
          <li><a href="../terms">Terms of Service</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="footer-copy">&copy; <script>document.write(new Date().getFullYear())<\/script> Baidu PPC Pro. All rights reserved.</div>
      <div class="footer-social">
        <a href="#" class="obf-email-icon" data-u="baidu" data-d="baidumarketing.com" aria-label="Email"><svg viewBox="0 0 24 24" fill="none" stroke="#D1D5DB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="22,4 12,13 2,4"/></svg></a>
      </div>
    </div>
  </div>
</footer>

<script>
function toggleMobileNav() {
  const links = document.getElementById('navLinks');
  const h = document.querySelector('.hamburger-icon');
  const c = document.querySelector('.close-icon');
  const o = document.getElementById('navOverlay');
  if (!links.classList.contains('open')) { links.classList.add('open'); h.style.display = 'none'; if(c) c.style.display = 'block'; o.classList.add('active'); document.body.style.overflow = 'hidden'; }
  else { links.classList.remove('open'); h.style.display = 'block'; if(c) c.style.display = 'none'; o.classList.remove('active'); document.body.style.overflow = ''; }
}
document.querySelectorAll('.nav-links a').forEach(a => { a.addEventListener('click', () => { if (window.innerWidth <= 900) toggleMobileNav(); }); });
document.querySelectorAll('.obf-email-link').forEach(function(el){el.textContent=el.dataset.u+'@'+el.dataset.d});
document.querySelectorAll('.obf-email-icon').forEach(function(el){el.href='mailto:'+el.dataset.u+'@'+el.dataset.d});
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "${title.replace(/"/g, '\\"')}",
  "description": "${title}",
  "url": "https://baidumarketing.com/blog/${slug}",
  "datePublished": "${date}",
  "dateModified": "${date}",
  "publisher": {
    "@type": "Organization",
    "name": "Baidu PPC Pro",
    "url": "https://baidumarketing.com",
    "logo": {
      "@type": "ImageObject",
      "url": "https://baidumarketing.com/assets/og-brand-default.png",
      "width": 1200,
      "height": 630
    }
  }
}
</script>
</body>
</html>`;

// 输出文件
const outDir = language === 'ja' ? 'ja/blog' : 'blog';
const outPath = path.join('C:/Users/HYE/WorkBuddy/20260411211839', outDir, `${slug}.html`);

// 确保目录存在
const outDirFull = path.dirname(outPath);
if (!fs.existsSync(outDirFull)) fs.mkdirSync(outDirFull, { recursive: true });

fs.writeFileSync(outPath, htmlFile, 'utf8');
console.log('✅ Generated:', outPath);
console.log('  Title:', title);
console.log('  Slug:', slug);
console.log('  Date:', date);
console.log('  Reading time:', readingTime, 'min');
