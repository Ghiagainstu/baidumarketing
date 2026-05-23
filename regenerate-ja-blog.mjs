import fs from 'fs';
import path from 'path';

// Simple Markdown to HTML converter (handles headings, bold, lists, blockquotes, tables)
function mdToHtml(md) {
  let html = md;
  
  // Tables (must be before other replacements)
  html = html.replace(/^(|[\s\S]*?)^(\|[^\n]*\|[\s\S]*?)(?=^\n|^#|$)/gm, (match, pre, table) => {
    const lines = table.trim().split('\n').filter(l => l.trim());
    if (lines.length < 2) return match;
    const headers = lines[0].split('|').filter(c => c.trim()).map(c => `<th>${c.trim()}</th>`).join('');
    const rows = lines.slice(2).map(r => {
      const cells = r.split('|').filter(c => c.trim()).map(c => `<td>${c.trim()}</td>`).join('');
      return `<tr>${cells}</tr>`;
    }).join('');
    return `<table><thead><tr>${headers}</tr></thead><tbody>${rows}</tbody></table>`;
  });
  
  // Code blocks
  html = html.replace(/```[\s\S]*?```/g, m => {
    const code = m.replace(/```\w*\n?/, '').replace(/```$/, '').trim();
    return `<pre><code>${code.replace(/</g, '&lt;').replace(/>/g, '&gt;')}</code></pre>`;
  });
  
  // Headings
  html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');
  html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
  html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
  
  // Horizontal rules
  html = html.replace(/^---$/gm, '<hr>');
  
  // Bold and italic
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
  
  // Inline code
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
  
  // Links
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
  
  // Images
  html = html.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1">');
  
  // Blockquotes
  html = html.replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>');
  
  // Lists - collect consecutive items
  html = html.replace(/((?:^[\d]+\. .+$\n?)+)/gm, m => {
    return '<ol>' + m.replace(/^\d+\. (.+)$/gm, '<li>$1</li>') + '</ol>';
  });
  html = html.replace(/((?:^- .+$\n?)+)/gm, m => {
    return '<ul>' + m.replace(/^- (.+)$/gm, '<li>$1</li>') + '</ul>';
  });
  
  // Paragraphs (lines not empty, not starting with <, not a header)
  const lines = html.split('\n');
  let result = [];
  let i = 0;
  while (i < lines.length) {
    const line = lines[i].trim();
    if (!line || line.startsWith('<')) {
      if (line) result.push(line);
      i++;
    } else {
      // Collect consecutive non-tag lines as a paragraph
      let para = line;
      i++;
      while (i < lines.length && lines[i].trim() && !lines[i].trim().startsWith('<')) {
        para += ' ' + lines[i].trim();
        i++;
      }
      result.push(`<p>${para}</p>`);
    }
  }
  
  return result.join('\n');
}

// Parse frontmatter
function parseFrontmatter(md) {
  const fm = {};
  const match = md.match(/^---\n([\s\S]*?)\n---/);
  if (match) {
    match[1].split('\n').forEach(line => {
      const idx = line.indexOf(':');
      if (idx > 0) {
        const k = line.substring(0, idx).trim();
        const v = line.substring(idx + 1).trim();
        fm[k] = v;
      }
    });
  }
  return fm;
}

