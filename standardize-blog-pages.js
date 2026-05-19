// standardize-blog-pages.js
// 让所有blog页面与 baidu-brand-protection-guide.html 的CSS完全一致
// 1. 统一HTML类名（takeaway-box→takeaway, cta-section→cta-box, stat-box→stat-card 等）
// 2. 补全所有缺失的CSS定义

const fs = require('fs');
const path = require('path');

const BLOG_DIR = path.join(__dirname, 'blog');
const BASELINE = path.join(BLOG_DIR, 'baidu-brand-protection-guide.html');

// 读取基准页面，提取 <style> 内容
function extractStyle(html) {
  const match = html.match(/<style>([\s\S]*?)<\/style>/);
  return match ? match[1] : null;
}

// 从基准页面提取完整的组件CSS块（在 </style> 之前插入到目标页面）
// 策略：提取基准页面 <style> 中所有「通用组件」的CSS规则
// 然后追加到每个blog页面的 <style> 末尾

const baselineHtml = fs.readFileSync(BASELINE, 'utf8');
const baselineStyle = extractStyle(baselineHtml);

if (!baselineStyle) {
  console.error('无法提取基准页面CSS');
  process.exit(1);
}

// 需要统一的类名映射（旧→新）
const classMappings = [
  [/class="takeaway-box"/g, 'class="takeaway"'],
  [/class="takeaway-box\s/g, 'class="takeaway" '],
  [/class="cta-section"/g, 'class="cta-box"'],
  [/class="cta-section\s/g, 'class="cta-box" '],
  [/class="article-cta"/g, 'class="cta-box"'],
  [/class="article-cta\s/g, 'class="cta-box" '],
  [/class="stat-box"/g, 'class="stat-card"'],
  [/class="stat-box\s/g, 'class="stat-card" '],
];

// 补全的CSS（从基准页面提取的通用组件样式）
// 这些CSS会追加到每个页面的 <style> 末尾
const supplementalCSS = `
/* ===== Added by standardize-blog-pages.js ===== */
/* Stats Grid */
.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 40px 0; }
.stat-card { background: var(--gray-50); padding: 28px 20px; border-radius: var(--radius); text-align: center; border: 1px solid var(--gray-200); }
.stat-number { font-size: 2.2rem; font-weight: 800; color: var(--blue); margin-bottom: 6px; }
.stat-label { font-size: .85rem; color: var(--gray-600); }

/* Comparison Table */
.comparison-table { width: 100%; border-collapse: separate; border-spacing: 0; margin: 40px 0; background: #fff; border-radius: var(--radius); overflow: hidden; box-shadow: var(--shadow-md); }
.comparison-table th { background: var(--blue); color: #fff; padding: 16px; text-align: left; font-weight: 600; font-size: .95rem; }
.comparison-table td { padding: 14px 16px; border-bottom: 1px solid var(--gray-200); color: var(--gray-700); font-size: .95rem; }
.comparison-table tr:last-child td { border-bottom: none; }
.comparison-table .check-col { text-align: center; font-size: 1.2rem; }
.check-yes { color: #10B981; }
.check-no { color: #EF4444; }

/* Callout */
.callout { padding: 20px 24px; border-radius: var(--radius); margin: 30px 0; border-left: 4px solid; display: flex; gap: 14px; align-items: flex-start; }
.callout-tip { background: #D1FAE5; border-color: #6EE7B7; }
.callout-warning { background: #FEF3C7; border-color: #FCD34D; }
.callout-insight { background: rgba(41,50,225,.06); border-color: rgba(41,50,225,.18); }
.callout-icon { font-size: 1.3rem; flex-shrink: 0; line-height: 1.6; }

/* Takeaway */
.takeaway { background: var(--gradient-brand); color: #fff; padding: 28px 32px; border-radius: var(--radius-lg); margin: 40px 0; }
.takeaway strong { display: block; font-size: .9rem; text-transform: uppercase; letter-spacing: .5px; margin-bottom: 10px; opacity: .85; }
.takeaway p { margin-bottom: 0 !important; color: #fff !important; font-size: 1.05rem !important; line-height: 1.7 !important; }
.takeaway ul { margin: 12px 0 0 0; padding-left: 20px; color: #fff !important; }
.takeaway ul li { color: #fff !important; margin-bottom: 6px; }

/* Blockquote (article-content) */
.article-content blockquote { margin: 30px 0; padding: 20px 24px; border-left: 4px solid var(--blue); background: var(--gray-50); border-radius: 0 var(--radius) var(--radius) 0; }
.article-content blockquote p { margin-bottom: 0 !important; font-style: italic; color: var(--gray-700) !important; font-size: 1.05rem !important; }
.article-content blockquote cite { display: block; margin-top: 10px; font-style: normal; font-size: .85rem; color: var(--gray-400); }

/* Chart Container */
.chart-container { margin: 40px 0; padding: 24px; background: var(--gray-50); border-radius: var(--radius-lg); border: 1px solid var(--gray-200); overflow-x: auto; }
.chart-container svg { display: block; width: 100%; height: auto; }
.chart-title { text-align: center; font-size: .9rem; font-weight: 600; color: var(--gray-600); margin-bottom: 16px; }

/* CTA Box */
.cta-box { background: var(--gradient-brand); color: #fff; padding: 48px; border-radius: var(--radius-xl); text-align: center; margin: 50px 0; }
.cta-box h2 { font-size: 2rem !important; font-weight: 700 !important; margin-bottom: 16px !important; color: #fff !important; }
.cta-box p { font-size: 1.05rem !important; margin-bottom: 30px !important; opacity: .9; color: #fff !important; }
.cta-btn { display: inline-block; background: #fff; color: var(--blue); padding: 14px 36px; border-radius: 8px; font-weight: 600; font-size: 1rem; transition: transform var(--transition-base), box-shadow var(--transition-base); }
.cta-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,.2); }

/* Related */
.related-section { padding: 60px 0; background: var(--gray-50); }
.related-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-top: 30px; }
.related-card { background: #fff; border-radius: var(--radius); padding: 24px; border: 1px solid var(--gray-200); transition: transform var(--transition-base), box-shadow var(--transition-base); }
.related-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); }
.related-card h4 { font-size: 1rem; font-weight: 600; margin-bottom: 8px; color: var(--gray-900); }
.related-card p { font-size: .85rem; color: var(--gray-600); }

/* Dark mode overrides for common components */
[data-theme="dark"] .stat-card { background: var(--gray-100); border-color: var(--gray-200); }
[data-theme="dark"] .comparison-table { background: var(--gray-100); }
[data-theme="dark"] .comparison-table th { background: var(--gray-200); color: var(--gray-800); }
[data-theme="dark"] .comparison-table td { border-bottom-color: var(--gray-200); color: var(--gray-600); }
[data-theme="dark"] .chart-container { background: var(--gray-100); border-color: var(--gray-200); }
[data-theme="dark"] .chart-title { color: var(--gray-600); }
[data-theme="dark"] .related-section { background: var(--gray-50); }
[data-theme="dark"] .related-card { background: var(--gray-100); border-color: var(--gray-200); }
[data-theme="dark"] .related-card h4 { color: #F9FAFB; }
/* ===== End of supplemental CSS ===== */
`;

const files = fs.readdirSync(BLOG_DIR).filter(f => f.endsWith('.html'));
let updated = 0;
let skipped = 0;

for (const file of files) {
  const filePath = path.join(BLOG_DIR, file);
  let html = fs.readFileSync(filePath, 'utf8');
  let modified = false;
  
  // 跳过基准页面
  if (file === 'baidu-brand-protection-guide.html') {
    skipped++;
    continue;
  }
  
  // 1. 统一HTML类名
  for (const [pattern, replacement] of classMappings) {
    if (pattern.test(html)) {
      html = html.replace(pattern, replacement);
      modified = true;
    }
  }
  
  // 2. 补全缺失的CSS（追加到 </style> 之前）
  // 检查是否已经有补充CSS（避免重复追加）
  if (!html.includes('===== Added by standardize-blog-pages.js =====')) {
    html = html.replace('</style>', supplementalCSS + '\n  </style>');
    modified = true;
  }
  
  if (modified) {
    fs.writeFileSync(filePath, html, 'utf8');
    updated++;
    console.log('已更新: ' + file);
  } else {
    skipped++;
  }
}

console.log(`\n完成: ${updated} 个页面已更新, ${skipped} 个页面跳过`);
