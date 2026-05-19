const fs = require('fs');
const path = require('path');

// Get all HTML files in root and ja/ directory
const rootFiles = fs.readdirSync('.').filter(f => f.endsWith('.html'));
const jaFiles = fs.readdirSync('./ja').filter(f => f.endsWith('.html')).map(f => path.join('ja', f));
const allFiles = [...rootFiles, ...jaFiles];

let fixedCount = 0;

allFiles.forEach(filePath => {
  if (!fs.existsSync(filePath)) return;
  
  let content = fs.readFileSync(filePath, 'utf8');
  let modified = false;
  
  // Remove .html extension from href attributes in navigation and footer links
  // Pattern: href="something.html" → href="something"
  // But ONLY for page links (not blog post links or external links)
  const pageNames = ['index', 'features', 'pricing', 'clients', 'faq', 'about', 'blog', 'contact', 'privacy', 'terms', 'why-baidu-ppc-pro', 'china-geo'];
  
  pageNames.forEach(page => {
    const regex = new RegExp(`href="${page}\.html"`, 'g');
    if (content.match(regex)) {
      content = content.replace(regex, `href="${page}"`);
      modified = true;
    }
  });
  
  // Also fix logo links (index.html → / or ./)
  if (filePath.startsWith('ja/')) {
    // For Japanese pages, logo should point to /ja/
    if (content.includes('href="index.html" class="nav-logo"')) {
      content = content.replace(/href="index\.html" class="nav-logo"/g, 'href="./" class="nav-logo"');
      modified = true;
    }
  } else {
    // For English pages, logo should point to /
    if (content.includes('href="index.html" class="nav-logo"')) {
      content = content.replace(/href="index\.html" class="nav-logo"/g, 'href="/" class="nav-logo"');
      modified = true;
    }
  }
  
  if (modified) {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log('Fixed:', filePath);
    fixedCount++;
  }
});

console.log(`\nDone! Fixed ${fixedCount} files.`);
