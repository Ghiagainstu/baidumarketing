/**
 * BPP Multi-Language Build Script
 * 
 * Core functions:
 *   1. sync   — Sync nav & footer HTML across all language versions
 *   2. ls     — List all pages by language
 *   3. navh   — Generate nav HTML snippet for a language
 *   4. ftr    — Generate footer HTML snippet for a language
 *   5. site   — Update sitemap.xml with all language entries
 *
 * Usage:
 *   node build.mjs sync          — Sync nav/footer in English pages
 *   node build.mjs sync ja       — Sync nav/footer in Japanese pages
 *   node build.mjs sync all      — Sync all languages
 *   node build.mjs ls            — List all pages
 *   node build.mjs ls ja         — List Japanese pages
 *   node build.mjs navh ja       — Print nav HTML for Japanese
 *   node build.mjs ftr ja        — Print footer HTML for Japanese
 *   node build.mjs site          — Update sitemap.xml
 *   node build.mjs lang ja       — Add Japanese dir + generate first page
 */

import fs from 'fs';
import path from 'path';

const ROOT = new URL('.', import.meta.url).pathname.replace(/^\/(\w:\/)/, '$1');
const LOCALES = path.join(ROOT, 'locales');
const LANG_CFG = JSON.parse(fs.readFileSync(path.join(LOCALES, 'languages.json'), 'utf8'));

// ====== HELPERS ======

function readJSON(file) {
  return JSON.parse(fs.readFileSync(path.join(LOCALES, file), 'utf8'));
}

function readFile(file) {
  return fs.readFileSync(path.join(ROOT, file), 'utf8');
}

function writeFile(file, content) {
  fs.writeFileSync(path.join(ROOT, file), content, 'utf8');
}

function getLangDir(langCode) {
  const lang = LANG_CFG.languages.find(l => l.code === langCode);
  return lang ? lang.dir : '';
}

function pagePath(page, langCode) {
  const dir = getLangDir(langCode);
  if (page === 'index') return dir ? `${dir}/index.html` : 'index.html';
  return dir ? `${dir}/${page}.html` : `${page}.html`;
}

function isHomePage(pagePath) {
  return pagePath.endsWith('index.html') || pagePath === 'index.html';
}

// ====== NAV HTML GENERATOR ======

