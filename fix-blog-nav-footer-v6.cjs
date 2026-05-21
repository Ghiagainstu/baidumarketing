// fix-blog-nav-footer-v6.cjs
// 批量修复博客页面的 nav 和 footer 问题
// 1. 添加 nav-right-group + lang-switch + nav-cta
// 3. 将 toggleLangMenu() 函数从 footer-copy 中移除，放到正确的 <script> 位置

const fs = require('fs');
const path = require('path');

const blogDir = 'blog';
const files = fs.readdirSync(blogDir).filter(f => f.endsWith('.html'));

let fixed = 0;
let errors = 0;

files.forEach(file => {
  const filePath = path.join(blogDir, file);
  let html = fs.readFileSync(filePath, 'utf8');
  let modified = false;

  // ============================================================
  // 修复 1: Nav - 添加 nav-right-group + lang-switch + nav-cta
  // ============================================================
  
  if (!html.includes('nav-right-group')) {
    // 找到 </div>\n</nav> 或 </div></nav> 之前的位置（nav-inner 结束前）
    // 在 nav-mobile-toggle 之前插入 nav-right-group
    
    const navTogglePattern = /(<button class="nav-mobile-toggle"[\s\S]*?<\/button>)/;
    if (navTogglePattern.test(html)) {
      const navRightGroup = `\n      <div class="nav-right-group">\n      <div class="lang-switch">\n        <button class="lang-switch-btn" onclick="toggleLangMenu()" aria-label="Language">\n          🇺🇸\n          <svg width="10" height="6" viewBox="0 0 10 6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M1 1l4 4 4-4"/></svg>\n        </button>\n        <div class="lang-switch-menu" id="langSwitchMenu">\n            <a href="/blog/${file.replace('.html', '')}" lang="en" class="lang-switch-item">🇺🇸 English</a>\n            <a href="/ja/blog/${file.replace('.html', '')}" lang="ja" class="lang-switch-item">🇯🇵 日本語</a>\n        </div>\n      </div>\n      \n      <a href="/contact.html" class="nav-cta">Get Started &rarr;</a>\n      </div>\n      `;
      
      html = html.replace(navTogglePattern, navRightGroup + '\n    $1');
      modified = true;
    }
  }

  // 如果 nav-cta 在 nav-inner 里但不是在 nav-right-group 里，需要移除（因为已经添加到 nav-right-group）
  // 先检查是否有单独的 nav-cta（不在 nav-right-group 里）
  if (html.includes('nav-right-group') && html.includes('class="nav-cta"')) {
    // 移除不在 nav-right-group 里的 nav-cta
    html = html.replace(/(?<!<div class="nav-right-group">[\s\S]*?)<a href="\/contact\.html" class="nav-cta">Get Started &rarr;<\/a>\s*\n/g, '');
    modified = true;
  }

  // ============================================================
  // 修复 2: Footer - 移除 footer-copy 内的 JS，添加 footer 语言链接
  // ============================================================
  
  // 检查 footer-copy 是否有错误的 JS
  if (html.includes('toggleLangMenu()') && html.includes('footer-copy')) {
    // 从 footer-copy 中移除整个 <script> 块
    // 先找到 footer-copy 的位置
    const footerCopyPattern = /(<div class="footer-copy">\s*&copy; <script>document\.write\(new Date\(\)\.getFullYear\(\)\)\s*)([\s\S]*?)(\s*<\/script> Baidu PPC Pro\. All rights reserved\.<\/div>)/;
    
    if (footerCopyPattern.test(html)) {
      html = html.replace(footerCopyPattern, '$1$3');
      modified = true;
    }
  }

  // 添加 footer 语言链接（在 footer-bottom 里，footer-social 之前）
  if (!html.includes('footer-lang') && html.includes('footer-bottom')) {
    const footerLang = `\n    <div class="footer-lang"><a href="/blog/${file.replace('.html', '')}">English</a> | <a href="/ja/blog/${file.replace('.html', '')}">日本語</a></div>\n    `;
    html = html.replace(/(<div class="footer-social">)/, footerLang + '$1');
    modified = true;
  }

  // ============================================================
  // 修复 3: 将 toggleLangMenu() 函数放到正确的位置
  // ============================================================
  
  // 检查是否已有正确的 toggleLangMenu 函数（在 </body> 之前的 <script> 里）
  const hasCorrectToggle = html.includes('function toggleLangMenu()') && !html.includes('footer-copy > script');
  
  if (!hasCorrectToggle && html.includes('toggleLangMenu()')) {
    // 需要添加正确的 toggleLangMenu 函数
    // 先检查文件末尾是否有 <script> 块
    const scriptBlockPattern = /(<script>\s*let mobileNavOpen[\s\S]*?<\/script>)/;
    
    if (scriptBlockPattern.test(html)) {
      // 在现有 script 块末尾的 </script> 之前添加 toggleLangMenu 函数
      const toggleFunc = `
  function toggleLangMenu() {
    const menu = document.getElementById('langSwitchMenu');
    if (menu) menu.classList.toggle('active');
  }
  document.addEventListener('click', function(e) {
    const menu = document.getElementById('langSwitchMenu');
    const btn = document.querySelector('.lang-switch-btn');
    if (menu && btn && !btn.contains(e.target) && !menu.contains(e.target)) {
      menu.classList.remove('active');
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
`;
      html = html.replace(scriptBlockPattern, '$1' + toggleFunc + '</script>');
      modified = true;
    }
  }

  // ============================================================
  // 写入文件
  // ============================================================
  
  if (modified) {
    fs.writeFileSync(filePath, html, 'utf8');
    fixed++;
    console.log(`✅ Fixed: ${file}`);
  } else {
    console.log(`⏭️  Skipped (no changes): ${file}`);
  }
});

console.log(`\n=== Done ===`);
console.log(`Fixed: ${fixed} / ${files.length}`);
