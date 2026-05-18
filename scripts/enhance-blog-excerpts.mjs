#!/usr/bin/env node
/**
 * enhance-blog-excerpts.mjs
 * 给 blog 首页卡片的摘要添加视觉增强（emoji 前缀）
 *
 * 策略：
 * 1. 读取 blog.html / ja/blog.html / ko/blog.html
 * 2. 分析每个 excerpt 的内容关键词
 * 3. 在开头添加相关 emoji
 * 4. 避免重复添加（已有时跳过）
 */

import fs from 'fs';
import path from 'path';
import { JSDOM } from 'jsdom';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');

// Emoji 关键词映射（按优先级排列）
const emojiRules = [
  // 广告相关
  { keywords: ['ad', 'ads', 'advertising', 'advertise', 'campaign', 'PPC', 'CPC', 'CPM', 'oCPM'], emoji: '📢' },
  { keywords: ['baidu', 'Baidu'], emoji: '🔍' },
  { keywords: ['keyword', 'keywords', 'negative', 'search term'], emoji: '🔑' },
  { keywords: ['budget', 'cost', 'spend', 'CPA', 'CPC', 'ROI', 'ROAS'], emoji: '💰' },
  { keywords: ['CTR', 'click', 'click-through', 'impression', 'impressions'], emoji: '📊' },
  { keywords: ['conversion', 'convert', 'goal', 'track'], emoji: '🎯' },
  { keywords: ['landing page', 'landing', 'LP'], emoji: '📄' },
  { keywords: ['audience', 'targeting', 'target'], emoji: '🎯' },
  { keywords: ['brand', 'branding'], emoji: '🏢' },
  { keywords: ['B2B', 'lead', 'leads', 'generation'], emoji: '🤝' },
  { keywords: ['AI', 'machine learning', 'algorithm'], emoji: '🤖' },
  { keywords: ['mobile', 'app', 'iOS', 'Android'], emoji: '📱' },
  { keywords: ['video', 'streaming', 'live'], emoji: '🎥' },
  { keywords: ['trend', '2025', '2026', 'future', 'update'], emoji: '📈' },
  { keywords: ['guide', 'how to', 'tutorial', 'step'], emoji: '📚' },
  { keywords: ['case study', 'example', 'real campaign'], emoji: '📋' },
  { keywords: ['policy', 'rule', 'compliance', 'regulation'], emoji: '⚖️' },
  { keywords: ['tip', 'tips', 'advice', 'best practice'], emoji: '💡' },
  { keywords: ['warning', 'avoid', 'mistake', 'error'], emoji: '⚠️' },
  { keywords: ['compare', 'vs', 'difference', 'versus'], emoji: '⚖️' },
  // 默认
  { keywords: [], emoji: '📝' },
];

function getEmojiForText(text) {
  const lower = text.toLowerCase();
  for (const rule of emojiRules) {
    if (rule.keywords.length === 0) return rule.emoji; // default
    if (rule.keywords.some(kw => lower.includes(kw.toLowerCase()))) {
      return rule.emoji;
    }
  }
  return '📝';
}

function enhanceExcerpts(indexFile) {
  const fullPath = path.join(ROOT, indexFile);
  if (!fs.existsSync(fullPath)) {
    console.log(`  ⏭️  Skipping (not found): ${indexFile}`);
    return { enhanced: 0, skipped: 0 };
  }

  let html = fs.readFileSync(fullPath, 'utf8');
  const dom = new JSDOM(html);
  const doc = dom.window.document;

  const cards = doc.querySelectorAll('.blog-card');
  let enhanced = 0;
  let skipped = 0;

  console.log(`\n📝 Processing: ${indexFile} (${cards.length} cards)`);

  cards.forEach((card, i) => {
    const excerptEl = card.querySelector('.blog-card-excerpt');
    if (!excerptEl) { skipped++; return; }

    let text = excerptEl.textContent.trim();

    // 跳过空或太短的 excerpt
    if (!text || text.length < 10) { skipped++; return; }

    // 检查是否已有 emoji
    const hasEmoji = /[\u{1F300}-\u{1F9FF}]/u.test(text);

    if (hasEmoji) {
      skipped++;
      return;
    }

    // 获取合适的 emoji
    const emoji = getEmojiForText(text);

    // 添加 emoji 到开头
    excerptEl.textContent = `${emoji} ${text}`;
    enhanced++;
  });

  if (enhanced > 0) {
    const updatedHtml = dom.serialize();
    fs.writeFileSync(fullPath, updatedHtml, 'utf8');
  }

  console.log(`  ✅ Enhanced: ${enhanced}, Skipped: ${skipped}`);
  return { enhanced, skipped };
}

console.log('🚀 Starting blog excerpt visual enhancement...\n');

const indexFiles = ['blog.html', 'ja/blog.html', 'ko/blog.html'];
const results = { totalEnhanced: 0, totalSkipped: 0 };

for (const file of indexFiles) {
  const { enhanced, skipped } = enhanceExcerpts(file);
  results.totalEnhanced += enhanced;
  results.totalSkipped += skipped;
}

console.log('\n\n✅ Blog excerpt enhancement complete!\n');
console.log('📊 Summary:');
console.log(`  Total enhanced: ${results.totalEnhanced}`);
console.log(`  Total skipped (already have emoji or empty): ${results.totalSkipped}`);
