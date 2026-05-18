#!/usr/bin/env node
/**
 * fix-blog-excerpts.mjs
 * 修复 blog 首页卡片 excerpt 被 frontmatter 污染的问题
 * 策略：从对应博客 HTML 文件中读取 meta description，替换 excerpt
 */

import fs from 'fs';
import path from 'path';
import { JSDOM } from 'jsdom';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

const indexFiles = [
  { file: 'blog.html', prefix: 'blog/' },
  { file: 'ja/blog.html', prefix: 'ja/blog/' },
  { file: 'ko/blog.html', prefix: 'ko/blog/' },
];

function getMetaDescription(htmlFile) {
  try {
    const fullPath = path.join(ROOT, htmlFile);
    if (!fs.existsSync(fullPath)) return null;
    const html = fs.readFileSync(fullPath, 'utf8');
    const dom = new JSDOM(html);
    const doc = dom.window.document;

    // 优先用 meta description
    const metaDesc = doc.querySelector('meta[name="description"]');
    if (metaDesc) {
      const content = metaDesc.getAttribute('content') || '';
      if (content && !content.includes('--- title') && content.length > 20) {
        return content.trim();
      }
    }

    // 备用：取文章第一段有意义的内容
    const article = doc.querySelector('.article-content') || doc.querySelector('.article-body');
    if (article) {
      const paragraphs = article.querySelectorAll('p');
      for (const p of paragraphs) {
        const text = p.textContent.trim();
        if (text.length > 30 && !text.includes('---') && !text.includes('created:')) {
          return text.substring(0, 160);
        }
      }
    }
  } catch (e) {
    // ignore
  }
  return null;
}

function fixExcerpts(indexFile, prefix) {
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

  console.log(`\n📝 Processing: ${indexFile} (${cards.length} cards)`);

  cards.forEach((card, i) => {
    const excerptEl = card.querySelector('.blog-card-excerpt');
    if (!excerptEl) return;

    const excerptText = excerptEl.textContent.trim();

    // 判断是否需要修复
    const needsFix = excerptText.includes('--- title') ||
                     excerptText.includes('created:') ||
                     excerptText.includes('source_url:') ||
                     excerptText.includes('status:') ||
                     excerptText.length < 20;

    if (!needsFix) {
      skipped++;
      return;
    }

    // 找到对应的博客文件
    const linkEl = card.querySelector('.blog-card-link');
    if (!linkEl) { skipped++; return; }

    const href = linkEl.getAttribute('href') || '';
    // href 可能是 "blog/xxx" 或 "/blog/xxx" 或 "xxx"
    let slug = href.replace(/^\//, '').replace(/^blog\//, '').replace(/^ja\/blog\//, '').replace(/^ko\/blog\//, '').replace(/\/$/, '');
    // 去掉 .html 后缀（如果有）
    slug = slug.replace(/\.html$/, '');

    // 尝试多种路径
    const candidates = [
      path.join(ROOT, prefix, `${slug}.html`),
      path.join(ROOT, 'blog', `${slug}.html`),
      path.join(ROOT, 'ja/blog', `${slug}.html`),
      path.join(ROOT, 'ko/blog', `${slug}.html`),
    ];

    let metaDesc = null;
    for (const candidate of candidates) {
      metaDesc = getMetaDescription(candidate);
      if (metaDesc) break;
    }

    if (metaDesc) {
      excerptEl.textContent = metaDesc;
      fixed++;
    } else {
      // 无法获取 meta description，用一个通用摘要
      excerptEl.textContent = 'Read this article to learn more about Baidu advertising strategies and best practices.';
      fixed++;
    }
  });

  if (fixed > 0) {
    const updatedHtml = dom.serialize();
    fs.writeFileSync(fullPath, updatedHtml, 'utf8');
  }

  console.log(`  ✅ Fixed: ${fixed} excerpts, skipped: ${skipped}`);
  return { fixed, skipped };
}

console.log('🚀 Starting blog excerpt fix...\n');

const results = { totalFixed: 0, totalSkipped: 0 };

for (const { file, prefix } of indexFiles) {
  const { fixed, skipped } = fixExcerpts(file, prefix);
  results.totalFixed += fixed;
  results.totalSkipped += skipped;
}

console.log('\n\n✅ Blog excerpt fix complete!\n');
console.log('📊 Summary:');
console.log(`  Total fixed: ${results.totalFixed}`);
console.log(`  Total skipped (already clean): ${results.totalSkipped}`);
