const fs = require('fs');
const path = require('path');

// Map of page file → nav link text that should be active
const activeMap = {
  'index.html': null, // homepage, no active nav link (logo is the home link)
  'why-baidu-ppc-pro.html': '選ばれる理由',
  'features.html': 'サービス',
  'pricing.html': '料金プラン',
  'clients.html': '実績',
  'faq.html': 'よくある質問',
  'about.html': '会社概要',
  'blog.html': 'ブログ',
  'contact.html': 'お問い合わせ',
  'privacy.html': null, // legal page, not in main nav
  'terms.html': null,    // legal page, not in main nav
};

const jaDir = 'c:/Users/HYE/WorkBuddy/20260411211839/ja';

Object.entries(activeMap).forEach(([file, activeText]) => {
  if (!activeText) return; // skip pages that don't have a nav link
  const filePath = path.join(jaDir, file);
  if (!fs.existsSync(filePath)) {
    console.log(`SKIP (not found): ${file}`);
    return;
  }
  let html = fs.readFileSync(filePath, 'utf8');
  const original = html;

  // Add class="active" to the nav link with the matching text
  // Pattern: <a href="...">activeText</a> → <a href="..." class="active">activeText</a>
  const regex = new RegExp(`(<a href="[^"]*")(>${escapeRegex(activeText)}</a>)`, 'g');
  html = html.replace(regex, '$1 class="active"$2');

  if (html !== original) {
    fs.writeFileSync(filePath, html, 'utf8');
    console.log(`FIXED: ${file} (added active to "${activeText}")`);
  } else {
    console.log(`WARN:  ${file} (pattern not found for "${activeText}")`);
  }
});

function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
