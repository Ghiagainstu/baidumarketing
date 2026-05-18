// scripts/fix-blog-categories.mjs
// 为 blog index 页面中的 <article> 标签添加 data-category 属性

import fs from 'fs';
import path from 'path';
import { JSDOM } from 'jsdom';

// 根据文件名判断分类
function getCategoryFromFilename(filename) {
  const f = filename.toLowerCase();
  
  // Feed Ads
  if (f.includes('feed')) return 'feed';
  
  // Landing Page
  if (f.includes('landing')) return 'landing';
  
  // Search Ads (包含 search, ad, keyword, bid, cpc, ocpc, cpm, billing, click, audience, v-sign, mcc, negative, url-wildcard, shared-budget, device-bid, display-name, creative-url, account-status, ppc-terms, how-much, can-i-do, brand-one, invalid-click, conversion, ppc-account, audit-rejection, report)
  if (f.includes('search') || 
      f.includes('ad-') || 
      f.includes('keyword') || 
      f.includes('cpc') || 
      f.includes('ocpc') || 
      f.includes('cpm') || 
      f.includes('billing') ||
      f.includes('click') ||
      f.includes('audience') ||
      f.includes('v-sign') ||
      f.includes('mcc') ||
      f.includes('negative') ||
      f.includes('url-wildcard') ||
      f.includes('shared-budget') ||
      f.includes('device-bid') ||
      f.includes('display-name') ||
      f.includes('creative-url') ||
      f.includes('account-status') ||
      f.includes('ppc-term') ||
      f.includes('how-much') ||
      f.includes('can-i-do') ||
      f.includes('brand-one') ||
      f.includes('invalid-click') ||
      f.includes('conversion') ||
      f.includes('ppc-account') ||
      f.includes('audit-rejection') ||
      f.includes('report') ||
      f.includes('baidu-ad-') ||
      f.includes('baidu-ads-') ||
      f.includes('conflicting')) return 'search';
  
  // Platform
  if (f.includes('platform') || 
      f.includes('app-ecosystem') || 
      f.includes('ecosystem') ||
      f.includes('account-structure') ||
      f.includes('creation-workflow')) return 'platform';
  
  // Strategy (包含 strategy, b2b, brand-protection, digital-marketing, native-ads, vs-google)
  if (f.includes('strategy') || 
      f.includes('b2b') || 
      f.includes('brand-protection') ||
      f.includes('digital-marketing') ||
      f.includes('native-ads') ||
      f.includes('vs-google') ||
      f.includes('why-b2b') ||
      f.includes('international-brand') ||
      f.includes('china-internet') ||
      f.includes('digital-consumer') ||
      f.includes('search-vs-ai') ||
      f.includes('ai-assistants') ||
      f.includes('2026-new-opportunities') ||
      f.includes('2025-earnings') ||
      f.includes('chinese-consumers')) return 'strategy';
      
  // Default: insights
  return 'insights';
}

// 处理单个 index 文件
function processIndexFile(filePath) {
  console.log(`\nProcessing: ${filePath}`);
  
  if (!fs.existsSync(filePath)) {
    console.log(`  File not found, skipping.`);
    return;
  }
  
  let html = fs.readFileSync(filePath, 'utf-8');
  const dom = new JSDOM(html);
  const doc = dom.window.document;
  
  const articles = doc.querySelectorAll('article.blog-card');
  console.log(`  Found ${articles.length} articles`);
  
  let updatedCount = 0;
  
  articles.forEach(article => {
    // 获取链接中的文件名
    const link = article.querySelector('a.blog-card-link');
    if (!link) return;
    
    const href = link.getAttribute('href');
    if (!href) return;
    
    // 提取文件名 (e.g., "blog/baidu-ad-creation-workflow-simplified-creative-upgrade" -> "baidu-ad-creation-workflow-simplified-creative-upgrade")
    const match = href.match(/\/([^/]+)\/?$/);
    if (!match) return;
    
    const filename = match[1];
    const category = getCategoryFromFilename(filename);
    
    // 添加 data-category 属性
    if (!article.hasAttribute('data-category')) {
      article.setAttribute('data-category', category);
      updatedCount++;
    }
  });
  
  // 写回文件
  const updatedHtml = doc.documentElement.outerHTML;
  fs.writeFileSync(filePath, updatedHtml, 'utf-8');
  
  console.log(`  Updated ${updatedCount} articles with data-category`);
}

// 主函数
function main() {
  const baseDir = path.resolve('.');
  
  const files = [
    path.join(baseDir, 'blog.html'),
    path.join(baseDir, 'ja', 'blog.html'),
    path.join(baseDir, 'ko', 'blog.html')
  ];
  
  files.forEach(f => processIndexFile(f));
  
  console.log('\n✅ Done! All blog index files updated with data-category attributes.');
}

main();
