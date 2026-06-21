const fs = require('fs');
const path = require('path');

function scan(dir, lang) {
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html') && !f.startsWith('_'));
  const issues = [];
  files.forEach(f => {
    const h = fs.readFileSync(path.join(dir, f), 'utf8');
    const fi = [];
    if (!h.includes('rel="canonical"')) fi.push('no-canonical');
    if (!h.includes('og:image')) fi.push('no-og:image');
    if (!h.includes('schema.org')) fi.push('no-schema');
    if (!h.includes('breadcrumb')) fi.push('no-breadcrumb');
    if (!h.includes('meta name="description"')) fi.push('no-meta-desc');
    if (!h.includes('nav-cta')) fi.push('no-nav-cta');
    if (!h.includes('function toggleLangMenu')) fi.push('no-toggleLangMenu');
    if (!h.includes('obf-email')) fi.push('no-obf-email');
    const slug = f.replace('.html', '');
    const fl = h.match(/footer-lang[\s\S]*?<a href="\/blog\/([^"]+)"/);
    if (fl && fl[1] !== slug) fi.push('footer-lang-slug-mismatch:' + fl[1]);
    const flCount = (h.match(/class="footer-lang"/g) || []).length;
    if (flCount > 1) fi.push('dup-footer-lang:' + flCount);
    const fc = h.match(/<div class="footer-copy">[\s\S]*?<\/div>/);
    if (fc && fc[0].includes('function toggleLangMenu')) fi.push('broken-footer-copy');
    const tc = (h.match(/function toggleLangMenu/g) || []).length;
    if (tc > 1) fi.push('dup-toggleLangMenu:' + tc);
    if (!h.includes('hreflang')) fi.push('no-hreflang');
    if (!h.includes('<title>')) fi.push('no-title');
    if (fi.length > 0) issues.push({ file: lang + '/' + f, issues: fi });
  });
  return issues;
}

const en = scan('blog', 'blog');
const ja = scan('ja/blog', 'ja/blog');
console.log('=== BLOG EN (' + en.length + ' files with issues) ===');
en.forEach(i => console.log(i.file + ': ' + i.issues.join(', ')));
console.log('\n=== BLOG JA (' + ja.length + ' files with issues) ===');
ja.forEach(i => console.log(i.file + ': ' + i.issues.join(', ')));
console.log('\nTotal EN:', en.length, '| Total JA:', ja.length);
