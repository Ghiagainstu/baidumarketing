#!/usr/bin/env node
/**
 * verify-published-html.mjs
 * 简化版：只验证 HTML 文件是否存在且有效
 * 不依赖 Obsidian 文件匹配
 */

import { readFileSync, existsSync, readdirSync, statSync } from 'fs';
import { join, resolve } from 'path';

const SITE_ROOT = resolve('.');
const SITE_URL = 'https://baidumarketing.com';
const blogDir = join(SITE_ROOT, 'blog');
const jaBlogDir = join(SITE_ROOT, 'ja', 'blog');

// 从 HTML 文件中提取标题
function extractTitleFromHtml(htmlPath) {
  try {
    const content = readFileSync(htmlPath, 'utf8');
    const titleMatch = content.match(/<title>([^<]+)<\/title>/);
    if (titleMatch) {
      return titleMatch[1]
        .replace(/ — Baidu PPC Pro.*$/, '')
        .replace(/ — Baidu PPC Pro Blog$/, '')
        .trim();
    }
    return null;
  } catch(e) {
    return null;
  }
}

function main() {
  console.log('=== 验证已发布博客（简化版）===\n');

  const enHtmlFiles = readdirSync(blogDir).filter(f => f.endsWith('.html'));
  const jpHtmlFiles = readdirSync(jaBlogDir).filter(f => f.endsWith('.html'));

  console.log(`📊 已发布文章: EN(${enHtmlFiles.length}) + JP(${jpHtmlFiles.length}) = ${enHtmlFiles.length + jpHtmlFiles.length} 篇\n`);

  const results = {
    valid: [],
    empty: [],
    noTitle: [],
    errors: []
  };

  // 验证 EN 博客
  console.log('--- EN 博客验证 ---\n');
  for (const file of enHtmlFiles) {
    const htmlPath = join(blogDir, file);
    const slug = file.replace('.html', '');
    const url = `${SITE_URL}/blog/${slug}.html`;

    try {
      const stats = statSync(htmlPath);
      if (stats.size < 1000) {
        results.empty.push({ file, lang: 'en', size: stats.size });
        continue;
      }

      const title = extractTitleFromHtml(htmlPath);
      if (!title) {
        results.noTitle.push({ file, lang: 'en' });
        continue;
      }

      results.valid.push({ file, slug, url, title });
    } catch (err) {
      results.errors.push({ file, lang: 'en', error: err.message });
    }
  }

  // 验证 JP 博客
  console.log('--- JP 博客验证 ---\n');
  for (const file of jpHtmlFiles) {
    const htmlPath = join(jaBlogDir, file);
    const slug = file.replace('.html', '');
    const url = `${SITE_URL}/ja/blog/${slug}.html`;

    try {
      const stats = statSync(htmlPath);
      if (stats.size < 1000) {
        results.empty.push({ file, lang: 'ja', size: stats.size });
        continue;
      }

      const title = extractTitleFromHtml(htmlPath);
      if (!title) {
        results.noTitle.push({ file, lang: 'ja' });
        continue;
      }

      results.valid.push({ file, slug, url, title });
    } catch (err) {
      results.errors.push({ file, lang: 'ja', error: err.message });
    }
  }

  // 输出结果
  console.log('\n=== 验证结果 ===\n');

  console.log(`✅ 有效 (${results.valid.length} 篇):`);
  results.valid.forEach(({ file, url, title }) => {
    console.log(`  - ${file}`);
    console.log(`    Title: ${title?.substring(0, 60)}...`);
    console.log(`    URL: ${url}`);
  });

  console.log(`\n⚠️  HTML 内容异常 (${results.empty.length} 篇):`);
  results.empty.forEach(({ file, lang, size }) => {
    console.log(`  - ${file} [${lang}] size: ${size} bytes`);
  });

  console.log(`\n⚠️  无标题 (${results.noTitle.length} 篇):`);
  results.noTitle.forEach(({ file, lang }) => {
    console.log(`  - ${file} [${lang}]`);
  });

  if (results.errors.length > 0) {
    console.log(`\n❌ 错误 (${results.errors.length} 篇):`);
    results.errors.forEach(({ file, lang, error }) => {
      console.log(`  - ${file} [${lang}]: ${error}`);
    });
  }

  console.log(`\n📊 统计:`);
  console.log(`  有效: ${results.valid.length}`);
  console.log(`  HTML 异常: ${results.empty.length}`);
  console.log(`  无标题: ${results.noTitle.length}`);
  console.log(`  错误: ${results.errors.length}`);
  console.log(`  总计: ${enHtmlFiles.length + jpHtmlFiles.length}`);
}

main();
