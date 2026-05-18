// fix-ja-blog-404-and-dates.mjs
// 修复日语博客索引页的两个问题：
// 1. 链接路径错误（href="ja/blog/..." → href="blog/..."）
// 2. 日期错误（从实际博客文件中提取正确日期）

import fs from 'fs';
import { JSDOM } from 'jsdom';

const blogIndex = 'ja/blog.html';
const blogDir = 'ja/blog';

console.log('🔧 修复日语博客索引页...\n');

// 读取索引页
let html = fs.readFileSync(blogIndex, 'utf-8');
const dom = new JSDOM(html);
const doc = dom.window.document;

// 获取所有文章卡片
const articles = doc.querySelectorAll('article.blog-card');
console.log(`📊 找到 ${articles.length} 个文章卡片\n`);

let linkFixCount = 0;
let dateFixCount = 0;

articles.forEach((article, index) => {
  const link = article.querySelector('a.blog-card-link');
  if (!link) return;
  
  const href = link.getAttribute('href');
  
  // 修复1：链接路径
  // 错误：href="ja/blog/slug"
  // 正确：href="blog/slug"（相对路径）或 href="/ja/blog/slug"（绝对路径）
  if (href && href.startsWith('ja/blog/')) {
    const newHref = href.replace(/^ja\/blog\//, 'blog/');
    link.setAttribute('href', newHref);
    linkFixCount++;
    console.log(`  ✅ 修复链接 ${index + 1}: ${href} → ${newHref}`);
  }
  
  // 修复2：日期
  // 从实际博客文件中提取正确日期
  const slugMatch = href.match(/\/([^/]+)\/?$/);
  if (!slugMatch) return;
  
  const slug = slugMatch[1];
  const blogFile = `${blogDir}/${slug}.html`;
  
  if (!fs.existsSync(blogFile)) {
    console.log(`  ⚠️  文件不存在: ${blogFile}`);
    return;
  }
  
  const blogHtml = fs.readFileSync(blogFile, 'utf-8');
  const blogDom = new JSDOM(blogHtml);
  const blogDoc = blogDom.window.document;
  
  // 从 article-meta 中提取日期
  const meta = blogDoc.querySelector('.article-meta');
  if (!meta) {
    console.log(`  ⚠️  找不到 .article-meta: ${slug}`);
    return;
  }
  
  const metaText = meta.textContent.trim();
  // 匹配日期格式：2026年5月2日
  const dateMatch = metaText.match(/(\d{4}年\d{1,2}月\d{1,2}日)/);
  
  if (!dateMatch) {
    console.log(`  ⚠️  找不到日期: ${slug} (${metaText})`);
    return;
  }
  
  const correctDate = dateMatch[1];
  
  // 更新索引页中的日期
  const metaSpan = article.querySelector('.blog-card-meta span');
  if (metaSpan) {
    const currentDate = metaSpan.textContent.trim();
    if (currentDate !== correctDate) {
      console.log(`  📅 修复日期 ${index + 1}: ${currentDate} → ${correctDate} (${slug})`);
      metaSpan.textContent = correctDate;
      dateFixCount++;
    }
  }
});

// 保存更新后的HTML
const updatedHtml = doc.documentElement.outerHTML;
fs.writeFileSync(blogIndex, updatedHtml, 'utf-8');

console.log(`\n✅ 修复完成：`);
console.log(`  - 链接修复: ${linkFixCount} 个`);
console.log(`  - 日期修复: ${dateFixCount} 个`);
console.log(`\n📝 文件已更新: ${blogIndex}`);
