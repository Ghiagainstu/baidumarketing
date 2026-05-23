// fix_ja_theme.mjs - 给所有JA博客注入 toggleTheme + 暗色模式初始化
import fs from 'fs';
import path from 'path';

const themeCode = `
function toggleTheme() {
  const html = document.documentElement;
  const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  html.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
  document.querySelector('meta[name="theme-color"]').content = next === 'dark' ? '#0B0F1A' : '#FFFFFF';
}
(function() {
  const saved = localStorage.getItem('theme');
  if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.setAttribute('data-theme', 'dark');
    document.querySelector('meta[name="theme-color"]').content = '#0B0F1A';
  }
})();`;

let fixed = 0, skipped = 0;
const dir = 'ja/blog';

fs.readdirSync(dir).filter(f => f.endsWith('.html')).forEach(f => {
  const filePath = path.join(dir, f);
  let html = fs.readFileSync(filePath, 'utf8');
  
  if (html.includes('function toggleTheme()')) {
    skipped++;
    return;
  }
  
  // 在 mobileNavOpen 之前插入 toggleTheme 代码
  if (html.includes('let mobileNavOpen')) {
    html = html.replace('let mobileNavOpen', themeCode + '\n\nlet mobileNavOpen');
    fs.writeFileSync(filePath, html, 'utf8');
    fixed++;
  } else {
    console.log('WARNING: ' + f + ' - no mobileNavOpen found');
  }
});

console.log('Fixed: ' + fixed + ', Skipped: ' + skipped);
