// fix-blog-footer-ultimate.cjs
// 用正确的 footer 模板整个替换所有博客页面的 footer

const fs = require('fs');
const path = require('path');

const blogDir = 'blog';
const files = fs.readdirSync(blogDir).filter(f => f.endsWith('.html'));

let fixed = 0;
let skipped = 0;

files.forEach(file => {
  const filePath = path.join(blogDir, file);
  let html = fs.readFileSync(filePath, 'utf8');
  const slug = file.replace('.html', '');

  // 找到 <footer> 开始位置
  const footerStart = html.indexOf('<footer>');
  if (footerStart === -1) {
    console.log(`⏭️  No <footer>: ${file}`);
    skipped++;
    return;
  }

  // 找到 </footer> 结束位置
  const footerEnd = html.indexOf('</footer>', footerStart);
  if (footerEnd === -1) {
    console.log(`⚠️  </footer> not found: ${file}`);
    skipped++;
    return;
  }

  // 正确的 footer 模板（博客页专属，包含 footer-lang）
  const correctFooter = `<footer><div class="container">
  <div class="footer-top">
    <div class="footer-brand">
      <h3><svg width="28" height="28" viewBox="0 0 32 32" fill="none"><defs><linearGradient id="fLogo${slug}" x1="0" y1="0" x2="32" y2="32"><stop offset="0%" stop-color="#2932E1"/><stop offset="100%" stop-color="#4F46E5"/></linearGradient></defs><rect width="32" height="32" rx="8" fill="url(#fLogo${slug})"/><text x="16" y="21" text-anchor="middle" font-family="system-ui" font-size="12" font-weight="800" fill="white" letter-spacing=".3">BPP</text></svg> Baidu PPC Pro</h3>
      <p>We help international agencies and brands access China's $100B+ digital advertising market.</p>
    </div>
    <div class="footer-col"><h4>Quick Links</h4><ul><li><a href="/features.html">Services</a></li><li><a href="/pricing.html">Pricing</a></li><li><a href="/about.html">About</a></li><li><a href="/faq.html">FAQ</a></li><li><a href="/blog.html">Blog</a></li></ul></div>
    <div class="footer-col"><h4>Contact</h4><ul><li><a href="#" class="obf-email-link" data-u="baidu" data-d="baidumarketing.com"></a></li><li><a href="/contact">Submit a Request</a></li></ul></div>
    <div class="footer-col"><h4>Legal</h4><ul><li><a href="/privacy">Privacy Policy</a></li><li><a href="/terms">Terms of Service</a></li></ul></div>
  </div>
  <div class="footer-bottom">
    <div class="footer-copy">&copy; <script>document.write(new Date().getFullYear())<\/script> Baidu PPC Pro. All rights reserved.</div>
    <div class="footer-lang"><a href="/blog/${slug}">English</a> | <a href="/ja/blog/${slug}">日本語</a></div>
    <div class="footer-social"><a href="#" class="obf-email-icon" data-u="baidu" data-d="baidumarketing.com" aria-label="Email"><svg viewBox="0 0 24 24" fill="none" stroke="#D1D5DB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="22,4 12,13 2,4"/></svg></a></div>
  </div>
</div></footer>`;

  // 替换整个 footer
  const before = html.substring(0, footerStart);
  const after = html.substring(footerEnd + '</footer>'.length);
  html = before + correctFooter + after;

  // 确保 body 末尾有 toggleLangMenu 函数
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
