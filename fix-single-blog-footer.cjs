// fix-single-blog-footer.cjs - 精确修复单个博客文件的 footer 和 script
const fs = require('fs');
const path = process.argv[2];

if (!path) {
  console.error('Usage: node fix-single-blog-footer.cjs <file-path>');
  process.exit(1);
}

let html = fs.readFileSync(path, 'utf8');

// 1. 找到并替换损坏的 footer-bottom 部分
// 损坏的特征：<div class="footer-copy"> 包含了 toggleLangMenu 函数定义
const badFooterCopyStart = '<div class="footer-copy">&copy; <script>document.write(new Date().getFullYear())\n  function toggleLangMenu() {';

const slug = path.split('/').pop().replace('.html', '');

const goodFooterBottom = `<div class="footer-bottom">
    <div class="footer-copy">&copy; <script>document.write(new Date().getFullYear())</script> Baidu PPC Pro. All rights reserved.</div>
    <div class="footer-lang"><a href="/blog/${slug}">English</a> | <a href="/ja/blog/${slug}">日本語</a></div>
    <div class="footer-social"><a href="#" class="obf-email-icon" data-u="baidu" data-d="baidumarketing.com" aria-label="Email"><svg viewBox="0 0 24 24" fill="none" stroke="#D1D5DB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="22,4 12,13 2,4"/></svg></a></div>
  </div>`;

// 找到 footer-copy 的错误开头到 </footer> 之前的所有内容
const footerBottomStart = html.indexOf('<div class="footer-bottom">');
if (footerBottomStart === -1) {
  console.log(`  ❌ 未找到 <div class="footer-bottom"> in ${path}`);
  process.exit(1);
}

// 找到 </footer> 的位置
const footerEnd = html.indexOf('</footer>');
if (footerEnd === -1) {
  console.log(`  ❌ 未找到 </footer> in ${path}`);
  process.exit(1);
}

// 替换从 footer-bottom 开始到 </footer> 之前的内容
const beforeFooter = html.substring(0, footerBottomStart);
const afterFooter = html.substring(footerEnd);

// 重新组装
html = beforeFooter + goodFooterBottom + '\n</div>\n</footer>' + afterFooter;

// 2. 在 <script> 标签内添加缺失的 toggleLangMenu 函数
// 检查是否已有 toggleLangMenu 定义
if (!html.includes('function toggleLangMenu()')) {
  // 在 </script> 之前添加 toggleLangMenu 函数
  const scriptEnd = html.lastIndexOf('</script>');
  if (scriptEnd !== -1) {
    const toggleLangMenuCode = `\n\nfunction toggleLangMenu() {
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
    
    html = html.substring(0, scriptEnd) + toggleLangMenuCode + html.substring(scriptEnd);
    console.log(`  ✅ 添加 toggleLangMenu() 函数`);
  }
}

// 3. 检查并修复 title 长度 (<=70 字符)
const titleMatch = html.match(/<title>(.*?)<\/title>/);
if (titleMatch) {
  const title = titleMatch[1];
  if (title.length > 70) {
    // 尝试缩短
    const shortTitle = title.substring(0, 67) + '...';
    html = html.replace(/<title>.*?<\/title>/, `<title>${shortTitle}</title>`);
    console.log(`  ✅ 缩短 title: ${title.length} → ${shortTitle.length} 字符`);
  }
}

fs.writeFileSync(path, html, 'utf8');
console.log(`  ✅ 修复完成: ${path}`);
console.log(`  ✅ footer-bottom 已修复`);
console.log(`  ✅ footer-lang 已统一（1个）`);
