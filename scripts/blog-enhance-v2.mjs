#!/usr/bin/env node
/**
 * blog-enhance-v2.mjs
 * 智能批量增强博客文章
 * 
 * 策略：
 * 1. 检测文件模板类型（旧 vs 新）
 * 2. 只增强内容（emoji、callout、takeaway）
 * 3. 不破坏已有结构
 */

import fs from 'fs';
import path from 'path';
import { JSDOM } from 'jsdom';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

// 需要增强的文件列表（今天新建的）
const filesToEnhance = [
  // EN
  'blog/baidu-ad-creation-workflow-simplified-creative-upgrade.html',
  'blog/baidu-ad-performance-diagnostic-tool.html',
  'blog/baidu-ads-campaign-upgrade-2025.html',
  'blog/baidu-brand-info-account-level.html',
  'blog/baidu-brand-zone-material-pre-review.html',
  'blog/baidu-click-fraud-ipv4-blocking.html',
  'blog/baidu-conversion-tracking-dedup.html',
  'blog/baidu-feed-ads-history-operation-records-upgrade.html',
  'blog/baidu-landing-page-audit-rejection-reasons.html',
  'blog/baidu-landing-page-report.html',
  'blog/baidu-ocpc-skip-data-accumulation.html',
  'blog/baidu-search-device-bid-coefficient-retirement.html',
  'blog/b2b-lead-generation-framework.html',
  'blog/baidu-2026-international-brands.html',
  // JA
  'ja/blog/baidu-ad-creation-workflow-simplified-creative-upgrade.html',
  'ja/blog/baidu-ad-performance-diagnostic-tool.html',
  'ja/blog/baidu-ads-campaign-upgrade-2025.html',
  'ja/blog/baidu-brand-info-account-level.html',
  'ja/blog/baidu-click-fraud-ipv4-blocking.html',
  'ja/blog/baidu-conversion-tracking-dedup.html',
  'ja/blog/baidu-feed-ads-history-operation-records-upgrade.html',
  'ja/blog/baidu-landing-page-audit-rejection-reasons.html',
  'ja/blog/baidu-landing-page-report.html',
  'ja/blog/baidu-ocpc-skip-data-accumulation.html',
  'ja/blog/baidu-search-device-bid-coefficient-retirement.html',
  'ja/blog/b2b-lead-generation-framework.html',
  'ja/blog/baidu-2026-international-brands.html',
  // KO
  'ko/blog/baidu-2026-new-opportunities.html',
  'ko/blog/baidu-ad-performance-diagnostic-tool.html',
  'ko/blog/baidu-ads-campaign-upgrade-2025.html',
  'ko/blog/baidu-brand-info-account-level.html',
  'ko/blog/baidu-click-fraud-ipv4-blocking.html',
  'ko/blog/baidu-conversion-tracking-dedup.html',
  'ko/blog/baidu-feed-ads-history-operation-records-upgrade.html',
  'ko/blog/baidu-landing-page-audit-rejection-reasons.html',
  'ko/blog/baidu-landing-page-report.html',
  'ko/blog/baidu-ocpc-skip-data-accumulation.html',
  'ko/blog/baidu-search-device-bid-coefficient-retirement.html'
];

function detectTemplate(doc) {
  // 检测模板类型
  const hasDataTheme = doc.documentElement.hasAttribute('data-theme') || doc.querySelector('[data-theme]');
  const hasBodyDark = doc.querySelector('body.dark');
  const hasVarBlue = doc.querySelector('style')?.textContent.includes('--blue');
  const hasVarPrimary = doc.querySelector('style')?.textContent.includes('--primary');
  
  if (hasBodyDark || hasVarPrimary) {
    return 'new'; // 新模板
  } else if (hasVarBlue || hasDataTheme) {
    return 'old'; // 旧模板
  }
  return 'unknown';
}

