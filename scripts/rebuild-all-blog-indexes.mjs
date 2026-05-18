/**
 * rebuild-all-blog-indexes.mjs
 * 从 blog/*.html / ja/blog/*.html / ko/blog/*.html 真实存在的文件
 * 重建 blog.html / ja/blog.html / ko/blog.html（可靠方案）
 * 用法：node scripts/rebuild-all-blog-indexes.mjs
 */

import fs from 'fs';
import { JSDOM } from 'jsdom';
import path from 'path';

const ROOT = 'C:\\Users\\HYE\\WorkBuddy\\20260411211839';

// 从 HTML 文件中提取 title 和 date
function extractMeta(fp) {
  try {
    const html = fs.readFileSync(fp, 'utf8');
    const dom = new JSDOM(html);
    const doc = dom.window.document;
    const titleTag = doc.querySelector('title');
    let title = titleTag ? titleTag.textContent.replace(/ — Baidu PPC Pro.*$/, '').trim() : path.basename(fp, '.html');
    // 尝试从 article-title 获取
    const h1 = doc.querySelector('.article-title, h1');
    if (h1) title = h1.textContent.trim();
    // 尝试从 card-title 获取（如果文件本身就是卡片预览）
    const cardTitle = doc.querySelector('.blog-card-title');
    if (cardTitle) title = cardTitle.textContent.trim();

    let dateStr = '';
    const metaSpan = doc.querySelector('.article-meta span, .blog-card-meta span');
    if (metaSpan) dateStr = metaSpan.textContent.trim();

    let desc = '';
    const metaDesc = doc.querySelector('meta[name="description"]');
    if (metaDesc) desc = metaDesc.getAttribute('content') || '';
    if (!desc) {
      const firstP = doc.querySelector('.article-content p, p');
      if (firstP) desc = firstP.textContent.trim().slice(0, 150);
    }

    return { title, dateStr, desc };
  } catch(e) {
    return { title: path.basename(fp, '.html'), dateStr: '', desc: '' };
  }
}

// 解析日期 → timestamp
function parseDate(dateStr) {
  if (!dateStr) return 0;
  dateStr = dateStr.trim();
  // YYYY-MM-DD
  let m = dateStr.match(/(\d{4})-(\d{2})-(\d{2})/);
  if (m) return new Date(parseInt(m[1]), parseInt(m[2])-1, parseInt(m[3])).getTime();
  // Mon DD, YYYY
  m = dateStr.match(/([A-Za-z]{3})\s+(\d{1,2}),\s*(\d{4})/);
  if (m) {
    const months = { jan:0,feb:1,mar:2,apr:3,may:4,jun:5,jul:6,aug:7,sep:8,oct:9,nov:10,dec:11 };
    const mm = months[m[1].toLowerCase()];
    if (mm !== undefined) return new Date(parseInt(m[3]), mm, parseInt(m[2])).getTime();
  }
  // Mon YYYY
  m = dateStr.match(/([A-Za-z]{3})\s+(\d{4})/);
  if (m) {
    const months = { jan:0,feb:1,mar:2,apr:3,may:4,jun:5,jul:6,aug:7,sep:8,oct:9,nov:10,dec:11 };
    const mm = months[m[1].toLowerCase()];
    if (mm !== undefined) return new Date(parseInt(m[2]), mm, 1).getTime();
  }
  // YYYY年MM月DD日
  m = dateStr.match(/(\d{4})年(\d{1,2})月(\d{1,2})?日?/);
  if (m) return new Date(parseInt(m[1]), parseInt(m[2])-1, parseInt(m[3]||'1')).getTime();
  // YYYY年MM月
  m = dateStr.match(/(\d{4})年(\d{1,2})月/);
  if (m) return new Date(parseInt(m[1]), parseInt(m[2])-1, 1).getTime();
  return 0;
}

