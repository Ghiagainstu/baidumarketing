/**
 * Fix .html suffix in blog posts' nav links
 * blog/*.html (EN) and ja/blog/*.html (JA)
 */

import fs from 'fs';
import path from 'path';

const ROOT = new URL('.', import.meta.url).pathname.replace(/^\/(\w:\/)/, '$1');

function fixBlogNav(dir) {
  if (!fs.existsSync(dir)) {
    console.log(`  ⏭️  ${dir} does not exist, skipping`);
    return 0;
  }

  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));
  let count = 0;

  for (const file of files) {
    const filePath = path.join(dir, file);
    let html = fs.readFileSync(filePath, 'utf8');

    // Fix all href="..." in <nav> that don't end with .html
    const newHtml = html.replace(
      /(<nav[\s\S]*?<\/nav>)/,
      (navSection) => {
        return navSection.replace(
          /href="([^"]*)"/g,
          (match, hrefValue) => {
            // Skip: empty, hash links, already has .html
            if (
              hrefValue === '' ||
              hrefValue.startsWith('#') ||
              hrefValue.endsWith('.html')
            ) {
              return match;
            }
            // Add .html suffix
            return `href="${hrefValue}.html"`;
          }
        );
      }
    );

    if (newHtml !== html) {
      fs.writeFileSync(filePath, newHtml, 'utf8');
      count++;
    }
  }

  console.log(`  ✅ ${dir}: ${count}/${files.length} posts updated`);
  return count;
}

console.log('\n🔧 Fixing .html suffix in blog post nav links...\n');

let total = 0;
total += fixBlogNav(path.join(ROOT, 'blog'));
total += fixBlogNav(path.join(ROOT, 'ja', 'blog'));

console.log(`\n  ✅ Total: ${total} blog posts updated\n`);
