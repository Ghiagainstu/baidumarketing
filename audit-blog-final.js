// audit-blog-final.js
const fs = require('fs');
const files = fs.readdirSync('blog').filter(f => f.endsWith('.html'));
let issues = [];
files.forEach(f => {
  const html = fs.readFileSync('blog/' + f, 'utf8');
  const hasNavRightGroup = html.includes('nav-right-group');
  const hasLangSwitch = html.includes('lang-switch');
  const hasBrokenFooter = html.includes('function toggleLangMenu()') && html.includes('footer-copy');
  const hasFooterLang = html.includes('footer-lang');
  if (!hasNavRightGroup || !hasLangSwitch || hasBrokenFooter || !hasFooterLang) {
    issues.push({file: f, nav: !hasNavRightGroup, lang: !hasLangSwitch, footer: hasBrokenFooter, footLang: !hasFooterLang});
  }
});
console.log('Total:', files.length);
console.log('Issues remaining:', issues.length);
if (issues.length > 0 && issues.length <= 10) {
  issues.forEach(i => {
    console.log(i.file, JSON.stringify({nav: i.nav, lang: i.lang, footer: i.footer, footLang: i.footLang}));
  });
if (issues.length > 10) console.log('(showing first 10 of', issues.length, 'issues)');
if (issues.length === 0) console.log('All files fixed!');
