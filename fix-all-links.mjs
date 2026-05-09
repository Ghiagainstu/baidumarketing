/**
 * Fix ALL internal links in all HTML files
 * Adds .html suffix to href="page" (no extension, not anchor, not external)
 * Covers: ja/*.html, ja/blog/*.html, and any other HTML files
 */

import fs from 'fs';
import path from 'path';

const ROOT = new URL('.', import.meta.url).pathname.replace(/^\/(\w:\/)/, '$1');

// List of known internal page names that need .html suffix
const KNOWN_PAGES = [
  'index', 'why-baidu-ppc-pro', 'features', 'pricing',
  'clients', 'faq', 'about', 'blog', 'contact',
  'privacy', 'terms', 'china-geo'
];

function fixFile(filePath) {
  if (!fs.existsSync(filePath)) return false;
  
  let html = fs.readFileSync(filePath, 'utf8');
  let modified = false;
  
  // Fix href="page" → href="page.html" for known internal pages
  // Only if NOT already ending with .html and NOT an anchor (#) and NOT external (http)
  const newHtml = html.replace(
    /href="([^"]*)"/g,
    (match, hrefValue) => {
      // Skip: empty, anchors, external URLs, already has extension
      if (
        hrefValue === '' ||
        hrefValue.startsWith('#') ||
        hrefValue.startsWith('http') ||
        hrefValue.startsWith('data:') ||
        hrefValue.startsWith('mailto:') ||
        hrefValue.endsWith('.html') ||
        hrefValue.includes('.', 1)  // has a dot that's not at position 0
      ) {
        return match;
      }
      
      // Check if it's a known internal page name
      const pageName = hrefValue.split('/').pop();  // handle ../page too
      if (KNOWN_PAGES.includes(pageName)) {
        return `href="${hrefValue}.html"`;
      }
      
      return match;
    }
  );
  
  if (newHtml !== html) {
    fs.writeFileSync(filePath, newHtml, 'utf8');
    return true;
  }
  return false;
}

function processDir(dir) {
  if (!fs.existsSync(dir)) {
    console.log(`  ⏭️  ${dir} not found, skipping`);
    return 0;
  }
  
  let count = 0;
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));
  
  for (const file of files) {
    const filePath = path.join(dir, file);
    if (fixFile(filePath)) {
      count++;
    }
  }
  
  console.log(`  ✅ ${dir}: ${count}/${files.length} files updated`);
  return count;
}

console.log('\n🔧 Fixing ALL internal links (adding .html suffix)...\n');

let total = 0;
total += processDir(path.join(ROOT, 'ja'));
total += processDir(path.join(ROOT, 'ja', 'blog'));
total += processDir(path.join(ROOT, 'blog'));
// Also fix EN core pages just in case
const enPages = ['index.html', 'about.html', 'features.html', 'pricing.html', 'clients.html', 'faq.html', 'contact.html', 'blog.html', 'privacy.html', 'terms.html', 'why-baidu-ppc-pro.html', 'china-geo.html'];
let enCount = 0;
for (const f of enPages) {
  if (fixFile(path.join(ROOT, f))) enCount++;
}
if (enCount > 0) console.log(`  ✅ EN core: ${enCount} files updated`);
total += enCount;

console.log(`\n  ✅ Total: ${total} files updated\n`);
