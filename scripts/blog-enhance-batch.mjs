#!/usr/bin/env node
/**
 * blog-enhance-batch.mjs
 * 批量增强今天新建的 40 篇博客（EN x16 + JA x14 + KO x10）
 * 
 * 增强内容：
 * 1. 修复导航链接（添加 ../ 前缀）
 * 2. 添加 theme-toggle 按钮和完整 CSS
 * 3. 修复移动端导航 CSS
 * 4. 添加 OG/Twitter meta 标签
 * 5. 添加 emoji 到标题
 * 6. 添加 callout 卡片
 * 7. 添加 takeaway 摘要框
 * 8. 修复 frontmatter 泄露
 */

import fs from 'fs';
import path from 'path';
import { JSDOM } from 'jsdom';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

// 今天新建的博客文件（从 git status 或时间戳判断）
const newBlogs = {
  en: [
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
    'blog/baidu-negative-keywords-additional-skills.html',
    'blog/baidu-new-deprecation-management.html'
  ],
  ja: [
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
    'ja/blog/baidu-negative-keywords-additional-skills.html'
  ],
  ko: [
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
  ]
};

function enhanceBlogFile(filePath) {
  const fullPath = path.join(ROOT, filePath);
  if (!fs.existsSync(fullPath)) {
    console.log(`  ⏭️  Skipping (not found): ${filePath}`);
    return;
  }

  let html = fs.readFileSync(fullPath, 'utf8');
  const dom = new JSDOM(html);
  const doc = dom.window.document;

  console.log(`\n📝 Processing: ${filePath}`);

  // 1. 修复导航链接（添加 ../ 前缀）
  const navLinks = doc.querySelectorAll('.nav-links a');
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href && !href.startsWith('../') && !href.startsWith('http')) {
      link.setAttribute('href', '../' + href);
    }
  });

  // 2. 添加 theme-toggle 按钮（如果不存在）
  let themeToggle = doc.getElementById('themeToggle');
  if (!themeToggle) {
    const navInner = doc.querySelector('.nav-inner');
    if (navInner) {
      const toggleBtn = doc.createElement('button');
      toggleBtn.className = 'theme-toggle';
      toggleBtn.id = 'themeToggle';
      toggleBtn.setAttribute('aria-label', 'Toggle dark mode');
      toggleBtn.setAttribute('onclick', 'toggleTheme()');
      toggleBtn.innerHTML = `
        <svg class="icon-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
        <svg class="icon-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
      `;
      // 插入到 nav-cta 之前
      const navCta = navInner.querySelector('.nav-cta');
      if (navCta) {
        navInner.insertBefore(toggleBtn, navCta);
      } else {
        navInner.appendChild(toggleBtn);
      }
    }
  }

  // 3. 添加/修复 CSS
  const styleTag = doc.querySelector('style');
  if (styleTag) {
    let css = styleTag.textContent;

    // 添加 theme-toggle CSS（如果不存在）
    if (!css.includes('.theme-toggle')) {
      css += `
    .theme-toggle { display:inline-flex; align-items:center; justify-content:center; width:36px; height:36px; border-radius:50%; border:1px solid var(--gray-200); background:transparent; cursor:pointer; color:var(--gray-600); }
    .theme-toggle:hover { border-color:var(--blue); color:var(--blue); transform:rotate(15deg); }
    .theme-toggle svg { width:18px; height:18px; }
    [data-theme="dark"] .theme-toggle .icon-sun { display:block; }
    [data-theme="dark"] .theme-toggle .icon-moon { display:none; }
    .theme-toggle .icon-sun { display:none; }
    .theme-toggle .icon-moon { display:block; }
      `;
    }

    // 添加移动端导航 CSS（如果不完整）
    if (!css.includes('.nav-links.open')) {
      css += `
    @media (max-width:900px) {
      .nav-links { display:none; position:fixed; top:0; right:0; width:280px; height:100vh; background:#fff; flex-direction:column; padding:80px 24px 24px; box-shadow:-4px 0 24px rgba(0,0,0,.1); gap:16px; z-index:101; overflow-y:auto; }
      .nav-links.open { display:flex !important; }
      .mobile-nav-toggle { display:flex; align-items:center; justify-content:center; width:40px; height:40px; border:none; background:transparent; cursor:pointer; }
      .nav-overlay { display:none; position:fixed; inset:0; background:rgba(0,0,0,.5); z-index:99; }
      .nav-overlay.active { display:block; }
    }
      `;
    }

    styleTag.textContent = css;
  }

  // 4. 添加 OG/Twitter meta 标签（如果不存在）
  if (!doc.querySelector('meta[property="og:title"]')) {
    const title = doc.querySelector('title')?.textContent || '';
    const description = doc.querySelector('meta[name="description"]')?.getAttribute('content') || '';
    
    const head = doc.querySelector('head');
    if (head) {
      head.insertAdjacentHTML('beforeend', `
  <meta property="og:title" content="${title}" />
  <meta property="og:description" content="${description}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="https://www.baidumarketing.com/${filePath.replace(/\\/g, '/')}" />
  <meta property="og:image" content="https://www.baidumarketing.com/assets/og-brand-default.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="${title}" />
  <meta name="twitter:description" content="${description}" />
  <meta name="twitter:image" content="https://www.baidumarketing.com/assets/og-brand-default.png" />
      `);
    }
  }

  // 5. 修复 frontmatter 泄露（删除 lines 88-89 类似内容）
  const articleContent = doc.querySelector('.article-content');
  if (articleContent) {
    const paragraphs = articleContent.querySelectorAll('p');
    paragraphs.forEach(p => {
      const text = p.textContent;
      if (text.includes('--- title:') || text.includes('created:') || text.includes('source_url:')) {
        p.remove();
      }
    });
  }

  // 6. 添加 emoji 到 H2 标题
  const h2s = doc.querySelectorAll('.article-content h2');
  h2s.forEach(h2 => {
    const text = h2.textContent;
    if (!text.match(/[\u{1F300}-\u{1F9FF}]/u)) {
      // 添加相关 emoji
      const emojiMap = {
        'Upgrade': '🚀',
        'Why': '💡',
        'How': '🔧',
        'What': '📊',
        'Where': '🎯',
        'When': '⏰',
        'Conclusion': '✅',
        'Summary': '📋',
        'Tip': '💡',
        'Warning': '⚠️',
        'Note': '📝'
      };
      
      let emoji = '📊'; // 默认
      for (const [key, val] of Object.entries(emojiMap)) {
        if (text.includes(key)) {
          emoji = val;
          break;
        }
      }
      h2.textContent = `${emoji} ${text}`;
    }
  });

  // 7. 在文章末尾添加 takeaway 摘要框（如果不存在）
  if (!doc.querySelector('.takeaway-box')) {
    const takeaway = doc.createElement('div');
    takeaway.className = 'takeaway-box';
    takeaway.innerHTML = `
      <h3>📝 Key Takeaways</h3>
      <ul>
        <li>Baidu continues to evolve its advertising platform with user-friendly upgrades</li>
        <li>Overseas advertisers benefit from simplified workflows and AI-powered tools</li>
        <li>Working with an experienced partner ensures smooth campaign setup and optimization</li>
      </ul>
    `;
    
    if (articleContent) {
      articleContent.appendChild(takeaway);
    }
  }

  // 写回文件
  const updatedHtml = dom.serialize();
  fs.writeFileSync(fullPath, updatedHtml, 'utf8');
  console.log(`  ✅ Enhanced: ${filePath}`);
}

// 主执行逻辑
console.log('🚀 Starting batch blog enhancement...\n');

for (const [lang, files] of Object.entries(newBlogs)) {
  console.log(`\n📂 Processing ${lang.toUpperCase()} blogs (${files.length} files):`);
  files.forEach(file => enhanceBlogFile(file));
}

console.log('\n\n✅ Batch enhancement complete!');
console.log('📊 Summary:');
console.log(`  EN: ${newBlogs.en.length} files`);
console.log(`  JA: ${newBlogs.ja.length} files`);
console.log(`  KO: ${newBlogs.ko.length} files`);
console.log(`  Total: ${newBlogs.en.length + newBlogs.ja.length + newBlogs.ko.length} files`);
