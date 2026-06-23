import fs from 'fs';

const mdPath = process.argv[2];
const htmlPath = process.argv[3];

const md = fs.readFileSync(mdPath, 'utf8');
let html = fs.readFileSync(htmlPath, 'utf8');

// Extract frontmatter
const fmMatch = md.match(/^---([\s\S]*?)---/);
const fm = {};
if (fmMatch) {
  fmMatch[1].split('\n').forEach(line => {
    const m = line.match(/^(\w+):\s*(.+)/);
    if (m) fm[m[1]] = m[2].replace(/^["']|["']$/g, '');
  });
}

// Simple MD to HTML
let body = md.replace(/^---[\s\S]*?---\n*/m, '');
body = body.replace(/^#\s+.*\n*/m, ''); // remove title h1
body = body.replace(/^#### (.+)$/gm, '<h4>$1</h4>');
body = body.replace(/^### (.+)$/gm, '<h3>$1</h3>');
body = body.replace(/^## (.+)$/gm, '<h2>$1</h2>');
body = body.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
body = body.replace(/\*(.+?)\*/g, '<em>$1</em>');
body = body.replace(/^- (.+)$/gm, '<li>$1</li>');
body = body.replace(/^(\d+)\. (.+)$/gm, '<li>$2</li>');
body = body.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');

// Wrap loose <li> in <ul>
body = body.replace(/((?:<li>.*<\/li>\s*)+)/g, '<ul>\n$1</ul>');

// Convert paragraphs
body = body.split('\n').map(line => {
  const t = line.trim();
  if (!t) return '';
  if (t.startsWith('<')) return line;
  return `<p>${t}</p>`;
}).join('\n');

// Clean wiki-links
body = body.replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, '<strong>$2</strong>');
body = body.replace(/\[\[([^\]]+)\]\]/g, '<strong>$1</strong>');

// Replace article content in HTML
// Find: from after <div class="article-content"> to the matching </div>
const startMarker = '<div class="article-content">';
const startIdx = html.indexOf(startMarker);
if (startIdx === -1) { console.error('article-content not found'); process.exit(1); }

// Find matching closing div
let depth = 0;
let i = startIdx;
let endIdx = -1;
while (i < html.length) {
  if (html.substr(i, 5) === '<div ') { depth++; i += 4; continue; }
  if (html.substr(i, 6) === '</div>') { 
    depth--; 
    if (depth === 0) { endIdx = i + 6; break; }
    i += 5; continue;
  }
  i++;
}

if (endIdx === -1) { console.error('Could not find closing div'); process.exit(1); }

const newArticle = `<div class="article-content">\n${body}\n    </div>`;
html = html.substring(0, startIdx) + newArticle + html.substring(endIdx);

// Update meta
const title = fm.title || 'Blog Post';
html = html.replace(/<title>[^<]*<\/title>/, `<title>${title} ¡ª Baidu PPC Pro Blog</title>`);
html = html.replace(/<meta property="og:title" content="[^"]*"/, `<meta property="og:title" content="${title}"`);
html = html.replace(/"headline":\s*"[^"]*"/, `"headline": "${title}"`);
if (fm.description) {
  html = html.replace(/<meta property="og:description" content="[^"]*"/, `<meta property="og:description" content="${fm.description}"`);
  html = html.replace(/<meta name="description" content="[^"]*"/, `<meta name="description" content="${fm.description}"`);
}

fs.writeFileSync(htmlPath, html, 'utf8');
console.log(`Updated ${htmlPath} (${html.length} bytes)`);
