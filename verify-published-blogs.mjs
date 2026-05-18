#!/usr/bin/env node
/**
 * verify-published-blogs.mjs
 * 核对所有已发布博客的状态
 * 1. 检查 HTML 文件是否存在且有内容
 * 2. 检查 Obsidian 文件是否已正确标记
 */

import { readFileSync, existsSync, readdirSync, statSync } from 'fs';
import { join, resolve } from 'path';

const OBSIDIAN_VAULT = 'E:\\Obsidian\\Baidu';
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
        .trim();
    }
    return null;
  } catch(e) {
    return null;
  }
}

// 从 markdown frontmatter 中提取字段
function getMdField(content, field) {
  const match = content.match(new RegExp(`^${field}:\\s*(.+)$`, 'm'));
  if (!match) return null;
  return match[1].trim().replace(/^["']|["']$/g, '');
}

// 主函数：验证已发布的博客
function verifyPublishedBlogs() {
  console.log('=== 核对已发布博客 ===\n');

  const enHtmlFiles = readdirSync(blogDir).filter(f => f.endsWith('.html'));
  const jpHtmlFiles = readdirSync(jaBlogDir).filter(f => f.endsWith('.html'));

  console.log(`📊 已发布文章: EN(${enHtmlFiles.length}) + JP(${jpHtmlFiles.length}) = ${enHtmlFiles.length + jpHtmlFiles.length} 篇\n`);

  const results = {
    verified: [],
    obsidianMissing: [],
    obsidianNotMarked: [],
    htmlEmpty: [],
    errors: []
  };

  // 验证 EN 博客
  console.log('--- EN 博客核对 ---\n');
  for (const file of enHtmlFiles) {
    const htmlPath = join(blogDir, file);
    const slug = file.replace('.html', '');
    const url = `${SITE_URL}/blog/${slug}.html`;

    // 检查 HTML 文件是否有内容
    const stats = statSync(htmlPath);
    if (stats.size < 1000) {
      results.htmlEmpty.push({ file, lang: 'en', size: stats.size });
      continue;
    }

    // 提取标题
    const title = extractTitleFromHtml(htmlPath);

    // 查找对应的 Obsidian 文件
    const obsidianFiles = readdirSync(OBSIDIAN_VAULT).filter(f =>
      f.endsWith('.md') &&
      readFileSync(join(OBSIDIAN_VAULT, f), 'utf8').includes(`slug: ${slug}`)
    );

    if (obsidianFiles.length === 0) {
      results.obsidianMissing.push({ file, slug, url, title });
    } else {
      // 检查 Obsidian 文件是否已标记
      const obsidianPath = join(OBSIDIAN_VAULT, obsidianFiles[0]);
      const content = readFileSync(obsidianPath, 'utf8');
      const status = getMdField(content, 'status');
      const urlEn = getMdField(content, 'url_en');

      if (status === 'published' && urlEn) {
        results.verified.push({ file: obsidianFiles[0], slug, url, title });
      } else {
        results.obsidianNotMarked.push({ file: obsidianFiles[0], slug, status, urlEn });
      }
    }
  }

  // 验证 JP 博客
  console.log('--- JP 博客核对 ---\n');
  for (const file of jpHtmlFiles) {
    const htmlPath = join(jaBlogDir, file);
    const slug = file.replace('.html', '');
    const url = `${SITE_URL}/ja/blog/${slug}.html`;

    // 检查 HTML 文件是否有内容
    const stats = statSync(htmlPath);
    if (stats.size < 1000) {
      results.htmlEmpty.push({ file, lang: 'ja', size: stats.size });
      continue;
    }

    // 提取标题
    const title = extractTitleFromHtml(htmlPath);

    // 查找对应的 Obsidian 文件
    const obsidianFiles = readdirSync(OBSIDIAN_VAULT).filter(f =>
      f.endsWith('.md') &&
      readFileSync(join(OBSIDIAN_VAULT, f), 'utf8').includes(`slug: ${slug}`)
    );

    if (obsidianFiles.length === 0) {
      results.obsidianMissing.push({ file, slug, url, title });
    } else {
      // 检查 Obsidian 文件是否已标记
      const obsidianPath = join(OBSIDIAN_VAULT, obsidianFiles[0]);
      const content = readFileSync(obsidianPath, 'utf8');
      const status = getMdField(content, 'status');
      const urlJp = getMdField(content, 'url_jp');

      if (status === 'published' && urlJp) {
        results.verified.push({ file: obsidianFiles[0], slug, url, title });
      } else {
        results.obsidianNotMarked.push({ file: obsidianFiles[0], slug, status, urlJp });
      }
    }
  }

  // 输出结果
  console.log('\n=== 核对结果 ===\n');

  console.log(`✅ 已验证 (${results.verified.length} 篇):`);
  results.verified.forEach(({ file, url }) => {
    console.log(`  - ${file}`);
    console.log(`    ${url}`);
  });

  console.log(`\n⚠️  Obsidian 文件未标记 (${results.obsidianNotMarked.length} 篇):`);
  results.obsidianNotMarked.forEach(({ file, slug, status, urlEn, urlJp }) => {
    console.log(`  - ${file}`);
    console.log(`    slug: ${slug}`);
    console.log(`    status: ${status || '(none)'}`);
    console.log(`    url_en: ${urlEn || '(none)'}`);
    console.log(`    url_jp: ${urlJp || '(none)'}`);
  });

  console.log(`\n❓ Obsidian 文件缺失 (${results.obsidianMissing.length} 篇):`);
  results.obsidianMissing.forEach(({ file, slug, url }) => {
    console.log(`  - HTML: ${file}`);
    console.log(`    slug: ${slug}`);
    console.log(`    URL: ${url}`);
  });

  console.log(`\n⚠️  HTML 文件内容异常 (${results.htmlEmpty.length} 篇):`);
  results.htmlEmpty.forEach(({ file, lang, size }) => {
    console.log(`  - ${file} [${lang}] size: ${size} bytes`);
  });

  console.log(`\n📊 统计:`);
  console.log(`  已验证: ${results.verified.length}`);
  console.log(`  Obsidian 未标记: ${results.obsidianNotMarked.length}`);
  console.log(`  Obsidian 缺失: ${results.obsidianMissing.length}`);
  console.log(`  HTML 异常: ${results.htmlEmpty.length}`);
}

verifyPublishedBlogs();
