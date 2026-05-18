#!/usr/bin/env node
/**
 * update-obsidian-blog-status.mjs
 * 扫描 Obsidian 博客，标记已发布的博客（添加 URL 和 push 状态）
 */

import { readFileSync, writeFileSync, existsSync, readdirSync } from 'fs';
import { join, resolve } from 'path';

const OBSIDIAN_VAULT = 'E:\\Obsidian\\Baidu';
const SITE_ROOT = resolve('.');
const SITE_URL = 'https://baidumarketing.com';

// 从 markdown frontmatter 中提取 slug
function extractSlug(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;

  const frontmatter = match[1];
  const slugMatch = frontmatter.match(/^slug:\s*(.+)$/m);
  if (!slugMatch) return null;

  return slugMatch[1].trim();
}

// 从 markdown frontmatter 中提取 language
function extractLanguage(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return null;

  const frontmatter = match[1];
  const langMatch = frontmatter.match(/^language:\s*(.+)$/m);
  if (!langMatch) return null;

  return langMatch[1].trim();
}

// 检查是否已发布（HTML 文件存在）
function isPublished(slug, lang) {
  if (lang === 'en') {
    return existsSync(join(SITE_ROOT, 'blog', `${slug}.html`));
  } else if (lang === 'jp') {
    return existsSync(join(SITE_ROOT, 'ja', 'blog', `${slug}.html`));
  }
  return false;
}

// 读取已有的 frontmatter 字段
function getExistingField(content, field) {
  const match = content.match(new RegExp(`^${field}:\\s*(.+)$`, 'm'));
  return match ? match[1].trim() : null;
}

// 更新 frontmatter（添加 URL 和 push 状态）
function updateFrontmatter(content, slug, lang) {
  const existingStatus = getExistingField(content, 'status');

  // 如果已经标记为 published，跳过
  if (existingStatus === 'published') {
    return null; // 已处理过
  }

  const today = new Date().toISOString().split('T')[0];
  let newFields = '';

  if (lang === 'en') {
    const existingUrlEn = getExistingField(content, 'url_en');
    if (!existingUrlEn) {
      newFields += `\nurl_en: ${SITE_URL}/blog/${slug}.html`;
    }
  } else if (lang === 'jp') {
    const existingUrlJp = getExistingField(content, 'url_jp');
    if (!existingUrlJp) {
      newFields += `\nurl_jp: ${SITE_URL}/ja/blog/${slug}.html`;
    }
  }

  const existingPushDate = getExistingField(content, 'push_date');
  if (!existingPushDate) {
    newFields += `\npush_date: ${today}`;
  }

  // 添加 status: published
  if (!existingStatus) {
    newFields += `\nstatus: published`;
  }

  if (!newFields.trim()) {
    return null; // 无需更新
  }

  // 在 --- 之前或第一个 --- 之后插入新字段
  const frontmatterEnd = content.indexOf('---', 4);
  const beforeEnd = content.substring(0, frontmatterEnd);
  const afterEnd = content.substring(frontmatterEnd);

  return beforeEnd + newFields + '\n' + afterEnd;
}

// 主函数
function main() {
  const obsidianPath = resolve(OBSIDIAN_VAULT);

  const results = {
    updated: [],
    alreadyPublished: [],
    notPublished: [],
    errors: []
  };

  try {
    const allFiles = readdirSync(obsidianPath).filter(f => f.endsWith('.md'));

    for (const file of allFiles) {
      const filePath = join(obsidianPath, file);
      const content = readFileSync(filePath, 'utf8');

      const slug = extractSlug(content);
      const lang = extractLanguage(content);

      if (!slug || !lang) continue;
      if (lang === 'ko') continue; // KO 尚未发布

      const published = isPublished(slug, lang);

      if (published) {
        const updatedContent = updateFrontmatter(content, slug, lang);

        if (updatedContent === null) {
          results.alreadyPublished.push({ file, slug, lang });
        } else {
          writeFileSync(filePath, updatedContent, 'utf8');
          results.updated.push({ file, slug, lang });
        }
      } else {
        results.notPublished.push({ file, slug, lang });
      }
    }

    // 输出结果
    console.log('=== Obsidian 博客状态更新结果 ===\n');

    console.log(`✅ 已更新 (${results.updated.length} 篇):`);
    results.updated.forEach(({ file, slug, lang }) => {
      const url = lang === 'en'
        ? `${SITE_URL}/blog/${slug}.html`
        : `${SITE_URL}/ja/blog/${slug}.html`;
      console.log(`  - ${file} → ${url}`);
    });

    console.log(`\n😊 已发布（无需更新）(${results.alreadyPublished.length} 篇):`);
    results.alreadyPublished.forEach(({ file, slug, lang }) => {
      console.log(`  - ${file} [${lang}]`);
    });

    console.log(`\n�等待着发布 (${results.notPublished.length} 篇):`);
    results.notPublished.forEach(({ file, slug, lang }) => {
      console.log(`  - ${file} [${lang}] slug: ${slug}`);
    });

    console.log(`\n📊 统计:`);
    console.log(`  已发布: ${results.updated.length + results.alreadyPublished.length}`);
    console.log(`  未发布: ${results.notPublished.length}`);
    console.log(`  本次更新: ${results.updated.length}`);

  } catch (err) {
    console.error('错误:', err.message);
    process.exit(1);
  }
}

main();
