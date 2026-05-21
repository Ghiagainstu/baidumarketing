// fix-footer-broken-final.cjs
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
  
  // 检查是否有 broken footer（toggleLangMenu 在 footer-copy 内）
  const footerCopyIdx = html.indexOf('<div class="footer-copy">');
  if (footerCopyIdx === -1) {
    skipped++;
    return;
  }
  
  const afterFooterCopy = html.substring(footerCopyIdx);
  if (!afterFooterCopy.includes('function toggleLangMenu()')) {
    // 已经修复过了
    skipped++;
    return;
  }
  
  // 找到 <script> 开始的位置（在 footer-copy 内）
  const scriptIdx = afterFooterCopy.indexOf('<script>');
  if (scriptIdx === -1) {
    console.log(`⚠️  No <script> found: ${file}`);
    skipped++;
    return;
  }
  
  // 找到 </script> 的位置（关闭 footer-copy 内的 script 标签）
  const scriptEndIdx = afterFooterCopy.indexOf('</script>', scriptIdx);
  if (scriptEndIdx === -1) {
    console.log(`⚠️  No </script> found: ${file}`);
    skipped++;
    return;
  }
  
  // 找到 footer-copy 的结束 </div>
  // 在 </script> 之后，找下一个 </div>
  const afterScript = afterFooterCopy.substring(scriptEndIdx + '</script>'.length);
  const footerDivEndIdx = afterScript.indexOf('</div>');
  if (footerDivEndIdx === -1) {
    console.log(`⚠️  No closing </div> found: ${file}`);
    skipped++;
    return;
  }
  
  // 现在：
  // - footerCopyIdx = <div class="footer-copy"> 的位置
  // - scriptIdx = <script> 在 footer-copy 内的相对位置
  // - scriptEndIdx + footerDivEndIdx = </script>... 到 </div> 的位置
  
  // 实际上，整个 footer-copy 的内容是：
  // <div class="footer-copy">© <script>document.write(...)\n  function toggleLangMenu() {...}\n  ...\n  </script> Baidu PPC Pro. All rights reserved.</div>
  
  // 我要把 <div class="footer-copy"> 到 </div> 整个替换掉
  
  const absScriptIdx = footerCopyIdx + scriptIdx;
  const absFooterDivEnd = footerCopyIdx + scriptIdx + (scriptEndIdx - scriptIdx) + '</script>'.length + footerDivEndIdx + '</div>'.length;
  
  // 替换：从 <div class="footer-copy"> 到 </div>
  const before = html.substring(0, footerCopyIdx);
  const after = html.substring(absFooterDivEnd);
  
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
