#!/usr/bin/env node
/**
 * add-slug-to-obsidian.mjs
 * 通过标题匹配，为 Obsidian 文件添加 slug 字段
 */

import { readFileSync, writeFileSync, readdirSync } from 'fs';
import { join, resolve } from 'path';

const OBSIDIAN_VAULT = 'E:\\Obsidian\\Baidu';
const SITE_ROOT = resolve('.');
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

// 从 markdown 文件中提取标题
function extractTitleFromMd(mdContent) {
  // frontmatter title
  const fmMatch = mdContent.match(/^---\n([\s\S]*?)\n---/);
  if (fmMatch) {
    const titleMatch = fmMatch[1].match(/^title:\s*"([^"]+)"/m);
    if (titleMatch) return titleMatch[1].trim();
    const titleMatch2 = fmMatch[1].match(/^title:\s*(.+)$/m);
    if (titleMatch2) return titleMatch2[1].trim();
  }
  // h1 title
  const h1Match = mdContent.match(/^#\s+(.+)$/m);
  if (h1Match) return h1Match[1].trim();
  return null;
}

// 标准化标题（用于匹配）
function normalizeTitle(title) {
  if (!title) return '';
  return title
    .toLowerCase()
    .replace(/[''""'']/g, "'")
    .replace(/[—–-]+/g, '-')
    .replace(/\s+/g, ' ')
    .trim();
}

// 检查 markdown 是否已有 slug
function hasSlug(content) {
  return /^slug:\s*.+$/m.test(content);
}

// 添加 slug 到 frontmatter
function addSlugToFrontmatter(content, slug) {
  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!fmMatch) {
    // 没有 frontmatter，添加一个
    return `---\nslug: ${slug}\n---\n\n${content}`;
  }

  // 有 frontmatter，在 --- 之前添加 slug
  const frontmatter = fmMatch[1];
  if (/^slug:\s*.+$/m.test(frontmatter)) {
    return null; // 已有 slug，无需添加
  }

  const beforeEnd = content.substring(0, content.indexOf('---', 4));
  const afterEnd = content.substring(content.indexOf('---', 4));

  return beforeEnd + `\nslug: ${slug}` + afterEnd;
}

// 主函数
function main() {
  // 获取所有已发布的 HTML 文件
  const enHtmlFiles = readdirSync(blogDir).filter(f => f.endsWith('.html'));
  const jpHtmlFiles = readdirSync(jaBlogDir).filter(f => f.endsWith('.html'));

  // 建立标题 → {slug, lang} 的映射
  const titleToSlug = {};

  for (const file of enHtmlFiles) {
    const htmlPath = join(blogDir, file);
    const title = extractTitleFromHtml(htmlPath);
    if (title) {
      const normalized = normalizeTitle(title);
      const slug = file.replace('.html', '');
      titleToSlug[normalized] = { slug, lang: 'en', htmlFile: file };
    }
  }

  for (const file of jpHtmlFiles) {
    const htmlPath = join(jaBlogDir, file);
    const title = extractTitleFromHtml(htmlPath);
    if (title) {
      const normalized = normalizeTitle(title);
      const slug = file.replace('.html', '');
      titleToSlug[normalized] = { slug, lang: 'ja', htmlFile: file };
    }
  }

  console.log(`📝 建立映射: ${Object.keys(titleToSlug).length} 个 HTML 标题\n`);

  // 扫描 Obsidian 文件
  const allMdFiles = readdirSync(OBSIDIAN_VAULT).filter(f => f.endsWith('.md'));

  const results = {
    added: [],
    alreadyHas: [],
    notFound: [],
    errors: []
  };

  for (const file of allMdFiles) {
    const filePath = join(OBSIDIAN_VAULT, file);
    const content = readFileSync(filePath, 'utf8');

    // 跳过已有 slug 的文件
    if (hasSlug(content)) {
      results.alreadyHas.push(file);
      continue;
    }

    const mdTitle = extractTitleFromMd(content);
    if (!mdTitle) {
      results.errors.push({ file, reason: '无标题' });
      continue;
    }

    const normalizedMdTitle = normalizeTitle(mdTitle);

    // 尝试匹配
    let matched = false;
    let slugInfo = null;

    // 精确匹配
    if (titleToSlug[normalizedMdTitle]) {
      matched = true;
      slugInfo = titleToSlug[normalizedMdTitle];
    }

    // 模糊匹配（前80个字符）
    if (!matched) {
      for (const [htmlTitle, info] of Object.entries(titleToSlug)) {
        if (htmlTitle.startsWith(normalizedMdTitle.substring(0, 50)) ||
            normalizedMdTitle.startsWith(htmlTitle.substring(0, 50))) {
          matched = true;
          slugInfo = info;
          break;
        }
      }
    }

    if (matched && slugInfo) {
      const updatedContent = addSlugToFrontmatter(content, slugInfo.slug);
      if (updatedContent) {
        writeFileSync(filePath, updatedContent, 'utf8');
        results.added.push({ file, slug: slugInfo.slug, lang: slugInfo.lang });
      } else {
        results.alreadyHas.push(file);
      }
    } else {
      results.notFound.push({ file, title: mdTitle });
    }
  }

  // 输出结果
  console.log('=== 添加 slug 结果 ===\n');

  console.log(`✅ 已添加 slug (${results.added.length} 篇):`);
  results.added.forEach(({ file, slug, lang }) => {
    console.log(`  - ${file} → slug: ${slug} [${lang}]`);
  });

  console.log(`\n😊 已有 slug (${results.alreadyHas.length} 篇):`);
  results.alreadyHas.forEach(file => {
    console.log(`  - ${file}`);
  });

  console.log(`\n⚠️  未找到匹配 (${results.notFound.length} 篇):`);
  results.notFound.forEach(({ file, title }) => {
    console.log(`  - ${file}: "${title?.substring(0, 60)}..."`);
  });

  if (results.errors.length > 0) {
    console.log(`\n⚠️  错误 (${results.errors.length} 篇):`);
    results.errors.forEach(({ file, reason }) => {
      console.log(`  - ${file}: ${reason}`);
    });
  }

  console.log(`\n📊 统计:`);
  console.log(`  已添加: ${results.added.length}`);
  console.log(`  已有 slug: ${results.alreadyHas.length}`);
  console.log(`  未找到: ${results.notFound.length}`);
}

main();
