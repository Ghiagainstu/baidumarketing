/**
 * update-blog-grid.mjs
 * 精准替换 #blogGrid 内容（保留 nav/footer/CSS 等完整结构）
 * 用法：node scripts/update-blog-grid.mjs
 */

import fs from 'fs';
import { JSDOM } from 'jsdom';

const ROOT = 'C:\\Users\\HYE\\WorkBuddy\\20260411211839';

const pages = [
  { indexFile: `${ROOT}\\blog.html`,       htmlDir: `${ROOT}\\blog`,       urlPrefix: 'blog/' },
  { indexFile: `${ROOT}\\ja\\blog.html`,   htmlDir: `${ROOT}\\ja\\blog`,   urlPrefix: 'ja/blog/' },
  { indexFile: `${ROOT}\\ko\\blog.html`,   htmlDir: `${ROOT}\\ko\\blog`,   urlPrefix: 'ko/blog/' },
];

function extractMeta(fp) {
  try {
    const html = fs.readFileSync(fp, 'utf8');
    const dom = new JSDOM(html);
    const doc = dom.window.document;
    let title = '';
    const t = doc.querySelector('title');
    if (t) title = t.textContent.replace(/ — Baidu PPC Pro.*$/, '').replace(/ — Baidu PPC Pro.*$/, '').trim();
    if (!title) {
      const h1 = doc.querySelector('.article-title, h1');
      if (h1) title = h1.textContent.trim();
    }
    let dateStr = '';
    const ms = doc.querySelector('.article-meta span, .blog-card-meta span');
    if (ms) dateStr = ms.textContent.trim();
    let desc = '';
    const md = doc.querySelector('meta[name="description"]');
    if (md) desc = md.getAttribute('content') || '';
    if (!desc) {
      const p = doc.querySelector('.article-content p, p');
      if (p) desc = p.textContent.trim().slice(0, 150);
    }
    return { title: title || '', dateStr: dateStr || '', desc: desc || '' };
  } catch(e) { return { title: '', dateStr: '', desc: '' }; }
}

function parseDate(dateStr) {
  if (!dateStr) return 0;
  dateStr = dateStr.trim();
  let m;
  // YYYY-MM-DD
  m = dateStr.match(/(\d{4})-(\d{2})-(\d{2})/);
  if (m) return new Date(parseInt(m[1]), parseInt(m[2])-1, parseInt(m[3])).getTime();
  // Mon DD, YYYY
  m = dateStr.match(/([A-Za-z]{3})\s+(\d{1,2}),\s*(\d{4})/);
  if (m) {
    const months = { jan:0,feb:1,mar:2,apr:3,may:4,jun:5,jul:6,aug:7,sep:8,oct:9,nov:10,dec:11 };
    const mm = months[m[1].toLowerCase()];
    if (mm !== undefined) return new Date(parseInt(m[3]), mm, parseInt(m[2])).getTime();
  }
  // YYYY年MM月DD日
  m = dateStr.match(/(\d{4})年(\d{1,2})月(\d{1,2})?日?/);
  if (m) return new Date(parseInt(m[1]), parseInt(m[2])-1, parseInt(m[3])||1).getTime();
  // YYYY年MM月
  m = dateStr.match(/(\d{4})年(\d{1,2})月/);
  if (m) return new Date(parseInt(m[1]), parseInt(m[2])-1, 1).getTime();
  // Mon YYYY
  m = dateStr.match(/([A-Za-z]{3})\s+(\d{4})/);
  if (m) {
    const months = { jan:0,feb:1,mar:2,apr:3,may:4,jun:5,jul:6,aug:7,sep:8,oct:9,nov:10,dec:11 };
    const mm = months[m[1].toLowerCase()];
    if (mm !== undefined) return new Date(parseInt(m[2]), mm, 1).getTime();
  }
  return 0;
}