// 重建单个 index 文件
function rebuildIndex(htmlFile, htmlDir, urlPrefix) {
  if (!fs.existsSync(htmlDir)) {
    console.log(`  ⚠️  Directory not found: ${htmlDir.replace(ROOT,'')}, skipping`);
    return;
  }
  if (!fs.existsSync(htmlFile)) {
    console.log(`  ⚠️  Index file not found: ${htmlFile.replace(ROOT,'')}, will create`);
  }

  // 读取所有 HTML 文件
  const files = fs.readdirSync(htmlDir)
    .filter(f => f.endsWith('.html'))
    .map(f => {
      const fp = path.join(htmlDir, f);
      const meta = extractMeta(fp);
      const slug = f.replace(/\.html$/, '');
      return { slug, ...meta, dateValue: parseDate(meta.dateStr) };
    })
    .sort((a, b) => b.dateValue - a.dateValue);

  console.log(`  Found ${files.length} HTML files in ${htmlDir.replace(ROOT,'')}`);

  // 生成卡片 HTML
  const cardsHtml = files.map(({ slug, title, dateStr, desc }) => {
    const descEsc = (desc || '').replace(/"/g, '&quot;').slice(0, 150);
    const titleEsc = title.replace(/"/g, '&quot;');
    return `      <article class="blog-card">
        <a href="${urlPrefix}${slug}" class="blog-card-link">
          <div class="blog-card-content">
            <h3 class="blog-card-title">${titleEsc}</h3>
            <p class="blog-card-excerpt">${descEsc}</p>
            <div class="blog-card-meta"><span>${dateStr || ''}</span></div>
          </div>
        </a>
      </article>`;
  }).join('\n');

  // 读取现有 index 文件或创建新的
  let html = '';
  if (fs.existsSync(htmlFile)) {
    html = fs.readFileSync(htmlFile, 'utf8');
    // 替换 #blogGrid 内容
    const gridRe = /(<div class="blog-grid" id="blogGrid">)[\s\S]*?(<\/div>\s*<\/main>)/;
    const replaceStr = `$1\n${cardsHtml}\n  $2`;
    if (gridRe.test(html)) {
      html = html.replace(gridRe, replaceStr);
    } else {
      console.log(`  ⚠️  #blogGrid pattern not matched, will rewrite file`);
    }
  }

  if (!html || !fs.existsSync(htmlFile)) {
    // 创建最小 index
    html = `<!DOCTYPE html>
<html lang="${urlPrefix.includes('ja') ? 'ja' : (urlPrefix.includes('ko') ? 'ko' : 'en')}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Blog — Baidu PPC Pro</title>
  <link rel="stylesheet" href="${urlPrefix}assets/style.css" />
</head>
<body>
  <main>
    <div class="blog-grid" id="blogGrid">
${cardsHtml}
    </div>
  </main>
</body>
</html>`;
  }

  fs.writeFileSync(htmlFile, html, 'utf8');
  console.log(`  ✅ Saved ${htmlFile.replace(ROOT, '')} (${files.length} cards)`);
}

console.log('Rebuilding all blog indexes from real HTML files...\n');

const tasks = [
  { htmlFile: `${ROOT}\\blog.html`,       htmlDir: `${ROOT}\\blog`,       urlPrefix: 'blog/' },
  { htmlFile: `${ROOT}\\ja\\blog.html`,   htmlDir: `${ROOT}\\ja\\blog`,   urlPrefix: 'ja/blog/' },
  { htmlFile: `${ROOT}\\ko\\blog.html`,   htmlDir: `${ROOT}\\ko\\blog`,   urlPrefix: 'ko/blog/' },
];

tasks.forEach(t => {
  console.log(`📁 ${t.htmlFile.replace(ROOT,'')}`);
  try { rebuildIndex(t.htmlFile, t.htmlDir, t.urlPrefix); } catch(e) { console.error(`  ❌ Error: ${e.message}`); }
  console.log('');
});

console.log('Done! Run sort-blog-cards.mjs to verify sorting.');