function generateNavHTML(langCode) {
  const nav = readJSON(`nav-${langCode}.json`);
  const langDir = getLangDir(langCode);
  const isDefault = langDir === '';
  // Nav/footer links: absolute path + .html suffix (required for subdirectory pages like ja/blog/)
  const absPrefix = langCode === 'en' ? '/' : `/${langDir}/`;
  // Language switcher links: absolute paths
  const langPrefix = ''; // not used — lang switcher uses absolute paths directly

  const links = [
    { href: `${absPrefix}why-baidu-ppc-pro.html`, label: nav.links.why },
    { href: `${absPrefix}features.html`, label: nav.links.services },
    { href: `${absPrefix}pricing.html`, label: nav.links.pricing },
    { href: `${absPrefix}clients.html`, label: nav.links.clients },
    { href: `${absPrefix}faq.html`, label: nav.links.faq },
    { href: `${absPrefix}about.html`, label: nav.links.about },
    { href: `${absPrefix}blog.html`, label: nav.links.blog },
    { href: `${absPrefix}contact.html`, label: nav.links.contact },
  ];

  // Build language switcher dropdown items (absolute paths)
  const langItems = LANG_CFG.languages
    .filter(l => l.active)
    .map(l => {
      const link = l.code === 'en' ? '/' : `/${l.dir}/`;
      return `          <a href="${link}" lang="${l.code}" class="lang-switch-item">${l.flag} ${l.nativeLabel}</a>`;
    })
    .join('\n');

  return `    <a href="${absPrefix}index.html" class="nav-logo">
      <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
        <defs><linearGradient id="logoGrad" x1="0" y1="0" x2="32" y2="32"><stop offset="0%" stop-color="#2932E1"/><stop offset="100%" stop-color="#4F46E5"/></linearGradient></defs>
        <rect width="32" height="32" rx="8" fill="url(#logoGrad)"/>
        <path d="M9.5 11.5c0-1.1.9-2 2-2h9c1.1 0 2 .9 2 2v9c0 1.1-.9 2-2 2h-9c-1.1 0-2-.9-2-2v-9z" stroke="white" stroke-width="1.2" fill="none" opacity=".35"/>
        <text x="16" y="21" text-anchor="middle" font-family="Inter,system-ui,sans-serif" font-size="12" font-weight="800" fill="white" letter-spacing=".3">BPP</text>
      </svg>
      Baidu PPC Pro
    </a>
    <div class="nav-links" id="navLinks">
${links.map(l => `      <a href="${l.href}">${l.label}</a>`).join('\n')}
      <a href="${absPrefix}contact.html" class="nav-mobile-cta">${nav.cta}</a>
    </div>
    <div class="nav-right-group">
    <div class="lang-switch">
      <button class="lang-switch-btn" onclick="toggleLangMenu()" aria-label="${nav.languageLabel}">
        ${LANG_CFG.languages.find(l => l.code === langCode)?.flag || '🌐'}
        <svg width="10" height="6" viewBox="0 0 10 6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M1 1l4 4 4-4"/></svg>
      </button>
      <div class="lang-switch-menu" id="langSwitchMenu">
${langItems}
      </div>
    </div>
    <a href="${absPrefix}contact.html" class="nav-cta">${nav.cta}</a>
    </div>
    <button class="nav-mobile-toggle" id="navToggle" onclick="toggleMobileNav()" aria-label="Menu">
      <svg class="hamburger-icon" width="22" height="22" viewBox="0 0 22 22" fill="none"><rect y="4" width="22" height="2" rx="1" fill="#374151"/><rect y="10" width="22" height="2" rx="1" fill="#374151"/><rect y="16" width="22" height="2" rx="1" fill="#374151"/></svg>
      <svg class="close-icon" width="22" height="22" viewBox="0 0 22 22" fill="none" style="display:none"><line x1="4" y1="4" x2="18" y2="18" stroke="#374151" stroke-width="2" stroke-linecap="round"/><line x1="18" y1="4" x2="4" y2="18" stroke="#374151" stroke-width="2" stroke-linecap="round"/></svg>
    </button>`;
}

// ====== FOOTER HTML GENERATOR ======

function generateFooterHTML(langCode) {
  const ftr = readJSON(`footer-${langCode}.json`);
  const langDir = getLangDir(langCode);
  const absPrefix = langCode === 'en' ? '/' : `/${langDir}/`;
  const aboutLink = `${absPrefix}about.html`;

  return `  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        <h3>
          <svg width="28" height="28" viewBox="0 0 32 32" fill="none"><defs><linearGradient id="fLogo" x1="0" y1="0" x2="32" y2="32"><stop offset="0%" stop-color="#2932E1"/><stop offset="100%" stop-color="#4F46E5"/></linearGradient></defs><rect width="32" height="32" rx="8" fill="url(#fLogo)"/><text x="16" y="21" text-anchor="middle" font-family="system-ui" font-size="12" font-weight="800" fill="white" letter-spacing=".3">BPP</text></svg>
          ${ftr.tagline}
        </h3>
        <p>${ftr.description}</p>
      </div>
      <div class="footer-col">
        <h4>${ftr.quickLinks}</h4>
        <ul>
          <li><a href="${absPrefix}features.html">${ftr.links.services}</a></li>
          <li><a href="${absPrefix}pricing.html">${ftr.links.pricing}</a></li>
          <li><a href="${aboutLink}">${ftr.links.about}</a></li>
          <li><a href="${absPrefix}faq.html">${ftr.links.faq}</a></li>
          <li><a href="${absPrefix}blog.html">${ftr.links.blog}</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>${ftr.contact}</h4>
        <ul>
          <li><a href="#" class="obf-email-link" data-u="baidu" data-d="baidumarketing.com"></a></li>
          <li><a href="${absPrefix}contact.html">${ftr.links.contact}</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>${ftr.legal}</h4>
        <ul>
          <li><a href="${absPrefix}privacy.html">${ftr.links.privacy}</a></li>
          <li><a href="${absPrefix}terms.html">${ftr.links.terms}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="footer-copy">© <script>document.write(new Date().getFullYear())</script> ${ftr.copyright}</div>
      <div class="footer-social">
        <a href="#" class="obf-email-icon" data-u="baidu" data-d="baidumarketing.com" aria-label="${ftr.emailAria}"><svg viewBox="0 0 24 24" fill="none" stroke="#D1D5DB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="22,4 12,13 2,4"/></svg></a>
      </div>
    </div>
  </div>`;
}

