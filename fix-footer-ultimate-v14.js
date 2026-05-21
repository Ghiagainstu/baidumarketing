// fix-footer-ultimate-v14.js
// 用计数器正确找到 footer-copy 的结束 </div>，然后整个替换

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
  
  // 找到 <div class="footer-copy"> 的位置
  const footerCopyIdx = html.indexOf('<div class="footer-copy">');
  if (footerCopyIdx === -1) {
    console.log(`⏭️  No footer-copy: ${file}`);
    skipped++;
    return;
  }
  
  // 用计数器找匹配的 </div>
  let divCount = 0;
  let searchIdx = footerCopyIdx;
  let footerCopyEndIdx = -1;
  
  while (searchIdx < html.length) {
    const nextDiv = html.indexOf('<div', searchIdx);
    const nextClose = html.indexOf('</div>', searchIdx);
    
    if (nextClose === -1) break;
    
    // 检查是否是 <div class="footer-copy"> 本身
    if (nextDiv !== -1 && nextDiv <= nextClose) {
      // <div> 在 </div> 之前，是新的 div 开始
      divCount++;
      searchIdx = nextDiv + 1;
    } else {
      // </div> 在 <div> 之前，是 div 结束
      divCount--;
      if (divCount === 0) {
        footerCopyEndIdx = nextClose;
        break;
      }
      searchIdx = nextClose + 1;
    }
  }
  
  if (footerCopyEndIdx === -1) {
    console.log(`⚠️  Could not find closing </div> for footer-copy: ${file}`);
    skipped++;
    return;
  }
  
  // 现在：footerCopyIdx 到 footerCopyEndIdx + '</div>'.length 是完整的 footer-copy div
  const footerCopyFull = html.substring(footerCopyIdx, footerCopyEndIdx + '</div>'.length);
  
  // 检查是否 broken（包含 toggleLangMenu）
  if (!footerCopyFull.includes('function toggleLangMenu(') && !footerCopyFull.includes('footer-lang')) {
    // 已经修复过了
    // 检查是否有 footer-lang
    if (!html.includes('footer-lang')) {
      // 需要添加 footer-lang
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
  // 构造正确的 footer-copy（不包含 footer-lang 和 footer-social）
  const correctedFooterCopy = `<div class="footer-copy">&copy; <script>document.write(new Date().getFullYear())</script> Baidu PPC Pro. All rights reserved.</div>\n`;
  
  // 提取 footer-lang 和 footer-social（从 broken footer-copy 里）
  let footerLang = '';
  let footerSocial = '';
  
  if (footerCopyFull.includes('footer-lang')) {
    const langIdx = footerCopyFull.indexOf('<div class="footer-lang">');
    const nextDiv = footerCopyFull.indexOf('</div>', langIdx + '<div class="footer-lang">'.length);
    if (nextDiv !== -1) {
      footerLang = footerCopyFull.substring(langIdx, nextDiv + '</div>'.length) + '\n';
    }
  }
  
  if (footerCopyFull.includes('footer-social')) {
    const socialIdx = footerCopyFull.indexOf('<div class="footer-social">');
    const nextClose = footerCopyFull.indexOf('</div>', socialIdx + '<div class="footer-social">'.length);
    if (nextClose !== -1) {
      footerSocial = footerCopyFull.substring(socialIdx, nextClose + '</div>'.length) + '\n';
    }
  }
  
  // 如果没有找到 footer-lang，使用默认的
  if (!footerLang) {
    footerLang = `<div class="footer-lang"><a href="/blog/${slug}">English</a> | <a href="/ja/blog/${slug}">日本語</a></div>\n`;
  }
  
  // 替换整个 broken footer-copy 为正确的
  const before = html.substring(0, footerCopyIdx);
  const after = html.substring(footerCopyEndIdx + '</div>'.length);
  const corrected = correctedFooterCopy + '    ' + footerLang + '    ' + footerSocial;
  
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
