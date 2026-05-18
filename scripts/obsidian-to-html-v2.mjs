/**
 * Obsidian MD → BPP HTML 批量转换脚本 (v2)
 * 修复：BOM、\r\n、broken --- delimiters、子目录路径
 *
 * 用法：node obsidian-to-html-v2.mjs
 */

import fs from 'fs';
import path from 'path';

// ============================================================
// 配置：要处理的文件列表 { obsidian路径, 输出slug, 输出语言 }
// ============================================================
const tasks = [
  // 5/16 item 9
  {
    src: 'E:/Obsidian/Baidu/bpp-baidu-brand-info-account-level-en.md',
    slug: 'baidu-brand-info-account-level',
    lang: 'en',
    outDir: '.',
  },
  {
    src: 'E:/Obsidian/Baidu/bpp-baidu-brand-info-account-level-jp.md',
    slug: 'baidu-brand-info-account-level',
    lang: 'ja',
    outDir: 'ja',
  },
  // 5/15 item 1
  {
    src: 'E:/Obsidian/Baidu/03-Search-Ads/bpp-why-b2b-baidu-search-en.md',
    slug: 'why-b2b-baidu-search',
    lang: 'en',
    outDir: '.',
  },
  {
    src: 'E:/Obsidian/Baidu/03-Search-Ads/bpp-why-b2b-baidu-search-jp.md',
    slug: 'why-b2b-baidu-search',
    lang: 'ja',
    outDir: 'ja',
  },
  // 5/15 item 2
  {
    src: 'E:/Obsidian/Baidu/01-Market-Insights/bpp-chinese-consumers-decision-journey-en.md',
    slug: 'chinese-consumers-decision-journey',
    lang: 'en',
    outDir: '.',
  },
  {
    src: 'E:/Obsidian/Baidu/01-Market-Insights/bpp-chinese-consumers-decision-journey-jp.md',
    slug: 'chinese-consumers-decision-journey',
    lang: 'ja',
    outDir: 'ja',
  },
  // 5/15 item 3
  {
    src: 'E:/Obsidian/Baidu/05-Strategy/bpp-b2b-lead-generation-framework-en.md',
    slug: 'b2b-lead-generation-framework',
    lang: 'en',
    outDir: '.',
  },
  {
    src: 'E:/Obsidian/Baidu/05-Strategy/bpp-b2b-lead-generation-framework-jp.md',
    slug: 'b2b-lead-generation-framework',
    lang: 'ja',
    outDir: 'ja',
  },
  // 5/15 item 4
  {
    src: 'E:/Obsidian/Baidu/01-Market-Insights/bpp-baidu-2026-international-brands-en.md',
    slug: 'baidu-2026-international-brands',
    lang: 'en',
    outDir: '.',
  },
  {
    src: 'E:/Obsidian/Baidu/01-Market-Insights/bpp-baidu-2026-international-brands-jp.md',
    slug: 'baidu-2026-international-brands',
    lang: 'ja',
    outDir: 'ja',
  },
  // 5/15 item 5
  {
    src: 'E:/Obsidian/Baidu/bpp-faq-international-brands-en.md',
    slug: 'faq-international-brands',
    lang: 'en',
    outDir: '.',
  },
  {
    src: 'E:/Obsidian/Baidu/bpp-faq-international-brands-jp.md',
    slug: 'faq-international-brands',
    lang: 'ja',
    outDir: 'ja',
  },
];

// ============================================================
// 1. 读取并解析 Obsidian 文件
// ============================================================
function fixBrokenFrontmatter(raw) {
  // 去除 BOM
  if (raw.charCodeAt(0) === 0xFEFF) raw = raw.slice(1);

  // 修复 broken ---：如果 --- 连在最后一行（无换行），先修复
  // 例如："author: Baidu PPC Pro Team---"
  raw = raw.replace(/(\S)---\s*$/m, '$1\n---');

  // 修复：如果 --- 前有字但无换行（非行首的情况）
  raw = raw.replace(/([^\r\n])---\r?\n/gm, '$1\n---\n');

  // 确保开头有 ---
  if (!raw.startsWith('---\n')) {
    raw = '---\n' + raw;
  }

  return raw;
}