// ====== LANGUAGE SWITCHER CSS ======

function getLangSwitcherCSS() {
  return `
    .nav-right-group {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-shrink: 0;
    }
    .lang-switch {
      position: relative;
      display: inline-flex;
    }
    .lang-switch-btn {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 6px 10px;
      border: 1px solid var(--gray-200);
      border-radius: 8px;
      background: transparent;
      cursor: pointer;
      font-size: .85rem;
      color: var(--gray-600);
      transition: all var(--transition-base);
    }
    .lang-switch-btn:hover {
      border-color: var(--blue);
      color: var(--blue);
    }
    .lang-switch-menu {
      position: absolute;
      top: calc(100% + 6px);
      right: 0;
      min-width: 150px;
      background: #fff;
      border: 1px solid var(--gray-200);
      border-radius: 10px;
      box-shadow: var(--shadow-md);
      padding: 6px;
      z-index: 200;
      opacity: 0;
      pointer-events: none;
      transition: opacity .2s, transform .2s;
      transform: translateY(-4px);
    }
    .lang-switch-menu.active {
      opacity: 1;
      pointer-events: auto;
      transform: translateY(0);
    }
    .lang-switch-item {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: .85rem;
      color: var(--gray-700);
      transition: background .15s;
      text-decoration: none;
    }
    .lang-switch-item:hover {
      background: var(--blue-light);
      color: var(--blue);
    }
    [data-theme="dark"] .lang-switch-btn {
      border-color: var(--gray-300);
      color: var(--gray-600);
    }
    [data-theme="dark"] .lang-switch-btn:hover {
      border-color: var(--blue);
      color: var(--blue);
    }
    [data-theme="dark"] .lang-switch-menu {
      background: var(--gray-100);
      border-color: var(--gray-200);
    }
    [data-theme="dark"] .lang-switch-item {
      color: var(--gray-700);
    }
    [data-theme="dark"] .lang-switch-item:hover {
      background: var(--blue-light);
    }
    @media (max-width: 768px) {
      .nav-right-group > .lang-switch { display: none; }
      .nav-mobile-toggle { display: flex; }
    }
    @media (min-width: 769px) {
      .nav-right-group { display: flex !important; }
    }
  `;
}

function getLangSwitcherScript() {
  return `
  function toggleLangMenu() {
    const menu = document.getElementById('langSwitchMenu');
    menu.classList.toggle('active');
  }
  document.addEventListener('click', function(e) {
    const menu = document.getElementById('langSwitchMenu');
    const btn = document.querySelector('.lang-switch-btn');
    if (menu && btn && !btn.contains(e.target) && !menu.contains(e.target)) {
      menu.classList.remove('active');
    }
  });
  // Highlight current language in switcher
  document.addEventListener('DOMContentLoaded', function() {
    const currentLang = document.documentElement.lang || 'en';
    document.querySelectorAll('.lang-switch-item').forEach(function(item) {
      if (item.getAttribute('lang') === currentLang) {
        item.style.fontWeight = '600';
        item.style.pointerEvents = 'none';
        item.style.opacity = '0.5';
      }
    });
  });`;
}

// ====== MAIN OPERATIONS ======

