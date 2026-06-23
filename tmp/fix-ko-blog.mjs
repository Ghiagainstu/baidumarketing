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
body = body.replace(/^#\s+.*\n*/m, '');
body = body.replace(/^#### (.+)$/gm, '<h4>$1</h4>');
body = body.replace(/^### (.+)$/gm, '<h3>$1</h3>');
body = body.replace(/^## (.+)$/gm, '<h2>$1</h2>');
body = body.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
body = body.replace(/\*(.+?)\*/g, '<em>$1</em>');
body = body.replace(/^- (.+)$/gm, '<li>$1</li>');
body = body.replace(/^(\d+)\. (.+)$/gm, '<li>$2</li>');
body = body.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
body = body.replace(/((?:<li>.*<\/li>\s*)+)/g, '<ul>\n$1</ul>');
body = body.replace(/\[\[([^\]|]+)\|([^\]]+)\]\]/g, '<strong>$2</strong>');
body = body.replace(/\[\[([^\]]+)\]\]/g, '<strong>$1</strong>');

// Convert loose paragraphs
body = body.split('\n').map(line => {
  const t = line.trim();
  if (!t) return '';
  if (t.startsWith('<')) return line;
  return '<p>' + t + '</p>';
}).join('\n');

// Find article content - try both div and article tags
let startMarker = '<article class="article-content">';
let startIdx = html.indexOf(startMarker);
let isArticle = true;
if (startIdx === -1) {
  startMarker = '<div class="article-content">';
  startIdx = html.indexOf(startMarker);
  isArticle = false;
}
if (startIdx === -1) { console.error('article-content not found'); process.exit(1); }

// Find matching closing tag
const openTag = isArticle ? '<article' : '<div';
const closeTag = isArticle ? '</article>' : '</div>';
let depth = 0;
let i = startIdx;
let endIdx = -1;
while (i < html.length) {
  if (html.substr(i, openTag.length + 1) === openTag + ' ' || html.substr(i, openTag.length + 1) === openTag + '>') { depth++; i += openTag.length; continue; }
  if (html.substr(i, closeTag.length) === closeTag) {
    depth--;
    if (depth === 0) { endIdx = i + closeTag.length; break; }
    i += closeTag.length - 1; continue;
  }
  i++;
}
if (endIdx === -1) { console.error('Could not find closing tag'); process.exit(1); }

const newArticle = startMarker + '\n' + body + '\n    ' + closeTag;
html = html.substring(0, startIdx) + newArticle + html.substring(endIdx);

// Update meta
const title = fm.title || 'Blog Post';
html = html.replace(/<title>[^<]*<\/title>/, '<title>' + title + ' \u2014 Baidu PPC Pro Blog</title>');
html = html.replace(/<meta property="og:title" content="[^"]*"/, '<meta property="og:title" content="' + title + '"');
html = html.replace(/"headline":\s*"[^"]*"/, '"headline": "' + title + '"');
if (fm.description) {
  html = html.replace(/<meta property="og:description" content="[^"]*"/, '<meta property="og:description" content="' + fm.description + '"');
  html = html.replace(/<meta name="description" content="[^"]*"/, '<meta name="description" content="' + fm.description + '"');
}

fs.writeFileSync(htmlPath, html, 'utf8');
console.log('Updated ' + htmlPath + ' (' + html.length + ' bytes)');
