#!/usr/bin/env node
/**
 * verify-and-fix-slugs.mjs
 * 验证 Obsidian 文件中的 slug 是否正确
 * 如果不正确，则删除错误的 slug（或修正）
 */

import { readFileSync, writeFileSync, readdirSync } from 'fs';
import { join } from 'path';

const OBSIDIAN_VAULT = 'E:/Obsidian/Baidu';
const SITE_ROOT = 'c:/Users/HYE/WorkBuddy/20260411211839';

// 读取 frontmatter
function readFrontmatter(mdPath) {
  try {
    const content = readFileSync(mdPath, 'utf8');
    const fmMatch = content.match(/^---\s*\n([\s\S]*?)\n---/);
    if (fmMatch) {
      const fm = {};
      fmMatch[1].split('\n').forEach(line => {
        const match = line.match(/^(\w+):\s*(.+)$/);
        if (match) {
          fm[match[1]] = match[2].trim().replace(/^["']|["']$/g, '');
        }
      });
      return { frontmatter: fm, raw: fmMatch[0], content: content };
    }
    return { frontmatter: {}, raw: '', content: content };
  } catch(e) {
    return null;
  }
}

// 更新 frontmatter（删除指定的键）
function removeFromFrontmatter(mdPath, keysToRemove) {
  const result = readFrontmatter(mdPath);
  if (!result) return false;
  
  const { frontmatter, raw, content } = result;
  
  // 删除指定的键
  keysToRemove.forEach(key => delete frontmatter[key]);
  
  // 构建新的 frontmatter
  let newRaw = '---\n';
  for (const [key, value] of Object.entries(frontmatter)) {
    newRaw += `${key}: ${value}\n`;
  }
  newRaw += '---\n';
  
  // 写入文件
  const newContent = content.replace(raw, newRaw);
  writeFileSync(mdPath, newContent, 'utf8');
  
  return true;
}

// 从 HTML 文件提取标题
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

// 从 Obsidian 文件提取标题
function extractTitleFromObsidian(mdPath) {
  try {
    const content = readFileSync(mdPath, 'utf8');
    
    // 先尝试从 frontmatter 提取 title
    const titleMatch = content.match(/^---\s*\ntitle:\s*(.+?)\n/);
    if (titleMatch) {
      return titleMatch[1].trim().replace(/^["']|["']$/g, '');
    }
    
    // 再尝试从第一个 h1 提取
    const h1Match = content.match(/^#\s+(.+)$/m);
    if (h1Match) {
      return h1Match[1].trim();
    }
    
    return null;
  } catch(e) {
    return null;
  }
}

// 标准化标题
function normalizeTitle(title) {
  return title
    .toLowerCase()
    .replace(/[^\w\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

// 主函数
function main() {
  console.log('🔍 验证 Obsidian 文件中的 slug...\n');
  
  const files = readdirSync(OBSIDIAN_VAULT);
  let correct = 0;
  let incorrect = 0;
  let fixed = 0;
  
  for (const file of files) {
    if (!file.endsWith('.md')) continue;
    
    const mdPath = join(OBSIDIAN_VAULT, file);
    const result = readFrontmatter(mdPath);
    if (!result) continue;
    
    const { frontmatter } = result;
    
    // 如果没有 slug 字段，跳过
    if (!frontmatter.slug) {
      continue;
    }
    
    const slug = frontmatter.slug;
    const mdTitle = extractTitleFromObsidian(mdPath);
    
    if (!mdTitle) {
      console.log(`⚠️  ${file}: 无法提取标题`);
      continue;
    }
    
    // 检查 EN 版本
    const enHtmlPath = join(SITE_ROOT, 'blog', `${slug}.html`);
    const jpHtmlPath = join(SITE_ROOT, 'ja', 'blog', `${slug}.html`);
    
    let enTitle = null;
    let jpTitle = null;
    
    try { enTitle = extractTitleFromHtml(enHtmlPath); } catch(e) {}
    try { jpTitle = extractTitleFromHtml(jpHtmlPath); } catch(e) {}
    
    const enMatch = enTitle && normalizeTitle(enTitle) === normalizeTitle(mdTitle);
    const jpMatch = jpTitle && normalizeTitle(jpTitle) === normalizeTitle(mdTitle);
    
    if (enMatch || jpMatch) {
      correct++;
      console.log(`✅ ${file}: slug="${slug}" 正确`);
    } else {
      incorrect++;
      console.log(`❌ ${file}: slug="${slug}" 错误`);
      console.log(`   MD 标题: ${mdTitle}`);
      if (enTitle) console.log(`   EN HTML 标题: ${enTitle}`);
      if (jpTitle) console.log(`   JP HTML 标题: ${jpTitle}`);
      
      // 询问是否删除错误的 slug
      // 这里自动删除（也可以改为交互式）
      const success = removeFromFrontmatter(mdPath, ['slug', 'url_en', 'url_jp', 'status', 'push_date']);
      if (success) {
        console.log(`   🔧 已删除错误的 slug 和相关字段`);
        fixed++;
      }
    }
  }
  
  console.log(`\n📊 验证完成:`);
  console.log(`   正确: ${correct}`);
  console.log(`   错误: ${incorrect}`);
  console.log(`   已修复: ${fixed}`);
}

main();
