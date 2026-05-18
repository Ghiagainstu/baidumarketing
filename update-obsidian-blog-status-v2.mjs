#!/usr/bin/env node
/**
 * update-obsidian-blog-status-v2.mjs
 * 通过标题匹配 Obsidian 博客和已发布的 HTML 文件，标记发布状态
 */

import { readFileSync, writeFileSync, existsSync, readdirSync } from 'fs';
import { join, resolve } from 'path';

const OBSIDIAN_VAULT = 'E:\\Obsidian\\Baidu';
const SITE_ROOT = resolve('.');
const SITE_URL = 'https://baidumarketing.com';

// 从 HTML 文件中提取标题
function extractTitleFromHtml(htmlPath) {
  try {
    const content = readFileSync(htmlPath, 'utf8');
    // 尝试从 <title> 标签提取
    const titleMatch = content.match(/<title>([^<]+)<\/title>/);
    if (titleMatch) return titleMatch[1].replace(/ — Baidu PPC Pro.*$/, '').trim();

    // 尝试从 <h1> 提取
    const h1Match = content.match(/<h1[^>]*class="article-title"[^>]*>([^<]+)<\/h1>/);
    if (h1Match) return h1Match[1].trim();

    return null;
  } catch {
    return null;
  }
}

// 从 markdown 文件中提取标题（第一个 # 标题）
function extractTitleFromMd(mdContent) {
  const match = mdContent.match(/^#\s+(.+)$/m);
  if (match) return match[1].trim();

  // 也检查 frontmatter 中的 title
  const fmMatch = mdContent.match(/^---\n([\s\S]*?)\n---/);
  if (fmMatch) {
    const titleMatch = fmMatch[1].match(/^title:\s*"(.+)"$/m);
    if (titleMatch) return titleMatch[1].trim();
  }

  return null;
}

// 从 markdown frontmatter 中提取字段
function getMdField(content, field) {
  const match = content.match(new RegExp(`^${field}:\\s*(.+)$`, 'm'));
  return match ? match[1].trim().replace(/^["']|["']$/g, '') : null;
}

// 添加或更新 frontmatter 字段
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

  for (const [key, value] of Object.entries(fields)) {
    const regex = new RegExp(`^${key}:.*$`, 'm');
    if (regex.test(frontmatter)) {
      // 已存在，跳过
      continue;
    }
    // 不存在，添加
    newFrontmatter += `\n${key}: ${value}`;
  }

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
      titleToEnHtml[title.toLowerCase()] = {
        slug: file.replace('.html', ''),
        path: htmlPath
      };
    }
  }

  for (const file of jpHtmlFiles) {
    const htmlPath = join(jaBlogDir, file);
    const title = extractTitleFromHtml(htmlPath);
    if (title) {
      titleToJpHtml[title.toLowerCase()] = {
        slug: file.replace('.html', ''),
        path: htmlPath
      };
    }
  }

  // 扫描 Obsidian 文件
  const allMdFiles = readdirSync(obsidianPath).filter(f => f.endsWith('.md'));

  const results = {
    updated: [],
    alreadyPublished: [],
    notPublished: [],
    errors: []
  };

  for (const file of allMdFiles) {
    const filePath = join(obsidianPath, file);
    const content = readFileSync(filePath, 'utf8');

    const mdTitle = extractTitleFromMd(content);
    const lang = getMdField(content, 'language');
    const existingStatus = getMdField(content, 'status');

    if (!lang || lang === 'ko') continue;

    // 尝试通过标题匹配
    let matched = false;
    let slug = null;
    let htmlLang = null;

    if (mdTitle) {
      const titleKey = mdTitle.toLowerCase();

      if (lang === 'en' && titleToEnHtml[titleKey]) {
        matched = true;
        slug = titleToEnHtml[titleKey].slug;
        htmlLang = 'en';
      } else if (lang === 'jp' && titleToJpHtml[titleKey]) {
        matched = true;
        slug = titleToJpHtml[titleKey].slug;
        htmlLang = 'ja';
      }
    }

    if (matched && slug) {
      const today = new Date().toISOString().split('T')[0];
      const fields = {};

      // 添加 slug（如果不存在）
      if (!getMdField(content, 'slug')) {
        fields.slug = slug;
      }

      // 添加 URL
      if (htmlLang === 'en' && !getMdField(content, 'url_en')) {
        fields.url_en = `${SITE_URL}/blog/${slug}.html`;
      } else if (htmlLang === 'ja' && !getMdField(content, 'url_jp')) {
        fields.url_jp = `${SITE_URL}/ja/blog/${slug}.html`;
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
        writeFileSync(filePath, updatedContent, 'utf8');
        results.updated.push({ file, slug, lang: htmlLang, fields });
      } else {
        results.alreadyPublished.push({ file, slug, lang: htmlLang });
      }
    } else {
      results.notPublished.push({ file, lang });
    }
  }

  // 输出结果
  console.log('=== Obsidian 博客状态更新结果 ===\n');

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
  results.notPublished.forEach(({ file, lang }) => {
    console.log(`  - ${file} [${lang}]`);
  });

  console.log(`\n📊 统计:`);
  console.log(`  已发布: ${results.updated.length + results.alreadyPublished.length}`);
  console.log(`  未发布: ${results.notPublished.length}`);
  console.log(`  本次更新: ${results.updated.length}`);
}

main();
