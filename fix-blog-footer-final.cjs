// fix-blog-footer-final.cjs
// 正确修复所有博客页面的 footer-copy broken script 问题

const fs = require('fs');
const path = require('path');

const blogDir = 'blog';
const files = fs.readdirSync(blogDir).filter(f => f.endsWith('.html'));

let fixed = 0;
let skipped = 0;

files.forEach(file => {
  const filePath = path.join(blogDir, file);
  let html = fs.readFileSync(filePath, 'utf8');
  
  // 检查 footer-copy 是否包含 toggleLangMenu 函数定义（broken）
  const footerCopyIdx = html.indexOf('<div class="footer-copy">');
  if (footerCopyIdx === -1) {
    console.log(`⏭️  No footer-copy: ${file}`);
    skipped++;
    return;
  }
  
  const afterFooterCopy = html.substring(footerCopyIdx);
  if (!afterFooterCopy.includes('function toggleLangMenu()') && !afterFooterCopy.includes('document.addEventListener')) {
    // 已经修复过了
    // 检查是否有 footer-lang
    if (!html.includes('footer-lang')) {
      // 需要添加 footer-lang
      const slug = file.replace('.html', '');
      const footerLang = `\n    <div class="footer-lang"><a href="/blog/${slug}">English</a> | <a href="/ja/blog/${slug}">日本語</a></div>\n    `;
      html = html.replace(/(<div class="footer-social">)/, footerLang + '$1');
      fs.writeFileSync(filePath, html, 'utf8');
      fixed++;
      console.log(`✅ Added footer-lang: ${file}`);
    } else {
      console.log(`⏭️  Already fixed: ${file}`);
      skipped++;
    }
    return;
  }
  
  // Broken - 需要修复
  // 找到 </script> Baidu PPC Pro. All rights reserved.</div> 的位置
  const endPattern = '</script> Baidu PPC Pro. All rights reserved.</div>';
  const endIdx = html.indexOf(endPattern, footerCopyIdx);
  if (endIdx === -1) {
    console.log(`⚠️  Pattern not found: ${file}`);
    skipped++;
    return;
  }
  
  // 替换整个 broken footer-copy
  const before = html.substring(0, footerCopyIdx);
  const after = html.substring(endIdx + endPattern.length);
  const slug = file.replace('.html', '');
  const corrected = `<div class="footer-copy">&copy; <script>document.write(new Date().getFullYear())</script> Baidu PPC Pro. All rights reserved.</div>\n    <div class="footer-lang"><a href="/blog/${slug}">English</a> | <a href="/ja/blog/${slug}">日本語</a></div>\n    `;
  
  html = before + corrected + after;
  
  // 确保 toggleLangMenu 函数在 body 末尾的 <script> 里
  if (!html.includes('function toggleLangMenu()')) {
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
  
  fs.writeFileSync(filePath, html, 'utf8');
  fixed++;
  console.log(`✅ ${file}`);
});

console.log(`\n=== Done: ${fixed} fixed, ${skipped} skipped ===`);