function parseObsidianMd(filePath) {
  let raw = fs.readFileSync(filePath, 'utf8');
  raw = fixBrokenFrontmatter(raw);

  // 分割 frontmatter 和 body
  let fm = {};
  let body = raw;

  const fmMatch = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n/);
  if (fmMatch) {
    fm = parseYamlLike(fmMatch[1]);
    body = raw.slice(fmMatch[0].length);
  } else {
    // 无 --- 格式：解析 # 标题之前的所有 key: value 行
    const lines = raw.split(/\r?\n/);
    const fmLines = [];
    const bodyLines = [];
    let inBody = false;
    for (const line of lines) {
      if (!inBody && line.startsWith('#')) inBody = true;
      if (!inBody) fmLines.push(line);
      else bodyLines.push(line);
    }
    fm = parseYamlLike(fmLines.join('\n'));
    body = bodyLines.join('\n');
  }

  // Fallback：date 缺失时用 created
  if (!fm.date && fm.created) {
    fm.date = fm.created;
  }
  // Fallback：description 缺失时从正文第一段生成（跳过标题行）
  if (!fm.description) {
    // 去除 HTML 标签、markdown 标题、粗体标记
    let plainBody = body.replace(/<[^>]+>/g, '');
    plainBody = plainBody.replace(/^#+\s*.+$/gm, ''); // 去除 markdown 标题行
    plainBody = plainBody.replace(/\*\*(.+?)\*\*/g, '$1');
    plainBody = plainBody.replace(/`([^`]+)`/g, '$1');
    plainBody = plainBody.trim();
    // 取第一个非空段落
    const paragraphs = plainBody.split(/\n{2,}/).map(p => p.trim()).filter(Boolean);
    const firstPara = paragraphs[0] || '';
    fm.description = firstPara.slice(0, 155) + (firstPara.length > 155 ? '...' : '');
  }

  return { fm, body: body.trim() };
}

function parseYamlLike(text) {
  const fm = {};
  // 简单解析 key: value（不处理嵌套）
  const re = /^(\w[\w-]*)\s*:\s*(.*)$/gm;
  let m;
  while ((m = re.exec(text)) !== null) {
    const key = m[1];
    let val = m[2].trim();
    // 去除首尾引号
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1);
    }
    fm[key] = val;
  }
  return fm;
}

// ============================================================
// 2. Markdown → HTML 转换（保留已有 HTML 块）
// ============================================================
function mdToHtml(md) {
  let html = md;

  // 保护 <div class="stats-grid"> 等 HTML 块不被转换
  const htmlBlocks = [];
  let idx = 0;
  html = html.replace(/<(div|table|blockquote|callout|takeaway|iframe)[\s\S]*?<\/\1>/gi, (match) => {
    const placeholder = `%%HTML_BLOCK_${idx}%%`;
    htmlBlocks.push(match);
    idx++;
    return placeholder;
  });

  // 转换 Markdown 语法
  // 标题
  html = html.replace(/^#### (.+)$/gm, '<h4>$1</h4>');
  html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
  html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
  html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');

  // 粗体
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

  // 行内代码
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

  // 链接
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');

  // 水平线
  html = html.replace(/^---$/gm, '<hr>');

  // 列表（简单处理）
  html = html.replace(/^- ✅ (.+)$/gm, '<li>✅ $1</li>');
  html = html.replace(/^- ❌ (.+)$/gm, '<li>❌ $1</li>');
  html = html.replace(/^- (.+)$/gm, '<li>$1</li>');

  // 段落：连续非空行包裹 <p>
  // 先按空行分割 blocks
  const blocks = html.split(/\n{2,}/);
  const converted = blocks.map(block => {
    const trimmed = block.trim();
    if (!trimmed) return '';
    // 已经是 HTML 块（占位符或 HTML 标签）
    if (trimmed.startsWith('%%HTML_BLOCK') || trimmed.startsWith('<')) return trimmed;
    // 列表块
    if (trimmed.includes('<li>')) {
      const items = trimmed.split('\n').map(l => l.trim()).filter(Boolean).join('');
      return `<ul>${items}</ul>`;
    }
    // 表格（以 | 开头）
    if (trimmed.startsWith('|')) return convertTable(trimmed);
    // 普通段落
    return `<p>${trimmed.replace(/\n/g, '<br>')}</p>`;
  }).filter(Boolean);

  html = converted.join('\n\n');

  // 还原 HTML 块
  htmlBlocks.forEach((block, i) => {
    html = html.replace(`%%HTML_BLOCK_${i}%%`, block);
  });

  return html;
}

function convertTable(mdTable) {
  const lines = mdTable.trim().split('\n').filter(l => l.trim());
  if (lines.length < 2) return mdTable;

  const parseRow = (line) => line.split('|').map(c => c.trim()).filter((_, i, a) => i > 0 && i < a.length - 1);
  const headerCells = parseRow(lines[0]);
  
  // 跳过第二行分隔符（|---|---|）
  const dataRows = lines.slice(2);

  let html = '<table class="comparison-table">\n<thead>\n<tr>';
  headerCells.forEach(cell => { html += `<th>${cell}</th>`; });
  html += '</tr>\n</thead>\n<tbody>';
  dataRows.forEach(row => {
    const cells = parseRow(row);
    html += '\n<tr>';
    cells.forEach(cell => { html += `<td>${cell}</td>`; });
    html += '</tr>';
  });
  html += '</tbody>\n</table>';
  return html;
}

// ============================================================
// 3. 加载 bpp-template-ultimate HTML 模板框架
// ============================================================
// 注意：这里生成的是博客文章页，需要：
// - <html lang="en" 或 lang="ja">
// - <article class="article-content">
// - 正确的 nav/footer/CSS

function generateBlogHtml({ fm, bodyHtml, slug, lang }) {
  const title = fm.title || 'Blog Post';
  const description = fm.description || '';
  const date = fm.date || '2025-01-01';
  const category = fm.category || 'insights';
  const readingTime = fm.reading_time || '5';
  const author = fm.author || 'Baidu PPC Pro Team';

  const isJa = lang === 'ja';
  const langPrefix = isJa ? '../' : '';
  const jaDir = isJa ? 'ja/' : '';
  const pageUrl = isJa
    ? `https://baidumarketing.com/ja/blog/${slug}`
    : `https://baidumarketing.com/blog/${slug}`;

  // 分类显示名
  const catDisplay = { insights: 'Market Insights', search: 'Search Ads', feed: 'Feed Ads', strategy: 'Strategy', landing: 'Landing Page', platform: 'Platform' };
  const catName = catDisplay[category] || category;
  const catClass = category;

  // 日期格式化
  const dateObj = new Date(date + 'T00:00:00Z');
  const dateStr = dateObj.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });

  return `<!DOCTYPE html>
<html lang="${isJa ? 'ja' : 'en'}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title} — Baidu PPC Pro${isJa ? ' Blog' : ' Blog'}</title>
  <meta name="description" content="${description.replace(/"/g, '&quot;')}">
  <link rel="canonical" href="${pageUrl}">

  <!-- Open Graph -->
  <meta property="og:type" content="article">
  <meta property="og:title" content="${title.replace(/"/g, '&quot;')}">
  <meta property="og:description" content="${description.replace(/"/g, '&quot;')}">
  <meta property="og:url" content="${pageUrl}">
  <meta property="og:image" content="https://baidumarketing.com/assets/og-brand-default.png">
  <meta property="og:site_name" content="Baidu PPC Pro">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${title.replace(/"/g, '&quot;')}">
  <meta name="twitter:description" content="${description.replace(/"/g, '&quot;')}">
  <meta name="twitter:image" content="https://baidumarketing.com/assets/og-brand-default.png">

  <!-- JSON-LD -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "${title.replace(/"/g, '\\"')}",
    "description": "${description.replace(/"/g, '\\"')}",
    "datePublished": "${date}",
    "author": { "@type": "Organization", "name": "Baidu PPC Pro Team" },
    "publisher": { "@type": "Organization", "name": "Baidu PPC Pro" },
    "mainEntityOfPage": { "@type": "WebPage", "@id": "${pageUrl}" }
  }
  </script>

  <meta name="theme-color" content="#1a56db">
  <meta name="color-scheme" content="light dark">

  <!-- Favicon (inline SVG, ALL SINGLE QUOTES) -->
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🔍</text></svg>">

  <!-- Preconnect -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

  <!-- Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">

  <style>
    :root {
      --primary: #1a56db; --primary-dark: #1e40af; --gray-50: #f9fafb; --gray-100: #f3f4f6;
      --gray-200: #e5e7eb; --gray-300: #d1d5db; --gray-400: #9ca3af; --gray-500: #6b7280;
      --gray-600: #4b5563; --gray-700: #374151; --gray-800: #1f2937; --gray-900: #111827;
      --white: #ffffff; --green-100: #d1fae5; --green-800: #065f46;
      --red-100: #fee2e2; --red-800: #991b1b;
      --radius: 8px; --shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Inter', sans-serif; color: var(--gray-800); background: var(--white); line-height: 1.6; }
    .container { max-width: 1140px; margin: 0 auto; padding: 0 20px; }

    /* Nav */
    nav { background: var(--white); box-shadow: var(--shadow); position: sticky; top: 0; z-index: 100; }
    .nav-inner { display: flex; align-items: center; justify-content: space-between; height: 64px; }
    .nav-logo { font-size: 1.2rem; font-weight: 700; color: var(--primary); text-decoration: none; }
    .nav-links { display: flex; gap: 24px; list-style: none; }
    .nav-links a { color: var(--gray-600); text-decoration: none; font-weight: 500; font-size: 0.9rem; }
    .nav-links a:hover { color: var(--primary); }
    .nav-right-group { display: flex; align-items: center; gap: 8px; }
    .nav-cta { background: var(--primary); color: white; padding: 8px 18px; border-radius: var(--radius); text-decoration: none; font-weight: 600; font-size: 0.85rem; }
    .lang-switch { position: relative; }
    .lang-switch-btn { background: none; border: 1px solid var(--gray-200); border-radius: var(--radius); padding: 6px 10px; cursor: pointer; font-size: 0.85rem; display: flex; align-items: center; gap: 4px; }
    .lang-switch-menu { position: absolute; top: calc(100% + 6px); right: 0; background: var(--white); border: 1px solid var(--gray-200); border-radius: var(--radius); box-shadow: 0 4px 12px rgba(0,0,0,0.1); min-width: 140px; z-index: 200; opacity: 0; pointer-events: none; transform: translateY(-4px); transition: all 0.15s ease; }
    .lang-switch-menu.open { opacity: 1; pointer-events: auto; transform: translateY(0); }
    .lang-switch-menu a { display: block; padding: 8px 14px; color: var(--gray-700); text-decoration: none; font-size: 0.85rem; }
    .lang-switch-menu a:hover { background: var(--gray-50); }
    .nav-toggle { display: none; background: none; border: none; cursor: pointer; }
    .nav-toggle span { display: block; width: 22px; height: 2px; background: var(--gray-800); margin: 4px 0; }
    .nav-overlay { display: none; }

    /* Mobile nav */
    @media (max-width: 900px) {
      .nav-links, .nav-right-group .nav-cta, .lang-switch { display: none; }
      .nav-toggle { display: block; }
      .nav-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 999; }
      .nav-overlay.open { display: block; }
      .nav-mobile-panel { display: none; position: fixed; top: 0; right: 0; width: 280px; height: 100%; background: var(--white); z-index: 1000; flex-direction: column; padding: 24px; }
      .nav-mobile-panel.open { display: flex; }
      .nav-mobile-panel a { display: block; padding: 12px 0; color: var(--gray-700); text-decoration: none; font-weight: 500; border-bottom: 1px solid var(--gray-100); }
    }

    /* Theme toggle */
    .theme-toggle { background: none; border: 1px solid var(--gray-200); border-radius: var(--radius); padding: 6px 8px; cursor: pointer; display: flex; align-items: center; }
    .theme-toggle svg { width: 18px; height: 18px; }
    body.dark { background: var(--gray-800); color: var(--gray-300); }
    body.dark nav { background: var(--gray-800); }
    body.dark .nav-links a { color: var(--gray-300); }
    body.dark .theme-toggle { border-color: var(--gray-600); }

    /* Article */
    main { padding: 40px 0; }
    .article-content { max-width: 720px; margin: 0 auto; padding: 0 20px; }
    .article-title { font-size: 2rem; font-weight: 700; margin-bottom: 12px; line-height: 1.3; }
    body.dark .article-title { color: var(--white); }
    .article-meta { display: flex; gap: 16px; align-items: center; color: var(--gray-500); font-size: 0.9rem; margin-bottom: 32px; flex-wrap: wrap; }
    .article-meta .dot { width: 3px; height: 3px; background: var(--gray-400); border-radius: 50%; }
    .article-category { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; margin-bottom: 12px; }
    .article-category.${catClass} { background: var(--primary); color: white; }
    .article-body h2 { font-size: 1.5rem; font-weight: 700; margin: 32px 0 16px; }
    body.dark .article-body h2 { color: var(--white); }
    .article-body h3 { font-size: 1.25rem; font-weight: 600; margin: 24px 0 12px; }
    body.dark .article-body h3 { color: var(--gray-200); }
    .article-body p { margin-bottom: 16px; }
    .article-body ul, .article-body ol { margin: 12px 0 12px 20px; }
    .article-body li { margin-bottom: 8px; }
    .article-body hr { border: none; border-top: 1px solid var(--gray-200); margin: 32px 0; }
    .article-body table { width: 100%; border-collapse: collapse; margin: 20px 0; }
    .article-body th, .article-body td { padding: 10px 14px; border: 1px solid var(--gray-200); text-align: left; font-size: 0.9rem; }
    .article-body th { background: var(--gray-100); font-weight: 600; }
    body.dark .article-body th { background: var(--gray-700); color: var(--white); }
    body.dark .article-body td { border-color: var(--gray-600); }

    /* Visual elements */
    .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin: 24px 0; }
    .stat-card { background: var(--gray-50); border-radius: var(--radius); padding: 20px; text-align: center; }
    body.dark .stat-card { background: var(--gray-700); }
    .stat-icon { font-size: 2rem; margin-bottom: 8px; }
    .stat-number { font-size: 1.5rem; font-weight: 700; color: var(--primary); }
    .stat-label { font-size: 0.85rem; color: var(--gray-500); margin-top: 4px; }
    .callout { border-radius: var(--radius); padding: 16px 20px; margin: 20px 0; border-left: 4px solid; }
    .callout.tip { background: var(--green-100); border-color: var(--green-800); }
    .callout.warning { background: var(--red-100); border-color: var(--red-800); }
    .takeaway { background: var(--gray-50); border-radius: var(--radius); padding: 20px 24px; margin: 24px 0; }
    body.dark .takeaway { background: var(--gray-700); }
    .takeaway h4 { margin-bottom: 12px; }
    .takeaway ul { margin-left: 20px; }
    .blockquote-highlight { border-left: 4px solid var(--primary); padding: 16px 20px; margin: 20px 0; font-style: italic; color: var(--gray-600); }

    /* Footer */
    footer { background: var(--gray-800); color: var(--gray-300); padding: 60px 0 0; }
    .footer-top { max-width: 1140px; margin: 0 auto; padding: 0 20px; display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 40px; padding-bottom: 40px; border-bottom: 1px solid var(--gray-700); }
    .footer-logo { font-size: 1.1rem; font-weight: 700; color: var(--white); margin-bottom: 12px; display: block; text-decoration: none; }
    .footer-desc { font-size: 0.85rem; line-height: 1.6; margin-bottom: 20px; }
    .footer-social { display: flex; gap: 12px; }
    .footer-social a { color: var(--gray-400); text-decoration: none; font-size: 0.9rem; }
    .footer-heading { color: var(--white); font-weight: 600; margin-bottom: 16px; font-size: 0.95rem; }
    .footer-links { list-style: none; }
    .footer-links li { margin-bottom: 10px; }
    .footer-links a { color: var(--gray-400); text-decoration: none; font-size: 0.85rem; }
    .footer-links a:hover { color: var(--white); }
    .footer-bottom { text-align: center; padding: 20px; font-size: 0.8rem; color: var(--gray-500); }
    .footer-bottom a { color: var(--gray-400); text-decoration: none; margin: 0 8px; }
    @media (max-width: 768px) {
      .footer-top { grid-template-columns: 1fr; gap: 24px; }
    }

    /* Dark mode footer */
    body.dark footer { background: #111827; }
    body.dark .footer-top { border-bottom-color: var(--gray-700); }
  </style>
</head>
<body>
  <!-- Nav -->
  <nav>
    <div class="container nav-inner">
      <a href="${langPrefix}index.html" class="nav-logo">Baidu PPC Pro</a>
      <ul class="nav-links">
        <li><a href="${langPrefix}why-baidu-ppc-pro">Why Baidu PPC Pro</a></li>
        <li><a href="${langPrefix}features">Services</a></li>
        <li><a href="${langPrefix}pricing">Pricing</a></li>
        <li><a href="${langPrefix}clients">Clients</a></li>
        <li><a href="${langPrefix}faq">FAQ</a></li>
        <li><a href="${langPrefix}about">About</a></li>
        <li><a href="${langPrefix}blog">Blog</a></li>
        <li><a href="${langPrefix}contact">Contact</a></li>
      </ul>
      <div class="nav-right-group">
        <a href="${langPrefix}contact" class="nav-cta">Get Started</a>
        <div class="lang-switch">
          <button class="lang-switch-btn" onclick="toggleLangMenu()">🌐 <span id="currentLang">${isJa ? '日本語' : 'English'}</span> ▾</button>
          <div class="lang-switch-menu" id="langMenu">
            <a href="${isJa ? '../blog/' + slug + '.html' : 'blog/' + slug + '.html'}">English</a>
            <a href="${isJa ? 'blog/' + slug + '.html' : 'ja/blog/' + slug + '.html'}">日本語</a>
          </div>
        </div>
        <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle theme">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        </button>
        <button class="nav-toggle" onclick="toggleNav()" aria-label="Toggle menu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </nav>
  <div class="nav-overlay" id="navOverlay" aria-hidden="true" onclick="toggleNav()"></div>
  <div class="nav-mobile-panel" id="mobilePanel">
    <a href="${langPrefix}why-baidu-ppc-pro">Why Baidu PPC Pro</a>
    <a href="${langPrefix}features">Services</a>
    <a href="${langPrefix}pricing">Pricing</a>
    <a href="${langPrefix}clients">Clients</a>
    <a href="${langPrefix}faq">FAQ</a>
    <a href="${langPrefix}about">About</a>
    <a href="${langPrefix}blog">Blog</a>
    <a href="${langPrefix}contact">Contact</a>
  </div>

  <main>
    <article class="article-content">
      <div class="article-category ${catClass}">${catName}</div>
      <h1 class="article-title">${title}</h1>
      <div class="article-meta">
        <span>${dateStr}</span>
        <span class="dot"></span>
        <span>${readingTime} min read</span>
        <span class="dot"></span>
        <span>By ${author}</span>
      </div>
      <div class="article-body">
        ${bodyHtml}
      </div>
    </article>
  </main>

  <!-- Footer -->
  <footer>
    <div class="footer-top">
      <div class="footer-col">
        <a href="${langPrefix}index.html" class="footer-logo">Baidu PPC Pro</a>
        <p class="footer-desc">We help overseas SMEs enter the Chinese market via Baidu PPC advertising. Transparent pricing, no hidden fees.</p>
        <div class="footer-social">
          <a href="https://www.baidu.com" target="_blank" rel="noopener">Baidu</a>
        </div>
      </div>
      <div class="footer-col">
        <h4 class="footer-heading">Services</h4>
        <ul class="footer-links">
          <li><a href="${langPrefix}features">Baidu Ads Management</a></li>
          <li><a href="${langPrefix}features">Keyword Research</a></li>
          <li><a href="${langPrefix}features">Landing Page</a></li>
          <li><a href="${langPrefix}features">Performance Report</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4 class="footer-heading">Company</h4>
        <ul class="footer-links">
          <li><a href="${langPrefix}about">About Us</a></li>
          <li><a href="${langPrefix}privacy">Privacy Policy</a></li>
          <li><a href="${langPrefix}terms">Terms of Service</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4 class="footer-heading">Connect</h4>
        <ul class="footer-links">
          <li><a href="${langPrefix}contact">Contact Us</a></li>
          <li><a href="${langPrefix}blog">Blog</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      &copy; <span id="copyright-year"></span> Baidu PPC Pro. All rights reserved.
      <a href="${langPrefix}privacy">Privacy</a> | <a href="${langPrefix}terms">Terms</a>
    </div>
  </footer>

  <script>
    // Theme
    function toggleTheme() {
      document.body.classList.toggle('dark');
      localStorage.setItem('theme', document.body.classList.contains('dark') ? 'dark' : 'light');
    }
    if (localStorage.getItem('theme') === 'dark') document.body.classList.add('dark');

    // Language menu
    function toggleLangMenu() {
      document.getElementById('langMenu').classList.toggle('open');
    }
    document.addEventListener('click', e => {
      if (!e.target.closest('.lang-switch')) document.getElementById('langMenu').classList.remove('open');
    });

    // Mobile nav
    function toggleNav() {
      document.getElementById('mobilePanel').classList.toggle('open');
      document.getElementById('navOverlay').classList.toggle('open');
    }

    // Copyright
    document.getElementById('copyright-year').textContent = new Date().getFullYear();
  </script>
</body>
</html>`;
}

