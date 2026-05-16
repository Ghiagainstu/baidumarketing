/**
 * add-blog-to-site.mjs - Auto-insert blog cards into blog.html + ja/blog.html,
 * and add URLs to sitemap.xml.
 *
 * Usage:
 *   node add-blog-to-site.mjs \
 *     --slug <slug> \
 *     --category <category> \
 *     --title-en "<title>" \
 *     --title-jp "<title-jp>" \
 *     --excerpt-en "<excerpt>" \
 *     --excerpt-jp "<excerpt-jp>" \
 *     --date-en "<date>" \
 *     --date-jp "<date-jp>" \
 *     --read-time "<time>"
 */

import fs from 'fs';
import path from 'path';

const ROOT = 'c:/Users/HYE/WorkBuddy/20260411211839';
const BLOG_HTML = path.join(ROOT, 'blog.html');
const JA_BLOG_HTML = path.join(ROOT, 'ja/blog.html');
const SITEMAP_XML = path.join(ROOT, 'sitemap.xml');

// Parse CLI args
const args = process.argv.slice(2);
const p = {};
for (let i = 0; i < args.length; i++) {
  if (args[i].startsWith('--')) {
    const key = args[i].slice(2);
    const val = (i + 1 < args.length && !args[i + 1].startsWith('--')) ? args[i + 1] : '';
    p[key] = val;
    i++;
  }
}

const { slug, category, 'title-en': titleEn, 'title-jp': titleJp,
        'excerpt-en': excerptEn, 'excerpt-jp': excerptJp,
        'date-en': dateEn, 'date-jp': dateJp, 'read-time': readTime } = p;

if (!slug || !category || !titleEn || !titleJp) {
  console.error('Missing required params: --slug, --category, --title-en, --title-jp');
  process.exit(1);
}

const svgIcon = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>';

// Tag display names
const tagEn = { search: 'Search Ads', insights: 'Market Insights', feed: 'Feed Ads', strategy: 'Strategy', landing: 'Landing Page', platform: 'Platform' };
const tagJp = { search: '検索広告', insights: '市場インサイト', feed: 'フィード広告', strategy: '戦略', landing: 'ランディングページ', platform: 'プラットフォーム' };

function makeCard(title, excerpt, date, isJp) {
  const tag = isJp ? (tagJp[category] || category) : (tagEn[category] || category);
  const prefix = isJp ? 'blog/' : 'blog/';
  return `      <!-- NEW: ${slug} -->\n      <div class="blog-card" data-category="${category}">\n        <span class="blog-card-tag ${category}">${tag}</span>\n        <h3 class="blog-card-title"><a href="${prefix}${slug}">${isJp ? '🧹' : '🧹'} ${title}</a></h3>\n        <p class="blog-card-excerpt">${excerpt}</p>\n        <div class="blog-card-meta"><span>${date}</span><span class="read-time">${svgIcon} ${readTime}</span></div>\n      </div>\n\n`;
}

function insertCard(filePath, title, excerpt, date, isJp) {
  let c = fs.readFileSync(filePath, 'utf8');
  const card = makeCard(title, excerpt, date, isJp);
  // Insert before the first card with matching data-category
  const re = new RegExp(`<div class="blog-card" data-category="${category}">`);
  const m = c.match(re);
  if (!m) { console.error(`Category "${category}" not found in ${path.basename(filePath)}`); return; }
  const idx = c.indexOf(m[0]);
  c = c.slice(0, idx) + card + c.slice(idx);
  fs.writeFileSync(filePath, c, 'utf8');
  console.log(`✅ Inserted ${isJp ? 'JP' : 'EN'} card into ${path.basename(filePath)}`);
}

function addSitemap() {
  let c = fs.readFileSync(SITEMAP_XML, 'utf8');
  const entryEn = `  <url>\n    <loc>https://www.baidumarketing.com/blog/${slug}</loc>\n    <priority>0.6</priority>\n  </url>\n`;
  const entryJp = `  <url>\n    <loc>https://www.baidumarketing.com/ja/blog/${slug}</loc>\n    <priority>0.6</priority>\n  </url>\n`;
  const pos = c.indexOf('</urlset>');
  if (pos === -1) { console.error('</urlset> not found'); return; }
  c = c.slice(0, pos) + entryEn + entryJp + c.slice(pos);
  fs.writeFileSync(SITEMAP_XML, c, 'utf8');
  console.log('✅ Added URLs to sitemap.xml');
}

// Execute
try {
  insertCard(BLOG_HTML, titleEn, excerptEn, dateEn, false);
  insertCard(JA_BLOG_HTML, titleJp, excerptJp, dateJp, true);
  addSitemap();
  console.log('✅ add-blog-to-site complete!');
} catch (e) {
  console.error('❌ Error:', e.message);
  process.exit(1);
}
