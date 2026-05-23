import fs from 'fs';

// Fix: wrap content in <article class="article-content">...</article>
function fixArticleWrapper(filePath) {
  let html = fs.readFileSync(filePath, 'utf8');
  
  // Check if already has <article class="article-content">
  if (html.includes('<article class="article-content">')) {
    console.log('Already has article wrapper:', filePath);
    return;
  }
  
  // Find </section> (end of article-hero) and insert <article>
  // Find <footer> and insert </article> before it
  const sectionEnd = html.indexOf('</section>');
  const footerStart = html.indexOf('<footer>');
  
  if (sectionEnd === -1 || footerStart === -1) {
    console.log('ERROR: could not find </section> or <footer>:', filePath);
    return;
  }
  
  // Insert <article> after </section>
  const before = html.substring(0, sectionEnd + '</section>'.length);
  const middle = html.substring(sectionEnd + '</section>'.length, footerStart);
  const after = html.substring(footerStart);
  
  const fixed = before + '\n  <article class="article-content">\n' + middle + '  </article>\n' + after;
  
  fs.writeFileSync(filePath, fixed, 'utf8');
  console.log('Fixed:', filePath);
}

const files = [
  'ja/blog/baidu-2026-new-opportunities.html',
  'ja/blog/baidu-ecosystem-numbers.html'
];

files.forEach(f => {
  if (fs.existsSync(f)) {
    fixArticleWrapper(f);
  } else {
    console.log('File not found:', f);
  }
});
