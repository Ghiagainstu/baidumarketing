/**
 * process-todays-obsidian-blogs.mjs
 * 自动处理 Obsidian 今天新建的博客：
 *   1. 扫描 E:/Obsidian/Baidu/*.md 中 created: 2026-05-17 的文件
 *   2. 按 slug + language 分组（en/jp/ko）
 *   3. 转换成 HTML（en→blog/, jp→ja/blog/, ko→ko/blog/）
 *   4. 更新 blog.html / ja/blog.html 卡片
 *   5. 更新 sitemap.xml
 *   6. 更新 Obsidian 文件 status/push_date/url
 * 用法：node scripts/process-todays-obsidian-blogs.mjs
 */

import fs from 'fs';
import { JSDOM } from 'jsdom';
import path from 'path';

const ROOT = 'C:\\Users\\HYE\\WorkBuddy\\20260411211839';
const OBSIDIAN = 'E:\\Obsidian\\Baidu';
const TODAY = '2026-05-17';

// ============================================================
// 1. 扫描 Obsidian 目录
// ============================================================
function scanTodaysFiles() {
  const files = fs.readdirSync(OBSIDIAN).filter(f => f.endsWith('.md'));
  const result = [];

  files.forEach(f => {
    const fp = path.join(OBSIDIAN, f);
    const raw = fs.readFileSync(fp, 'utf8');
    // 检查 created 字段或文件修改时间
    const fm = parseFrontmatter(raw, fp);
    const stat = fs.statSync(fp);
    const isToday = fm.created === TODAY ||
      (stat.mtime.toISOString().startsWith('2026-05-17')) ||
      (stat.birthtimeMs && stat.birthtimeMs > Date.parse('2026-05-17') && stat.birthtimeMs < Date.parse('2026-05-18'));
    if (isToday) {
      if (fm.slug && fm.language) {
        result.push({ file: fp, slug: fm.slug, lang: fm.language, frontmatter: fm });
      } else {
        console.log(`  ⚠️  Skipping ${f} — missing slug or language in frontmatter`);
      }
    }
  });

  return result;
}

