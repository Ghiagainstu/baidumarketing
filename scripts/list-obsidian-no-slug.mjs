#!/usr/bin/env node
import { readFileSync, readdirSync } from 'fs';
import { join } from 'path';

const VAULT = 'E:/Obsidian/Baidu';
const files = readdirSync(VAULT);

console.log('📝 没 slug 的 Obsidian 文件（应该是昨天新建的 blog）：\n');

let count = 0;
for (const file of files) {
  if (!file.endsWith('.md')) continue;
  
  const content = readFileSync(join(VAULT, file), 'utf8');
  const fmMatch = content.match(/^---\s*\n([\s\S]*?)\n---/);
  
  if (fmMatch) {
    const hasSlug = fmMatch[1].includes('\nslug:');
    if (!hasSlug) {
      // 提取标题
      const titleMatch = fmMatch[1].match(/title:\s*(.+)/);
      const title = titleMatch ? titleMatch[1].trim().replace(/^["']|["']$/g, '') : '(无标题)';
      count++;
      console.log(`${count}. ${file}`);
      console.log(`   标题: ${title.substring(0, 60)}`);
    }
  }
}

console.log(`\n📊 共 ${count} 个文件需要 push`);
