#!/usr/bin/env node
/**
 * update-obsidian-blog-status-v3.mjs
 * 通过标题匹配 Obsidian 博客和已发布的 HTML 文件，标记发布状态
 * 改进：更健壮的标题提取和匹配
 */

import { readFileSync, writeFileSync, existsSync, readdirSync } from 'fs';
import { join, resolve } from 'path';

const OBSIDIAN_VAULT = 'E:\\Obsidian\\Baidu';
const SITE_ROOT = resolve('.');
const SITE_URL = 'https://baidumarketing.com';

// 从 HTML 文件中提取标题（多种方式）
function extractTitleFromHtml(htmlPath) {
  try {
    const content = readFileSync(htmlPath, 'utf8');

    // 方式1: <title> 标签
    const titleMatch = content.match(/<title>([^<]+)<\/title>/);
    if (titleMatch) {
      return titleMatch[1]
        .replace(/ — Baidu PPC Pro.*$/, '')
        .replace(/ — Baidu PPC Pro Blog$/, '')
        .trim();
    }

    // 方式2: og:title meta 标签
    const ogTitleMatch = content.match(/<meta property=["']og:title["'][^>]*content=["']([^"']+)["']/);
    if (ogTitleMatch) return ogTitleMatch[1].trim();

    // 方式3: <h1 class="article-title">
    const h1Match = content.match(/<h1[^>]*class=["'][^"']*article-title[^"']*["'][^>]*>([^<]+)<\/h1>/);
    if (h1Match) return h1Match[1].trim();

    return null;
  } catch (e) {
    return null;
  }
}

// 标准化标题（用于匹配）
function normalizeTitle(title) {
  if (!title) return '';
  return title
    .toLowerCase()
    .replace(/[''""''""''']/g, "'")
    .replace(/[—–-]+/g, '-')
    .replace(/\s+/g, ' ')
    .trim();
}

// 从 markdown 文件中提取标题
function extractTitleFromMd(mdContent) {
  // 方式1: frontmatter 中的 title
  const fmMatch = mdContent.match(/^---\n([\s\S]*?)\n---/);
  if (fmMatch) {
    const titleMatch = fmMatch[1].match(/^title:\s*"([^"]+)"/m);
    if (titleMatch) return titleMatch[1].trim();
    const titleMatch2 = fmMatch[1].match(/^title:\s*(.+)$/m);
    if (titleMatch2) return titleMatch2[1].trim();
  }

  // 方式2: 第一个 # 标题
  const h1Match = mdContent.match(/^#\s+(.+)$/m);
  if (h1Match) return h1Match[1].trim();

  return null;
}

// 从 markdown frontmatter 中提取字段
function getMdField(content, field) {
  const match = content.match(new RegExp(`^${field}:\\s*(.+)$`, 'm'));
  if (!match) return null;
  return match[1].trim().replace(/^["']|["']$/g, '');
}

// 更新 markdown frontmatter
function updateMdFrontmatter(content, fields) {
  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!fmMatch) {
    // 没有 frontmatter，添加一个
    let newFm = '---\n';
    for (const [key, value] of Object.entries(fields)) {
      newFm += `${key}: ${value}\n`;
    }
    newFm += '---\n\n';
    return newFm + content;
  }

  const frontmatter = fmMatch[1];
  let newFrontmatter = frontmatter;
  let added = false;

  for (const [key, value] of Object.entries(fields)) {
    const regex = new RegExp(`^${key}:.*$`, 'm');
    if (regex.test(frontmatter)) {
      // 已存在，跳过
      continue;
    }
    // 不存在，添加
    newFrontmatter += `\n${key}: ${value}`;
    added = true;
  }

  if (!added) return null; // 无需更新

  return content.replace(/^---\n[\s\S]*?\n---/, `---\n${newFrontmatter.trim()}\n---`);
}

// 主函数
function main() {
  const obsidianPath = resolve(OBSIDIAN_VAULT);
  const blogDir = join(SITE_ROOT, 'blog');
  const jaBlogDir = join(SITE_ROOT, 'ja', 'blog');

  // 获取所有已发布的 HTML 文件（EN 和 JP）
  const enHtmlFiles = readdirSync(blogDir).filter(f => f.endsWith('.html'));
  const jpHtmlFiles = readdirSync(jaBlogDir).filter(f => f.endsWith('.html'));

  console.log(`📊 已发布文章: EN(${enHtmlFiles.length}) + JP(${jpHtmlFiles.length}) = ${enHtmlFiles.length + jpHtmlFiles.length} 篇\n`);

  // 建立标题 → HTML 文件路径的映射
  const titleToEnHtml = {};
  const titleToJpHtml = {};

  for (const file of enHtmlFiles) {
    const htmlPath = join(blogDir, file);
    const title = extractTitleFromHtml(htmlPath);
    if (title) {
      const normalized = normalizeTitle(title);
      titleToEnHtml[normalized] = {
        slug: file.replace('.html', ''),
        path: htmlPath,
        originalTitle: title
      };
    }
  }

  for (const file of jpHtmlFiles) {
    const htmlPath = join(jaBlogDir, file);
    const title = extractTitleFromHtml(htmlPath);
    if (title) {
      const normalized = normalizeTitle(title);
      titleToJpHtml[normalized] = {
        slug: file.replace('.html', ''),
        path: htmlPath,
        originalTitle: title
      };
    }
  }

  console.log(`📝 成功提取标题: EN(${Object.keys(titleToEnHtml).length}) + JP(${Object.keys(titleToJpHtml).length})\n`);

  // 扫描 Obsidian 文件
  const allMdFiles = readdirSync(obsidianPath).filter(f => f.endsWith('.md'));

  const results = {
    updated: [],
    alreadyPublished: [],
    notPublished: [],
    errors: []
  };

  let matchCount = 0;

  for (const file of allMdFiles) {
    const filePath = join(obsidianPath, file);
    const content = readFileSync(filePath, 'utf8');

    const mdTitle = extractTitleFromMd(content);
    const lang = getMdField(content, 'language');
    const existingStatus = getMdField(content, 'status');
    const slug = getMdField(content, 'slug');

    if (!lang || lang === 'ko') continue;
    if (!mdTitle) {
      results.errors.push({ file, reason: '无标题' });
      continue;
    }

    // 尝试匹配
    const normalizedMdTitle = normalizeTitle(mdTitle);
    let matched = false;
    let htmlInfo = null;
    let matchLang = null;

    // 优先使用 slug 匹配
    if (slug) {
      if (lang === 'en' && existsSync(join(blogDir, `${slug}.html`))) {
        matched = true;
        matchLang = 'en';
        htmlInfo = { slug };
      } else if (lang === 'jp' && existsSync(join(jaBlogDir, `${slug}.html`))) {
        matched = true;
        matchLang = 'ja';
        htmlInfo = { slug };
      }
    }

    // 其次使用标题匹配
    if (!matched) {
      if (lang === 'en' && titleToEnHtml[normalizedMdTitle]) {
        matched = true;
        matchLang = 'en';
        htmlInfo = titleToEnHtml[normalizedMdTitle];
      } else if (lang === 'ja' && titleToJpHtml[normalizedMdTitle]) {
        matched = true;
        matchLang = 'ja';
        htmlInfo = titleToJpHtml[normalizedMdTitle];
      }
    }

    if (matched && htmlInfo) {
      matchCount++;
      const today = new Date().toISOString().split('T')[0];
      const fields = {};

      // 添加 slug（如果不存在）
      if (!slug && htmlInfo.slug) {
        fields.slug = htmlInfo.slug;
      }

      // 添加 URL
      if (matchLang === 'en' && !getMdField(content, 'url_en')) {
        fields.url_en = `${SITE_URL}/blog/${htmlInfo.slug}.html`;
      } else if (matchLang === 'ja' && !getMdField(content, 'url_jp')) {
        fields.url_jp = `${SITE_URL}/ja/blog/${htmlInfo.slug}.html`;
      }

      // 添加状态
      if (!existingStatus) {
        fields.status = 'published';
      }

      // 添加 push_date
      if (!getMdField(content, 'push_date')) {
        fields.push_date = today;
      }

      if (Object.keys(fields).length > 0) {
        const updatedContent = updateMdFrontmatter(content, fields);
        if (updatedContent) {
          writeFileSync(filePath, updatedContent, 'utf8');
          results.updated.push({ file, slug: htmlInfo.slug, lang: matchLang, fields });
        } else {
          results.alreadyPublished.push({ file, slug: htmlInfo.slug, lang: matchLang });
        }
      } else {
        results.alreadyPublished.push({ file, slug: htmlInfo.slug, lang: matchLang });
      }
    } else {
      results.notPublished.push({ file, lang, title: mdTitle });
    }
  }

  // 输出结果
  console.log('=== Obsidian 博客状态更新结果 ===\n');
  console.log(`匹配成功: ${matchCount} 篇\n`);

  console.log(`✅ 已更新 (${results.updated.length} 篇):`);
  results.updated.forEach(({ file, slug, lang, fields }) => {
    const url = lang === 'en'
      ? `${SITE_URL}/blog/${slug}.html`
      : `${SITE_URL}/ja/blog/${slug}.html`;
    console.log(`  - ${file}`);
    console.log(`    → ${url}`);
    console.log(`    fields: ${Object.keys(fields).join(', ')}`);
  });

  console.log(`\n😊 已发布（无需更新）(${results.alreadyPublished.length} 篇):`);
  results.alreadyPublished.forEach(({ file, slug, lang }) => {
    console.log(`  - ${file} [${lang}] slug: ${slug}`);
  });

  console.log(`\n⏳ 未发布/未匹配 (${results.notPublished.length} 篇):`);
  results.notPublished.forEach(({ file, lang, title }) => {
    console.log(`  - ${file} [${lang}] "${title?.substring(0, 50)}..."`);
  });

  if (results.errors.length > 0) {
    console.log(`\n⚠️  错误 (${results.errors.length} 篇):`);
    results.errors.forEach(({ file, reason }) => {
      console.log(`  - ${file}: ${reason}`);
    });
  }

  console.log(`\n📊 统计:`);
  console.log(`  已发布: ${results.updated.length + results.alreadyPublished.length}`);
  console.log(`  未发布: ${results.notPublished.length}`);
  console.log(`  本次更新: ${results.updated.length}`);
}

main();
