// fix-broken-footer-v8.cjs
// 修复 footer-copy 内错误嵌套 <script> 的问题

const fs = require('fs');
const path = require('path');

const files = [
  'blog/baidu-2025-earnings-geo.html',
  'blog/baidu-brand-zone-material-pre-review.html',
  'blog/baidu-feed-account-structure.html',
  'blog/baidu-keyword-match-types-guide.html',
  'blog/baidu-ppc-account-status-guide.html',
  'blog/baidu-ppc-terms-explained.html',
  'blog/baidu-search-video-format-guide.html',
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
  let modified = false;

  // 修复 footer-copy 内的 broken script
  // 匹配：<div class="footer-copy">© <script>...</script> Baidu PPC Pro. All rights reserved.</div>
  const brokenPattern = /<div class="footer-copy">\s*&copy; <script>document\.write\(new Date\(\)\.getFullYear\(\)\)\s*function toggleLangMenu[\s\S]*?<\/script> Baidu PPC Pro\. All rights reserved\.<\/div>/;

  if (brokenPattern.test(html)) {
    html = html.replace(brokenPattern, '<div class="footer-copy">&copy; <script>document.write(new Date().getFullYear())<\/script> Baidu PPC Pro. All rights reserved.</div>');
    modified = true;
  }

  // 如果已修复，确保 toggleLangMenu 函数在正确的位置（body 末尾的 <script> 里）
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
    // 在最后一个 </script> 之前插入
    const lastScriptIdx = html.lastIndexOf('</script>');
    if (lastScriptIdx !== -1) {
      html = html.slice(0, lastScriptIdx) + toggleCode + '  ' + html.slice(lastScriptIdx);
    }
  }

  if (modified) {
    fs.writeFileSync(f, html, 'utf8');
    fixed++;
    console.log(`✅ ${f}`);
  } else {
    console.log(`⚠️ No change: ${f}`);
  }
});

console.log(`\n=== Done: ${fixed}/${files.length} ===`);
