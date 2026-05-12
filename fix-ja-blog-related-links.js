const fs = require('fs');
const path = require('path');

// Batch fix all JA blog pages: change ../blog/...html to /ja/blog/...html
const dir = 'c:/Users/HYE/WorkBuddy/20260411211839/ja/blog';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

let fixedCount = 0;
for (const file of files) {
  const filePath = path.join(dir, file);
  let html = fs.readFileSync(filePath, 'utf8');
  let count = 0;
  
  // Fix related links: ../blog/...html → /ja/blog/...html
  html = html.replace(/href="\.\.\/blog\/([^"]*\.html)"/g, (match, p1) => {
    count++;
    return `href="/ja/blog/${p1}"`;
  });
  
  if (count > 0) {
    fs.writeFileSync(filePath, html, 'utf8');
    console.log(`Fixed ${count} links in ${file}`);
    fixedCount += count;
  }
}

console.log(`\nTotal links fixed: ${fixedCount}`);
