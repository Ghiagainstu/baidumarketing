const fs = require('fs');
const dir = 'ja/blog';
let fixed = 0;

for (const f of fs.readdirSync(dir).filter(x => x.endsWith('.html'))) {
  const fp = dir + '/' + f;
  let c = fs.readFileSync(fp, 'utf8');

  // Skip pages that already have article-hero
  if (c.includes('article-hero')) continue;

  // Extract title from <h1 class="article-title">
  const titleMatch = c.match(/<h1 class="article-title">([\s\S]*?)<\/h1>/);
  if (!titleMatch) continue;
  const title = titleMatch[1].trim();

  // Extract date from article-meta (first span)
  let dateStr = '';
  const dateMatch = c.match(/<div class="article-meta">\s*<span>(\d{4}-\d{2}-\d{2})<\/span>/);
  if (dateMatch) {
    const [y, m, d] = dateMatch[1].split('-');
    dateStr = `${y}年${parseInt(m)}月${parseInt(d)}日`;
  }

  // Extract reading time (third span: "N min read")
  let readingTime = '1';
  const rtMatch = c.match(/<span>(\d+) min read<\/span>/);
  if (rtMatch) readingTime = rtMatch[1];

  // Determine category from the breadcrumb or article content
  let category = 'ブログ'; // default
  const catMatch = c.match(/<a href="\/ja\/blog\/[^"]*"[^>]*>(\S+)<\/a>/);
  // Try getting category from tags/first section
  const h2Match = c.match(/<h2>[^<]*<\/h2>/);
  if (h2Match) {
    // Use first h2 as a hint but stick with default
  }

  // Remove frontmatter leak: <p>--- status: published title: "..."</p>
  c = c.replace(/<p>---[\s\S]*?---\s*<\/p>\s*/g, '');

  // Build the new article-hero section
  const articleHero = `  <section class="article-hero">
    <div style="position:absolute;top:-80px;right:-80px;width:400px;height:400px;background:radial-gradient(circle,rgba(41,50,225,.06) 0%,transparent 70%);pointer-events:none;" aria-hidden="true"></div>
    <div class="container">
      <div class="breadcrumb"><a href="/ja/">ホーム</a> / <a href="/ja/blog.html">ブログ</a> / ${category}</div>
      <h1 class="article-title">${title}</h1>
      <div class="article-meta"><span>${dateStr}</span><span><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>読了時間 約${readingTime}分</span>
    <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg> Baidu PPC Pro チーム</span>
      </div>
    </div>
  </section>`;

  // Replace the main content area:
  // Old: <main>\n    <article class="article-content">\n      <div class="article-meta">...</div>\n...<h1>...</h1>...
  // New: <main>\n  <section class="article-hero">...</section>\n  <section...><article class="article-content">...</article></section>

  // Remove the old article-meta div + h1 from within article-content
  c = c.replace(/<div class="article-meta">[\s\S]*?<\/div>\s*/g, '');
  c = c.replace(/<h1 class="article-title">[\s\S]*?<\/h1>\s*/g, '');

  // Wrap remaining content: <article class="article-content">...</article> → <section>...<article>
  c = c.replace(
    /<main>\s*<article class="article-content">/,
    '<main>\n' + articleHero + '\n\n  <section class="article-section">\n    <div class="container">\n      <article class="article-content">'
  );

  // Close the new wrappers before </article>
  c = c.replace(
    /<\/article>\s*<\/main>/,
    '      </article>\n    </div>\n  </section>\n</main>'
  );

  fs.writeFileSync(fp, c, 'utf8');
  console.log('Fixed:', fp);
  fixed++;
}

console.log('Total fixed:', fixed);
