const fs = require('fs');
const path = require('path');

// Fix ja/blog/baidu-2026-new-opportunities.html
const filePath = 'c:/Users/HYE/WorkBuddy/20260411211839/ja/blog/baidu-2026-new-opportunities.html';
let html = fs.readFileSync(filePath, 'utf8');

// 1. Fix logo link: ../../ja/index" → /ja/
html = html.replace(/href="\.\.\/\.\.\/ja\/index"/g, 'href="/ja/"');
html = html.replace(/href="\.\.\/\.\.\/ja\/index(?!\.html)"/g, 'href="/ja/"');

// 2. Fix nav links: ../../ja/why-baidu-ppc-pro" → /ja/why-baidu-ppc-pro.html
const navLinks = [
  ['why-baidu-ppc-pro', 'why-baidu-ppc-pro.html'],
  ['features', 'features.html'],
  ['pricing', 'pricing.html'],
  ['clients', 'clients.html'],
  ['faq', 'faq.html'],
  ['about', 'about.html'],
  ['blog', 'blog.html'],
  ['contact', 'contact.html'],
];
for (const [old, newFile] of navLinks) {
  html = html.replace(new RegExp(`href="\\.\\.\\/\\.\\.\\/ja\\/${old}"`, 'g'), `href="/ja/${newFile}"`);
}

// 3. Fix footer links (same pattern)
for (const [old, newFile] of navLinks) {
  html = html.replace(new RegExp(`href="\\.\\.\\/\\.\\.\\/ja\\/${old}"`, 'g'), `href="/ja/${newFile}"`);
}

// 4. Fix breadcrumb links
html = html.replace(/href="\.\.\/\.\.\/ja\/index"/g, 'href="/ja/"');
html = html.replace(/href="\.\.\/\.\.\/ja\/blog"/g, 'href="/ja/blog.html"');

// 5. Fix CTA button links
html = html.replace(/href="\.\.\/\.\.\/ja\/contact"/g, 'href="../contact.html"');

// 6. Fix related links: ../../ja/blog/... → ../blog/...
html = html.replace(/href="\.\.\/\.\.\/ja\/blog\/([^"]*\.html)"/g, 'href="../blog/$1"');
html = html.replace(/href="\.\.\/\.\.\/ja\/blog\/([^"]*)"(?!\.html)/g, 'href="../blog/$1.html"');

// 7. Fix lang-switch links
html = html.replace(/href="\.\.\/index"/g, 'href="/"');
html = html.replace(/href="\.\.\/ja\/index"/g, 'href="/ja/"');

// 8. Remove nav-cta
html = html.replace(/<a href="\.\.\/\.\.\/ja\/contact" class="nav-cta">[^<]*<\/a>/g, '');

// 9. Fix lang-switch button (should be like other JA pages)
html = html.replace(/🇯🇵 ▼/g, '🇯🇵');

fs.writeFileSync(filePath, html, 'utf8');
console.log('Fixed:', filePath);
