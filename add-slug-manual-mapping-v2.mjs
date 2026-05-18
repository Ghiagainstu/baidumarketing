#!/usr/bin/env node
/**
 * add-slug-manual-mapping-v2.mjs
 * 根据正确路径和映射，批量添加 slug 到 Obsidian 文件
 */

import { readFileSync, writeFileSync, existsSync, readdirSync } from 'fs';
import { join } from 'path';

const OBSIDIAN_VAULT = 'E:\\Obsidian\\Baidu';
const SITE_ROOT = 'c:/Users/HYE/WorkBuddy/20260411211839';

// 已知映射：Obsidian 文件名 -> { slug, lang }
// 只包含确认了 HTML 文件存在的映射
const KNOWN_MAPPINGS = [
  // 这些已经在之前的处理中更新过了
  // 这里添加的是"未匹配"但 HTML 确实存在的文件
  // 通过检查 HTML 文件是否存在来确认

  // 检查 HTML 是否存在（手动验证过的）
  // bpp-baidu-inactive-keyword-cleanup-2025-*.md -> HTML 存在
  // bpp-baidu-search-ads-1-1-desktop-images-*.md -> HTML 存在
];

// 动态检查：读取 Obsidian 文件，检查是否有 slug，如果没有则添加
function addSlug(content, slug) {
  if (/^slug:\s*.+$/m.test(content)) {
    return null; // 已有 slug
  }

  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!fmMatch) {
    return `---\nslug: ${slug}\n---\n\n${content}`;
  }

  const fmEnd = content.indexOf('---', 4);
  const beforeEnd = content.substring(0, fmEnd);
  const afterEnd = content.substring(fmEnd);

  return beforeEnd + `\nslug: ${slug}` + afterEnd;
}

function main() {
  console.log('=== 添加 slug 到 Obsidian 文件 (v2) ===\n');

  // 读取 Obsidian 目录中的所有 md 文件
  const { readdirSync } = require('fs');
  const allMdFiles = readdirSync(OBSIDIAN_VAULT).filter(f => f.endsWith('.md'));

  const results = {
    added: [],
    alreadyHas: [],
    noSlugField: []
  };

  // 对于每个 Obsidian 文件，检查是否需要添加 slug
  for (const file of allMdFiles) {
    const filePath = join(OBSIDIAN_VAULT, file);
    const content = readFileSync(filePath, 'utf8');

    // 跳过非博客文件（通过检查是否有特定 frontmatter 字段）
    const hasLanguage = /^language:\s*.+$/m.test(content);
    const hasCategory = /^category:\s*.+$/m.test(content);
    if (!hasLanguage && !hasCategory) {
      // 可能不是博客文章，跳过
      continue;
    }

    // 检查是否已有 slug
    if (/^slug:\s*.+$/m.test(content)) {
      results.alreadyHas.push(file);
      continue;
    }

    // 没有 slug，尝试从标题生成
    const titleMatch = content.match(/^title:\s*"([^"]+)"/m);
    if (!titleMatch) continue;

    const title = titleMatch[1];
    // 生成 slug：小写，替换特殊字符为连字符
    const slug = title
      .toLowerCase()
      .replace(/[^\w\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .trim();

    // 检查这个 slug 的 HTML 是否存在
    const enHtmlExists = existsSync(join(SITE_ROOT, 'blog', `${slug}.html`));
    const jpHtmlExists = existsSync(join(SITE_ROOT, 'ja', 'blog', `${slug}.html`));

    if (enHtmlExists || jpHtmlExists) {
      const updated = addSlug(content, slug);
      if (updated) {
        writeFileSync(filePath, updated, 'utf8');
        results.added.push({ file, slug });
      }
    } else {
      results.noSlugField.push({ file, title: title.substring(0, 50) });
    }
  }

  console.log(`✅ 已添加 slug (${results.added.length} 篇):`);
  results.added.forEach(({ file, slug }) => {
    console.log(`  - ${file} → ${slug}`);
  });

  console.log(`\n😊 已有 slug (${results.alreadyHas.length} 篇):`);
  results.alreadyHas.forEach(file => {
    console.log(`  - ${file}`);
  });

  console.log(`\n⚠️  无法匹配 (${results.noSlugField.length} 篇):`);
  results.noSlugField.forEach(({ file, title }) => {
    console.log(`  - ${file}: "${title}..."`);
  });

  console.log(`\n📊 统计:`);
  console.log(`  已添加: ${results.added.length}`);
  console.log(`  已有 slug: ${results.alreadyHas.length}`);
  console.log(`  无法匹配: ${results.noSlugField.length}`);
}

main();
