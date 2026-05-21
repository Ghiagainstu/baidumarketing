// fix-all-blog-footer-v11.cjs
// 正确修复 footer-copy 内的 broken JS

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

  // ==========================================================
  // 修复1: footer-copy 内的 broken <script>
  // 正确的 footer-copy：&copy; <script>...</script> Text</div>
  // Broken：<script> 里包含 toggleLangMenu 函数定义
  // ==========================================================
  
  const footerCopyIdx = html.indexOf('<div class="footer-copy">');
  if (footerCopyIdx !== -1) {
    // 找到 footer-copy 的结束 </div>
    const afterFooterCopy = html.substring(footerCopyIdx + '<div class="footer-copy">'.length);
    // 找到下一个 </div>（footer-copy 的结束标签）
    const endDivIdx = afterFooterCopy.indexOf('</div>');
    if (endDivIdx !== -1) {
      const footerContent = afterFooterCopy.substring(0, endDivIdx);
      // 检查是否包含 toggleLangMenu 函数定义（broken）
      if (footerContent.includes('function toggleLangMenu') || footerContent.includes('document.addEventListener')) {
          // 替换整个 footer-copy 内容
          const slug = file.replace('.html', '');
          const corrected = `&copy; <script>document.write(new Date().getFullYear())</script> Baidu PPC Pro. All rights reserved.`;
          html = html.substring(0, footerCopyIdx + '<div class="footer-copy">'.length) 
                 + corrected 
                 + html.substring(footerCopyIdx + '<div class="footer-copy">'.length + endDivIdx + '</div>'.length);
          modified = true;
        }
    }
  }

  // ==========================================================
  // 修复2: 添加 footer-lang（在 footer-social 前）
  // ==========================================================
  if (!html.includes('footer-lang') && html.includes('footer-bottom')) {
    const slug = file.replace('.html', '');
    const footerLang = `\n    <div class="footer-lang"><a href="/blog/${slug}">English</a> | <a href="/ja/blog/${slug}">日本語</a></div>\n    `;
    html = html.replace(/(<div class="footer-social">)/, footerLang + '$1');
    modified = true;
  }

  // ==========================================================
  // 修复3: 确保 toggleLangMenu 函数在 body 末尾的 <script> 里
  // ==========================================================
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

  // 写入
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
