// fix_all_js_v2.mjs - 修复所有博客文件缺失的 JS 函数（v2 简化版）
import fs from 'fs';
import path from 'path';

const blogDir = 'blog';
const jaBlogDir = 'ja/blog';

// 从 bpp-template-ultimate 提取的完整 JS（格式化版本，易读）
const jsCode = `
function toggleLangMenu() {
  const menu = document.getElementById('langSwitchMenu');
  if (menu) menu.classList.toggle('open');
}
document.addEventListener('click', function(e) {
  const menu = document.getElementById('langSwitchMenu');
  const btn = document.querySelector('.lang-switch-btn');
  if (menu && btn && !btn.contains(e.target) && !menu.contains(e.target)) {
    menu.classList.remove('open');
  }
});
document.addEventListener('DOMContentLoaded', function() {
  const currentLang = document.documentElement.lang || 'en';
  document.querySelectorAll('.lang-switch-item').forEach(function(item) {
    if (item.getAttribute('lang') === currentLang) {
      item.style.fontWeight = '600';
      item.style.pointerEvents = 'none';
      item.style.opacity = '0.5';
    }
  });
});

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
})();

let mobileNavOpen = false;
function toggleMobileNav() {
  const links = document.getElementById('navLinks');
  const hamburger = document.querySelector('.hamburger-icon');
  const closeX = document.querySelector('.close-icon');
  const overlay = document.getElementById('navOverlay');
  mobileNavOpen = !mobileNavOpen;
  if (mobileNavOpen) {
    links.classList.add('open');
    hamburger.style.display = 'none';
    closeX.style.display = 'block';
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  } else {
    links.classList.remove('open');
    hamburger.style.display = 'block';
    closeX.style.display = 'none';
    overlay.classList.remove('active');
    document.body.style.overflow = '';
  }
}
document.querySelectorAll('.nav-links a').forEach(link => {
  link.addEventListener('click', () => { if (mobileNavOpen) toggleMobileNav(); });
});

document.querySelectorAll('.obf-email').forEach(function(el){el.textContent=el.dataset.u+'@'+el.dataset.d});
document.querySelectorAll('.obf-email-link').forEach(function(el){var a=el.dataset.u+'@'+el.dataset.d;el.href='mailto:'+a;if(!el.textContent)el.textContent=a});
document.querySelectorAll('.obf-email-icon').forEach(function(el){el.href='mailto:'+el.dataset.u+'@'+el.dataset.d});

window.addEventListener('scroll', () => { document.getElementById('backToTop').classList.toggle('visible', window.scrollY > 600); });
`;

function fixFile(filePath) {
  let html = fs.readFileSync(filePath, 'utf8');
  
  // 检查是否已有 toggleTheme（完整 JS 的标志）
  if (html.includes('function toggleTheme()')) {
    return 'already-ok';
  }
  
  // 找到最后一个 <script> 标签的位置
  const lastScriptStart = html.lastIndexOf('<script>');
  if (lastScriptStart === -1) {
    return 'no-script-start';
  }
  
  // 找到对应的 </script> 结束位置
  const lastScriptEnd = html.indexOf('</script>', lastScriptStart);
  if (lastScriptEnd === -1) {
    return 'no-script-end';
  }
  
  // 构建新的 script 块
  const newScriptBlock = '<script>' + jsCode + '\n</script>';
  
  // 重组文件：前面部分 + 新 script 块 + 后面部分（应该是 </body></html>）
  const before = html.substring(0, lastScriptStart);
  const after = html.substring(lastScriptEnd + 9); // +9 是 </script> 的长度
  
  const newHtml = before + newScriptBlock + after;
  fs.writeFileSync(filePath, newHtml, 'utf8');
  return 'fixed';
}

let enFixed = 0, enSkipped = 0, enErrors = 0;
console.log('=== Fixing EN blog files ===');
fs.readdirSync(blogDir).filter(f => f.endsWith('.html')).forEach(f => {
  const filePath = path.join(blogDir, f);
  const result = fixFile(filePath);
  if (result === 'fixed') { enFixed++; }
  else if (result === 'already-ok') { enSkipped++; }
  else { console.log('Error: ' + f + ' - ' + result); enErrors++; }
});
console.log('EN: fixed=' + enFixed + ', skipped=' + enSkipped + ', errors=' + enErrors);

if (fs.existsSync(jaBlogDir)) {
  let jaFixed = 0, jaSkipping = 0, jaErrors = 0;
  console.log('\n=== Fixing JA blog files ===');
  fs.readdirSync(jaBlogDir).filter(f => f.endsWith('.html')).forEach(f => {
    const filePath = path.join(jaBlogDir, f);
    const result = fixFile(filePath);
    if (result === 'fixed') { jaFixed++; }
    else if (result === 'already-ok') { jaSkipping++; }
    else { console.log('Error: ' + f + ' - ' + result); jaErrors++; }
  });
  console.log('JA: fixed=' + jaFixed + ', skipped=' + jaSkipping + ', errors=' + jaErrors);
}

console.log('\nDone!');
