/**
 * Fix remaining URL inconsistencies in JA blog posts
 * 
 * 1. Related post links: add .html suffix
 * 2. Lang-switch links: use directory form (consistent with core pages)
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const BLOG_DIR = path.join(__dirname, 'ja', 'blog');

let relatedFixed = 0;
let langFixed = 0;

const files = fs.readdirSync(BLOG_DIR).filter(f => f.endsWith('.html'));

for (const file of files) {
  const filePath = path.join(BLOG_DIR, file);
  let html = fs.readFileSync(filePath, 'utf8');
  let modified = false;

  // 1. Fix related post links - add .html suffix to href="../../ja/blog/slug"
  // But only in .related-card or .related-section context
  const relatedPattern = /href="(\.\.\/\.\.\/ja\/blog\/[a-z0-9-]+)(?!\.html|")/g;
  const newHtml = html.replace(relatedPattern, (match, path) => {
    relatedFixed++;
    return `href="${path}.html"`;
  });
  if (newHtml !== html) {
    html = newHtml;
    modified = true;
  }

  // 2. Fix lang-switch links - use directory form for consistency
  // Change: href="../../index.html" -> href="../../" (EN)
  // Change: href="../../ja/index.html" -> href="../../ja/" (JA)
  const enLang = html.match(/href="\.\.\/\.\.\/index\.html" lang="en"/);
  const jaLang = html.match(/href="\.\.\/\.\.\/ja\/index\.html" lang="ja"/);
  
  if (enLang) {
    html = html.replace(enLang[0], 'href="../../" lang="en"');
    langFixed++;
    modified = true;
  }
  if (jaLang) {
    html = html.replace(jaLang[0], 'href="../../ja/" lang="ja"');
    langFixed++;
    modified = true;
  }

  if (modified) {
    fs.writeFileSync(filePath, html, 'utf8');
  }
}

console.log(`✅ Fixed related post links: ${relatedFixed}`);
console.log(`✅ Fixed lang-switch links: ${langFixed}`);
console.log(`✅ Total files modified: ${files.length}`);