function syncNavFooter(langCode) {
  const langDir = getLangDir(langCode);
  const pages = LANG_CFG.pages;
  const navHTML = generateNavHTML(langCode);
  const footerHTML = generateFooterHTML(langCode);
  const langCSS = getLangSwitcherCSS();
  const langScript = getLangSwitcherScript();
  let count = 0;

  for (const page of pages) {
    const filePath = pagePath(page, langCode);
    
    // Skip if file doesn't exist
    if (!fs.existsSync(path.join(ROOT, filePath))) {
      console.log(`  ⏭️  ${filePath} — not found`);
      continue;
    }

    let html = readFile(filePath);
    let modified = false;

    // Replace nav section (between <nav> and </nav>)
    const navMatch = html.match(/<nav>[\s\S]*?<\/nav>/);
    if (navMatch) {
      html = html.replace(navMatch[0], `<nav>\n  <div class="container nav-inner">\n${navHTML}\n  </div>\n</nav>`);
      modified = true;
    }

    // Ensure lang-switch CSS is in the styles
    if (!html.includes('lang-switch')) {
      html = html.replace('</style>', `${langCSS}\n</style>`);
      modified = true;
    }

    // Ensure lang-switch JS is in the scripts
    if (!html.includes('toggleLangMenu')) {
      const scriptEnd = html.lastIndexOf('</script>');
      if (scriptEnd !== -1) {
        const insertPos = html.lastIndexOf('</script>');
        html = html.slice(0, insertPos) + `\n${langScript}\n` + html.slice(insertPos);
      }
      modified = true;
    }

    // Replace footer section (between <footer> and </footer>)
    const footerMatch = html.match(/<footer>[\s\S]*?<\/footer>/);
    if (footerMatch) {
      html = html.replace(footerMatch[0], `<footer>\n${footerHTML}\n</footer>`);
      modified = true;
    }

    if (modified) {
      writeFile(filePath, html);
      count++;
    } else {
      console.log(`  ⚠️  ${filePath} — could not parse`);
    }
  }

  console.log(`  ✅ ${count} pages updated for '${langCode}'`);
  return count;
}

function listPages(langCode) {
  const langs = langCode 
    ? [LANG_CFG.languages.find(l => l.code === langCode)].filter(Boolean)
    : LANG_CFG.languages.filter(l => l.active);

  console.log(`\n📄 BPP Pages by Language:\n`);
  for (const lang of langs) {
    console.log(`  ${lang.flag} ${lang.label} (/${lang.dir || '/'}):`);
    for (const page of LANG_CFG.pages) {
      const filePath = pagePath(page, lang.code);
      const exists = fs.existsSync(path.join(ROOT, filePath)) ? '✅' : '⬜';
      console.log(`    ${exists} ${filePath}`);
    }
    // Blog pages
    const blogDir = lang.dir ? path.join(ROOT, lang.dir, 'blog') : path.join(ROOT, 'blog');
    if (fs.existsSync(blogDir)) {
      const posts = fs.readdirSync(blogDir).filter(f => f.endsWith('.html'));
      console.log(`    📝 blog/ (${posts.length} posts)`);
    }
    console.log('');
  }
}

