#!/usr/bin/env node
/**
 * fix-meta-tags.mjs
 * 修复增强后文件的 meta 标签格式问题
 */

import fs from 'fs';
import path from 'path';
import { JSDOM } from 'jsdom';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

const filesToFix = [
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
  // JA
  'ja/blog/baidu-ad-creation-workflow-simplified-creative-upgrade.html',
  'ja/blog/baidu-ad-performance-diagnostic-tool.html',
  'ja/blog/baidu-brand-info-account-level.html',
  'ja/blog/baidu-click-fraud-ipv4-blocking.html',
  'ja/blog/baidu-conversion-tracking-dedup.html',
  'ja/blog/baidu-feed-ads-history-operation-records-upgrade.html',
  'ja/blog/baidu-landing-page-audit-rejection-reasons.html',
  'ja/blog/baidu-landing-page-report.html',
  'ja/blog/baidu-ocpc-skip-data-accumulation.html',
  'ja/blog/baidu-search-device-bid-coefficient-retirement.html',
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

function fixFile(filePath) {
  const fullPath = path.join(ROOT, filePath);
  if (!fs.existsSync(fullPath)) {
    console.log(`  ⏭️  Skipping (not found): ${filePath}`);
    return;
  }

  let html = fs.readFileSync(fullPath, 'utf8');
  const dom = new JSDOM(html);
  const doc = dom.window.document;
  
  console.log(`\n🔧 Fixing: ${filePath}`);
  let fixed = 0;

  // 1. 修复 twitter:description（如果被 frontmatter 污染）
  const twitterDesc = doc.querySelector('meta[name="twitter:description"]');
  if (twitterDesc) {
    const content = twitterDesc.getAttribute('content');
    if (content && (content.includes('--- title:') || content.includes('created:') || content.includes('&quot;'))) {
      // 从 meta description 获取正确的值
      const metaDesc = doc.querySelector('meta[name="description"]');
      let newDesc = '';
      if (metaDesc) {
        newDesc = metaDesc.getAttribute('content') || '';
      }
      // 如果 meta description 也是坏的，使用 title
      if (!newDesc || newDesc.includes('--- title:')) {
        const title = doc.querySelector('title');
        newDesc = title ? title.textContent.replace(/ — Baidu PPC Pro.*/, '').replace(/ — Baidu PPC Pro Blog.*/, '') : '';
      }
      twitterDesc.setAttribute('content', newDesc);
      fixed++;
      console.log(`  ✅ Fixed twitter:description`);
    }
  }

  // 2. 修复 meta description（如果被 frontmatter 污染）
  const metaDesc = doc.querySelector('meta[name="description"]');
  if (metaDesc) {
    const content = metaDesc.getAttribute('content');
    if (content && (content.includes('--- title:') || content.includes('created:') || content.length < 20)) {
      // 尝试从文章第一段获取描述
      const articleContent = doc.querySelector('.article-content') || doc.querySelector('.article-body');
      let newDesc = '';
      if (articleContent) {
        const firstP = articleContent.querySelector('p');
        if (firstP) {
          newDesc = firstP.textContent.trim().substring(0, 160);
        }
      }
      // 如果还是空的，使用 title
      if (!newDesc) {
        const title = doc.querySelector('title');
        newDesc = title ? title.textContent.replace(/ — Baidu PPC Pro.*/, '').replace(/ — Baidu PPC Pro Blog.*/, '') : '';
      }
      metaDesc.setAttribute('content', newDesc);
      fixed++;
      console.log(`  ✅ Fixed meta description`);
    }
  }

  // 3. 确保 OG 和 Twitter title 一致
  const ogTitle = doc.querySelector('meta[property="og:title"]');
  const twitterTitle = doc.querySelector('meta[name="twitter:title"]');
  const titleTag = doc.querySelector('title');
  
  if (ogTitle && titleTag) {
    ogTitle.setAttribute('content', titleTag.textContent);
  }
  if (twitterTitle && titleTag) {
    twitterTitle.setAttribute('content', titleTag.textContent);
  }

  if (fixed > 0) {
    const updatedHtml = dom.serialize();
    fs.writeFileSync(fullPath, updatedHtml, 'utf8');
    console.log(`  ✅ Fixed ${fixed} issues in ${filePath}`);
  } else {
    console.log(`  ✓ No issues found in ${filePath}`);
  }
}

console.log('🚀 Starting meta tag fixes...\n');

for (const file of filesToFix) {
  try {
    fixFile(file);
  } catch (error) {
    console.error(`  ❌ Error fixing ${file}:`, error.message);
  }
}

console.log('\n\n✅ Meta tag fixes complete!');
