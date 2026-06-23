import fs from 'fs';
import path from 'path';

// Simple markdown to HTML converter for BPP blog content
function mdToHtml(md) {
  let html = md;
  
  // Remove frontmatter
  html = html.replace(/^---[\s\S]*?---\n*/m, '');
  
  // Remove title heading (first # heading)
  html = html.replace(/^#\s+.*\n*/m, '');
  
  // Convert headers
  html = html.replace(/^#### (.+)$/gm, '<h4>$1</h4>');
  html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
  html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
  
  // Convert bold
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  
  // Convert italic
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
  
  // Convert links
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
  
  // Convert unordered lists
  html = html.replace(/^- (.+)$/gm, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>\n?)+/g, (match) => '<ul>\n' + match + '</ul>');
  
  // Convert ordered lists
  html = html.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');
  
  // Convert tables - basic support
  html = html.replace(/\|(.+)\|\n\|[-| ]+\|\n((?:\|.+\|\n?)+)/g, (match, header, body) => {
    const headers = header.split('|').map(h => h.trim()).filter(Boolean);
    const rows = body.trim().split('\n').map(row => 
      row.split('|').map(c => c.trim()).filter(Boolean)
    );
    let table = '<table class="comparison-table">\n<thead><tr>';
    headers.forEach(h => table += `<th>${h}</th>`);
    table += '</tr></thead>\n<tbody>';
    rows.forEach(row => {
      table += '<tr>';
      row.forEach(cell => table += `<td>${cell}</td>`);
      table += '</tr>';
    });
    table += '</tbody></table>';
    return table;
  });
  
  // Convert code blocks
  html = html.replace(/```[\w]*\n([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
  
  // Convert inline code
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
  
  // Convert blockquotes
  html = html.replace(/^> (.+)$/gm, '<blockquote>$1</blockquote>');
  
  // Convert horizontal rules
  html = html.replace(/^---$/gm, '<hr>');
  
  // Convert paragraphs (lines that don't start with HTML tags)
  const lines = html.split('\n');
  const result = [];
  let inBlock = false;
  
  for (let line of lines) {
    const trimmed = line.trim();
    if (!trimmed) {
      if (inBlock) result.push('');
      continue;
    }
    if (trimmed.startsWith('<')) {
      result.push(line);
      continue;
    }
    result.push(`<p>${trimmed}</p>`);
  }
  
  html = result.join('\n');
  
  // Clean up empty paragraphs
  html = html.replace(/<p>\s*<\/p>/g, '');
  
  // Convert Obsidian callout divs (already HTML in the MD)
  // Keep as-is
  
  return html;
}

// Read the MD file
const mdPath = process.argv[2];
const outPath = process.argv[3];

if (!mdPath || !outPath) {
  console.error('Usage: node md-to-blog.mjs <input.md> <output.html>');
  process.exit(1);
}

const md = fs.readFileSync(mdPath, 'utf8');
const htmlBody = mdToHtml(md);

// Read the existing HTML template (from a working ko blog page)
const templatePath = process.argv[4] || 'ko/blog/baidu-create-2026-agent-era.html';
const template = fs.readFileSync(templatePath, 'utf8');

// Extract frontmatter for title/description
const fmMatch = md.match(/^---([\s\S]*?)---/);
const fm = {};
if (fmMatch) {
  fmMatch[1].split('\n').forEach(line => {
    const m = line.match(/^(\w+):\s*(.+)/);
    if (m) fm[m[1]] = m[2].replace(/^["']|["']$/g, '');
  });
}

// Replace the article content in the template
const title = fm.title || 'Blog Post';
const desc = fm.description || '';

// Find article content section and replace
let result = template;

// Replace article title
result = result.replace(/<h1 class="article-title">[^<]*<\/h1>/, `<h1 class="article-title">${title}</h1>`);

// Replace article body - find the article-content div
const bodyStart = result.indexOf('<div class="article-content">');
const bodyEnd = result.indexOf('</div>\n    </section>', bodyStart);
const closeDivIdx = result.indexOf('</div>', bodyStart + 30);

if (bodyStart !== -1) {
  // Find the end of article-content div
  let depth = 0;
  let idx = bodyStart;
  let endIdx = -1;
  while (idx < result.length) {
    if (result.substr(idx, 5) === '<div ') depth++;
    if (result.substr(idx, 6) === '</div>') {
      depth--;
      if (depth === 0) { endIdx = idx + 6; break; }
    }
    idx++;
  }
  
  if (endIdx !== -1) {
    result = result.substring(0, bodyStart) + 
             `<div class="article-content">\n${htmlBody}\n    </div>` + 
             result.substring(endIdx);
  }
}

// Update title tag
result = result.replace(/<title>[^<]*<\/title>/, `<title>${title} ¡ª Baidu PPC Pro Blog</title>`);

// Update og:title
result = result.replace(/<meta property="og:title" content="[^"]*"/, `<meta property="og:title" content="${title}"`);

// Update og:description  
if (desc) {
  result = result.replace(/<meta property="og:description" content="[^"]*"/, `<meta property="og:description" content="${desc}"`);
  result = result.replace(/<meta name="description" content="[^"]*"/, `<meta name="description" content="${desc}"`);
}

// Update JSON-LD headline
result = result.replace(/"headline":\s*"[^"]*"/, `"headline": "${title}"`);

fs.writeFileSync(outPath, result, 'utf8');
console.log(`Created ${outPath} (${result.length} bytes)`);
