/**
 * Emergency fix: repair truncated related post links + add .html correctly
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const BLOG_DIR = path.join(__dirname, 'ja', 'blog');

let truncated = 0;
let added = 0;

const files = fs.readdirSync(BLOG_DIR).filter(f => f.endsWith('.html'));

for (const file of files) {
  const filePath = path.join(BLOG_DIR, file);
  let html = fs.readFileSync(filePath, 'utf8');

  // Step 1: Fix truncated links
  // Pattern: ../../ja/blog/slug-trunc.html"e"  ->  ../../ja/blog/slug-full.html"
  html = html.replace(
    /href="(\.\.\/\.\.\/ja\/blog\/[a-z0-9-]+)\.html"([a-z0-9])"/g,
    (m, slug, lastChar) => { truncated++; return `href="${slug}${lastChar}.html"`; }
  );

  // Step 2: Add .html to ../../ja/blog/ links that are missing it
  // Match optional .html to avoid double-adding
  html = html.replace(
    /href="(\.\.\/\.\.\/ja\/blog\/[a-z0-9-]+)(\.html)?"/g,
    (m, hrefVal, hasHtml) => {
      if (hasHtml) return m; // Already has .html
      added++;
      return `href="${hrefVal}.html"`;
    }
  );

  fs.writeFileSync(filePath, html, 'utf8');
}

console.log(`✅ Fixed truncated links: ${truncated}`);
console.log(`✅ Added .html to links: ${added}`);
console.log(`✅ Total files processed: ${files.length}`);
