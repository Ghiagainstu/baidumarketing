/**
 * fix-all-blog-indexes.mjs
 * 修复 blog.html / ja/blog.html / ko/blog.html 的语言混排问题
 * 用法：node scripts/fix-all-blog-indexes.mjs
 */

import fs from 'fs';
import { JSDOM } from 'jsdom';

const ROOT = 'C:\\Users\\HYE\\WorkBuddy\\20260411211839';

const pages = [
  { file: `${ROOT}\\blog.html`,        keepLang: 'en', dir: '' },
  { file: `${ROOT}\\ja\\blog.html`,    keepLang: 'ja', dir: 'ja' },
  { file: `${ROOT}\\ko\\blog.html`,    keepLang: 'ko', dir: 'ko' },
];

function fixPage(filePath, keepLang, dirPrefix) {
  if (!fs.existsSync(filePath)) {
    console.log(`  ⚠️  ${filePath.replace(ROOT, '')} not found, skipping`);
    return;
  }

  const html = fs.readFileSync(filePath, 'utf8');
  const dom = new JSDOM(html);
  const doc = dom.window.document;
  const grid = doc.getElementById('blogGrid');
  if (!grid) { console.log(`  ⚠️  #blogGrid not found`); return; }

  const cards = Array.from(grid.children).filter(el => el.classList.contains('blog-card'));
  console.log(`  Found ${cards.length} total cards`);

  const kept = [], removed = [];
  cards.forEach(card => {
    const link = card.querySelector('a');
    const href = link ? (link.getAttribute('href') || '') : '';
    // 判断这张卡片属于哪种语言
    const isJa = href.includes('ja/blog/');
    const isKo = href.includes('ko/blog/');
    const isEn = href.includes('blog/') && !isJa && !isKo;

    let wrong = false;
    if (keepLang === 'en' && (isJa || isKo)) wrong = true;
    if (keepLang === 'ja' && (isEn || isKo)) wrong = true;
    if (keepLang === 'ko' && (isEn || isJa)) wrong = true;

    if (wrong) {
      const title = card.querySelector('.blog-card-title');
      removed.push(title ? title.textContent.trim().slice(0, 50) : href);
    } else {
      kept.push(card);
    }
  });

  if (removed.length > 0) {
    console.log(`  🗑️  Removing ${removed.length} wrong-language cards:`);
    removed.forEach(r => console.log(`     - ${r}`));
  }

  // 按日期排序
  const sorted = kept.map(card => {
    const metaSpan = card.querySelector('.blog-card-meta > span');
    const dateStr = metaSpan ? metaSpan.textContent.trim() : '';
    // 简单解析日期 → timestamp
    let ts = 0;
    const m1 = dateStr.match(/(\d{4})-(\d{2})-(\d{2})/);
    if (m1) ts = new Date(parseInt(m1[1]), parseInt(m1[2])-1, parseInt(m1[3])).getTime();
    const m2 = dateStr.match(/(\w+)\s+(\d{1,2}),\s*(\d{4})/);
    if (m2) {
      const months = { jan:0,feb:1,mar:2,apr:3,may:4,jun:5,jul:6,aug:7,sep:8,oct:9,nov:10,dec:11 };
      const m = months[m2[1].toLowerCase()];
      if (m !== undefined) ts = new Date(parseInt(m2[3]), m, parseInt(m2[2])).getTime();
    }
    const m3 = dateStr.match(/(\d{4})年(\d{1,2})月(\d{1,2})?日?/);
    if (m3) ts = new Date(parseInt(m3[1]), parseInt(m3[2])-1, parseInt(m3[3]||'1')).getTime();
    const m4 = dateStr.match(/^[A-Za-z]{3}\s+(\d{4})/);
    if (m4) {
      const months = { jan:0,feb:1,mar:2,apr:3,may:4,jun:5,jul:6,aug:7,sep:8,oct:9,nov:10,dec:11 };
      const m = months[dateStr.slice(0,3).toLowerCase()];
      if (m !== undefined) ts = new Date(parseInt(m4[1]), m, 1).getTime();
    }
    return { card, ts: ts || 0 };
  }).sort((a, b) => b.ts - a.ts);

  console.log(`  ✅ Keeping ${kept.length} cards, sorted:`);
  sorted.forEach((item, i) => {
    const title = item.card.querySelector('.blog-card-title');
    const meta = item.card.querySelector('.blog-card-meta > span');
    const t = title ? title.textContent.trim().slice(0, 45) : '';
    const d = meta ? meta.textContent.trim() : '';
    console.log(`     ${i+1}. [${d}] ${t}`);
  });

  grid.innerHTML = '';
  sorted.forEach(({ card }) => grid.appendChild(card));
  fs.writeFileSync(filePath, dom.serialize(), 'utf8');
  console.log(`  ✅ Saved ${filePath.replace(ROOT, '')}`);
}

