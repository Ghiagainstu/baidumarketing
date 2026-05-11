const fs = require('fs');
const path = require('path');

const BLOG_DIR = 'C:/Users/HYE/WorkBuddy/20260411211839/blog';
const VAULT_DIR = 'E:/Obsidian/Baidu';

// 分类映射：folder name → vault subfolder
const CATEGORY_MAP = {
  'insights':     '01-Market-Insights',
  'search':       '03-Search-Ads',
  'feed':         '04-Feed-Ads',
  'strategy':     '05-Strategy',
  'landing':     '06-Landing-Page',
  'platform':     '02-Platform',
};

// 读取 HTML 文件，提取信息
function parseBlogHTML(filePath) {
  const html = fs.readFileSync(filePath, 'utf8');

  // 提取 title（从 <title> 标签）
  const titleMatch = html.match(/<title>(.*?)<\/title>/);
  const title = titleMatch ? titleMatch[1].replace(/ — Baidu PPC Pro.*/, '').replace(/ — Baidu PPC Pro Blog.*/, '').trim() : '';

  // 提取 description
  const descMatch = html.match(/<meta name="description" content="(.*?)"/);
  const description = descMatch ? descMatch[1] : '';

  // 提取 category（从 blog-card data-category 的对应，这里从 HTML 里找）
  // 从文章内容找 category，或者从附近的 blog.html 找
  // 简化：从 HTML 注释或内容推断
  const category = inferCategory(path.basename(filePath, '.html'), title);

  // 提取发布日期（从文章内容或文件名推断）
  const date = inferDate(filePath);

  // 提取正文（<article class="article-content"> 内容）
  const articleMatch = html.match(/<article class="article-content">([\s\S]*?)<\/article>/);
  const bodyHTML = articleMatch ? articleMatch[1] : '';

  return { title, description, category, date, bodyHTML, slug: path.basename(filePath, '.html') };
}

function inferCategory(slug, title) {
  if (slug.includes('earnings') || slug.includes('ai-assistants') || slug.includes('internet-numbers') || slug.includes('search-vs-ai') || slug.includes('digital-consumer')) return 'insights';
  if (slug.includes('ecosystem') || slug.includes('app-ecosystem') || slug.includes('user-data') || slug.includes('display-name') || slug.includes('v-sign') || slug.includes('account-status') || slug.includes('ppc-different') || slug.includes('vs-google') || slug.includes('url-wildcard') || slug.includes('search-ad-video-format')) return 'platform';
  if (slug.includes('feed') || slug.includes('native-ads')) return 'feed';
  if (slug.includes('keyword-research') || slug.includes('digital-marketing') || slug.includes('can-i-do') || slug.includes('how-much') || slug.includes('ppc-terms')) return 'strategy';
  if (slug.includes('landing') || slug.includes('bounce')) return 'landing';
  if (slug.includes('cpm') || slug.includes('ocpm') || slug.includes('pricing-models')) return 'search';
  return 'search'; // 默认
}

function inferDate(filePath) {
  const html = fs.readFileSync(filePath, 'utf8');
  // 尝试从内容里找日期
  const dateMatch = html.match(/(\d{4})[\s\S]{0,200}?(January|February|March|April|May|June|July|August|September|October|November|December)[\s\S]{0,50}?(\d{1,2})/i);
  // 默认用文件修改日期
  const stats = fs.statSync(filePath);
  const d = stats.mtime;
  return d.toISOString().split('T')[0];
}

// 极简 HTML → Markdown 转换
function htmlToMarkdown(html) {
  let md = html;

  // 移除 script 和 style 标签
  md = md.replace(/<script[\s\S]*?<\/script>/gi, '');
  md = md.replace(/<style[\s\S]*?<\/style>/gi, '');

  // 标题
  md = md.replace(/<h1[^>]*>(.*?)<\/h1>/gi, '# $1');
  md = md.replace(/<h2[^>]*>(.*?)<\/h2>/gi, '## $1');
  md = md.replace(/<h3[^>]*>(.*?)<\/h3>/gi, '### $1');
  md = md.replace(/<h4[^>]*>(.*?)<\/h4>/gi, '#### $1');

  // 粗体/斜体
  md = md.replace(/<strong[^>]*>(.*?)<\/strong>/gi, '**$1**');
  md = md.replace(/<b[^>]*>(.*?)<\/b>/gi, '**$1**');
  md = md.replace(/<em[^>]*>(.*?)<\/em>/gi, '*$1*');

  // 链接
  md = md.replace(/<a[^>]*href="([^"]*)"[^>]*>(.*?)<\/a>/gi, '[$2]($1)');

  // 图片
  md = md.replace(/<img[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*\/?>/gi, '![$2]($1)');
  md = md.replace(/<img[^>]*src="([^"]*)"[^>]*\/?>/gi, '![]($1)');

  // 列表
  md = md.replace(/<li[^>]*>(.*?)<\/li>/gi, '- $1');
  md = md.replace(/<ul[^>]*>([\s\S]*?)<\/ul>/gi, '$1');
  md = md.replace(/<ol[^>]*>([\s\S]*?)<\/ol>/gi, (_, content) => {
    let i = 1;
    return content.replace(/<li[^>]*>(.*?)<\/li>/gi, () => `${i++}. $1`);
  });

  // 段落
  md = md.replace(/<p[^>]*>(.*?)<\/p>/gi, '\n$1\n');

  // 换行
  md = md.replace(/<br\s*\/?>/gi, '\n');
  md = md.replace(/<div[^>]*>(.*?)<\/div>/gi, '\n$1\n');

  // 移除所有剩余的 HTML 标签
  md = md.replace(/<[^>]+>/g, '');

  // 解码 HTML 实体
  md = md.replace(/&nbsp;/g, ' ');
  md = md.replace(/&amp;/g, '&');
  md = md.replace(/&lt;/g, '<');
  md = md.replace(/&gt;/g, '>');
  md = md.replace(/&quot;/g, '"');
  md = md.replace(/&#39;/g, "'");
  md = md.replace(/&mdash;/g, '—');
  md = md.replace(/&ndash;/g, '–');

  // 清理多余空行
  md = md.replace(/\n{3,}/g, '\n\n');

  return md.trim();
}

