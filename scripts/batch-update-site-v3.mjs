/**
 * 批量更新博客到网站（v3）
 * 功能：生成 HTML + 更新 blog.html + 更新 sitemap.xml + 同步 Obsidian
 * 用法：node batch-update-site-v3.mjs
 */

import fs from 'fs';
import path from 'path';

// ============================================================
// 配置：12 个任务
// ============================================================
const TASKS = [
  { obs: 'E:/Obsidian/Baidu/bpp-baidu-brand-info-account-level-en.md', slug: 'baidu-brand-info-account-level', lang: 'en', cat: 'search', catDisplay: 'Search Ads' },
  { obs: 'E:/Obsidian/Baidu/bpp-baidu-brand-info-account-level-jp.md', slug: 'baidu-brand-info-account-level', lang: 'ja', cat: 'search', catDisplay: 'Search Ads' },
  { obs: 'E:/Obsidian/Baidu/03-Search-Ads/bpp-why-b2b-baidu-search-en.md', slug: 'why-b2b-baidu-search', lang: 'en', cat: 'search', catDisplay: 'Search Ads' },
  { obs: 'E:/Obsidian/Baidu/03-Search-Ads/bpp-why-b2b-baidu-search-jp.md', slug: 'why-b2b-baidu-search', lang: 'ja', cat: 'search', catDisplay: 'Search Ads' },
  { obs: 'E:/Obsidian/Baidu/01-Market-Insights/bpp-chinese-consumers-decision-journey-en.md', slug: 'chinese-consumers-decision-journey', lang: 'en', cat: 'insights', catDisplay: 'Market Insights' },
  { obs: 'E:/Obsidian/Baidu/01-Market-Insights/bpp-chinese-consumers-decision-journey-jp.md', slug: 'chinese-consumers-decision-journey', lang: 'ja', cat: 'insights', catDisplay: 'Market Insights' },
  { obs: 'E:/Obsidian/Baidu/05-Strategy/bpp-b2b-lead-generation-framework-en.md', slug: 'b2b-lead-generation-framework', lang: 'en', cat: 'strategy', catDisplay: 'Strategy' },
  { obs: 'E:/Obsidian/Baidu/05-Strategy/bpp-b2b-lead-generation-framework-jp.md', slug: 'b2b-lead-generation-framework', lang: 'ja', cat: 'strategy', catDisplay: 'Strategy' },
  { obs: 'E:/Obsidian/Baidu/01-Market-Insights/bpp-baidu-2026-international-brands-en.md', slug: 'baidu-2026-international-brands', lang: 'en', cat: 'insights', catDisplay: 'Market Insights' },
  { obs: 'E:/Obsidian/Baidu/01-Market-Insights/bpp-baidu-2026-international-brands-jp.md', slug: 'baidu-2026-international-brands', lang: 'ja', cat: 'insights', catDisplay: 'Market Insights' },
  { obs: 'E:/Obsidian/Baidu/bpp-faq-international-brands-en.md', slug: 'faq-international-brands', lang: 'en', cat: 'faq', catDisplay: 'FAQ' },
  { obs: 'E:/Obsidian/Baidu/bpp-faq-international-brands-jp.md', slug: 'faq-international-brands', lang: 'ja', cat: 'faq', catDisplay: 'FAQ' },
];

// ============================================================
// 工具函数
// ============================================================
function fixAndParseMd(fp) {
  let raw = fs.readFileSync(fp, 'utf8');
  if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);

  // 修复 broken ---：在 --- 前加换行
  raw = raw.replace(/([^\r\n])---\r?\n/gm, '$1\n---\n');
  raw = raw.replace(/([^\r\n])---\s*$/gm, '$1\n---\n');

  // 确保开头有 ---
  if (!raw.startsWith('---\n')) raw = '---\n' + raw;

  // 分割 frontmatter
  const m = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/);
  if (!m) { console.error('  PARSE ERROR: no frontmatter in', fp.split('/').pop()); return null; }

  const fm = {};
  m[1].split(/\r?\n/).forEach(line => {
    const i = line.indexOf(':');
    if (i < 0) return;
    const k = line.slice(0, i).trim();
    let v = line.slice(i + 1).trim();
    if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) v = v.slice(1, -1);
    fm[k] = v;
  });

  // Fallback
  if (!fm.date && fm.created) fm.date = fm.created;
  if (!fm.reading_time) fm.reading_time = '5';

  const body = raw.slice(m[0].length).trim();
  return { fm, body };
}

