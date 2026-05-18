#!/usr/bin/env node
/**
 * smart-match-obsidian.mjs
 * 智能匹配：slug 匹配后验证标题，标题不匹配则拒绝
 */

import { readFileSync, writeFileSync, readdirSync } from 'fs';
import { join } from 'path';

const OBSIDIAN_VAULT = 'E:/Obsidian/Baidu';
const SITE_ROOT = 'c:/Users/HYE/WorkBuddy/20260411211839';
const TODAY = new Date().toISOString().split('T')[0];

// 提取 HTML 标题
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

// 计算标题相似度（token 重叠度）
function titleSimilarity(title1, title2) {
  const t1 = normalizeTitle(title1);
  const t2 = normalizeTitle(title2);
  
  // 精确匹配
  if (t1 === t2) return 1.0;
  
  const words1 = new Set(t1.split(' ').filter(w => w.length > 2));
  const words2 = new Set(t2.split(' ').filter(w => w.length > 2));
  
  if (words1.size === 0 || words2.size === 0) return 0;
  
  const intersection = new Set([...words1].filter(x => words2.has(x)));
  const overlap = intersection.size / Math.max(words1.size, words2.size);
  
  return overlap;
}

// 读取 Obsidian 文件的 frontmatter
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

// 更新 Obsidian 文件的 frontmatter
function updateFrontmatter(mdPath, updates) {
  const result = readFrontmatter(mdPath);
  if (!result) return false;
  
  const { frontmatter, raw, content } = result;
  
  // 合并更新
  const newFm = { ...frontmatter, ...updates };
  
  // 构建新的 frontmatter
  let newRaw = '---\n';
  for (const [key, value] of Object.entries(newFm)) {
    newRaw += `${key}: ${value}\n`;
  }
  newRaw += '---\n';
  
  // 写入文件
  const newContent = raw ? content.replace(raw, newRaw) : newRaw + content;
  writeFileSync(mdPath, newContent, 'utf8');
  
  return true;
}

// 获取所有 HTML 文件
function getHtmlFiles() {
  const htmlFiles = [];
  
  // EN blogs
  const enDir = join(SITE_ROOT, 'blog');
  try {
    readdirSync(enDir).forEach(file => {
      if (file.endsWith('.html') && file !== 'index.html') {
        const slug = file.replace('.html', '');
        const title = extractTitleFromHtml(join(enDir, file));
        if (title) {
          htmlFiles.push({
            slug,
            title,
            normalizedTitle: normalizeTitle(title),
            path: join(enDir, file),
            lang: 'en'
          });
        }
      }
    });
  } catch(e) {}
  
  // JP blogs
  const jpDir = join(SITE_ROOT, 'ja', 'blog');
  try {
    readdirSync(jpDir).forEach(file => {
      if (file.endsWith('.html') && file !== 'index.html') {
        const slug = file.replace('.html', '');
        const title = extractTitleFromHtml(join(jpDir, file));
        if (title) {
          htmlFiles.push({
            slug,
            title,
            normalizedTitle: normalizeTitle(title),
            path: join(jpDir, file),
            lang: 'jp'
          });
        }
      }
    });
  } catch(e) {}
  
  return htmlFiles;
}

// 获取所有 Obsidian 文件
function getObsidianFiles() {
  const mdFiles = [];
  
  try {
    readdirSync(OBSIDIAN_VAULT).forEach(file => {
      if (file.endsWith('.md')) {
        const mdPath = join(OBSIDIAN_VAULT, file);
        const title = extractTitleFromObsidian(mdPath);
        if (title) {
          mdFiles.push({
            title,
            normalizedTitle: normalizeTitle(title),
            path: mdPath,
            filename: file
          });
        }
      }
    });
  } catch(e) {}
  
  return mdFiles;
}

// 主匹配逻辑（增强验证）
function matchFiles() {
  console.log('🔍 开始智能匹配 HTML 和 Obsidian 文件...\n');
  
  const htmlFiles = getHtmlFiles();
  const mdFiles = getObsidianFiles();
  
  console.log(`📄 找到 ${htmlFiles.length} 个 HTML 文件`);
  console.log(`📝 找到 ${mdFiles.length} 个 Obsidian 文件\n`);
  
  const matches = [];
  const uncertain = [];
  const unmatched = [];
  const matchedMdPaths = new Set();
  
  for (const html of htmlFiles) {
    let matched = false;
    
    // 策略1: slug 匹配（验证标题）
    for (const md of mdFiles) {
      if (matchedMdPaths.has(md.path)) continue;
      
      const result = readFrontmatter(md.path);
      if (result && result.frontmatter.slug === html.slug) {
        // 验证标题是否匹配
        const similarity = titleSimilarity(html.title, md.title);
        
        if (similarity > 0.5) {  // 50% 相似度阈值
          matches.push({ html, md, strategy: 'slug+title', similarity });
          matchedMdPaths.add(md.path);
          matched = true;
          break;
        } else {
          // slug 匹配但标题不匹配，记录为"不确定"
          uncertain.push({ html, md, slug: html.slug, similarity });
        }
      }
    }
    
    if (matched) continue;
    
    // 策略2: 标题精确匹配
    for (const md of mdFiles) {
      if (matchedMdPaths.has(md.path)) continue;
      
      if (md.normalizedTitle === html.normalizedTitle) {
        matches.push({ html, md, strategy: 'title-exact', similarity: 1.0 });
        matchedMdPaths.add(md.path);
        matched = true;
        break;
      }
    }
    
    if (matched) continue;
    
    // 策略3: 标题模糊匹配（高相似度）
    for (const md of mdFiles) {
      if (matchedMdPaths.has(md.path)) continue;
      
      const similarity = titleSimilarity(html.title, md.title);
      
      if (similarity > 0.6) {  // 60% 相似度阈值
        matches.push({ html, md, strategy: 'title-fuzzy', similarity });
        matchedMdPaths.add(md.path);
        matched = true;
        break;
      }
    }
    
    if (!matched) {
      unmatched.push(html);
    }
  }
  
  return { matches, uncertain, unmatched, htmlFiles, mdFiles };
}

