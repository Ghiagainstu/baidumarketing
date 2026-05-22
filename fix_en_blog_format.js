const fs = require('fs');
const dir = 'blog';
let fixed = 0;

for (const f of fs.readdirSync(dir).filter(x => x.endsWith('.html'))) {
  const fp = dir + '/' + f;
  let c = fs.readFileSync(fp, 'utf8');
  let changed = false;

  // 1. Fix breadcrumb: Blog link from "/" to "/blog.html" (only in breadcrumb context)
  c = c.replace(
    /(<div class="breadcrumb"><a href="\/">Home<\/a> \/ <a href=")\/(">Blog<\/a>)/g,
    '$1/blog.html$2'
  );
  if (c.includes('href="/blog.html">Blog</a>')) changed = true;

  // 2. Fix related article links: /blog/slug → /blog/slug.html
  // Match links in related articles section (after article content, not in nav/lang-switch)
  c = c.replace(
    /href="\/blog\/([a-z0-9-]+)"/g,
    function(match, slug) {
      if (slug.endsWith('.html') || slug === 'index') return match;
      return 'href="/blog/' + slug + '.html"';
    }
  );

  if (changed) {
    fs.writeFileSync(fp, c, 'utf8');
    fixed++;
    console.log('Fixed:', fp);
  }
}

console.log('Total fixed:', fixed);