// 检查 MD 文件是否已存在（通过标题模糊匹配）
function existsInVault(title, vaultDir) {
  const files = getAllFiles(vaultDir, '.md');
  for (const file of files) {
    const content = fs.readFileSync(file, 'utf8');
    // 检查前 5 行是否包含相似标题
    const firstLines = content.split('\n').slice(0, 10).join('\n');
    const titleWords = title.toLowerCase().replace(/[^\w\s]/g, '').split(' ').filter(w => w.length > 3);
    for (const word of titleWords) {
      if (firstLines.toLowerCase().includes(word)) {
        return file;
      }
    }
  }
  return null;
}

function getAllFiles(dir, ext) {
  let results = [];
  if (!fs.existsSync(dir)) return results;
  const list = fs.readdirSync(dir);
  for (const file of list) {
    const full = path.join(dir, file);
    const stat = fs.statSync(full);
    if (stat && stat.isDirectory()) {
      results = results.concat(getAllFiles(full, ext));
    } else if (file.endsWith(ext)) {
      results.push(full);
    }
  }
  return results;
}

// 生成 Obsidian 格式的 MD 内容
function generateMD(post, vaultSubdir) {
  const lines = [];
  lines.push('---');
  lines.push(`title: "${post.title}"`);
  lines.push(`date: ${post.date}`);
  lines.push(`category: ${post.category}`);
  lines.push(`source: "https://baidumarketing.com/blog/${post.slug}"`);
  lines.push(`tags: ["Baidu", "PPC", "${post.category}"]`);
  lines.push('---\n');
  if (post.description) {
    lines.push(`> ${post.description}\n`);
  }
  lines.push(post.markdown);
  return lines.join('\n');
}

// 主流程
function main() {
  const files = fs.readdirSync(BLOG_DIR).filter(f => f.endsWith('.html')).sort();
  console.log(`找到 ${files.length} 篇博客\n`);

  const results = { skipped: [], added: [], errors: [] };

  for (const file of files) {
    const filePath = path.join(BLOG_DIR, file);
    const slug = file.replace('.html', '');

    try {
      const post = parseBlogHTML(filePath);
      const existing = existsInVault(post.title, VAULT_DIR);

      if (existing) {
        results.skipped.push({ slug, title: post.title, existing });
        continue;
      }

      // 转换 HTML → Markdown
      post.markdown = htmlToMarkdown(post.bodyHTML);
      post.date = inferDate(filePath);

      // 确定目标目录
      const subdir = CATEGORY_MAP[post.category] || '03-Search-Ads';
      const targetDir = path.join(VAULT_DIR, subdir);
      if (!fs.existsSync(targetDir)) fs.mkdirSync(targetDir, { recursive: true });

      // 生成文件名：序号-kebab-title.md
      const existingFiles = fs.readdirSync(targetDir).filter(f => f.endsWith('.md')).sort();
      let nextNum = 1;
      if (existingFiles.length > 0) {
        const lastFile = existingFiles[existingFiles.length - 1];
        const numMatch = lastFile.match(/^(\d+)-/);
        if (numMatch) nextNum = parseInt(numMatch[1]) + 1;
      }
      const kebabTitle = post.title.toLowerCase()
        .replace(/[^\w\s-]/g, '')
        .replace(/\s+/g, '-')
        .substring(0, 60);
      const fileName = `${String(nextNum).padStart(2, '0')}-${kebabTitle}.md`;
      const targetPath = path.join(targetDir, fileName);

      const mdContent = generateMD(post, subdir);
      fs.writeFileSync(targetPath, mdContent, 'utf8');
      results.added.push({ slug, title: post.title, file: `${subdir}/${fileName}` });
      console.log(`✅ 已添加: ${subdir}/${fileName}`);

    } catch (e) {
      results.errors.push({ slug, error: e.message });
      console.error(`❌ 错误: ${slug} — ${e.message}`);
    }
  }

  console.log(`\n=== 完成 ===`);
  console.log(`跳过（已存在）: ${results.skipped.length}`);
  console.log(`新添加: ${results.added.length}`);
  console.log(`错误: ${results.errors.length}`);

  if (results.skipped.length > 0) {
    console.log('\n跳过列表:');
    results.skipped.forEach(s => console.log(`  - ${s.slug} → ${path.basename(s.existing)}`));
  }
}

main();
