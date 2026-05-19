// check-missing-styles.js
// 检查blog页面缺少哪些视觉CSS样式定义
// 用法: node check-missing-styles.js

const fs = require('fs');
const path = require('path');

const BLOG_DIR = path.join(__dirname, 'blog');

// 需要检查的视觉CSS类名
const requiredStyles = [
  'stats-grid',
  'stat-card',
  'comparison-table',
  'callout',
  'takeaway',
  'cta-box',
  'chart-container',
  'article-hero',
  'article-title',
  'article-meta',
  'article-content',
  'related-section',
  'related-grid',
  'related-card',
  'back-to-top',
];

const files = fs.readdirSync(BLOG_DIR).filter(f => f.endsWith('.html'));
const results = [];

for (const file of files) {
  const filePath = path.join(BLOG_DIR, file);
  const html = fs.readFileSync(filePath, 'utf8');
  const missing = [];
  
  for (const cls of requiredStyles) {
    // 检查是否有该class的CSS定义（在<style>标签内）
    const regex = new RegExp('\\.' + cls + '\\s*\\{', 'i');
    if (!regex.test(html)) {
      missing.push(cls);
    }
  }
  
  if (missing.length > 0) {
    results.push({ file, missing });
  }
}

console.log('缺少视觉CSS样式定义的页面：');
for (const r of results) {
  console.log('\n' + r.file + ':');
  console.log('  缺少: ' + r.missing.join(', '));
}

console.log('\n总计: ' + results.length + ' 个页面有问题');
