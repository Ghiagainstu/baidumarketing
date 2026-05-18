#!/usr/bin/env node
/**
 * export-slug-mapping.mjs
 * 导出所有 Obsidian 文件的 slug 映射，便于手动审核和修正
 */

import { readFileSync, writeFileSync, readdirSync } from 'fs';
import { join } from 'path';

const OBSIDIAN_VAULT = 'E:/Obsidian/Baidu';

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

// 提取标题
function extractTitle(mdPath) {
  try {
    const content = readFileSync(mdPath, 'utf8');
    const titleMatch = content.match(/^---\s*\ntitle:\s*(.+?)\n/);
    if (titleMatch) {
      return titleMatch[1].trim().replace(/^["']|["']$/g, '');
    }
    const h1Match = content.match(/^#\s+(.+)$/m);
    if (h1Match) {
      return h1Match[1].trim();
    }
    return null;
  } catch(e) {
    return null;
  }
}

// 主函数
function main() {
  console.log('📋 导出 Obsidian 文件的 slug 映射...\n');
  
  const files = readdirSync(OBSIDIAN_VAULT);
  const mappings = [];
  
  for (const file of files) {
    if (!file.endsWith('.md')) continue;
    
    const mdPath = join(OBSIDIAN_VAULT, file);
    const result = readFrontmatter(mdPath);
    if (!result) continue;
    
    const { frontmatter } = result;
    const title = extractTitle(mdPath);
    
    mappings.push({
      filename: file,
      title: title || '(无标题)',
      slug: frontmatter.slug || '(无 slug)',
      status: frontmatter.status || '(未推送)',
      url_en: frontmatter.url_en || '',
      url_jp: frontmatter.url_jp || ''
    });
  }
  
  // 保存为 JSON
  const jsonPath = join('c:/Users/HYE/WorkBuddy/20260411211839', 'scripts', 'slug-mapping.json');
  writeFileSync(jsonPath, JSON.stringify(mappings, null, 2), 'utf8');
  console.log(`✅ 映射已导出到: ${jsonPath}`);
  
  // 也保存为 CSV（便于在 Excel 中编辑）
  let csv = 'filename,title,slug,status,url_en,url_jp\n';
  mappings.forEach(m => {
    const title = (m.title || '').replace(/"/g, '""');
    csv += `"${m.filename}","${title}","${m.slug}","${m.status}","${m.url_en}","${m.url_jp}"\n`;
  });
  const csvPath = join('c:/Users/HYE/WorkBuddy/20260411211839', 'scripts', 'slug-mapping.csv');
  writeFileSync(csvPath, '\uFEFF' + csv, 'utf8');  // 添加 BOM 以便 Excel 正确打开 UTF-8
  console.log(`✅ 映射已导出到: ${csvPath}`);
  
  // 输出统计
  const withSlug = mappings.filter(m => m.slug !== '(无 slug)').length;
  const withoutSlug = mappings.filter(m => m.slug === '(无 slug)').length;
  
  console.log(`\n📊 统计:`);
  console.log(`   有 slug: ${withSlug}`);
  console.log(`   无 slug: ${withoutSlug}`);
  
  // 输出所有有误的 slug（需要手动检查）
  console.log(`\n⚠️  请手动检查以下文件的 slug 是否正确：`);
  mappings.forEach(m => {
    if (m.slug !== '(无 slug)') {
      console.log(`   - ${m.filename}: slug="${m.slug}"`);
      console.log(`     标题: ${m.title.substring(0, 50)}...`);
    }
  });
}

main();