function mdToHtml(md) {
  let html = md;

  // 保护 HTML 块
  const blocks = [];
  let idx = 0;
  html = html.replace(/<(div|table|blockquote|callout|takeaway|iframe|stats-grid|comparison-table)[\s\S]*?<\/\1>/gi, m => { blocks.push(m); return `%%BLOCK_${idx++}%%`; });

  // Markdown 转换
  html = html.replace(/^#### (.+)$/gm, '<h4>$1</h4>');
  html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
  html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
  html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
  html = html.replace(/^---$/gm, '<hr>');

  // 列表
  html = html.replace(/^- ✅ (.+)$/gm, '<li>✅ $1</li>');
  html = html.replace(/^- ❌ (.+)$/gm, '<li>❌ $1</li>');
  html = html.replace(/^- (.+)$/gm, '<li>$1</li>');

  // 按空行分块
  const parts = html.split(/\n{2,}/).map(p => p.trim()).filter(Boolean);
  const converted = parts.map(p => {
    if (p.startsWith('%%BLOCK_') || p.startsWith('<')) return p;
    if (p.includes('<li>')) {
      const items = p.split('\n').map(l => l.trim()).filter(Boolean).join('');
      return `<ul>${items}</ul>`;
    }
    if (p.startsWith('|')) return mdTableToHtml(p);
    return `<p>${p.replace(/\n/g, '<br>')}</p>`;
  });

  html = converted.join('\n\n');

  // 还原 HTML 块
  blocks.forEach((b, i) => { html = html.replace(`%%BLOCK_${i}%%`, b); });
  return html;
}

function mdTableToHtml(md) {
  const rows = md.trim().split('\n').filter(Boolean);
  if (rows.length < 2) return md;
  const parseRow = r => r.split('|').map(c => c.trim()).filter((_, i, a) => i > 0 && i < a.length - 1);
  const head = parseRow(rows[0]);
  const body = rows.slice(2).map(r => parseRow(r));
  let h = '<table class="comparison-table">\n<thead>\n<tr>';
  head.forEach(c => { h += `<th>${c}</th>`; });
  h += '</tr>\n</thead>\n<tbody>';
  body.forEach(r => { h += '\n<tr>'; r.forEach(c => { h += `<td>${c}</td>`; }); h += '</tr>'; });
  h += '</tbody>\n</table>';
  return h;
}

function generateHtml({ fm, bodyHtml, slug, lang, cat, catDisplay }) {
  const title = fm.title || 'Blog Post';
  const desc = (fm.description || '').replace(/"/g, '&quot;');
  const date = fm.date || '2026-01-01';
  const rt = fm.reading_time || '5';
  const author = fm.author || 'Baidu PPC Pro Team';
  const isJa = lang === 'ja';
  const prefix = isJa ? '../' : '';
  const url = isJa ? `https://baidumarketing.com/ja/blog/${slug}` : `https://baidumarketing.com/blog/${slug}`;
  const dateObj = new Date(date + 'T00:00:00Z');
  const dateStr = dateObj.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
  const catClassMap = { insights: 'insights', search: 'search', feed: 'feed', strategy: 'strategy', landing: 'landing', platform: 'platform', faq: 'faq' };
  const catClass = catClassMap[cat] || cat;

  return `<!DOCTYPE html>
<html lang="${isJa ? 'ja' : 'en'}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title} — Baidu PPC Pro Blog</title>
  <meta name="description" content="${desc}">
  <link rel="canonical" href="${url}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="${title.replace(/"/g, '&quot;')}">
  <meta property="og:description" content="${desc}">
  <meta property="og:url" content="${url}">
  <meta property="og:image" content="https://baidumarketing.com/assets/og-brand-default.png">
  <meta property="og:site_name" content="Baidu PPC Pro">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${title.replace(/"/g, '&quot;')}">
  <meta name="twitter:description" content="${desc}">
  <meta name="twitter:image" content="https://baidumarketing.com/assets/og-brand-default.png">
  <script type="application/ld+json">
  { "@context":"https://schema.org","@type":"BlogPosting","headline":"${title.replace(/"/g, '\\"')}","description":"${desc.replace(/"/g, '\\"')}","datePublished":"${date}","author":{"@type":"Organization","name":"Baidu PPC Pro Team"},"publisher":{"@type":"Organization","name":"Baidu PPC Pro"},"mainEntityOfPage":{"@type":"WebPage","@id":"${url}"} }
  </script>
  <meta name="theme-color" content="#1a56db">
  <meta name="color-scheme" content="light dark">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🔍</text></svg>">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root { --primary:#1a56db;--primary-dark:#1e40af;--gray-50:#f9fafb;--gray-100:#f3f4f6;--gray-200:#e5e7eb;--gray-300:#d1d5db;--gray-400:#9ca3af;--gray-500:#6b7280;--gray-600:#4b5563;--gray-700:#374151;--gray-800:#1f2937;--gray-900:#111827;--white:#ffffff;--green-100:#d1fae5;--green-800:#065f46;--red-100:#fee2e2;--red-800:#991b1b;--radius:8px;--shadow:0 1px 3px rgba(0,0,0,0.1); }
    * { margin:0; padding:0; box-sizing:border-box; }
    body { font-family:'Inter',sans-serif; color:var(--gray-800); background:var(--white); line-height:1.6; }
    .container { max-width:1140px; margin:0 auto; padding:0 20px; }
    nav { background:var(--white); box-shadow:var(--shadow); position:sticky; top:0; z-index:100; }
    .nav-inner { display:flex; align-items:center; justify-content:space-between; height:64px; }
    .nav-logo { font-size:1.2rem; font-weight:700; color:var(--primary); text-decoration:none; }
    .nav-links { display:flex; gap:24px; list-style:none; }
    .nav-links a { color:var(--gray-600); text-decoration:none; font-weight:500; font-size:0.9rem; }
    .nav-links a:hover { color:var(--primary); }
    .nav-right-group { display:flex; align-items:center; gap:8px; }
    .nav-cta { background:var(--primary); color:white; padding:8px 18px; border-radius:var(--radius); text-decoration:none; font-weight:600; font-size:0.85rem; }
    .lang-switch { position:relative; }
    .lang-switch-btn { background:none; border:1px solid var(--gray-200); border-radius:var(--radius); padding:6px 10px; cursor:pointer; font-size:0.85rem; display:flex; align-items:center; gap:4px; }
    .lang-switch-menu { position:absolute; top:calc(100% + 6px); right:0; background:var(--white); border:1px solid var(--gray-200); border-radius:var(--radius); box-shadow:0 4px 12px rgba(0,0,0,0.1); min-width:140px; z-index:200; opacity:0; pointer-events:none; transform:translateY(-4px); transition:all 0.15s ease; }
    .lang-switch-menu.open { opacity:1; pointer-events:auto; transform:translateY(0); }
    .lang-switch-menu a { display:block; padding:8px 14px; color:var(--gray-700); text-decoration:none; font-size:0.85rem; }
    .lang-switch-menu a:hover { background:var(--gray-50); }
    .nav-toggle { display:none; background:none; border:none; cursor:pointer; }
    .nav-toggle span { display:block; width:22px; height:2px; background:var(--gray-800); margin:4px 0; }
    .nav-overlay { display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:999; }
    .nav-overlay.open { display:block; }
    .nav-mobile-panel { display:none; position:fixed; top:0; right:0; width:280px; height:100%; background:var(--white); z-index:1000; flex-direction:column; padding:24px; }
    .nav-mobile-panel.open { display:flex; }
    .nav-mobile-panel a { display:block; padding:12px 0; color:var(--gray-700); text-decoration:none; font-weight:500; border-bottom:1px solid var(--gray-100); }
    @media(max-width:900px) { .nav-links,.nav-right-group .nav-cta,.lang-switch { display:none; } .nav-toggle { display:block; } }
    .theme-toggle { background:none; border:1px solid var(--gray-200); border-radius:var(--radius); padding:6px 8px; cursor:pointer; display:flex; align-items:center; }
    .theme-toggle svg { width:18px; height:18px; }
    body.dark { background:var(--gray-800); color:var(--gray-300); }
    body.dark nav { background:var(--gray-800); }
    body.dark .nav-links a { color:var(--gray-300); }
    body.dark .theme-toggle { border-color:var(--gray-600); }
    main { padding:40px 0; }
    .article-content { max-width:720px; margin:0 auto; padding:0 20px; }
    .article-title { font-size:2rem; font-weight:700; margin-bottom:12px; line-height:1.3; }
    body.dark .article-title { color:var(--white); }
    .article-meta { display:flex; gap:16px; align-items:center; color:var(--gray-500); font-size:0.9rem; margin-bottom:32px; flex-wrap:wrap; }
    .article-meta .dot { width:3px; height:3px; background:var(--gray-400); border-radius:50%; }
    .article-category { display:inline-block; padding:4px 12px; border-radius:20px; font-size:0.8rem; font-weight:600; margin-bottom:12px; }
    .article-category.${catClass} { background:var(--primary); color:white; }
    .article-body h2 { font-size:1.5rem; font-weight:700; margin:32px 0 16px; }
    body.dark .article-body h2 { color:var(--white); }
    .article-body h3 { font-size:1.25rem; font-weight:600; margin:24px 0 12px; }
    body.dark .article-body h3 { color:var(--gray-200); }
    .article-body p { margin-bottom:16px; }
    .article-body ul,.article-body ol { margin:12px 0 12px 20px; }
    .article-body li { margin-bottom:8px; }
    .article-body hr { border:none; border-top:1px solid var(--gray-200); margin:32px 0; }
    .article-body table { width:100%; border-collapse:collapse; margin:20px 0; }
    .article-body th,.article-body td { padding:10px 14px; border:1px solid var(--gray-200); text-align:left; font-size:0.9rem; }
    .article-body th { background:var(--gray-100); font-weight:600; }
    body.dark .article-body th { background:var(--gray-700); color:var(--white); }
    body.dark .article-body td { border-color:var(--gray-600); }
    .stats-grid { display:grid; grid-template-columns:repeat(auto-fit, minmax(200px,1fr)); gap:16px; margin:24px 0; }
    .stat-card { background:var(--gray-50); border-radius:var(--radius); padding:20px; text-align:center; }
    body.dark .stat-card { background:var(--gray-700); }
    .stat-icon { font-size:2rem; margin-bottom:8px; }
    .stat-number { font-size:1.5rem; font-weight:700; color:var(--primary); }
    .stat-label { font-size:0.85rem; color:var(--gray-500); margin-top:4px; }
    .callout { border-radius:var(--radius); padding:16px 20px; margin:20px 0; border-left:4px solid; }
    .callout.tip { background:var(--green-100); border-color:var(--green-800); }
    .callout.warning { background:var(--red-100); border-color:var(--red-800); }
    .takeaway { background:var(--gray-50); border-radius:var(--radius); padding:20px 24px; margin:24px 0; }
    body.dark .takeaway { background:var(--gray-700); }
    .takeaway h4 { margin-bottom:12px; }
    .takeaway ul { margin-left:20px; }
    .blockquote-highlight { border-left:4px solid var(--primary); padding:16px 20px; margin:20px 0; font-style:italic; color:var(--gray-600); }
    footer { background:var(--gray-800); color:var(--gray-300); padding:60px 0 0; }
    .footer-top { max-width:1140px; margin:0 auto; padding:0 20px; display:grid; grid-template-columns:2fr 1fr 1fr 1fr; gap:40px; padding-bottom:40px; border-bottom:1px solid var(--gray-700); }
    .footer-logo { font-size:1.1rem; font-weight:700; color:var(--white); margin-bottom:12px; display:block; text-decoration:none; }
    .footer-desc { font-size:0.85rem; line-height:1.6; margin-bottom:20px; }
    .footer-social { display:flex; gap:12px; }
    .footer-social a { color:var(--gray-400); text-decoration:none; font-size:0.9rem; }
    .footer-heading { color:var(--white); font-weight:600; margin-bottom:16px; font-size:0.95rem; }
    .footer-links { list-style:none; }
    .footer-links li { margin-bottom:10px; }
    .footer-links a { color:var(--gray-400); text-decoration:none; font-size:0.85rem; }
    .footer-links a:hover { color:var(--white); }
    .footer-bottom { text-align:center; padding:20px; font-size:0.8rem; color:var(--gray-500); }
    .footer-bottom a { color:var(--gray-400); text-decoration:none; margin:0 8px; }
    body.dark footer { background:#111827; }
    body.dark .footer-top { border-bottom-color:var(--gray-700); }
    @media(max-width:768px) { .footer-top { grid-template-columns:1fr; gap:24px; } }
  </style>
</head>
<body>
  <nav>
    <div class="container nav-inner">
      <a href="${prefix}index.html" class="nav-logo">Baidu PPC Pro</a>
      <ul class="nav-links">
        <li><a href="${prefix}why-baidu-ppc-pro">Why Baidu PPC Pro</a></li>
        <li><a href="${prefix}features">Services</a></li>
        <li><a href="${prefix}pricing">Pricing</a></li>
        <li><a href="${prefix}clients">Clients</a></li>
        <li><a href="${prefix}faq">FAQ</a></li>
        <li><a href="${prefix}about">About</a></li>
        <li><a href="${prefix}blog">Blog</a></li>
        <li><a href="${prefix}contact">Contact</a></li>
      </ul>
      <div class="nav-right-group">
        <a href="${prefix}contact" class="nav-cta">Get Started</a>
        <div class="lang-switch">
          <button class="lang-switch-btn" onclick="toggleLangMenu()">🌐 <span id="currentLang">${isJa ? '日本語' : 'English'}</span> ▾</button>
          <div class="lang-switch-menu" id="langMenu">
            <a href="${isJa ? '../blog/' + slug + '.html' : 'blog/' + slug + '.html'}">English</a>
            <a href="${isJa ? 'blog/' + slug + '.html' : 'ja/blog/' + slug + '.html'}">日本語</a>
          </div>
        </div>
        <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle theme">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        </button>
        <button class="nav-toggle" onclick="toggleNav()" aria-label="Toggle menu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </nav>
  <div class="nav-overlay" id="navOverlay" aria-hidden="true" onclick="toggleNav()"></div>
  <div class="nav-mobile-panel" id="mobilePanel">
    <a href="${prefix}why-baidu-ppc-pro">Why Baidu PPC Pro</a>
    <a href="${prefix}features">Services</a>
    <a href="${prefix}pricing">Pricing</a>
    <a href="${prefix}clients">Clients</a>
    <a href="${prefix}faq">FAQ</a>
    <a href="${prefix}about">About</a>
    <a href="${prefix}blog">Blog</a>
    <a href="${prefix}contact">Contact</a>
  </div>
  <main>
    <article class="article-content">
      <div class="article-category ${catClass}">${catDisplay}</div>
      <h1 class="article-title">${title}</h1>
      <div class="article-meta">
        <span>${dateStr}</span>
        <span class="dot"></span>
        <span>${rt} min read</span>
        <span class="dot"></span>
        <span>By ${author}</span>
      </div>
      <div class="article-body">
        ${bodyHtml}
      </div>
    </article>
  </main>
  <footer>
    <div class="footer-top">
      <div class="footer-col">
        <a href="${prefix}index.html" class="footer-logo">Baidu PPC Pro</a>
        <p class="footer-desc">We help overseas SMEs enter the Chinese market via Baidu PPC advertising. Transparent pricing, no hidden fees.</p>
        <div class="footer-social"><a href="https://www.baidu.com" target="_blank" rel="noopener">Baidu</a></div>
      </div>
      <div class="footer-col">
        <h4 class="footer-heading">Services</h4>
        <ul class="footer-links">
          <li><a href="${prefix}features">Baidu Ads Management</a></li>
          <li><a href="${prefix}features">Keyword Research</a></li>
          <li><a href="${prefix}features">Landing Page</a></li>
          <li><a href="${prefix}features">Performance Report</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4 class="footer-heading">Company</h4>
        <ul class="footer-links">
          <li><a href="${prefix}about">About Us</a></li>
          <li><a href="${prefix}privacy">Privacy Policy</a></li>
          <li><a href="${prefix}terms">Terms of Service</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4 class="footer-heading">Connect</h4>
        <ul class="footer-links">
          <li><a href="${prefix}contact">Contact Us</a></li>
          <li><a href="${prefix}blog">Blog</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      &copy; <span id="copyright-year"></span> Baidu PPC Pro. All rights reserved.
      <a href="${prefix}privacy">Privacy</a> | <a href="${prefix}terms">Terms</a>
    </div>
  </footer>
  <script>
    function toggleTheme() { document.body.classList.toggle('dark'); localStorage.setItem('theme', document.body.classList.contains('dark')?'dark':'light'); }
    if(localStorage.getItem('theme')==='dark') document.body.classList.add('dark');
    function toggleLangMenu() { document.getElementById('langMenu').classList.toggle('open'); }
    document.addEventListener('click', e => { if(!e.target.closest('.lang-switch')) document.getElementById('langMenu').classList.remove('open'); });
    function toggleNav() { document.getElementById('mobilePanel').classList.toggle('open'); document.getElementById('navOverlay').classList.toggle('open'); }
    document.getElementById('copyright-year').textContent = new Date().getFullYear();
  </script>
</body>
</html>`;
}

// ============================================================
// 主流程
// ============================================================
const enCards = [];
const jaCards = [];
const sitemapEntries = [];

for (const task of TASKS) {
  try {
    const parsed = fixAndParseMd(task.obs);
    if (!parsed) { console.log(`  SKIP (parse failed): ${task.obs.split('/').pop()}`); continue; }
    const { fm, body } = parsed;
    if (!fm.title) { console.log(`  SKIP (no title): ${task.obs.split('/').pop()}`); continue; }

    const bodyHtml = mdToHtml(body);
    const html = generateHtml({ fm, bodyHtml, slug: task.slug, lang: task.lang, cat: task.cat, catDisplay: task.catDisplay });

    const outDir = task.lang === 'ja' ? 'ja/blog' : 'blog';
    const outPath = path.join(outDir, task.slug + '.html');
    fs.mkdirSync(path.dirname(outPath), { recursive: true });
    fs.writeFileSync(outPath, html, 'utf8');
    console.log(`  ✓ ${outPath}`);

    // 生成卡片数据
    const desc = (fm.description || body.replace(/<[^>]+>/g,'').slice(0,100) + '...');
    const date = fm.date || '2026-01-01';
    const d = new Date(date + 'T00:00:00Z');
    const dateStr = d.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
    const rt = fm.reading_time || '5';
    const catClassMap = { insights:'insights', search:'search', strategy:'strategy', faq:'faq' };
    const catClass = catClassMap[task.cat] || task.cat;

    const cardHtml = `      <div class="blog-card" data-category="${task.cat}">\n        <span class="blog-card-tag ${catClass}">${task.catDisplay}</span>\n        <h3 class="blog-card-title"><a href="${task.lang==='ja'?'ja/':''}blog/${task.slug}.html">${fm.title}</a></h3>\n        <p class="blog-card-excerpt">${desc}</p>\n        <div class="blog-card-meta">\n          <span>${dateStr}</span>\n          <span class="read-time"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> ${rt} min</span>\n        </div>\n      </div>`;

    if (task.lang === 'en') enCards.push(cardHtml);
    else jaCards.push(cardHtml);

    const pageUrl = task.lang === 'ja'
      ? `https://baidumarketing.com/ja/blog/${task.slug}`
      : `https://baidumarketing.com/blog/${task.slug}`;
    sitemapEntries.push(`  <url>\n    <loc>${pageUrl}</loc>\n    <lastmod>${date}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>`);

    // 同步到 Obsidian: 更新 status/push_date/url
    let obsRaw = fs.readFileSync(task.obs, 'utf8');
    const obsBom = obsRaw.charCodeAt(0) === 0xFEFF;
    if (obsBom) obsRaw = obsRaw.slice(1);
    if (!obsRaw.includes('status:')) obsRaw = obsRaw.replace(/^---\r?\n/, '---\nstatus: published\n');
    if (!obsRaw.includes('push_date:')) obsRaw = obsRaw.replace(/\n---/, '\npush_date: 2026-05-17\n---');
    const urlField = task.lang === 'ja' ? 'url_ja:' : 'url_en:';
    if (!obsRaw.includes(urlField)) obsRaw = obsRaw.replace(/\n---/, `\n${urlField} ${pageUrl}\n---`);
    fs.writeFileSync(task.obs, (obsBom ? '\uFEFF' : '') + obsRaw, 'utf8');

  } catch (err) {
    console.error(`  ERROR: ${task.obs.split('/').pop()}: ${err.message}`);
  }
}

// 更新 blog.html
console.log('\nUpdating blog.html...');
let blogHtml = fs.readFileSync('blog.html', 'utf8');
const enCardBlock = enCards.join('\n\n');
// 在 "Inactive Keyword Cleanup 2025" 注释前插入
blogHtml = blogHtml.replace(/(<!-- NEW: Inactive Keyword)/, `${enCardBlock}\n\n      $1`);
fs.writeFileSync('blog.html', blogHtml, 'utf8');
console.log(`  ✓ Inserted ${enCards.length} EN cards into blog.html`);

// 更新 ja/blog.html
console.log('Updating ja/blog.html...');
if (fs.existsSync('ja/blog.html')) {
  let jaBlogHtml = fs.readFileSync('ja/blog.html', 'utf8');
  const jaCardBlock = jaCards.join('\n\n');
  jaBlogHtml = jaBlogHtml.replace(/(<!-- NEW: Inactive Keyword)/, `${jaCardBlock}\n\n      $1`);
  fs.writeFileSync('ja/blog.html', jaBlogHtml, 'utf8');
  console.log(`  ✓ Inserted ${jaCards.length} JA cards into ja/blog.html`);
} else {
  console.log('  ja/blog.html not found, skipping');
}

// 更新 sitemap.xml
console.log('Updating sitemap.xml...');
let sitemap = fs.readFileSync('sitemap.xml', 'utf8');
const sitemapBlock = sitemapEntries.join('\n');
sitemap = sitemap.replace(/(\s*<\/urlset>)/, `\n${sitemapBlock}\n$1`);
fs.writeFileSync('sitemap.xml', sitemap, 'utf8');
console.log(`  ✓ Added ${sitemapEntries.length} URLs to sitemap.xml`);

console.log('\nDONE! All 12 articles processed.');
