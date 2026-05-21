// fix-footer-bottom-v13.js
// 整个替换 <footer-bottom> 区块为正确结构

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
  
  // 找到 <footer-bottom> 开始位置
  const bottomStart = html.indexOf('<div class="footer-bottom">');
  if (bottomStart === -1) {
    console.log(`⏭️  No footer-bottom: ${file}`);
    skipping++;
    return;
  }
  
  // 找到 </footer> 的位置（footer 结束）
  const footerEnd = html.indexOf('</footer>');
  if (footerEnd === -1) {
    console.log(`⚠️  </footer> not found: ${file}`);
    skipping++;
    return;
  }
  
  // 找到 footer-bottom 的结束 </div>（在 </footer> 之前）
  // footer-bottom 包含：footer-copy + footer-lang + footer-social + 结束 </div>
  // 结构：<div class="footer-bottom"> ... </div> (然后是 </footer>)
  
  // 从 bottomStart 开始，找匹配的 </div>
  let divCount = 0;
  let searchIdx = bottomStart;
  let bottomEnd = -1;
  
  while (searchIdx < footerEnd) {
    const nextDiv = html.indexOf('<div', searchIdx);
    const nextClose = html.indexOf('</div>', searchIdx);
    
    if (nextClose === -1) break;
    
    // 检查是否是 footer-bottom 的结束标签
    // footer-bottom 包含 3 个直接子 div：footer-copy, footer-lang, footer-social
    // 所以 divCount 应该是：遇到 <div> +1，遇到 </div> -1，当 divCount == 0 时就是 footer-bottom 的结束
    
    // 重新计算：从 bottomStart + '<div class="footer-bottom">'.length 开始
    // 遇到 <div 且不是 </div> 时 +1，遇到 </div> 时 -1
    
    break; // 退出，用简单方式
  }
  
  // 简单方式：直接构造正确的 footer-bottom，替换从 bottomStart 到 footerEnd 之前的内容
  const before = html.substring(0, bottomStart);
  const after = html.substring(footerEnd); // 从 </footer> 开始
  
  // 正确的 footer-bottom 结构
  const correctBottom = `<div class="footer-bottom">
    <div class="footer-copy">&copy; <script>document.write(new Date().getFullYear())</script> Baidu PPC Pro. All rights reserved.</div>
    <div class="footer-lang"><a href="/blog/${slug}">English</a> | <a href="/ja/blog/${slug}">日本語</a></div>
    <div class="footer-social"><a href="#" class="obf-email-icon" data-u="baidu" data-d="baidumarketing.com" aria-label="Email"><svg viewBox="0 0 24 24" fill="none" stroke="#D1D5DB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="22,4 12,13 2,4"/></svg></a></div>
  </div>
</footer>`;
  
  // 需要保留 footer-top，只替换 footer-bottom 到 </footer> 的部分
  // 找到 footer-top 的结束位置（</div> 后面是 footer-bottom）
  const topEnd = html.lastIndexOf('</div>', bottomStart);
  
  if (topEnd === -1) {
    console.log(`⚠️  footer-top end not found: ${file}`);
    skipping++;
    return;
  }
  
  // 重新构造
  const beforeTop = html.substring(0, topEnd + '</div>'.length);
  const corrected = beforeTop + '\n' + correctBottom;
  
  // 检查是否有变化
  if (corrected === html) {
    console.log(`⏭️  Already correct: ${file}`);
    skipping++;
    return;
  }
  
  fs.writeFileSync(filePath, corrected, 'utf8');
  fixed++;
  console.log(`✅ ${file}`);
});

console.log(`\n=== Done: ${fixed} fixed, ${skipping} skipped ===`);
