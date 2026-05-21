// fix-blog-nav-footer-v10.cjs
// 简单直接：在 nav-mobile-toggle 前插入 nav-right-group

const fs = require('fs');
const path = require('path');

const blogDir = 'blog';
const files = fs.readdirSync(blogDir).filter(f => f.endsWith('.html'));

let fixed = 0;
let skipped = 0;

files.forEach(file => {
  const filePath = path.join(blogDir, file);
  let html = fs.readFileSync(filePath, 'utf8');
  let modified = false;
  const slug = file.replace('.html', '');

  // ============================================================
  // 修复1: 在 nav-mobile-toggle 前插入 nav-right-group
  // ============================================================
  if (!html.includes('nav-right-group')) {
    const target = '<button class="nav-mobile-toggle"';
    const idx = html.indexOf(target);
    if (idx !== -1) {
      const navRightGroup = `<div class="nav-right-group">\n      <div class="lang-switch">\n        <button class="lang-switch-btn" onclick="toggleLangMenu()" aria-label="Language">\n          🇺🇸\n          <svg width="10" height="6" viewBox="0 0 10 6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M1 1l4 4 4-4"/></svg>\n        </button>\n        <div class="lang-switch-menu" id="langSwitchMenu">\n            <a href="/blog/${slug}" lang="en" class="lang-switch-item">🇺🇸 English</a>\n            <a href="/ja/blog/${slug}" lang="ja" class="lang-switch-item">🇯🇵 日本語</a>\n        </div>\n      </div>\n      \n      <a href="/contact.html" class="nav-cta">Get Started &rarr;</a>\n      </div>\n      `;
      html = html.slice(0, idx) + navRightGroup + '\n    ' + html.slice(idx);
      modified = true;
    }
  }

  // ============================================================
  // 修复2: 移除 footer-copy 内的 broken JS
  // ============================================================
  const footerCopyIdx = html.indexOf('<div class="footer-copy">');
  if (footerCopyIdx !== -1) {
    // 检查是否有 broken JS（toggleLangMenu 在 footer-copy 内）
    const section = html.substring(footerCopyIdx, footerCopyIdx + 2000);
    if (section.includes('function toggleLangMenu()') || section.includes('document.addEventListener')) {
      // 找到 </script> Baidu PPC Pro. All rights reserved.</div> 的位置
      const endIdx = html.indexOf('</script> Baidu PPC Pro. All rights reserved.</div>', footerCopyIdx);
      if (endIdx !== -1) {
        const before = html.substring(0, footerCopyIdx);
        const after = html.substring(endIdx + '</script> Baidu PPC Pro. All rights reserved.</div>'.length);
        const corrected = `<div class="footer-copy">&copy; <script>document.write(new Date().getFullYear())</script> Baidu PPC Pro. All rights reserved.</div>\n`;
        html = before + corrected + after;
        modified = true;
      }
    }
  }

  // ============================================================
  // 修复3: 添加 footer-lang（在 footer-social 前）
  // ============================================================
  if (!html.includes('footer-lang') && html.includes('footer-bottom')) {
    const footerLang = `    <div class="footer-lang"><a href="/blog/${slug}">English</a> | <a href="/ja/blog/${slug}">日本語</a></div>\n    `;
    html = html.replace(/(<div class="footer-social">)/, footerLang + '$1');
    modified = true;
  }

  // ============================================================
  // 修复4: 添加 toggleLangMenu 函数到 body 末尾的 <script>
  // ============================================================
  if (modified && !html.includes('function toggleLangMenu()')) {
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
    const lastScriptIdx = html.lastIndexOf('</script>');
    if (lastScriptIdx !== -1) {
      html = html.slice(0, lastScriptIdx) + toggleCode + '  ' + html.slice(lastScriptIdx);
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
    skipped++;
    console.log(`⏭️  ${file}`);
  }
});

console.log(`\n=== Done: ${fixed} fixed, ${skipped} skipped ===`);
