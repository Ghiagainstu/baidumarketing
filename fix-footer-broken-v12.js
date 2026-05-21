// fix-footer-broken-v12.js
// 正确修复 footer-copy 内错误嵌套 JS 的问题

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
  // 修复：footer-copy 内的 <script> 标签包含了 toggleLangMenu 函数
  // 正确做法：<script> 里只保留 document.write(new Date().getFullYear())
  // ============================================================

  const footerCopyIdx = html.indexOf('<div class="footer-copy">');
  if (footerCopyIdx === -1) {
    console.log(`⏭️  No footer-copy: ${file}`);
    skipped++;
    return;
  }

  // 在 footer-copy 区域内查找 <script>
  const afterFooterCopy = html.substring(footerCopyIdx);
  const scriptIdx = afterFooterCopy.indexOf('<script>');
  if (scriptIdx === -1) {
    console.log(`⏭️  No <script> in footer-copy: ${file}`);
    skipped++;
    return;
  }

  // 检查 <script> 是否包含 toggleLangMenu（broken）
  const scriptContent = afterFooterCopy.substring(scriptIdx + '<script>'.length);
  const scriptEndIdx = scriptContent.indexOf('</script>');
  if (scriptEndIdx === -1) {
    console.log(`⏭️  No </script> found: ${file}`);
    skipped++;
    return;
  }

  const scriptBody = scriptContent.substring(0, scriptEndIdx);
  if (!scriptBody.includes('function toggleLangMenu()')) {
    // 已经修复过了
    // 检查是否有 footer-lang
    if (!html.includes('footer-lang')) {
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
  // 替换 <script>...</script> 为 <script>document.write(new Date().getFullYear())</script>
  const beforeScript = afterFooterCopy.substring(0, scriptIdx);
  const afterScript = afterFooterCopy.substring(scriptIdx + '<script>'.length + scriptEndIdx + '</script>'.length);

  const correctedScript = `<script>document.write(new Date().getFullYear())</script>`;
  const correctedFooterCopy = html.substring(footerCopyIdx, footerCopyIdx + '<div class="footer-copy">'.length)
                           + correctedScript
                           + afterScript;

  html = html.substring(0, footerCopyIdx) + correctedFooterCopy;

  // 添加 footer-lang（在 footer-social 前）
  if (!html.includes('footer-lang')) {
    const footerLang = `\n    <div class="footer-lang"><a href="/blog/${slug}">English</a> | <a href="/ja/blog/${slug}">日本語</a></div>\n    `;
    html = html.replace(/(<div class="footer-social">)/, footerLang + '$1');
  }

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