function enhanceContent(doc, filePath) {
  let enhancements = 0;
  
  // 1. 添加 emoji 到 H2 标题（如果还没有）
  const h2s = doc.querySelectorAll('h2');
  h2s.forEach(h2 => {
    const text = h2.textContent.trim();
    if (!text.match(/[\u{1F300}-\u{1F9FF}]/u)) {
      // 根据关键词添加 emoji
      const emojiMap = {
        'Upgrade': '🚀', 'Why': '💡', 'How': '🔧', 'What': '📊',
        'Where': '🎯', 'When': '⏰', 'Conclusion': '✅', 'Summary': '📋',
        'Tip': '💡', 'Warning': '⚠️', 'Note': '📝', 'Step': '🔢',
        'Framework': '🏗️', 'Guide': '📚', 'Strategy': '♟️', 'Tool': '🛠️'
      };
      
      let emoji = '📊'; // 默认
      for (const [key, val] of Object.entries(emojiMap)) {
        if (text.includes(key)) {
          emoji = val;
          break;
        }
      }
      h2.textContent = `${emoji} ${text}`;
      enhancements++;
    }
  });
  
  // 2. 添加 emoji 到 H3 标题
  const h3s = doc.querySelectorAll('h3');
  let h3Counter = 1;
  h3s.forEach(h3 => {
    const text = h3.textContent.trim();
    if (!text.match(/[\u{1F300}-\u{1F9FF}]/u)) {
      h3.textContent = `${h3Counter}️⃣ ${text}`;
      h3Counter++;
      enhancements++;
    }
  });
  
  // 3. 添加 takeaway 摘要框（如果不存在）
  if (!doc.querySelector('.takeaway-box') && !doc.querySelector('.takeaway')) {
    const articleContent = doc.querySelector('.article-content') || doc.querySelector('.article-body');
    if (articleContent) {
      const takeaway = doc.createElement('div');
      takeaway.className = 'takeaway-box';
      takeaway.innerHTML = `
        <h3>📝 Key Takeaways</h3>
        <ul>
          <li>Baidu advertising platform continues to evolve with new features</li>
          <li>Overseas advertisers can benefit from these updates with the right partner</li>
          <li>Professional management ensures compliance and optimal performance</li>
        </ul>
      `;
      articleContent.appendChild(takeaway);
      enhancements++;
    }
  }
  
  // 4. 增强 callout（如果已有 callout 但缺少 emoji）
  const callouts = doc.querySelectorAll('.callout');
  callouts.forEach(callout => {
    const firstChild = callout.firstElementChild;
    if (firstChild && !firstChild.textContent.match(/[\u{1F300}-\u{1F9FF}]/u)) {
      // 添加默认 icon
      const icon = doc.createElement('span');
      icon.className = 'callout-icon';
      icon.textContent = '💡';
      callout.insertBefore(icon, firstChild);
      enhancements++;
    }
  });
  
  return enhancements;
}

function fixFrontmatter(doc) {
  // 删除泄露的 frontmatter
  let removed = 0;
  const articleContent = doc.querySelector('.article-content') || doc.querySelector('.article-body');
  
  if (articleContent) {
    const elements = articleContent.querySelectorAll('p, div');
    elements.forEach(el => {
      const text = el.textContent;
      if (text.includes('--- title:') || 
          text.includes('created:') || 
          text.includes('source_url:') ||
          text.includes('category:') ||
          text.includes('tags:') ||
          text.includes('slug:') ||
          text.includes('language:') ||
          text.includes('author:')) {
        el.remove();
        removed++;
      }
    });
  }
  
  return removed;
}

function processFile(filePath) {
  const fullPath = path.join(ROOT, filePath);
  if (!fs.existsSync(fullPath)) {
    console.log(`  ⏭️  Skipping (not found): ${filePath}`);
    return { success: false, reason: 'not found' };
  }
  
  try {
    let html = fs.readFileSync(fullPath, 'utf8');
    const dom = new JSDOM(html);
    const doc = dom.window.document;
    
    console.log(`\n📝 Processing: ${filePath}`);
    
    // 检测模板类型
    const templateType = detectTemplate(doc);
    console.log(`  📊 Template type: ${templateType}`);
    
    // 修复 frontmatter 泄露
    const removed = fixFrontmatter(doc);
    if (removed > 0) {
      console.log(`  🧹 Removed ${removed} frontmatter elements`);
    }
    
    // 增强内容
    const enhancements = enhanceContent(doc, filePath);
    if (enhancements > 0) {
      console.log(`  ✨ Added ${enhancements} content enhancements`);
    }
    
    // 写回文件
    const updatedHtml = dom.serialize();
    fs.writeFileSync(fullPath, updatedHtml, 'utf8');
    
    console.log(`  ✅ Enhanced: ${filePath}`);
    return { success: true, templateType, removed, enhancements };
    
  } catch (error) {
    console.error(`  ❌ Error processing ${filePath}:`, error.message);
    return { success: false, reason: error.message };
  }
}

// 主执行逻辑
console.log('🚀 Starting smart blog enhancement...\n');
console.log(`📋 Total files to process: ${filesToEnhance.length}\n`);

const results = {
  success: 0,
  failed: 0,
  templates: { old: 0, new: 0, unknown: 0 },
  totalRemoved: 0,
  totalEnhancements: 0
};

for (const file of filesToEnhance) {
  const result = processFile(file);
  if (result.success) {
    results.success++;
    results.templates[result.templateType]++;
    results.totalRemoved += result.removed || 0;
    results.totalEnhancements += result.enhancements || 0;
  } else {
    results.failed++;
  }
}

console.log('\n\n✅ Batch enhancement complete!\n');
console.log('📊 Summary:');
console.log(`  Success: ${results.success} files`);
console.log(`  Failed: ${results.failed} files`);
console.log(`  Template types: Old=${results.templates.old}, New=${results.templates.new}, Unknown=${results.templates.unknown}`);
console.log(`  Frontmatter removed: ${results.totalRemoved} elements`);
console.log(`  Content enhancements: ${results.totalEnhancements} items`);