// 为 ko 创建 blog.html（如果不存在）
function createKoIndex() {
  const koDir = `${ROOT}\\ko\\blog`;
  if (!fs.existsSync(koDir)) { console.log('  ⚠️  ko/blog/ directory not found'); return; }

  const htmlFiles = fs.readdirSync(koDir).filter(f => f.endsWith('.html') && f !== 'index.html');
  console.log(`  Found ${htmlFiles.length} KO HTML files in ko/blog/`);

  const cardsHtml = htmlFiles.map(f => {
    const slug = f.replace(/\.html$/, '');
    // 从 HTML 文件读取 title 和 date
    const raw = fs.readFileSync(`${koDir}\\${f}`, 'utf8');
    const titleMatch = raw.match(/<title>(.*?)<\/title>/);
    const title = titleMatch ? titleMatch[1].replace(/ — Baidu PPC Pro.*$/, '').trim() : slug;
    const dateMatch = raw.match(/<span>([^<]+)<\/span>/);
    const dateStr = dateMatch ? dateMatch[1].trim() : '2026年5月';
    const descMatch = raw.match(/<meta name="description" content="([^"]*)"/);
    const desc = descMatch ? descMatch[1] : '';
    return { slug, title, dateStr, desc, htmlFile: f };
  }).sort((a, b) => {
    // 按日期排序
    const ta = a.dateStr, tb = b.dateStr;
    const ma = ta.match(/(\d{4})-(\d{2})-(\d{2})/);
    const mb = tb.match(/(\d{4})-(\d{2})-(\d{2})/);
    if (ma && mb) return new Date(mb[1],mb[2]-1,mb[3]) - new Date(ma[1],ma[2]-1,ma[3]);
    return 0;
  }).map(({ slug, title, dateStr, desc }) => {
    const descEsc = desc.replace(/"/g, '&quot;').slice(0, 150);
    const titleEsc = title.replace(/"/g, '&quot;');
    return `      <article class="blog-card">
        <a href="ko/blog/${slug}" class="blog-card-link">
          <div class="blog-card-content">
            <h3 class="blog-card-title">${titleEsc}</h3>
            <p class="blog-card-excerpt">${descEsc}</p>
            <div class="blog-card-meta"><span>${dateStr}</span></div>
          </div>
        </a>
      </article>`;
  }).join('\n');

  // 读取模板（从 ja/blog.html 复制结构）
  const jaHtml = fs.readFileSync(`${ROOT}\\ja\\blog.html`, 'utf8');
  // 替换 #blogGrid 内容
  const newHtml = jaHtml.replace(
    /(<main>[\s\S]*?<div class="blog-grid" id="blogGrid">)[\s\S]*?(<\/div>\s*<\/main>)/,
    '$1\n' + cardsHtml + '\n  $2'
  ).replace(/ja\/blog\//g, 'ko/blog/')
   .replace(/lang="ja"/g, 'lang="ko"')
   .replace(/— Baidu PPC Pro Blog/, '— Baidu PPC Pro')
   .replace(/\/ja\/blog\//g, '/ko/blog/');

  fs.writeFileSync(`${ROOT}\\ko\\blog.html`, newHtml, 'utf8');
  console.log(`  ✅ Created ko\\blog.html with ${htmlFiles.length} cards`);
}

console.log('Fixing all blog indexes...\n');
pages.forEach(p => {
  console.log(`📁 ${p.keepLang.toUpperCase()}: ${p.file.replace(ROOT, '')}`);
  try { fixPage(p.file, p.keepLang, p.dir); } catch(e) { console.error(`  ❌ Error: ${e.message}`); }
  console.log('');
});

// 创建 ko/blog.html
console.log('📁 Creating ko\\blog.html...');
try { createKoIndex(); } catch(e) { console.error(`  ❌ Error: ${e.message}`); }

console.log('\nDone!');