// ============================================================
// 4. 主流程：读取 → 转换 → 写入 HTML
// ============================================================
const results = [];

for (const task of tasks) {
  try {
    console.log(`\nProcessing: ${task.src.split('/').pop()}`);

    // 检查源文件是否存在
    if (!fs.existsSync(task.src)) {
      console.log(`  SKIP: source file not found: ${task.src}`);
      results.push({ task, status: 'skip', reason: 'source not found' });
      continue;
    }

    const { fm, body } = parseObsidianMd(task.src);

    // 验证必需字段
    if (!fm.title || !fm.slug) {
      console.log(`  SKIP: missing title or slug in frontmatter`);
      results.push({ task, status: 'skip', reason: 'missing title/slug' });
      continue;
    }

    const bodyHtml = mdToHtml(body);
    const html = generateBlogHtml({ fm, bodyHtml, slug: task.slug, lang: task.lang });

    // 写入文件
    const outPath = task.outDir === 'ja'
      ? path.join('ja/blog', task.slug + '.html')
      : path.join('blog', task.slug + '.html');

    // 确保目录存在
    fs.mkdirSync(path.dirname(outPath), { recursive: true });
    fs.writeFileSync(outPath, html, 'utf8');

    console.log(`  ✓ Written: ${outPath}`);
    results.push({ task, status: 'ok', outPath });
  } catch (err) {
    console.error(`  ERROR: ${err.message}`);
    results.push({ task, status: 'error', reason: err.message });
  }
}

// 汇总
console.log('\n========== SUMMARY ==========');
results.forEach(r => {
  const name = r.task.src.split('/').pop();
  if (r.status === 'ok') console.log(`  ✓ ${name} → ${r.outPath}`);
  else console.log(`  ✗ ${name} → ${r.status.toUpperCase()}: ${r.reason}`);
});
console.log(`\nTotal: ${results.length}, OK: ${results.filter(r => r.status === 'ok').length}, Skip/Error: ${results.filter(r => r.status !== 'ok').length}`);
