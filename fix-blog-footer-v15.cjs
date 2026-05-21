// fix-blog-footer-v15.cjs - 精确修复博客文件的 footer 问题
const fs = require('fs');
const path = process.argv[2];

if (!path) {
  console.error('Usage: node fix-blog-footer-v15.cjs <file-path>');
  process.exit(1);
}

let html = fs.readFileSync(path, 'utf8');
const slug = path.split('/').pop().replace('.html', '');

// === 步骤1: 提取正确的 footer-top (保留不变) ===
const footerStart = html.indexOf('<footer>');
const footerTopEnd = html.indexOf('<div class="footer-bottom">');

if (footerStart === -1 || footerTopEnd === -1) {
  console.log(`  ❌ 未找到 <footer> 或 <div class="footer-bottom"> in ${path}`);
  process.exit(1);
}

const footerOpen = html.substring(footerStart, footerTopEnd);

// === 步骤2: 构建正确的 footer-bottom ===
const correctFooterBottom = `  <div class="footer-bottom">
    <div class="footer-copy">&copy; <script>document.write(new Date().getFullYear())</script> Baidu PPC Pro. All rights reserved.</div>
    <div class="footer-lang"><a href="/blog/${slug}">English</a> | <a href="/ja/blog/${slug}">日本語</a></div>
    <div class="footer-social"><a href="#" class="obf-email-icon" data-u="baidu" data-d="baidumarketing.com" aria-label="Email"><svg viewBox="0 0 24 24" fill="none" stroke="#D1D5DB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="22,4 12,13 2,4"/></svg></a></div>
  </div>
</div>
</footer>
`;

// === 步骤3: 找到 </footer> 之后的内容 ===
const afterFooterStart = html.indexOf('</footer>') + '</footer>'.length;
const afterFooter = html.substring(afterFooterStart);

// === 步骤4: 重新组装 HTML ===
html = footerOpen + correctFooterBottom + afterFooter;

// === 步骤5: 确保 toggleLangMenu 函数在 <script> 标签中 ===
if (!html.includes('function toggleLangMenu()')) {
  const toggleLangMenuCode = `
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
  
  // 找到最后一个 <script> 标签的 </script> 之前
  const lastScriptEnd = html.lastIndexOf('</script>');
  if (lastScriptEnd !== -1) {
    // 检查这个 </script> 是否在 </body> 之前
    const bodyEnd = html.indexOf('</body>');
    if (bodyEnd === -1 || lastScriptEnd < bodyEnd) {
      html = html.substring(0, lastScriptEnd) + toggleLangMenuCode + '\n' + html.substring(lastScriptEnd);
      console.log(`  ✅ 添加 toggleLangMenu() 函数`);
    }
  }
}

// === 步骤6: 检查并修复 title 长度 ===
const titleMatch = html.match(/<title>(.*?)<\/title>/);
if (titleMatch) {
  const title = titleMatch[1];
  if (title.length > 70) {
    // 尝试智能缩短
    const parts = title.split(' — ');
    if (parts.length > 1) {
      const mainTitle = parts[0];
      const suffix = parts[parts.length - 1];
      if (mainTitle.length > 60) {
        const newTitle = mainTitle.substring(0, 57) + '... — ' + suffix;
        html = html.replace(/<title>.*?<\/title>/, `<title>${newTitle}</title>`);
        console.log(`  ✅ 缩短 title: ${title.length} → ${newTitle.length} 字符`);
      }
    }
  }
}

fs.writeFileSync(path, html, 'utf8');
console.log(`✅ 修复完成: ${path}`);
console.log(`   - footer-bottom 已修复`);
console.log(`   - footer-lang 已统一 (1个)`);
