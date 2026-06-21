// audit-v2.js
const fs = require('fs');
const files = fs.readdirSync('blog').filter(f => f.endsWith('.html') && !f.startsWith('_'));
let issues = [];
files.forEach(f => {
  const html = fs.readFileSync('blog/' + f, 'utf8');
  const hasFooterLang = html.includes('footer-lang');
  const hasNavRightGroup = html.includes('nav-right-group');
  const hasLangSwitch = html.includes('lang-switch');
  if (!hasFooterLang || !hasNavRightGroup || !hasLangSwitch) {
    issues.push(f + ' | nav:' + !hasNavRightGroup + ' | lang:' + !hasLangSwitch + ' | footLang:' + !hasFooterLang);
  }
});
console.log('Total:', files.length);
console.log('Issues:', issues.length);
if (issues.length) issues.forEach(i => console.log(i));
else console.log('ALL FIXED!');
