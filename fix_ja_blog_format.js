const fs = require('fs');
const dir = 'ja/blog';
let fixed = 0;

for (const f of fs.readdirSync(dir).filter(x => x.endsWith('.html'))) {
  const fp = dir + '/' + f;
  let c = fs.readFileSync(fp, 'utf8');
  let changed = false;

  // 1. Add html[lang="ja"] .nav-links rule after .nav-links { ... gap:24px; ... }
  if (!c.includes('html[lang="ja"]') && c.includes('.nav-links { display:flex; gap:24px;')) {
    c = c.replace(
      '.nav-links { display:flex; gap:24px; align-items:center; }',
      '.nav-links { display:flex; gap:24px; align-items:center; } html[lang="ja"] .nav-links { gap:20px; font-size:.82rem; }'
    );
    changed = true;
  }

  // 2. Fix breadcrumb: /ja/blog → /ja/blog.html
  if (c.includes('href="/ja/blog"')) {
    c = c.replace(/href="\/ja\/blog"/g, 'href="/ja/blog.html"');
    changed = true;
  }

  // 3. Fix related article links: /ja/blog/slug → /ja/blog/slug.html
  // Match all internal links in "You May Also Like" section (they're absolute /ja/blog/...)
  c = c.replace(
    /href="\/ja\/blog\/([a-z0-9-]+)"/g,
    function(match, slug) {
      // Don't add .html if it already has it
      if (slug.endsWith('.html')) return match;
      // Don't add .html to homepage links
      if (slug === 'index') return match;
      changed = true;
      return 'href="/ja/blog/' + slug + '.html"';
    }
  );

  if (changed) {
    fs.writeFileSync(fp, c, 'utf8');
    console.log('Fixed:', fp);
    fixed++;
  }
}

console.log('Total fixed:', fixed);
