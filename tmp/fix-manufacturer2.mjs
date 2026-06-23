import fs from 'fs';
const f = 'ko/blog/b2b-manufacturer-baidu-case-study.html';
let h = fs.readFileSync(f, 'utf8');

const title = '???? ? 400? ?? ??: ?? ???? ??? PPC? ?? ??? ??? ??';
const desc = '?? ?? ??? ?? ???? ??? PPC? 90? ?? ?? ?? 47?? ??? ??';
const slug = 'b2b-manufacturer-baidu-case-study';

// Fix <title>
h = h.replace(/<title>[^<]*<\/title>/, '<title>' + title + ' ¡ª Baidu PPC Pro Blog</title>');

// Fix og:title  
h = h.replace(/og:title[^>]*content="[^"]*"/, 'og:title" content="' + title + '"');

// Fix twitter:title
h = h.replace(/twitter:title[^>]*content="[^"]*"/, 'twitter:title" content="' + title + '"');

// Fix JSON-LD - find the block and replace placeholders
h = h.replace(/"headline":"[^"]*"/, '"headline":"' + title + '"');
h = h.replace(/"description":"[^"]*"/, '"description":"' + desc + '"');
h = h.replace(/"datePublished":"[^"]*"/, '"datePublished":"2026-06-23"');
h = h.replace(/"dateModified":"[^"]*"/, '"dateModified":"2026-06-23"');
h = h.replace(/ko\/blog\/[^"]*?(?="})/, 'ko/blog/' + slug);

// Remove duplicate <h1> at line 295
const lines = h.split('\n');
const newLines = [];
let h1Count = 0;
for (const line of lines) {
  if (line.includes('<h1 class="article-title">')) {
    h1Count++;
    if (h1Count > 1) continue; // skip duplicate
  }
  if (line.trim() === '<p>---</p>') continue; // skip bare ---
  newLines.push(line);
}

fs.writeFileSync(f, newLines.join('\n'), 'utf8');
console.log('Fixed:', f);