// 更新匹配的文件
function updateMatches(matches) {
  console.log(`\n📝 开始更新 ${matches.length} 个匹配的文件...\n`);
  
  let updated = 0;
  let skipped = 0;
  
  for (const { html, md, strategy, similarity } of matches) {
    const result = readFrontmatter(md.path);
    if (!result) continue;
    
    // 检查是否已经标记过
    if (result.frontmatter.status === 'pushed' && result.frontmatter.push_date === TODAY) {
      console.log(`⏭️  跳过 (已更新): ${md.filename}`);
      skipped++;
      continue;
    }
    
    // 构建更新
    const updates = {
      slug: html.slug,
      status: 'pushed',
      push_date: TODAY
    };
    
    // 根据语言添加 URL
    if (html.lang === 'en') {
      updates.url_en = `https://baidumarketing.com/blog/${html.slug}`;
      updates.url_jp = '';
    } else {
      updates.url_en = '';
      updates.url_jp = `https://baidumarketing.com/ja/blog/${html.slug}`;
    }
    
    // 更新文件
    const success = updateFrontmatter(md.path, updates);
    
    if (success) {
      console.log(`✅ 更新: ${md.filename} (策略: ${strategy}, 相似度: ${similarity.toFixed(2)})`);
      console.log(`   slug: ${html.slug}`);
      console.log(`   HTML 标题: ${html.title.substring(0, 60)}...`);
      console.log(`   MD 标题: ${md.title.substring(0, 60)}...`);
      updated++;
    } else {
      console.log(`❌ 失败: ${md.filename}`);
    }
  }
  
  console.log(`\n📊 更新完成: ${updated} 个更新, ${skipped} 个跳过`);
}

// 主函数
function main() {
  const { matches, uncertain, unmatched, htmlFiles, mdFiles } = matchFiles();
  
  console.log('\n📊 匹配结果:');
  console.log(`   高置信度匹配: ${matches.length}`);
  console.log(`   低置信度（需审核）: ${uncertain.length}`);
  console.log(`   未匹配: ${unmatched.length}`);
  
  if (matches.length > 0) {
    console.log('\n✅ 高置信度匹配详情:');
    matches.forEach(({ html, md, strategy, similarity }) => {
      console.log(`   - ${html.slug} (${html.lang}) <-> ${md.filename} [${strategy}, ${(similarity * 100).toFixed(0)}%]`);
    });
  }
  
  if (uncertain.length > 0) {
    console.log('\n⚠️  低置信度匹配（需人工审核）:');
    uncertain.forEach(({ html, md, slug, similarity }) => {
      console.log(`   - ${slug} (${html.lang}) <-> ${md.filename} [相似度: ${(similarity * 100).toFixed(0)}%]`);
      console.log(`     HTML 标题: ${html.title.substring(0, 50)}...`);
      console.log(`     MD 标题: ${md.title.substring(0, 50)}...`);
    });
  }
  
  if (unmatched.length > 0) {
    console.log('\n⚠️  未匹配的文件:');
    unmatched.forEach(html => {
      console.log(`   - ${html.slug} (${html.lang}): ${html.title.substring(0, 50)}...`);
    });
  }
  
  // 更新高置信度匹配
  if (matches.length > 0) {
    updateMatches(matches);
  }
  
  // 保存低置信度匹配到文件
  if (uncertain.length > 0) {
    const uncertainPath = join(SITE_ROOT, 'scripts', 'uncertain-matches.json');
    writeFileSync(uncertainPath, JSON.stringify(uncertain, null, 2), 'utf8');
    console.log(`\n💾 低置信度匹配已保存到: ${uncertainPath}`);
  }
  
  // 保存未匹配列表到文件
  if (unmatched.length > 0) {
    const unmatchedPath = join(SITE_ROOT, 'scripts', 'unmatched-files.json');
    writeFileSync(unmatchedPath, JSON.stringify(unmatched, null, 2), 'utf8');
    console.log(`💾 未匹配文件列表已保存到: ${unmatchedPath}`);
  }
}

main();
