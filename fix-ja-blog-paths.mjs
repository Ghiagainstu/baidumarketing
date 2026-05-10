/**
 * Fix ALL nav/breadcrumb/footer/CTA/related links in JA blog posts
 * 
 * Bug: from ja/blog/slug, ../../ja/ resolves to /ja/ja/ (WRONG)
 * Fix: replace ../../ja/ with ../ in ALL hrefs that end with .html
 * 
 * Lang-switch links use ../../ and ../../ja/ (directory form) — leave untouched
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const BLOG_DIR = path.join(__dirname, 'ja', 'blog');

let fixed = 0;
const files = fs.readdirSync(BLOG_DIR).filter(f => f.endsWith('.html'));

for (const file of files) {
  const filePath = path.join(BLOG_DIR, file);
  let html = fs.readFileSync(filePath, 'utf8');
  let changed = false;

  // Replace href="../../ja/XXXX.html" -> href="../XXXX.html"
  // Only for .html-ending hrefs (excludes lang-switch which uses directory form)
  const newHtml = html.replace(
    /href="\.\.\/\.\.\/ja\/([^"]*\.html)"/g,
    (match, pagePath) => {
      changed = true;
      fixed++;
      return `href="../${pagePath}"`;
    }
  );

  if (changed) {
    fs.writeFileSync(filePath, newHtml, 'utf8');
  }
}

console.log(`✅ Fixed ${fixed} .html links across ${files.length} blog posts`);
console.log(`   (Lang-switch links preserved — they use directory form)`);
