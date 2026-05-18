/**
 * sort-blog-cards.mjs
 * 按日期排序 blog.html / ja/blog.html 的博客卡片（最新在前）
 * 用法：node scripts/sort-blog-cards.mjs
 */

import fs from 'fs';
import { JSDOM } from 'jsdom';

const ROOT = 'C:\\Users\\HYE\\WorkBuddy\\20260411211839';

const files = [
  `${ROOT}\\blog.html`,
  `${ROOT}\\ja\\blog.html`,
  `${ROOT}\\ko\\blog.html`,
];

// 解析各种日期格式，返回 Date 对象（无法解析返回 null）
function parseDate(str) {
  if (!str) return null;
  str = str.trim();

  // 中文/日文格式：2025年12月8日 / 2025年12月
  const zhMatch = str.match(/(\d{4})年(\d{1,2})月(\d{1,2})?日?/);
  if (zhMatch) {
    const y = parseInt(zhMatch[1]), m = parseInt(zhMatch[2]) - 1;
    const d = zhMatch[3] ? parseInt(zhMatch[3]) : 1;
    return new Date(y, m, d);
  }

  // English: "Apr 2026", "Dec 2024"
  const enMatch = str.match(/([A-Za-z]{3})\s+(\d{4})/);
  if (enMatch) {
    const months = { jan:0, feb:1, mar:2, apr:3, may:4, jun:5, jul:6, aug:7, sep:8, oct:9, nov:10, dec:11 };
    const m = months[enMatch[1].toLowerCase()];
    if (m !== undefined) return new Date(parseInt(enMatch[2]), m, 1);
  }

  // English: "Jul 14, 2021", "Dec 08, 2025"
  const enMatch2 = str.match(/([A-Za-z]{3})\s+(\d{1,2}),\s*(\d{4})/);
  if (enMatch2) {
    const months = { jan:0, feb:1, mar:2, apr:3, may:4, jun:5, jul:6, aug:7, sep:8, oct:9, nov:10, dec:11 };
    const m = months[enMatch2[1].toLowerCase()];
    if (m !== undefined) return new Date(parseInt(enMatch2[3]), m, parseInt(enMatch2[2]));
  }

  // ISO: 2025-12-08
  const isoMatch = str.match(/(\d{4})-(\d{2})-(\d{2})/);
  if (isoMatch) return new Date(parseInt(isoMatch[1]), parseInt(isoMatch[2]) - 1, parseInt(isoMatch[3]));

  return null;
}

function sortBlogFile(filePath) {
  const html = fs.readFileSync(filePath, 'utf8');
  const dom = new JSDOM(html);
  const doc = dom.window.document;

  const grid = doc.getElementById('blogGrid');
  if (!grid) { console.log(`  ⚠️  #blogGrid not found in ${filePath}`); return; }

  // 提取所有直接子元素（卡片）
  const children = Array.from(grid.children);
  const cards = children.filter(el => el.classList.contains('blog-card'));

  console.log(`  Found ${cards.length} cards`);

  // 提取日期并排序
  const sorted = cards.map(card => {
    const metaSpan = card.querySelector('.blog-card-meta > span');
    const dateStr = metaSpan ? metaSpan.textContent.trim() : '';
    const date = parseDate(dateStr);
    return { card, dateStr, date, dateValue: date ? date.getTime() : 0 };
  }).sort((a, b) => b.dateValue - a.dateValue);

  // 打印排序结果
  console.log(`  Sorted order:`);
  sorted.forEach((item, i) => {
    const titleEl = item.card.querySelector('.blog-card-title');
    const title = titleEl ? titleEl.textContent.trim().slice(0, 60) : '(no title)';
    console.log(`    ${i+1}. [${item.dateStr}] ${title}`);
  });

  // 重写 grid 内容
  grid.innerHTML = '';
  sorted.forEach(({ card }) => grid.appendChild(card));

  // 写回文件
  fs.writeFileSync(filePath, dom.serialize(), 'utf8');
  console.log(`  ✅ Saved ${filePath.replace(ROOT, '')}`);
}

console.log('Sorting blog cards by date (newest first)...\n');
files.forEach(f => {
  console.log(`📁 Processing: ${f.replace(ROOT, '')}`);
  try { sortBlogFile(f); } catch(e) { console.error(`  ❌ Error: ${e.message}`); }
  console.log('');
});
console.log('Done!');
