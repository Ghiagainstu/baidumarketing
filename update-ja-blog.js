/**
 * update-ja-blog.js v3
 * 直接用翻译文件中的日文标题/摘要替换 ja/blog.html
 * 通过 slug 定位，支持 clean URL (无.html)
 */

const fs = require('fs');
const path = require('path');

const MD_FILE = path.join(__dirname, 'ja', 'blog-cards-ja.md');
const HTML_FILE = path.join(__dirname, 'ja', 'blog.html');
const OUT_FILE = HTML_FILE; // 直接覆盖，先备份

function parseEntries(md) {
  const entries = [];
  const blocks = md.split(/(?=^## \d+\. )/m);
  for (const block of blocks) {
    if (!block.trim()) continue;
    const lines = block.trim().split('\n');
    const slug = lines[0].replace(/^## \d+\. /, '').trim();
    let title = '', excerpt = '', link = '';
    for (const line of lines) {
      let m;
      if (m = line.match(/^\- \*\*タイトル\*\*: `(.+?)`/)) title = m[1];
      else if (m = line.match(/^\- \*\*抜粋\*\*: `(.+?)`/)) excerpt = m[1];
      else if (m = line.match(/^\- \*\*リンク\*\*: `(.+?)`/)) link = m[1];
    }
    // link 可能是 blog/slug.html，去掉 .html 以匹配 clean URL
    const href = (link || slug).replace(/^\.+/, '').replace(/\.html$/, '');
    if (title) entries.push({ slug, title, excerpt, href });
  }
  console.log(`解析到 ${entries.length} 条`);
  return entries;
}

function update(html, entries) {
  let s = html;
  let ok = 0, fail = 0;

  for (const e of entries) {
    // 构造在 <a href="..."> 之后的标题正则表达式
    // 匹配: <a href="HREF">TITLE</a>
    const titleRegex = new RegExp(
      `(<a href="${e.href.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}">)[^<]*(</a>)`,
      'g'
    );
    const before = s;
    s = s.replace(titleRegex, `$1${e.title}$2`);

    // 匹配摘要: 在 href 之后找 <p class="blog-card-excerpt">...</p>
    // 更鲁棒的做法：找到 href 位置，然后向后找第一个 blog-card-excerpt
    const pos = s.indexOf(`href="${e.href}"`);
    if (pos === -1) {
      console.log(`  ✗ 未找到 href: ${e.href}`);
      fail++;
      continue;
    }

    // 从 pos 向后找 <p class="blog-card-excerpt"> 
    const excerptStart = s.indexOf('<p class="blog-card-excerpt">', pos);
    if (excerptStart === -1) {
      console.log(`  ✗ 未找到 excerpt: ${e.href}`);
      fail++;
      continue;
    }
    const excerptEnd = s.indexOf('</p>', excerptStart);
    const oldExcerpt = s.substring(excerptStart, excerptEnd + 4);

    // 检查是否成功替换了标题
    if (s === before) {
      console.log(`  ✗ 标题替换失败: ${e.slug}`);
      fail++;
      continue;
    }

    // 替换摘要
    const newExcerpt = `<p class="blog-card-excerpt">${e.excerpt}</p>`;
    s = s.substring(0, excerptStart) + newExcerpt + s.substring(excerptEnd + 4);

    ok++;
    console.log(`  ✓ ${ok}: ${e.slug}`);
  }

  console.log(`\n成功: ${ok}, 失败: ${fail}`);
  return s;
}

function updateMeta(html) {
  let s = html;
  s = s.replace(/<title>[^<]*<\/title>/, '<title>百度広告に関するよくある質問 — Baidu PPC Pro</title>');
  s = s.replace(
    /<meta name="description" content="[^"]*"\s*\/>/,
    '<meta name="description" content="海外企業のアカウント開設からコンプライアンス要件まで、百度広告アカウントの開設・運用に必要なすべてを解説します。" />'
  );
  s = s.replace(
    /<meta property="og:title" content="[^"]*"\s*\/>/,
    '<meta property="og:title" content="百度広告に関するよくある質問 — Baidu PPC Pro" />'
  );
  s = s.replace(
    /<meta property="og:description" content="[^"]*"\s*\/>/,
    '<meta property="og:description" content="海外企業のアカウント開設からコンプライアンス要件まで、百度広告アカウントの開設・運用に必要なすべてを解説します。" />'
  );
  s = s.replace(
    /<meta name="twitter:title" content="[^"]*"\s*\/>/,
    '<meta name="twitter:title" content="百度広告に関するよくある質問 — Baidu PPC Pro" />'
  );
  s = s.replace(
    /<meta name="twitter:description" content="[^"]*"\s*\/>/,
    '<meta name="twitter:description" content="海外企業のアカウント開設からコンプライアンス要件まで、百度広告アカウントの開設・運用に必要なすべてを解説します。" />'
  );
  return s;
}

function main() {
  const md = fs.readFileSync(MD_FILE, 'utf8');
  const entries = parseEntries(md);
  if (!entries.length) { console.error('无条目'); return; }

  let html = fs.readFileSync(HTML_FILE, 'utf8');

  console.log('备份原文件...');
  fs.writeFileSync(HTML_FILE + '.bak', html, 'utf8');

  console.log('更新卡片...');
  html = update(html, entries);

  console.log('更新 meta...');
  html = updateMeta(html);

  fs.writeFileSync(HTML_FILE, html, 'utf8');
  console.log(`\n完成！原文件已备份至 ${HTML_FILE}.bak`);
}

main();