function parseFrontmatter(raw, fp) {
  const fm = {};
  if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);
  // 修复 broken ---
  let fixed = raw.replace(/([^\r\n])---\r?\n/gm, '$1\n---\n').replace(/([^\r\n])---\s*$/gm, '$1\n---\n');
  if (!fixed.startsWith('---\n')) fixed = '---\n' + fixed;

  const m = fixed.match(/^---\n([\s\S]*?)\n---\n/);
  if (!m) { return fm; }

  const lines = m[1].split(/\r?\n/);
  lines.forEach(line => {
    const mm = line.match(/^(\w[\w-]*)\s*:\s*(.*)/);
    if (mm) {
      let val = mm[2].trim();
      val = val.replace(/^["']|["']$/g, '');
      const arrMatch = val.match(/^\[(.*)\]$/);
      if (arrMatch) {
        fm[mm[1]] = arrMatch[1].split(',').map(s => s.trim().replace(/^["']|["']$/g, ''));
      } else {
        fm[mm[1]] = val;
      }
    }
  });
  return fm;
}

// ============================================================
// 2. MD → HTML 转换
// ============================================================
function mdToHtml(mdContent, frontmatter) {
  let body = mdContent;
  // 去掉 frontmatter
  body = body.replace(/^---\n[\s\S]*?\n---\n/, '');
  // 去掉 BOM
  if (body.charCodeAt(0) === 0xFEFF) body = body.slice(1);

  // 保留原有 HTML 标签（stats-grid, table, callout, takeaway 等）
  // 只转换纯 Markdown 部分

  // 标题
  body = body.replace(/^#### (.+)$/gm, '<h4>$1</h4>');
  body = body.replace(/^### (.+)$/gm, '<h3>$1</h3>');
  body = body.replace(/^## (.+)$/gm, '<h2>$1</h2>');
  body = body.replace(/^# (.+)$/gm, '<h1 class="article-title">$1</h1>');

  // 粗体
  body = body.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

  // 链接
  body = body.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');

  // 列表 → 先标记 <li>，再包 <ul>
  body = body.replace(/^[\-\*] (.+)$/gm, '<li>$1</li>');
  // 将连续的 <li> 包进 <ul>
  body = body.replace(/(<li>.*?<\/li>)(\s*<li>.*?<\/li>)*/gs, match => {
    return '<ul>' + match + '</ul>';
  });

  // 段落（连续非空行，不以 < 开头）
  const lines = body.split(/\r?\n/);
  let html = '';
  let inP = false;
  lines.forEach(line => {
    const trimmed = line.trim();
    if (!trimmed) { if (inP) { html += '</p>\n'; inP = false; } return; }
    if (trimmed.startsWith('<')) {
      if (inP) { html += '</p>\n'; inP = false; }
      html += line + '\n';
    } else {
      if (!inP) { html += '<p>'; inP = true; }
      html += trimmed + ' ';
    }
  });
  if (inP) html += '</p>\n';

  return html;
}

// ============================================================
// 3. 生成完整博客 HTML 文件
// ============================================================
function generateBlogHtml(slug, lang, mdFilePath, frontmatter) {
  const raw = fs.readFileSync(mdFilePath, 'utf8');
  const bodyHtml = mdToHtml(raw, frontmatter);

  const title = frontmatter.title || slug;
  const dateStr = (frontmatter.date || TODAY);
  const desc = frontmatter.description || '';
  const author = frontmatter.author || 'Baidu PPC Pro Team';
  const langAttr = lang === 'ja' ? 'ja' : (lang === 'ko' ? 'ko' : 'en');
  const prefix = lang === 'ja' ? 'ja/' : (lang === 'ko' ? 'ko/' : '');
  const enSlug = frontmatter.en_slug || slug;

  // 提取第一段作为 excerpt
  const textContent = bodyHtml.replace(/<[^>]+>/g, '').trim();
  const firstP = textContent.split(/\s+/).slice(0, 30).join(' ');

  const html = `<!DOCTYPE html>
<html lang="${langAttr}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>${title} — Baidu PPC Pro${lang === 'ja' ? ' Blog' : ''}</title>
  <meta name="description" content="${desc || firstP.slice(0, 155).replace(/"/g, '&quot;')}" />
  <link rel="alternate" hreflang="${lang === 'ja' ? 'ja' : 'en'}" href="https://www.baidumarketing.com/${prefix}blog/${slug}" />
  <link rel="alternate" hreflang="x-default" href="https://www.baidumarketing.com/blog/${enSlug}" />
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop offset='0%25' stop-color='%232932E1'/><stop offset='100%25' stop-color='%234F46E5'/></linearGradient></defs><rect width='32' height='32' rx='8' fill='url(%23g)'/><text x='16' y='21.5' text-anchor='middle' font-family='system-ui' font-size='13' font-weight='800' fill='white' letter-spacing='.5'>BPP</text></svg>" />
  <style>
    ${getBlogCss(lang)}
  </style>
</head>
<body>
  ${getBlogNav(lang)}
  <main>
    <article class="article-content">
      <div class="article-meta">
        <span>${dateStr}</span>
        <span>·</span>
        <span>${Math.max(1, Math.ceil(bodyHtml.replace(/<[^>]+>/g, '').split(/\s+/).length / 200))} min read</span>
        <span>·</span>
        <span>${author}</span>
      </div>
      ${bodyHtml}
    </article>
  </main>
  ${getBlogFooter(lang)}
  <script>
    ${getBlogJs(lang)}
  </script>
</body>
</html>`;

  return html;
}

function getBlogCss(lang) {
  const prefix = lang === 'ja' ? '../' : (lang === 'ko' ? '../' : '');
  return `    * { margin:0; padding:0; box-sizing:border-box; }
    :root { --blue: #2932E1; --gray-50: #F9FAFB; --gray-100: #F3F4F6; --gray-200: #E5E7EB; --gray-600: #4B5563; --gray-700: #374151; --gray-800: #1F2937; --gray-900: #111827; }
    body { font-family: system-ui, -apple-system, sans-serif; color: var(--gray-900); line-height: 1.6; }
    a { color: var(--blue); text-decoration: none; }
    .nav-inner { max-width: 1140px; margin:0 auto; padding:0 24px; display:flex; align-items:center; justify-content:space-between; height:64px; }
    .nav-links { display:flex; gap:24px; align-items:center; }
    .nav-links a { color: var(--gray-700); font-size:.9rem; }
    .nav-links a:hover { color: var(--blue); }
    .nav-cta { background: var(--blue); color:#fff; padding:8px 20px; border-radius:8px; font-size:.85rem; font-weight:600; }
    .mobile-nav-toggle { display:none; background:none; border:none; cursor:pointer; padding:8px; }
    .article-content { max-width:740px; margin:40px auto; padding:0 24px; }
    .article-title { font-size:2rem; font-weight:800; margin-bottom:16px; line-height:1.3; }
    .article-meta { display:flex; gap:12px; font-size:.85rem; color:var(--gray-600); margin-bottom:24px; }
    .article-content h2 { font-size:1.4rem; font-weight:700; margin:32px 0 16px; }
    .article-content h3 { font-size:1.15rem; font-weight:700; margin:24px 0 12px; }
    .article-content h4 { font-size:1.05rem; font-weight:700; margin:20px 0 10px; }
    .article-content p { margin-bottom:16px; }
    .article-content ul { margin:0 0 16px 20px; }
    .article-content li { margin-bottom:8px; }
    .article-content table { width:100%; border-collapse:collapse; margin:16px 0; }
    .article-content th, .article-content td { border:1px solid var(--gray-200); padding:10px 14px; text-align:left; font-size:.9rem; }
    .article-content th { background:var(--gray-50); font-weight:600; }
    .stats-grid { display:grid; grid-template-columns:repeat(auto-fit, minmax(140px,1fr)); gap:16px; margin:24px 0; }
    .stat-card { background:var(--gray-50); border-radius:12px; padding:20px; text-align:center; border:1px solid var(--gray-200); }
    .stat-number { font-size:1.4rem; font-weight:800; color:var(--blue); }
    .stat-label { font-size:.8rem; color:var(--gray-600); margin-top:4px; }
    .callout { border-radius:12px; padding:20px 24px; margin:24px 0; display:flex; gap:14px; align-items:flex-start; }
    .callout-warning { background:#FEF3C7; border:1px solid #FCD34D; }
    .callout-tip { background:#D1FAE5; border:1px solid #6EE7B7; }
    .callout-insight { background:rgba(41,50,225,.06); border:1px solid rgba(41,50,225,.18); }
    .takeaway-box { background:linear-gradient(135deg,#EEF0FF 0%,#F5F3FF 100%); border:1px solid #C7D2FE; border-radius:12px; padding:24px; margin:32px 0; }
    .takeaway-box h3, .takeaway-box h4 { font-size:1rem; font-weight:700; margin-bottom:12px; color:var(--blue); }
    .takeaway-box ul { list-style:none; display:flex; flex-direction:column; gap:8px; }
    .takeaway-box ul li { font-size:.9rem; padding-left:20px; position:relative; }
    .takeaway-box ul li::before { content:'✓'; position:absolute; left:0; color:var(--blue); font-weight:700; }
    footer { background:var(--gray-800); color:#D1D5DB; padding:56px 0 24px; }
    .footer-top { display:grid; grid-template-columns:2fr 1fr 1fr 1fr; gap:40px; padding-bottom:40px; border-bottom:1px solid rgba(255,255,255,.1); max-width:1140px; margin:0 auto; padding-left:24px; padding-right:24px; }
    .footer-col h4 { color:#fff; font-size:.85rem; font-weight:600; margin-bottom:14px; }
    .footer-col ul { list-style:none; display:flex; flex-direction:column; gap:8px; }
    .footer-col ul li a { font-size:.85rem; color:#9CA3AF; }
    .footer-bottom { display:flex; justify-content:space-between; align-items:center; max-width:1140px; margin:0 auto; padding:24px 24px 0; }
    [data-theme="dark"] { --gray-50:#1F2937; --gray-100:#374151; --gray-700:#D1D5DB; --gray-900:#F9FAFB; }
    [data-theme="dark"] .stat-card { background:var(--gray-100); border-color:var(--gray-200); }
    [data-theme="dark"] footer { background:#070B14 !important; }
    @media (max-width:900px) { .nav-links { display:none; } .mobile-nav-toggle { display:flex; } }
`;
}

function getBlogNav(lang) {
  const up = lang === 'ja' ? '../' : (lang === 'ko' ? '../' : '');
  return `  <nav>
    <div class="nav-inner">
      <a href="${up}index" class="nav-logo"><svg width="28" height="28" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#2932E1"/><text x="16" y="21.5" text-anchor="middle" fill="#fff" font-weight="800" font-size="13">BPP</text></svg> Baidu PPC Pro</a>
      <div class="nav-links" id="navLinks">
        <a href="${up}why-baidu-ppc-pro">Why Baidu PPC Pro</a>
        <a href="${up}features">Services</a>
        <a href="${up}pricing">Pricing</a>
        <a href="${up}clients">Clients</a>
        <a href="${up}faq">FAQ</a>
        <a href="${up}about">About</a>
        <a href="${up}blog">Blog</a>
        <a href="${up}contact">Contact</a>
      </div>
      <a href="${up}contact" class="nav-cta">Get Started →</a>
      <button class="mobile-nav-toggle" id="navToggle" aria-label="Menu" onclick="toggleMobileNav()"><svg viewBox="0 0 24 24" width="24" height="24"><path d="M3 12h18M3 6h18M3 18h18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>
    </div>
  </nav>
  <div class="nav-overlay" id="navOverlay" onclick="toggleMobileNav()"></div>`;
}

function getBlogFooter(lang) {
  const up = lang === 'ja' ? '../' : (lang === 'ko' ? '../' : '');
  return `  <footer>
    <div class="footer-top">
      <div class="footer-brand">
        <h3><svg width="20" height="20" viewBox="0 0 32 32"><rect width="32" height="32" rx="8" fill="#2932E1"/><text x="16" y="21.5" text-anchor="middle" fill="#fff" font-weight="800" font-size="13">BPP</text></svg> Baidu PPC Pro</h3>
        <p>We help international agencies and brands access China's digital advertising market.</p>
      </div>
      <div class="footer-col"><h4>Quick Links</h4><ul><li><a href="${up}features">Services</a></li><li><a href="${up}pricing">Pricing</a></li><li><a href="${up}clients">Clients</a></li><li><a href="${up}about">About</a></li><li><a href="${up}faq">FAQ</a></li><li><a href="${up}blog">Blog</a></li></ul></div>
      <div class="footer-col"><h4>Contact</h4><ul><li><a href="#" class="obf-email-link" data-u="baidu" data-d="baidumarketing.com"></a></li><li><a href="${up}contact">Submit a Request</a></li></ul></div>
      <div class="footer-col"><h4>Legal</h4><ul><li><a href="${up}privacy">Privacy Policy</a></li><li><a href="${up}terms">Terms of Service</a></li></ul></div>
    </div>
    <div class="footer-bottom">
      <div class="footer-copy">&copy; <script>document.write(new Date().getFullYear())<\/script> Baidu PPC Pro. All rights reserved.</div>
    </div>
  </footer>`;
}

function getBlogJs(lang) {
  return `    let mobileNavOpen = false;
    function toggleMobileNav() {
      const links = document.getElementById('navLinks');
      const overlay = document.getElementById('navOverlay');
      mobileNavOpen = !mobileNavOpen;
      if (mobileNavOpen) { links.classList.add('open'); overlay.classList.add('active'); } 
      else { links.classList.remove('open'); overlay.classList.remove('active'); }
    }
    (function(){ var t=document.documentElement, s; try { s=localStorage.getItem('theme'); } catch(e){} if(s==='dark'||(!s&&window.matchMedia('(prefers-color-scheme:dark)').matches)) t.setAttribute('data-theme','dark'); })();
    document.querySelectorAll('.obf-email-link').forEach(function(el){var a=el.dataset.u+'@'+el.dataset.d;el.href='mailto:'+a;if(!el.textContent.trim())el.textContent=a});
  `;
}

// ============================================================
// 4. 更新 blog.html / ja/blog.html
// ============================================================
function updateBlogIndex(lang, newSlugs) {
  const filePath = lang === 'ja' ? `${ROOT}\\ja\\blog.html` : `${ROOT}\\blog.html`;
  if (!fs.existsSync(filePath)) { console.log(`  ⚠️  ${filePath} not found, skipping`); return; }

  const html = fs.readFileSync(filePath, 'utf8');
  const dom = new JSDOM(html);
  const doc = dom.window.document;
  const grid = doc.getElementById('blogGrid');
  if (!grid) { console.log(`  ⚠️  #blogGrid not found in ${filePath}`); return; }

  // 为新 slug 生成卡片并插入到 #blogGrid 开头
  newSlugs.forEach(({ slug, title, dateStr, desc }) => {
    const cardHtml = `      <article class="blog-card">
        <a href="${lang === 'ja' ? 'ja/blog/' : 'blog/'}${slug}" class="blog-card-link">
          <div class="blog-card-content">
            <h3 class="blog-card-title">${title}</h3>
            <p class="blog-card-excerpt">${(desc || '').replace(/"/g, '&quot;')}</p>
            <div class="blog-card-meta"><span>${dateStr || '2026年5月'}</span></div>
          </div>
        </a>
      </article>`;
    const tempDom = new JSDOM(cardHtml).window.document;
    const card = tempDom.querySelector('.blog-card');
    grid.insertBefore(card, grid.firstChild);
  });

  fs.writeFileSync(filePath, dom.serialize(), 'utf8');
  console.log(`  ✅ Updated ${filePath.replace(ROOT, '')} (+${newSlugs.length} cards)`);
}

// ============================================================
// 5. 更新 sitemap.xml
// ============================================================
function updateSitemap(newUrls) {
  const fp = `${ROOT}\\sitemap.xml`;
  let xml = fs.readFileSync(fp, 'utf8');
  const insertPos = xml.indexOf('</urlset>');
  if (insertPos === -1) { console.log('  ⚠️  </urlset> not found in sitemap.xml'); return; }

  const newEntries = newUrls.map(u => `  <url>
    <loc>https://www.baidumarketing.com/${u.loc}</loc>
    <lastmod>${TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>`).join('\n');

  xml = xml.slice(0, insertPos) + newEntries + '\n' + xml.slice(insertPos);
  fs.writeFileSync(fp, xml, 'utf8');
  console.log(`  ✅ Updated sitemap.xml (+${newUrls.length} URLs)`);
}

// ============================================================
// 6. 更新 Obsidian 文件 frontmatter
// ============================================================
function updateObsidianFrontmatter(filePath, lang, slug) {
  let raw = fs.readFileSync(filePath, 'utf8');
  if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);
  
  const urlPath = lang === 'ja' ? `ja/blog/${slug}` : (lang === 'ko' ? `ko/blog/${slug}` : `blog/${slug}`);
  
  // 更新或添加 status, push_date, url
  const updates = {
    'status': 'published',
    'push_date': TODAY,
    [lang === 'ja' ? 'url_ja' : (lang === 'ko' ? 'url_ko' : 'url_en')]: `https://www.baidumarketing.com/${urlPath}`
  };

  let lines = raw.split(/\r?\n/);
  const fmEnd = lines.findIndex((l, i) => i > 0 && l.trim() === '---');
  
  // 在 --- 结束前插入或更新字段
  if (fmEnd > 0) {
    const before = lines.slice(0, fmEnd);
    const after = lines.slice(fmEnd);
    const newLines = [...before];
    Object.entries(updates).forEach(([k, v]) => {
      const idx = newLines.findIndex(l => l.startsWith(k + ':'));
      if (idx >= 0) {
        newLines[idx] = `${k}: ${v}`;
      } else {
        newLines.push(`${k}: ${v}`);
      }
    });
    lines = [...newLines, ...after];
  }
  
  fs.writeFileSync(filePath, lines.join('\n'), 'utf8');
}

// ============================================================
// Main
// ============================================================
function main() {
  console.log(`Scanning Obsidian for files created on ${TODAY}...\n`);

  const files = scanTodaysFiles();
  if (files.length === 0) { console.log('No new files found for today. Done.'); return; }

  console.log(`Found ${files.length} new blog file(s):\n`);
  files.forEach(f => console.log(`  - [${f.lang}] ${f.slug}  (${path.basename(f.file)})`));
  console.log('');

  // 按语言分组
  const byLang = {};
  files.forEach(f => {
    if (!byLang[f.lang]) byLang[f.lang] = [];
    byLang[f.lang].push(f);
  });

  const allNewUrls = [];

  // 处理每种语言
  for (const [lang, items] of Object.entries(byLang)) {
    console.log(`\nProcessing [${lang}] (${items.length} file(s))...`);

    const newSlugs = [];

    items.forEach(item => {
      const { file, slug, lang: l, frontmatter: fm } = item;
      const title = fm.title || slug;
      const dateStr = fm.date || TODAY;
      const desc = fm.description || '';

      // 生成 HTML
      const html = generateBlogHtml(slug, l, file, fm);
      const outDir = l === 'en' ? `${ROOT}\\blog` : `${ROOT}\\${l}\\blog`;
      if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
      const outPath = `${outDir}\\${slug}.html`;
      fs.writeFileSync(outPath, html, 'utf8');
      console.log(`  ✅ ${outPath.replace(ROOT, '')}`);

      newSlugs.push({ slug, title, dateStr, desc });

      // sitemap URL
      const loc = lang === 'en' ? `blog/${slug}.html` : `${l}/blog/${slug}.html`;
      allNewUrls.push({ loc });

      // 更新 Obsidian frontmatter
      updateObsidianFrontmatter(file, l, slug);
    });

    // 更新 blog index
    updateBlogIndex(lang, newSlugs);
  }

  // 更新 sitemap
  if (allNewUrls.length > 0) {
    console.log(`\nUpdating sitemap.xml...`);
    updateSitemap(allNewUrls);
  }

  console.log('\n✅ All done! Remember to run sort-blog-cards.mjs to re-sort, then git push.');
}

main();
