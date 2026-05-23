// fix_all_toggle.mjs - 全站修复缺失的 JS 函数
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

const mobileNavCode = `
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
});`;

const langSwitchCode = `
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
});`;

const obfEmailCode = `
document.querySelectorAll('.obf-email').forEach(function(el){el.textContent=el.dataset.u+'@'+el.dataset.d});
document.querySelectorAll('.obf-email-link').forEach(function(el){var a=el.dataset.u+'@'+el.dataset.d;el.href='mailto:'+a;if(!el.textContent)el.textContent=a});
document.querySelectorAll('.obf-email-icon').forEach(function(el){el.href='mailto:'+el.dataset.u+'@'+el.dataset.d});`;

const backToTopCode = `
window.addEventListener('scroll', () => { document.getElementById('backToTop').classList.toggle('visible', window.scrollY > 600); });`;

function fixFile(filePath) {
  let html = fs.readFileSync(filePath, 'utf8');
  let changed = false;
  
  // 找到最后一个 <script> 的位置
  const lastScriptStart = html.lastIndexOf('<script>');
  if (lastScriptStart === -1) return 'no-script';
  
  // 如果最后一个 script 块只有 backToTop（说明之前替换不完整），直接替换
  const lastScriptEnd = html.indexOf('</script>', lastScriptStart);
  const lastScriptContent = html.substring(lastScriptStart + 8, lastScriptEnd).trim();
  
  if (lastScriptContent.includes('backToTop') && !lastScriptContent.includes('toggleLangMenu')) {
    // 整个块需要替换
    const fullScript = '<script>' + langSwitchCode + '\n' + themeCode + '\n' + mobileNavCode + '\n' + obfEmailCode + '\n' + backToTopCode + '\n</script>';
    html = html.substring(0, lastScriptStart) + fullScript + html.substring(lastScriptEnd + 9);
    changed = true;
  } else {
    // 逐个检查，缺失的就插入
    const insertPoint = lastScriptEnd; // 在 </script> 之前插入
    let inserts = '';
    
    if (!lastScriptContent.includes('function toggleLangMenu')) {
      inserts += langSwitchCode;
      changed = true;
    }
    if (!lastScriptContent.includes('function toggleTheme')) {
      // 在 mobileNavOpen 之前插入
      if (lastScriptContent.includes('let mobileNavOpen')) {
        html = html.replace(/let mobileNavOpen/, themeCode + '\n\nlet mobileNavOpen');
        changed = true;
      } else {
        inserts += themeCode;
      }
    }
    if (!lastScriptContent.includes('function toggleMobileNav')) {
      // 在 obf-email 之前插入
      if (lastScriptContent.includes('obf-email')) {
        html = html.replace(/document\.querySelectorAll\('.obf-email'\)/, mobileNavCode + '\n\n' + "document.querySelectorAll('.obf-email')");
      } else {
        inserts += mobileNavCode;
      }
      changed = true;
    }
    if (!lastScriptContent.includes('obf-email')) {
      // 在 backToTop 之前插入
      if (lastScriptContent.includes('backToTop')) {
        html = html.replace(/window\.addEventListener\('scroll'/, obfEmailCode + '\n\nwindow.addEventListener(\'scroll\'');
      } else {
        inserts += obfEmailCode;
      }
      changed = true;
    }
    if (!lastScriptContent.includes('backToTop')) {
      inserts += backToTopCode;
      changed = true;
    }
    
    if (inserts) {
      html = html.substring(0, lastScriptEnd) + inserts + html.substring(lastScriptEnd);
    }
  }
  
  if (changed) {
    fs.writeFileSync(filePath, html, 'utf8');
    return 'fixed';
  }
  return 'ok';
}

// 处理所有目录
const dirs = [
  { dir: '.', label: 'Root' },
  { dir: 'blog', label: 'EN Blog' },
  { dir: 'ja', label: 'JA Core' },
  { dir: 'ja/blog', label: 'JA Blog' },
];

dirs.forEach(({ dir, label }) => {
  if (!fs.existsSync(dir)) return;
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));
  let fixed = 0, ok = 0, err = 0;
  
  files.forEach(f => {
    const filePath = path.join(dir, f);
    const result = fixFile(filePath);
    if (result === 'fixed') fixed++;
    else if (result === 'ok') ok++;
    else { console.log('  ERROR: ' + f + ' - ' + result); err++; }
  });
  
  console.log(label + ': ' + files.length + ' files — fixed=' + fixed + ', ok=' + ok + ', err=' + err);
});
