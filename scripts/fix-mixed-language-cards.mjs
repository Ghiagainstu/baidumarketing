/**
 * fix-mixed-language-cards.mjs
 * 修复 blog.html / ja/blog.html 中混排的错误：
 *   - blog.html 只保留链接到 blog/ 的卡片（删掉 ja/blog/ 的）
 *   - ja/blog.html 只保留链接到 ja/blog/ 的卡片（删掉 blog/ 的）
 *   - 然后按日期重新排序
 * 用法：node scripts/fix-mixed-language-cards.mjs
 */

import fs from 'fs';
import { JSDOM } from 'jsdom';

const ROOT = 'C:\\Users\\HYE\\WorkBuddy\\20260411211839';

const files = [
  { path: `${ROOT}\\blog.html`,        keepLang: 'en' },
  { path: `${ROOT}\\ja\\blog.html`,    keepLang: 'ja' },
];

function parseDate(str) {
  if (!str) return null;
  str = str.trim();
  const zhMatch = str.match(/(\d{4})年(\d{1,2})月(\d{1,2})?日?/);
  if (zhMatch) {
    const y = parseInt(zhMatch[1]), m = parseInt(zhMatch[2]) - 1;
    const d = zhMatch[3] ? parseInt(zhMatch[3]) : 1;
    return new Date(y, m, d);
  }
  const enMatch2 = str.match(/([A-Za-z]{3})\s+(\d{1,2}),\s*(\d{4})/);
  if (enMatch2) {
    const months = { jan:0, feb:1, mar:2, apr:3, may:4, jun:5, jul:6, aug:7, sep:8, oct:9, nov:10, dec:11 };
    const m = months[enMatch2[1].toLowerCase()];
    if (m !== undefined) return new Date(parseInt(enMatch2[3]), m, parseInt(enMatch2[2]));
  }
  const enMatch = str.match(/([A-Za-z]{3})\s+(\d{4})/);
  if (enMatch) {
    const months = { jan:0, feb:1, mar:2, apr:3, may:4, jun:5, jul:6, aug:7, sep:8, oct:9, nov:10, dec:11 };
    const m = months[enMatch[1].toLowerCase()];
    if (m !== undefined) return new Date(parseInt(enMatch[2]), m, 1);
  }
  const isoMatch = str.match(/(\d{4})-(\d{2})-(\d{2})/);
  if (isoMatch) return new Date(parseInt(isoMatch[1]), parseInt(isoMatch[2]) - 1, parseInt(isoMatch[3]));
  return null;
}

function fixAndSortFile(filePath, keepLang) {
  const html = fs.readFileSync(filePath, 'utf8');
  const dom = new JSDOM(html);
  const doc = dom.window.document;
  const grid = doc.getElementById('blogGrid');
  if (!grid) { console.log(`  ⚠️  #blogGrid not found in ${filePath}`); return; }

  const cards = Array.from(grid.children).filter(el => el.classList.contains('blog-card'));
  console.log(`  Found ${cards.length} total cards`);

  const kept = [], removed = [];
  cards.forEach(card => {
    // 卡片里的链接可能在 .blog-card-link / a.blog-card / .blog-card-title a
    const link = card.querySelector('.blog-card-link') || card.querySelector('a.blog-card') || card.querySelector('.blog-card-title a') || card.querySelector('a');
    const href = link ? (link.getAttribute('href') || '') : '';
    // 支持绝对路径(/ja/blog/)和相对路径(ja/blog/)
    const isJa = href && (href.includes('ja/blog/') || href.includes('/ja/blog/'));
    const isEn = href && (href.includes('blog/') || href.includes('/blog/')) && !isJa;

    if (keepLang === 'en') {
      if (isJa) {
        const title = card.querySelector('.blog-card-title');
        removed.push(title ? title.textContent.trim().slice(0, 50) : href);
      } else {
        kept.push(card);
      }
    } else if (keepLang === 'ja') {
      if (isEn) {
        const title = card.querySelector('.blog-card-title');
        removed.push(title ? title.textContent.trim().slice(0, 50) : href);
      } else {
        kept.push(card);
      }
    }
  });

  if (removed.length > 0) {
    console.log(`  🗑️  Removing ${removed.length} wrong-language cards:`);
    removed.forEach(r => console.log(`     - ${r}`));
  }

  // 按日期排序（最新在前）
  const sorted = kept.map(card => {
    const metaSpan = card.querySelector('.blog-card-meta > span');
    const dateStr = metaSpan ? metaSpan.textContent.trim() : '';
    const date = parseDate(dateStr);
    return { card, dateStr, dateValue: date ? date.getTime() : 0 };
  }).sort((a, b) => b.dateValue - a.dateValue);

  console.log(`  ✅ Keeping ${kept.length} cards, sorted order:`);
  sorted.forEach((item, i) => {
    const titleEl = item.card.querySelector('.blog-card-title');
    const title = titleEl ? titleEl.textContent.trim().slice(0, 55) : '(no title)';
    console.log(`     ${i+1}. [${item.dateStr}] ${title}`);
  });

  grid.innerHTML = '';
  sorted.forEach(({ card }) => grid.appendChild(card));
  fs.writeFileSync(filePath, dom.serialize(), 'utf8');
  console.log(`  ✅ Saved ${filePath.replace(ROOT, '')}`);
}

console.log('Fixing mixed-language blog cards...\n');
files.forEach(f => {
  console.log(`📁 ${f.keepLang === 'en' ? 'EN' : 'JA'}: ${f.path.replace(ROOT, '')}`);
  try { fixAndSortFile(f.path, f.keepLang); } catch(e) { console.error(`  ❌ Error: ${e.message}`); }
  console.log('');
});
console.log('Done!');
