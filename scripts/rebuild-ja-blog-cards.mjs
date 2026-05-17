/**
 * rebuild-ja-blog-cards.mjs
 * 从 ja/blog/*.html 文件重新生成 ja/blog.html 的所有博客卡片
 * 用法：node scripts/rebuild-ja-blog-cards.mjs
 */

import fs from 'fs';
import { JSDOM } from 'jsdom';

const ROOT = 'C:\\Users\\HYE\\WorkBuddy\\20260411211839';
const JA_BLOG_HTML = `${ROOT}\\ja\\blog.html`;
const JA_BLOG_DIR = `${ROOT}\\ja\\blog`;

// 解析日期字符串，返回 Date 对象
function parseDate(str) {
  if (!str) return null;
  str = str.trim();
  const zhMatch = str.match(/(\d{4})年(\d{1,2})月(\d{1,2})?日?/);
  if (zhMatch) {
    const y = parseInt(zhMatch[1]), m = parseInt(zhMatch[2]) - 1;
    const d = zhMatch[3] ? parseInt(zhMatch[3]) : 1;
    return new Date(y, m, d);
  }
  const enMatch2 = str.match(/([A-Za-z]{3})\s+(\d{1,2}),\s*(\d{4})/);
  if (enMatch2) {
    const months = { jan:0, feb:1, mar:2, apr:3, may:4, jun:5, jul:6, aug:7, sep:8, oct:9, nov:10, dec:11 };
    const m = months[enMatch2[1].toLowerCase()];
    if (m !== undefined) return new Date(parseInt(enMatch2[3]), m, parseInt(enMatch2[2]));
  }
  const enMatch = str.match(/([A-Za-z]{3})\s+(\d{4})/);
  if (enMatch) {
    const months = { jan:0, feb:1, mar:2, apr:3, may:4, jun:5, jul:6, aug:7, sep:8, oct:9, nov:10, dec:11 };
    const m = months[enMatch[1].toLowerCase()];
    if (m !== undefined) return new Date(parseInt(enMatch[2]), m, 1);
  }
  const isoMatch = str.match(/(\d{4})-(\d{2})-(\d{2})/);
  if (isoMatch) return new Date(parseInt(isoMatch[1]), parseInt(isoMatch[2]) - 1, parseInt(isoMatch[3]));
  return null;
}

// 从博客 HTML 文件中提取元数据
function extractMeta(filePath) {
  const html = fs.readFileSync(filePath, 'utf8');
  const dom = new JSDOM(html);
  const doc = dom.window.document;

  // 标题：从 <title> 或 .article-title 或 h1
  let title = '';
  const titleTag = doc.querySelector('title');
  if (titleTag) title = titleTag.textContent.replace(/ — Baidu PPC Pro.*$/, '').replace(/ — Baidu PPC Pro.*$/, '').trim();
  if (!title) {
    const h1 = doc.querySelector('.article-title, h1');
    if (h1) title = h1.textContent.trim();
  }

  // 日期：从 .article-meta span 或 time 标签
  let dateStr = '';
  const metaSpan = doc.querySelector('.article-meta span, time');
  if (metaSpan) dateStr = metaSpan.textContent.trim();

  // description：从 meta tag 或第一段
  let desc = '';
  const metaDesc = doc.querySelector('meta[name="description"]');
  if (metaDesc) desc = metaDesc.getAttribute('content') || '';
  if (!desc) {
    const firstP = doc.querySelector('.article-content p, article p');
    if (firstP) desc = firstP.textContent.trim().slice(0, 150);
  }

  // 图片：从 OG image 或第一张图片
  let img = '';
  const ogImg = doc.querySelector('meta[property="og:image"]');
  if (ogImg) img = ogImg.getAttribute('content') || '';
  if (!img) {
    const firstImg = doc.querySelector('.article-content img, article img');
    if (firstImg) img = firstImg.getAttribute('src') || '';
  }

  return { title, dateStr, desc, img };
}

// 生成博客卡片 HTML
function makeCard(slug, meta) {
  const { title, dateStr, desc, img } = meta;
  const imgSrc = img || 'https://via.placeholder.com/400x250?text=No+Image';
  return `
      <article class="blog-card">
        <a href="ja/blog/${slug}" class="blog-card-link">
          <div class="blog-card-image">
            <img src="${imgSrc}" alt="${title.replace(/"/g, '&quot;')}" />
          </div>
          <div class="blog-card-content">
            <h3 class="blog-card-title">${title}</h3>
            <p class="blog-card-excerpt">${desc}</p>
            <div class="blog-card-meta"><span>${dateStr || '2026年5月'}</span></div>
          </div>
        </a>
      </article>`;
}

// 主函数
function rebuild() {
  // 读取所有 ja/blog/*.html 文件
  const files = fs.readdirSync(JA_BLOG_DIR)
    .filter(f => f.endsWith('.html') && f !== 'index.html')
    .map(f => {
      const slug = f.replace(/\.html$/, '');
      const filePath = `${JA_BLOG_DIR}\\${f}`;
      const meta = extractMeta(filePath);
      const date = parseDate(meta.dateStr);
      return { slug, meta, date, dateValue: date ? date.getTime() : 0 };
    })
    .sort((a, b) => b.dateValue - a.dateValue);

  console.log(`Found ${files.length} JA blog HTML files`);
  files.forEach((item, i) => {
    console.log(`  ${i+1}. [${item.meta.dateStr}] ${item.meta.title.slice(0, 50)}`);
  });

  // 生成卡片 HTML
  const cardsHtml = files.map(f => makeCard(f.slug, f.meta)).join('\n');

  // 读取 ja/blog.html 并替换 #blogGrid 内容
  const html = fs.readFileSync(JA_BLOG_HTML, 'utf8');
  const dom = new JSDOM(html);
  const doc = dom.window.document;
  const grid = doc.getElementById('blogGrid');
  if (!grid) { console.error('❌ #blogGrid not found in ja/blog.html'); return; }
  grid.innerHTML = cardsHtml;
  fs.writeFileSync(JA_BLOG_HTML, dom.serialize(), 'utf8');
  console.log(`✅ Rebuilt ja/blog.html with ${files.length} cards`);
}

rebuild();