function updatePage(indexFile, htmlDir, urlPrefix) {
  if (!fs.existsSync(htmlDir)) {
    console.log(`  ⚠️  Dir not found: ${htmlDir.replace(ROOT,'')}, skipping`);
    return;
  }

  // 读取所有 HTML 文件并提取元数据
  const files = fs.readdirSync(htmlDir).filter(f => f.endsWith('.html'));
  console.log(`  Found ${files.length} HTML files in ${htmlDir.replace(ROOT,'')}`);

  const cardsData = files.map(f => {
    const fp = `${htmlDir}\\${f}`;
    const meta = extractMeta(fp);
    const slug = f.replace(/\.html$/, '');
    return { slug, ...meta, dateValue: parseDate(meta.dateStr) };
  }).sort((a, b) => b.dateValue - a.dateValue);

  // 生成卡片 HTML
  const cardsHtml = cardsData.map(({ slug, title, dateStr, desc }) => {
    const descEsc = (desc || '').replace(/"/g, '&quot;').slice(0, 155);
    const titleEsc = (title || slug).replace(/"/g, '&quot;');
    return `      <article class="blog-card">
        <a href="${urlPrefix}${slug}" class="blog-card-link">
          <div class="blog-card-content">
            <h3 class="blog-card-title">${titleEsc}</h3>
            <p class="blog-card-excerpt">${descEsc}</p>
            <div class="blog-card-meta"><span>${dateStr || ''}</span></div>
          </div>
        </a>
      </article>`;
  }).join('\n');

  // 读取现有 index 文件
  if (!fs.existsSync(indexFile)) {
    console.log(`  ⚠️  Index file not found, creating minimal: ${indexFile.replace(ROOT,'')}`);
    // 创建一个基本文件
    const lang = urlPrefix.startsWith('ja') ? 'ja' : (urlPrefix.startsWith('ko') ? 'ko' : 'en');
    const minimal = `<!DOCTYPE html>
<html lang="${lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Blog — Baidu PPC Pro${lang==='ja'?' Blog':''}</title>
  <meta name="description" content="Baidu advertising blog">
  <link rel="stylesheet" href="${urlPrefix}../assets/style.css">
</head>
<body>
  ${getNav(lang)}
  <main>
    <div class="blog-grid" id="blogGrid">
${cardsHtml}
    </div>
  </main>
  ${getFooter(lang)}
</body>
</html>`;
    fs.writeFileSync(indexFile, minimal, 'utf8');
    console.log(`  ✅ Created ${indexFile.replace(ROOT,'')} (${cardsData.length} cards)`);
    return;
  }

  let html = fs.readFileSync(indexFile, 'utf8');

  // 精准替换 #blogGrid 内容
  // 方法：找到 id="blogGrid" 的 div，替换其 innerHTML
  const dom = new JSDOM(html);
  const doc = dom.window.document;
  const grid = doc.getElementById('blogGrid');
  if (!grid) {
    console.log(`  ⚠️  #blogGrid not found in ${indexFile.replace(ROOT,'')}, skipping`);
    return;
  }
  grid.innerHTML = '\n' + cardsHtml + '\n';
  fs.writeFileSync(indexFile, dom.serialize(), 'utf8');
  console.log(`  ✅ Updated ${indexFile.replace(ROOT,'')} (${cardsData.length} cards)`);
}

// 简易 nav/footer 生成（仅用于新建文件）
function getNav(lang) {
  const up = lang === 'en' ? '' : '../';
  return `  <nav>
    <div class="nav-inner">
      <a href="${up}index" class="nav-logo"><strong>BPP</strong> Baidu PPC Pro</a>
      <div class="nav-links">
        <a href="${up}why-baidu-ppc-pro">Why Baidu PPC Pro</a>
        <a href="${up}features">Services</a>
        <a href="${up}pricing">Pricing</a>
        <a href="${up}clients">Clients</a>
        <a href="${up}faq">FAQ</a>
        <a href="${up}about">About</a>
        <a href="${up}blog">Blog</a>
        <a href="${up}contact">Contact</a>
      </div>
    </div>
  </nav>`;
}
function getFooter(lang) {
  const up = lang === 'en' ? '' : '../';
  return `  <footer>
    <div class="footer-top">
      <div class="footer-brand"><h3><strong>BPP</strong> Baidu PPC Pro</h3></div>
      <div class="footer-col"><h4>Links</h4><ul><li><a href="${up}blog">Blog</a></li></ul></div>
    </div>
  </footer>`;
}

console.log('Updating all blog index files...\n');
pages.forEach(p => {
  console.log(`📁 ${p.indexFile.replace(ROOT,'')}`);
  try { updatePage(p.indexFile, p.htmlDir, p.urlPrefix); }
  catch(e) { console.error(`  ❌ Error: ${e.message}`); }
  console.log('');
});
console.log('Done!');
