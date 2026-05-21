// fix-blog-nav-footer-v7.cjs
// 直接字符串替换，修复 nav 和 footer

const fs = require('fs');
const path = require('path');

const blogDir = 'blog';
const files = fs.readdirSync(blogDir).filter(f => f.endsWith('.html'));

let fixed = 0;
let errs = 0;

files.forEach(file => {
  const filePath = path.join(blogDir, file);
  let html = fs.readFileSync(filePath, 'utf8');
  let modified = false;
  const slug = file.replace('.html', '');

  // ============================================================
  // 修复 Nav：在 nav-mobile-toggle 前插入 nav-right-group
  // ============================================================
  if (!html.includes('nav-right-group')) {
    const navCtaPattern = /(<a href="\/contact\.html" class="nav-cta">Get Started &rarr;<\/a>\s*)/;
    if (navCtaPattern.test(html)) {
      const navRightGroup = `<div class="nav-right-group">
      <div class="lang-switch">
        <button class="lang-switch-btn" onclick="toggleLangMenu()" aria-label="Language">
          🇺🇸
          <svg width="10" height="6" viewBox="0 0 10 6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M1 1l4 4 4-4"/></svg>
        </button>
        <div class="lang-switch-menu" id="langSwitchMenu">
            <a href="/blog/${slug}" lang="en" class="lang-switch-item">🇺🇸 English</a>
            <a href="/ja/blog/${slug}" lang="ja" class="lang-switch-item">🇯🇵 日本語</a>
        </div>
      </div>
      \n      <a href="/contact.html" class="nav-cta">Get Started &rarr;</a>
      </div>
      `;
      html = html.replace(navCtaPattern, navRightGroup + '\n    ');
      modified = true;
    }
  }

  // ============================================================
  // 修复 Footer：移除 footer-copy 内的 JS，添加 footer 语言链接
  // ============================================================
  
  // 移除 footer-copy 里的 <script>...</script> 块
  const brokenFooterPattern = /(<div class="footer-copy">\s*&copy; <script>document\.write\(new Date\(\)\.getFullYear\(\)\)\s*)([\s\S]*?)(\s*<\/script> Baidu PPC Pro\. All rights reserved\.<\/div>)/;
  if (brokenFooterPattern.test(html)) {
    html = html.replace(brokenFooterPattern, '$1$3');
    modified = true;
  }

  // 添加 footer 语言链接（在 footer-social 之前）
  if (!html.includes('footer-lang') && html.includes('footer-bottom')) {
    const footerLang = `\n    <div class="footer-lang"><a href="/blog/${slug}">English</a> | <a href="/ja/blog/${slug}">日本語</a></div>\n    `;
    html = html.replace(/(<div class="footer-social">)/, footerLang + '$1');
    modified = true;
  }

  // ============================================================
  // 添加/修复 toggleLangMenu() 函数（在末尾 <script> 里）
  // ============================================================
  
  // 检查是否已有正确的 toggleLangMenu（在 body 末尾的 script 里，不在 footer 里）
  const hasToggleInBody = (html.match(/<script>/g) || []).length > 1;
  
  if (modified && !html.includes('function toggleLangMenu()')) {
    // 在文件末尾的 </script> 前添加 toggleLangMenu 函数
    const toggleCode = `
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
    // 找到最后一个 </script> 之前插入
    const lastScriptIdx = html.lastIndexOf('</script>');
    if (lastScriptIdx !== -1) {
      html = html.slice(0, lastScriptIdx) + toggleCode + '  ' + html.slice(lastScriptIdx);
      modified = true;
    }
  }

  // ============================================================
  // 写入
  // ============================================================
  if (modified) {
    fs.writeFileSync(filePath, html, 'utf8');
    fixed++;
    console.log(`✅ ${file}`);
  } else {
    console.log(`⏭️  ${file}`);
  }
});

console.log(`\n=== Done: ${fixed}/${files.length} ===`);
