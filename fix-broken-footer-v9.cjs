// fix-broken-footer-v9.cjs
// 直接用 indexOf + substring 修复 footer-copy 内的 broken script

const fs = require('fs');

const files = [
  'blog/baidu-2025-earnings-geo.html',
  'blog/baidu-brand-zone-material-pre-review.html',
  'blog/baidu-feed-account-structure.html',
  'blog/baidu-keyword-match-types-guide.html',
  'blog/baidu-ppc-account-status-guide.html',
  'blog/baidu-ppc-terms-explained.html',
  'blog/baidu-url-wildcard-guide.html',
  'blog/can-i-do-baidu-ppc.html',
  'blog/china-internet-numbers-2025.html',
  'blog/digital-consumer-9trillion.html',
  'blog/feed-landing-page-optimization.html',
  'blog/how-much-does-baidu-ppc-cost.html',
  'blog/landing-page-bounce-rate.html',
  'blog/search-vs-ai-usage.html'
];

let fixed = 0;

files.forEach(f => {
  if (!fs.existsSync(f)) {
    console.log(`⏭️  Not found: ${f}`);
    return;
  }
  let html = fs.readFileSync(f, 'utf8');

  // 找到 broken footer-copy: <div class="footer-copy">© <script>...toggleLangMenu...
  const startIdx = html.indexOf('<div class="footer-copy">');
  if (startIdx === -1) {
    console.log(`⏭️  No footer-copy: ${f}`);
    return;
  }

  // 找到 </div> 结束 footer-copy（在 </script> Baidu PPC Pro 之后）
  // 结构：<div class="footer-copy">© <script>...\n  };\n  </script> Baidu PPC Pro. All rights reserved.</div>
  const scriptEndIdx = html.indexOf('</script> Baidu PPC Pro. All rights reserved.', startIdx);
  if (scriptEndIdx === -1) {
    console.log(`⚠️  Pattern not found: ${f}`);
    return;
  }

  const endIdx = html.indexOf('</div>', scriptEndIdx);
  if (endIdx === -1) {
    console.log(`⚠️  Closing div not found: ${f}`);
    return;
  }

  // 替换整个 broken footer-copy
  const before = html.substring(0, startIdx);
  const after = html.substring(endIdx + 6); // +6 for </div>
  const corrected = '<div class="footer-copy">&copy; <script>document.write(new Date().getFullYear())</script> Baidu PPC Pro. All rights reserved.</div>\n';

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

  fs.writeFileSync(f, html, 'utf8');
  fixed++;
  console.log(`✅ ${f}`);
});

console.log(`\n=== Done: ${fixed}/${files.length} ===`);
