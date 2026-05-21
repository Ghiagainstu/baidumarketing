// audit-simple.js
const fs = require('fs');
const files = fs.readdirSync('blog').filter(f => f.endsWith('.html'));
let issues = [];
files.forEach(f => {
  const html = fs.readFileSync('blog/' + f, 'utf8');
  const hasBrokenFooter = html.includes('function toggleLangMenu()') && html.includes('footer-copy');
  const hasFooterLang = html.includes('footer-lang');
  const hasNavRightGroup = html.includes('nav-right-group');
  const hasLangSwitch = html.includes('lang-switch');
  if (hasBrokenFooter || !hasFooterLang || !hasNavRightGroup || !hasLangSwitch) {
    issues.push(f + ' | nav:' + !hasNavRightGroup + ' | lang:' + !hasLangSwitch + ' | footer:' + hasBrokenFooter + ' | footLang:' + !hasFooterLang);
  }
});
console.log('Total:', files.length);
console.log('Issues:', issues.length);
issues.forEach(i => console.log(i));
if (issues.length === 0) console.log('ALL FIXED!');
