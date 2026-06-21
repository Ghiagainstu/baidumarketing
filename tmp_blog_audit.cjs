const fs = require('fs');
const path = require('path');

// Sample 3 blog posts to check hreflang, canonical, structured data
const samples = [
  'blog/baidu-2026-new-opportunities.html',
  'ja/blog/baidu-2026-new-opportunities.html',
  'ko/blog/baidu-2026-new-opportunities.html'
];

function g(t, re) {
  const m = t.match(re);
  return m ? m[1].trim() : '';
}

for (const f of samples) {
  if (!fs.existsSync(f)) { console.log('\n=== ' + f + ' === MISSING'); continue; }
  const t = fs.readFileSync(f, 'utf8');
  const htmlLang = g(t, /<html[^>]*\slang=["']([^"']+)/i);
  const title = g(t, /<title>([\s\S]*?)<\/title>/i);
  const desc = g(t, /<meta[^>]+name=["']description["'][^>]*content=["']([^"']*)/i);
  const canon = g(t, /<link[^>]+rel=["']canonical["'][^>]*href=["']([^"']*)/i);
  const alts = [...t.matchAll(/<link[^>]+hreflang=["']([^"']+)["'][^>]+href=["']([^"']+)["']/gi)].map(m=>m[1]+'='+m[2]);
  const hasSchema = t.includes('application/ld+json');
  const hasNav = t.includes('<nav') || t.includes('navbar');
  const hasFooter = t.includes('<footer');
  console.log('\n=== ' + f + ' ===');
  console.log('html_lang:', htmlLang);
  console.log('title:', title.slice(0,100));
  console.log('canonical:', canon);
  console.log('hreflangs:', alts.join(' | '));
  console.log('has_schema_markup:', hasSchema);
  console.log('has_nav:', hasNav, 'has_footer:', hasFooter);
  console.log('description:', desc.slice(0,120));
}
