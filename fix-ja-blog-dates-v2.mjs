// fix-ja-blog-dates-v2.mjs
// 从日语博客实际文件中提取正确的发布日期，更新索引页
// 支持多种日期格式

import fs from 'fs';
import { JSDOM } from 'jsdom';

const blogIndex = 'ja/blog.html';
const blogDir = 'ja/blog';

console.log('🔧 修复日语博客索引日期（v2 - 支持多种格式）...\n');

// 读取索引页
let html = fs.readFileSync(blogIndex, 'utf-8');
const dom = new JSDOM(html);
const doc = dom.window.document;

const articles = doc.querySelectorAll('article.blog-card');
console.log(`📊 找到 ${articles.length} 个文章卡片\n`);

let fixed = 0;
let skipped = 0;

articles.forEach((article, index) => {
  const link = article.querySelector('a.blog-card-link');
  if (!link) return;
  
  const href = link.getAttribute('href');
  const slugMatch = href.match(/\/([^/]+)\/?$/);
  if (!slugMatch) return;
  
  const slug = slugMatch[1];
  const blogFile = `${blogDir}/${slug}.html`;
  
  if (!fs.existsSync(blogFile)) {
    console.log(`  ⚠️  文件不存在: ${blogFile}`);
    skipped++;
    return;
  }
  
  const blogHtml = fs.readFileSync(blogFile, 'utf-8');
  const blogDom = new JSDOM(blogHtml);
  const blogDoc = blogDom.window.document;
  
  // 方法1: 从 JSON-LD 中提取 datePublished（最可靠）
  let correctDate = null;
  const scripts = blogDoc.querySelectorAll('script[type="application/ld+json"]');
  for (const script of scripts) {
    const text = script.textContent;
    const dpMatch = text.match(/"datePublished":\s*"(\d{4})-(\d{2})-(\d{2})"/);
    if (dpMatch) {
      const [_, year, month, day] = dpMatch;
      correctDate = `${year}年${parseInt(month)}月${parseInt(day)}日`;
      break;
    }
  }
  
  // 方法2: 从 .article-meta 提取（多种格式）
  if (!correctDate) {
    const meta = blogDoc.querySelector('.article-meta');
    if (meta) {
      const metaText = meta.textContent;
      
      // 格式1: 2026年5月2日
      let dateMatch = metaText.match(/(\d{4}年\d{1,2}月\d{1,2}日)/);
      if (dateMatch) correctDate = dateMatch[1];
      
      // 格式2: 2026年5月（只有年月）
      if (!correctDate) {
        dateMatch = metaText.match(/(\d{4}年\d{1,2}月)/);
        if (dateMatch) correctDate = dateMatch[1];
      }
      
      // 格式3: May 2026 / May 17, 2026（英文格式）
      if (!correctDate) {
        const enMatch = metaText.match(/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2}),?\s*(\d{4})/);
        if (enMatch) {
          const months = {Jan:1, Feb:2, Mar:3, Apr:4, May:5, Jun:6, Jul:7, Aug:8, Sep:9, Oct:10, Nov:11, Dec:12};
          const m = months[enMatch[1]];
          const d = enMatch[2] ? parseInt(enMatch[2]) : null;
          const y = parseInt(enMatch[3]);
          correctDate = d ? `${y}年${m}月${d}日` : `${y}年${m}月`;
        }
      }
    }
  }
  
  if (!correctDate) {
    console.log(`  ⚠️  无法提取日期: ${slug}`);
    skipped++;
    return;
  }
  
  // 更新索引页中的日期
  const metaSpan = article.querySelector('.blog-card-meta span');
  if (metaSpan) {
    const current = metaSpan.textContent.trim();
    if (current !== correctDate) {
      console.log(`  ✅ ${index + 1}: ${current} → ${correctDate} (${slug})`);
      metaSpan.textContent = correctDate;
      fixed++;
    }
  }
});

// 保存
const updatedHtml = doc.documentElement.outerHTML;
fs.writeFileSync(blogIndex, updatedHtml, 'utf-8');

console.log(`\n✅ 完成：修复 ${fixed} 个，跳过 ${skipped} 个`);
console.log(`📝 文件已更新: ${blogIndex}`);
