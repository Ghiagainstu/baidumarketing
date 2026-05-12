const fs = require('fs');
const path = require('path');

// Check all JA pages for relative path links
const dirs = [
  'c:/Users/HYE/WorkBuddy/20260411211839/ja',
  'c:/Users/HYE/WorkBuddy/20260411211839/ja/blog',
];

let totalIssues = 0;

for (const dir of dirs) {
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));
  for (const file of files) {
    const filePath = path.join(dir, file);
    const content = fs.readFileSync(filePath, 'utf8');
    
    // Find all href="..." that are relative (start with ../ or ./ or just a path without /)
    const relativeLinks = content.match(/href="\.\.[^"]*"/g) || [];
    const withoutHtml = content.match(/href="[^"]*"[^>]*>(?![^<]*<\/a>)/g) || [];
    
    if (relativeLinks.length > 0) {
      console.log(`\n${filePath}:`);
      relativeLinks.forEach(link => {
        console.log(`  ${link}`);
        totalIssues++;
      });
    }
  }
}

console.log(`\nTotal files with relative links: ${totalIssues}`);
