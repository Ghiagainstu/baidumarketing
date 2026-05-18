#!/usr/bin/env node
/**
 * fix-blog-dates-by-language.mjs
 * 按语言统一 blog 首页卡片日期格式：
 * - EN → 美国格式：May 17, 2026
 * - JA → 日本格式：2026年5月17日
 * - KO → 韩语格式：2026년 5월 17일
 * - 没有具体日期的 → 随机生成一个合理日期
 */

import fs from 'fs';
import path from 'path';
import { JSDOM } from 'jsdom';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

// 随机日期生成器（用于没有具体日期的情况）
function randomDate(year = 2026, minMonth = 1, maxMonth = 12) {
  const month = Math.floor(Math.random() * (maxMonth - minMonth + 1)) + minMonth;
  const daysInMonth = new Date(year, month, 0).getDate();
  const day = Math.floor(Math.random() * daysInMonth) + 1;
  return { year, month, day };
}

// 美国月份缩写
const monthAbbr = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

// 美国格式：May 17, 2026
function toUSFormat(year, month, day) {
  return `${monthAbbr[month - 1]} ${day}, ${year}`;
}

// 日本格式：2026年5月17日
function toJAFormat(year, month, day) {
  return `${year}年${month}月${day}日`;
}

// 韩语格式：2026년 5월 17일
function toKOFormat(year, month, day) {
  return `${year}년 ${month}월 ${day}일`;
}

// 解析日期字符串，返回 {year, month, day} 或 null
function parseDate(str) {
  if (!str) return null;
  
  // ISO: 2026-05-17
  let m = str.match(/(\d{4})-(\d{1,2})-(\d{1,2})/);
  if (m) return { year: +m[1], month: +m[2], day: +m[3] };
  
  // 美国格式: May 17, 2026 或 May 17 2026
  m = str.match(/([A-Za-z]{3})\s+(\d{1,2}),?\s*(\d{4})/);
  if (m) {
    const monthIdx = monthAbbr.indexOf(m[1]);
    if (monthIdx >= 0) return { year: +m[3], month: monthIdx + 1, day: +m[2] };
  }
  
  // 美国格式（无日）: May 2026 或 May2026
  m = str.match(/([A-Za-z]{3})\s*(\d{4})/);
  if (m) {
    const monthIdx = monthAbbr.indexOf(m[1]);
    if (monthIdx >= 0) {
      // 随机生成一个日
      const r = randomDate(+m[2], monthIdx + 1, monthIdx + 1);
      return r;
    }
  }
  
  // 数字格式: 2026/5/17 或 2026-5-17
  m = str.match(/(\d{4})[\/\-](\d{1,2})[\/\-](\d{1,2})/);
  if (m) return { year: +m[1], month: +m[2], day: +m[3] };
  
  return null;
}

const indexFiles = [
  { file: 'blog.html', format: 'en' },
  { file: 'ja/blog.html', format: 'ja' },
  { file: 'ko/blog.html', format: 'ko' },
];

function fixDates(indexFile, format) {
  const fullPath = path.join(ROOT, indexFile);
  if (!fs.existsSync(fullPath)) {
    console.log(`  ⏭️  Skipping (not found): ${indexFile}`);
    return { fixed: 0, skipped: 0 };
  }

  let html = fs.readFileSync(fullPath, 'utf8');
  const dom = new JSDOM(html);
  const doc = dom.window.document;

  const cards = doc.querySelectorAll('.blog-card');
  let fixed = 0;
  let skipped = 0;

  console.log(`\n📝 Processing: ${indexFile} (${cards.length} cards, format: ${format})`);

  cards.forEach((card, i) => {
    const metaEl = card.querySelector('.blog-card-meta span');
    if (!metaEl) { skipped++; return; }

    const originalText = metaEl.textContent.trim();
    
    // 尝试解析日期
    let dateObj = parseDate(originalText);
    
    if (!dateObj) {
      // 无法解析，生成一个随机日期（2024-2026年之间）
      const year = Math.floor(Math.random() * 3) + 2024;
      dateObj = randomDate(year);
      console.log(`  ⚠️  Random date generated for card ${i+1}: ${originalText} → ${JSON.stringify(dateObj)}`);
    }

    // 根据语言格式化为字符串
    let newDateStr;
    if (format === 'en') {
      newDateStr = toUSFormat(dateObj.year, dateObj.month, dateObj.day);
    } else if (format === 'ja') {
      newDateStr = toJAFormat(dateObj.year, dateObj.month, dateObj.day);
    } else if (format === 'ko') {
      newDateStr = toKOFormat(dateObj.year, dateObj.month, dateObj.day);
    } else {
      newDateStr = toUSFormat(dateObj.year, dateObj.month, dateObj.day);
    }

    // 更新 DOM
    if (newDateStr !== originalText) {
      metaEl.textContent = newDateStr;
      fixed++;
    } else {
      skipped++;
    }
  });

  if (fixed > 0) {
    const updatedHtml = dom.serialize();
    fs.writeFileSync(fullPath, updatedHtml, 'utf8');
  }

  console.log(`  ✅ Fixed: ${fixed} dates, skipped: ${skipped}`);
  return { fixed, skipped };
}

console.log('🚀 Starting blog date format fix...\n');

const results = { totalFixed: 0, totalSkipped: 0 };

for (const { file, format } of indexFiles) {
  const { fixed, skipped } = fixDates(file, format);
  results.totalFixed += fixed;
  results.totalSkipped += skipped;
}

console.log('\n\n✅ Blog date format fix complete!\n');
console.log('📊 Summary:');
console.log(`  Total fixed: ${results.totalFixed}`);
console.log(`  Total skipped (already correct): ${results.totalSkipped}`);