// Read template and replace placeholders
function generateBlogHtml(templateHtml, frontmatter, articleHtml, slug) {
  let html = templateHtml;
  
  const title = frontmatter.title || slug;
  const description = frontmatter.description || '';
  const date = frontmatter.date || '2026-01-01';
  const readingTime = frontmatter['reading_time'] || '5';
  const category = frontmatter.category || 'insights';
  
  // Format date for display
  const dateObj = new Date(date);
  const dateStr = dateObj.toLocaleDateString('ja-JP', { year: 'numeric', month: 'long', day: 'numeric' });
  
  // Replace title in <title> and OG tags
  html = html.replace(/<title>.*?<\/title>/, `<title>${title} — Baidu PPC Pro Blog</title>`);
  html = html.replace(/(<meta property="og:title" content=").*?(" \/>)/, `$1${title}$2`);
  html = html.replace(/(<meta name="twitter:title" content=").*?(" \/>)/, `$1${title}$2`);
  html = html.replace(/(<meta name="description" content=").*?(" \/>)/, `$1${description}$2`);
  html = html.replace(/(<meta property="og:description" content=").*?(" \/>)/, `$1${description}$2`);
  html = html.replace(/(<meta name="twitter:description" content=").*?(" \/>)/, `$1${description}$2`);
  
  // Replace canonical and OG URL
  html = html.replace(/(<link rel="canonical" href=").*?(" \/>)/g, `$1https://www.baidumarketing.com/ja/blog/${slug}$2`);
  html = html.replace(/(<meta property="og:url" content=").*?(" \/>)/, `$1https://www.baidumarketing.com/ja/blog/${slug}$2`);
  
  // Replace hreflang links
  html = html.replace(/(<link rel="alternate" hreflang="en" href=").*?(" \/>)/, `$1https://www.baidumarketing.com/blog/${slug}$2`);
  html = html.replace(/(<link rel="alternate" hreflang="ja" href=").*?(" \/>)/, `$1https://www.baidumarketing.com/ja/blog/${slug}$2`);
  html = html.replace(/(<link rel="alternate" hreflang="x-default" href=").*?(" \/>)/, `$1https://www.baidumarketing.com/blog/${slug}$2`);
  
  // Replace article-hero section
  const heroReplacement = `  <section class="article-hero">
    <div style="position:absolute;top:-80px;right:-80px;width:400px;height:400px;background:radial-gradient(circle,rgba(41,50,225,.06) 0%,transparent 70%);pointer-events:none;" aria-hidden="true"></div>
    <div class="container">
      <div class="breadcrumb"><a href="/ja/">ホーム</a> / <a href="/ja/blog.html">ブログ</a></div>
      <h1 class="article-title">${title}</h1>
      <div class="article-meta"><span>${dateStr}</span><span> · </span><span>${readingTime} min read</span><span> · </span><span>Baidu PPC Pro Team</span></div>
    </div>
  </section>`;
  html = html.replace(/<section class="article-hero">[\s\S]*?<\/section>/, heroReplacement);
  
  // Replace article-content section
  html = html.replace(/(<article class="article-content">)[\s\S]*?(<\/article>)/, `$1\n${articleHtml}\n  $2`);
  
  return html;
}

// Main
const vaultPath = 'E:/Obsidian/Baidu/';
const outputBase = 'c:/Users/HYE/WorkBuddy/20260411211839/';
const templatePath = outputBase + 'ja/blog/baidu-ocpc-skip-data-accumulation.html';

const files = [
  { md: '02-Platform/baidu-2026-new-opportunities-jp.md', slug: 'baidu-2026-new-opportunities' },
  { md: '02-Platform/bpp-06-baidu-ecosystem-data-jp.md', slug: 'baidu-ecosystem-numbers' }
];

async function main() {
  // Read template
  if (!fs.existsSync(templatePath)) {
    console.error('Template not found:', templatePath);
    return;
  }
  const template = fs.readFileSync(templatePath, 'utf8');
  console.log('Template loaded, length:', template.length);
  
  for (const file of files) {
    const mdPath = vaultPath + file.md;
    if (!fs.existsSync(mdPath)) {
      console.log('MD file not found:', mdPath);
      continue;
    }
    
    const md = fs.readFileSync(mdPath, 'utf8');
    const frontmatter = parseFrontmatter(md);
    console.log('Frontmatter:', JSON.stringify(frontmatter, null, 2));
    
    // Extract content (after frontmatter)
    const contentStart = md.indexOf('---', 3) + 3;
    const content = md.substring(contentStart).trim();
    
    // Convert Markdown to HTML
    const articleHtml = mdToHtml(content);
    console.log('Article HTML length:', articleHtml.length);
    
    // Generate full HTML
    const html = generateBlogHtml(template, frontmatter, articleHtml, file.slug);
    
    // Write output
    const outPath = outputBase + `ja/blog/${file.slug}.html`;
    fs.writeFileSync(outPath, html, 'utf8');
    console.log('Generated:', outPath);
  }
}

main().catch(console.error);
