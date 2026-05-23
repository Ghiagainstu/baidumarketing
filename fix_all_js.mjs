// fix_all_js.mjs - 修复所有博客文件缺失的 JS 函数
import fs from 'fs';

const blogDir = 'blog';
const jaBlogDir = 'ja/blog';

// 完整的最后 script 块内容（从 bpp-template-ultimate 提取）
const fullScript = `<script>
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
</script>`;

function fixFile(filePath) {
  let html = fs.readFileSync(filePath, 'utf8');
  
  // 检查是否已有完整的 JS（包含 toggleTheme）
  if (html.includes('function toggleTheme()')) {
    return 'already-ok';
  }
  
  // 查找最后一个 </script> 之后的内容（应该是 </body></html>）
  const lastScriptEnd = html.lastIndexOf('</script>');
  if (lastScriptEnd === -1) {
    return 'no-script-tag';
  }
  
  // 检查最后一个 script 块是否完整
  const afterLastScript = html.substring(lastScriptEnd + 9); // +9 是 </script> 的长度
  
  // 替换最后一个 script 块
  // 找到倒数第二个 </script> 的位置，然后重写最后一块
  const allScriptEnds = [];
  let pos = 0;
  while ((pos = html.indexOf('</script>', pos)) !== -1) {
    allScriptEnds.push(pos);
    pos += 9;
  }
  
  if (allScriptEnds.length === 0) {
    return 'no-script';
  }
  
  // 找到最后一个 <script> 的开始位置
  const lastScriptStart = html.lastIndexOf('<script>');
  if (lastScriptStart === -1) {
    return 'no-script-start';
  }
  
  // 重写文件：保留前面所有内容，替换最后一个 script 块
  const beforeLastScript = html.substring(0, lastScriptStart);
  const afterLastScript2 = html.substring(lastScriptEnd + 9);
  
  // afterLastScript2 应该包含 </body></html>
  // 但也可能有其他内容
  
  const newHtml = beforeLastScript + fullScript + '\n' + afterLastScript2;
  fs.writeFileSync(filePath, newHtml, 'utf8');
  return 'fixed';
}

// 修复 EN 博客
const enFiles = fs.readdirSync(blogDir).filter(f => f.endsWith('.html'));
let enFixed = 0, enSkipped = 0, enErrors = 0;

console.log('=== Fixing EN blog files ===');
enFiles.forEach(f => {
  const filePath = blogDir + '/' + f;
  const result = fixFile(filePath);
  if (result === 'fixed') { enFixed++; }
  else if (result === 'already-ok') { enSkipped++; }
  else { 
    console.log('Error: ' + f + ' - ' + result);
    enErrors++; 
  }
});
console.log('EN: fixed=' + enFixed + ', skipped=' + enSkipped + ', errors=' + enErrors);

// 修复 JA 博客
if (fs.existsSync(jaBlogDir)) {
  const jaFiles = fs.readdirSync(jaBlogDir).filter(f => f.endsWith('.html'));
  let jaFixed = 0, jaSkipped = 0, jaErrors = 0;
  
  console.log('\n=== Fixing JA blog files ===');
  jaFiles.forEach(f => {
    const filePath = jaBlogDir + '/' + f;
    const result = fixFile(filePath);
    if (result === 'fixed') { jaFixed++; }
    else if (result === 'already-ok') { jaSkipped++; }
    else { 
      console.log('Error: ' + f + ' - ' + result);
      jaErrors++; 
    }
  });
  console.log('JA: fixed=' + jaFixed + ', skipped=' + jaSkipped + ', errors=' + jaErrors);
}

console.log('\nDone!');