function generateSitemap() {
  const baseURL = 'https://www.baidumarketing.com';
  const lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
    '  xmlns:xhtml="http://www.w3.org/1999/xhtml">'
  ];

  for (const page of LANG_CFG.pages) {
    const pageName = page === 'index' ? '' : page;
    
    // English version (default)
    const enURL = pageName ? `${baseURL}/${pageName}` : baseURL;
    
    // Build alternates for each active language
    const alternates = LANG_CFG.languages
      .filter(l => l.active)
      .map(l => {
        const altName = page === 'index' ? '' : page;
        const altURL = l.dir ? `${baseURL}/${l.dir}/${altName}` : enURL;
        return `      <xhtml:link rel="alternate" hreflang="${l.code}" href="${altURL}" />`;
      })
      .join('\n');

    const urlLine = pageName ? `${baseURL}/${pageName}` : baseURL;

    lines.push(`  <url>`);
    lines.push(`    <loc>${urlLine}</loc>`);
    lines.push(alternates);
    // Get priority for this page
    const lang = LANG_CFG.languages.find(l => l.code === 'en');
    lines.push(`    <priority>${page === 'index' ? '1.0' : '0.8'}</priority>`);
    lines.push(`  </url>`);
  }

  // Blog posts in English
  const blogDir = path.join(ROOT, 'blog');
  if (fs.existsSync(blogDir)) {
    const posts = fs.readdirSync(blogDir).filter(f => f.endsWith('.html'));
    for (const post of posts) {
      const slug = post.replace('.html', '');
      lines.push(`  <url>`);
      lines.push(`    <loc>${baseURL}/blog/${slug}</loc>`);
      lines.push(`    <priority>0.6</priority>`);
      lines.push(`  </url>`);
    }
  }

  // Japanese pages
  for (const page of LANG_CFG.pages) {
    const jaDir = path.join(ROOT, 'ja');
    const jaFilePath = page === 'index' ? path.join(jaDir, 'index.html') : path.join(jaDir, `${page}.html`);
    if (fs.existsSync(jaFilePath)) {
      const pageName = page === 'index' ? '' : page;
      const urlLine = pageName ? `${baseURL}/ja/${pageName}` : `${baseURL}/ja`;
      lines.push(`  <url>`);
      lines.push(`    <loc>${urlLine}</loc>`);
      lines.push(`    <xhtml:link rel="alternate" hreflang="ja" href="${urlLine}" />`);
      lines.push(`    <priority>0.8</priority>`);
      lines.push(`  </url>`);
    }
  }

  // Japanese blog posts
  const jaBlogDir = path.join(ROOT, 'ja', 'blog');
  if (fs.existsSync(jaBlogDir)) {
    const posts = fs.readdirSync(jaBlogDir).filter(f => f.endsWith('.html'));
    for (const post of posts) {
      const slug = post.replace('.html', '');
      lines.push(`  <url>`);
      lines.push(`    <loc>${baseURL}/ja/blog/${slug}</loc>`);
      lines.push(`    <priority>0.6</priority>`);
      lines.push(`  </url>`);
    }
  }

  lines.push(`</urlset>`);
  
  writeFile('sitemap.xml', lines.join('\n') + '\n');
  console.log('  ✅ sitemap.xml updated');
}

// ====== CLI ======

const args = process.argv.slice(2);
const cmd = args[0];

switch (cmd) {
  case 'sync':
    const langArg = args[1] || 'en';
    console.log(`\n🔄 Syncing nav & footer...\n`);
    if (langArg === 'all') {
      let total = 0;
      for (const lang of LANG_CFG.languages.filter(l => l.active)) {
        total += syncNavFooter(lang.code);
      }
      console.log(`\n  ✅ Total: ${total} pages updated across all languages`);
    } else {
      syncNavFooter(langArg);
    }
    console.log('');
    break;

  case 'ls':
    listPages(args[1]);
    break;

  case 'navh':
    const nlang = args[1] || 'en';
    console.log(generateNavHTML(nlang));
    break;

  case 'ftr':
    const flang = args[1] || 'en';
    console.log(generateFooterHTML(flang));
    break;

  case 'site':
    console.log(`\n🔄 Updating sitemap...\n`);
    generateSitemap();
    console.log('');
    break;

  case 'help':
  default:
    console.log(`
BPP Build Script — Multi-Language Management

Usage:
  node build.mjs sync [lang]   Sync nav/footer for a language (default: en, use "all" for all)
  node build.mjs ls [lang]     List pages by language
  node build.mjs navh [lang]   Print generated nav HTML for a language
  node build.mjs ftr [lang]    Print generated footer HTML for a language
  node build.mjs site          Update sitemap.xml with multi-language entries
  node build.mjs help          Show this help

Examples:
  node build.mjs sync          Sync English pages
  node build.mjs sync ja       Sync Japanese pages
  node build.mjs sync all      Sync all languages
  node build.mjs ls            List all pages in all languages
`);
}
