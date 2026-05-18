#!/usr/bin/env node
/**
 * add-slug-manual-mapping.mjs
 * 根据已知映射关系，批量添加 slug 到 Obsidian 文件
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join } from 'path';

const OBSIDIAN_VAULT = 'E:\\Obsidian\\Baidu';

// 已知映射：Obsidian 文件名（不含扩展名）-> slug
// 基于 HTML 文件名和标题比对建立
const MAPPING = {
  // EN blogs (这些 Obsidian 文件缺少 slug)
  // 需要通过标题匹配来找到对应关系

  // JP blogs (这些 Obsidian 文件缺少 slug)
  // 需要通过标题匹配来找到对应关系
};

// 由于自动匹配失败，我直接读取 Obsidian 文件并手动建立映射
// 这里是已知的部分映射

const KNOWN_MAPPINGS = [
  // 格式：{ obsidianFile, slug, lang }
  // EN
  { obsidianFile: 'bpp-baidu-ad-creation-flow-simplified-en.md', slug: 'baidu-ad-creation-workflow-simplified-creative-upgrade', lang: 'en' },
  { obsidianFile: 'bpp-baidu-ads-campaign-upgrade-2025-en.md', slug: 'baidu-ads-campaign-upgrade-2025', lang: 'en' },
  { obsidianFile: 'bpp-baidu-brand-info-account-level-en.md', slug: 'baidu-brand-info-account-level', lang: 'en' },
  { obsidianFile: 'bpp-baidu-brand-zone-pre-review-en.md', slug: 'baidu-brand-zone-pre-review', lang: 'en' },
  { obsidianFile: 'bpp-baidu-custom-form-retirement-en.md', slug: 'baidu-custom-form-creative-component-retirement', lang: 'en' },
  { obsidianFile: 'bpp-baidu-keyword-zero-impression-diagnosis-en.md', slug: 'baidu-keyword-zero-impression-diagnosis', lang: 'en' },
  { obsidianFile: 'bpp-faq-international-brands-en.md', slug: 'baidu-ppc-faq-international-brands', lang: 'en' },
  { obsidianFile: 'faq-b2b-market-insights-en.md', slug: 'baidu-advertising-faq-b2b-market-insights', lang: 'en' },

  // JP
  { obsidianFile: 'bpp-baidu-ad-creation-flow-simplified-jp.md', slug: 'baidu-ad-creation-workflow-simplified-creative-upgrade', lang: 'ja' },
  { obsidianFile: 'bpp-baidu-ads-campaign-upgrade-2025-jp.md', slug: 'baidu-ads-campaign-upgrade-2025', lang: 'ja' },
  { obsidianFile: 'bpp-baidu-brand-info-account-level-jp.md', slug: 'baidu-brand-info-account-level', lang: 'ja' },
  { obsidianFile: 'bpp-baidu-brand-zone-pre-review-jp.md', slug: 'baidu-brand-zone-pre-review', lang: 'ja' },
  { obsidianFile: 'bpp-baidu-custom-form-retirement-jp.md', slug: 'baidu-custom-form-creative-component-retirement', lang: 'ja' },
  { obsidianFile: 'bpp-baidu-keyword-zero-impression-diagnosis-jp.md', slug: 'baidu-keyword-zero-impression-diagnosis', lang: 'ja' },
  { obsidianFile: 'bpp-faq-international-brands-jp.md', slug: 'baidu-ppc-faq-international-brands', lang: 'ja' },
  { obsidianFile: 'faq-b2b-market-insights-jp.md', slug: 'baidu-advertising-faq-b2b-market-insights', lang: 'ja' },
];

// 检查 HTML 文件是否存在
function checkHtmlExists(slug, lang) {
  if (lang === 'en') {
    return existsSync(join(OBSIDIAN_VAULT, '..', '..', 'c:', 'Users', 'HYE', 'WorkBuddy', '20260411211839', 'blog', `${slug}.html`));
  } else if (lang === 'ja') {
    return existsSync(join(OBSIDIAN_VAULT, '..', '..', 'c:', 'Users', 'HYE', 'WorkBuddy', '20260411211839', 'ja', 'blog', `${slug}.html`));
  }
  return false;
}

// 添加 slug 到 frontmatter
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
  console.log('=== 手动映射：添加 slug 到 Obsidian 文件 ===\n');

  const results = {
    updated: [],
    alreadyHas: [],
    htmlMissing: [],
    errors: []
  };

  for (const { obsidianFile, slug, lang } of KNOWN_MAPPINGS) {
    const filePath = join(OBSIDIAN_VAULT, obsidianFile);

    if (!existsSync(filePath)) {
      results.errors.push({ file: obsidianFile, reason: '文件不存在' });
      continue;
    }

    // 检查 HTML 是否存在
    const htmlExists = checkHtmlExists(slug, lang);
    if (!htmlExists) {
      results.htmlMissing.push({ file: obsidianFile, slug, lang });
      continue;
    }

    const content = readFileSync(filePath, 'utf8');

    // 检查是否已有 slug
    if (/^slug:\s*.+$/m.test(content)) {
      results.alreadyHas.push({ file: obsidianFile, slug });
      continue;
    }

    // 添加 slug
    const updated = addSlug(content, slug);
    if (updated) {
      writeFileSync(filePath, updated, 'utf8');
      results.updated.push({ file: obsidianFile, slug, lang });
    }
  }

  console.log(`✅ 已更新 (${results.updated.length} 篇):`);
  results.updated.forEach(({ file, slug, lang }) => {
    console.log(`  - ${file} → ${slug} [${lang}]`);
  });

  console.log(`\n😊 已有 slug (${results.alreadyHas.length} 篇):`);
  results.alreadyHas.forEach(({ file, slug }) => {
    console.log(`  - ${file} (${slug})`);
  });

  console.log(`\n⚠️  HTML 缺失 (${results.htmlMissing.length} 篇):`);
  results.htmlMissing.forEach(({ file, slug, lang }) => {
    console.log(`  - ${file} → ${slug} [${lang}] (HTML 不存在)`);
  });

  if (results.errors.length > 0) {
    console.log(`\n❌ 错误 (${results.errors.length} 篇):`);
    results.errors.forEach(({ file, reason }) => {
      console.log(`  - ${file}: ${reason}`);
    });
  }

  console.log(`\n📊 统计:`);
  console.log(`  已更新: ${results.updated.length}`);
  console.log(`  已有 slug: ${results.alreadyHas.length}`);
  console.log(`  HTML 缺失: ${results.htmlMissing.length}`);
}

main();
