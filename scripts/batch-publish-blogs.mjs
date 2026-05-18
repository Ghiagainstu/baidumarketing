#!/usr/bin/env node
/**
 * batch-publish-blogs.mjs
 * 批量发布昨天新建的 blog：更新 blog.html / sitemap.xml → git push → 同步 Obsidian
 */

import { readFileSync, writeFileSync, appendFileSync } from 'fs';
import { join } from 'path';

const SITE_ROOT = 'c:/Users/HYE/WorkBuddy/20260411211839';
const TODAY = new Date().toISOString().split('T')[0];

// 新 blog 列表（已创建 HTML 的）
const NEW_BLOGS = [
  {
    slug: 'baidu-ads-campaign-upgrade-2025',
    title: 'Baidu Ads Campaign Upgrades 2025: What Actually Changed',
    date: '2025-10-16',
    category: 'platform',
    excerpt: 'Baidu shipped three real platform upgrades in October 2025: simplified campaign creation, AI copywriting improvements, and better targeting filters.',
    readTime: 8,
    isJP: false
  },
  {
    slug: 'baidu-custom-form-retirement',
    title: 'Baidu Retires Custom Form Creative Component: What Advertisers Need to Know',
    date: '2024-07-24',
    category: 'search',
    excerpt: 'Baidu retired the Custom Form creative component in July 2024. Here is what changed, whether it affects your account.',
    readTime: 6,
    isJP: false
  }
];

// 读取文件
function readFile(path) {
  return readFileSync(join(SITE_ROOT, path), 'utf8');
}

// 写入文件
function writeFile(path, content) {
  writeFileSync(join(SITE_ROOT, path), content, 'utf8');
}

// 追加到文件
function appendFile(path, content) {
  appendFileSync(join(SITE_ROOT, path), content, 'utf8');
}

// 生成 blog-card HTML
function generateCard(blog) {
  const dateStr = new Date(blog.date).toLocaleDateString('en-US', { month: 'short', year: 'numeric', day: 'numeric' });
  return `      <!-- NEW: ${blog.slug} -->
      <div class="blog-card" data-category="${blog.category}">
        <span class="blog-card-tag ${blog.category}">${blog.category.charAt(0).toUpperCase() + blog.category.slice(1)}</span>
        <h3 class="blog-card-title"><a href="blog/${blog.slug}">${blog.title}</a></h3>
        <p class="blog-card-excerpt">${blog.excerpt}</p>
        <div class="blog-card-meta"><span>${dateStr}</span><span class="read-time"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> ${blog.readTime} min</span></div>
      </div>\n`;
}

// 更新 blog.html
function updateBlogHtml() {
  console.log('📝 更新 blog.html...');
  let html = readFile('blog.html');
  
  for (const blog of NEW_BLOGS) {
    const cardHtml = generateCard(blog);
    
    // 找到对应 category 的最后一个 card，在其后插入
    const categoryRegex = new RegExp(`(<div class="blog-card" data-category="${blog.category}">[\\s\\S]*?</div>)\\n(      <!--|    </section>)`, 'g');
    const matches = [...html.matchAll(categoryRegex)];
    
    if (matches.length > 0) {
      const lastMatch = matches[matches.length - 1];
      const insertPos = html.indexOf(lastMatch[0]) + lastMatch[0].length;
      html = html.slice(0, insertPos) + '\n' + cardHtml + html.slice(insertPos);
      console.log(`   ✅ 插入 ${blog.slug} 到 ${blog.category} 分类`);
    }
  }
  
  writeFile('blog.html', html);
  console.log('   ✅ blog.html 更新完成');
}

// 更新 sitemap.xml
function updateSitemap() {
  console.log('📋 更新 sitemap.xml...');
  const sitemapPath = 'sitemap.xml';
  let xml = readFile(sitemapPath);
  
  for (const blog of NEW_BLOGS) {
    const urlBlock = `  <url>
    <loc>https://baidumarketing.com/blog/${blog.slug}</loc>
    <lastmod>${blog.date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.6</priority>
  </url>\n</urlset>`;
    
    xml = xml.replace('</urlset>', urlBlock);
    console.log(`   ✅ 添加 ${blog.slug} 到 sitemap`);
  }
  
  writeFile(sitemapPath, xml);
  console.log('   ✅ sitemap.xml 更新完成');
}

// 更新 Obsidian frontmatter
function updateObsidian() {
  console.log('📋 更新 Obsidian frontmatter...');
  
  for (const blog of NEW_BLOGS) {
    // 找到对应的 Obsidian 文件
    const obsidianPath = join('E:/Obsidian/Baidu', `bpp-${blog.slug}-en.md`);
    try {
      const content = readFileSync(obsidianPath, 'utf8');
      const fmMatch = content.match(/^---\s*\n([\s\S]*?)\n---/);
      
      if (fmMatch) {
        // 添加 slug 和 status
        let newFm = fmMatch[1] + `\nslug: ${blog.slug}\nstatus: pushed\npush_date: ${TODAY}\nurl_en: https://baidumarketing.com/blog/${blog.slug}\nurl_jp: \n`;
        const newContent = content.replace(fmMatch[1], newFm);
        writeFileSync(obsidianPath, newContent, 'utf8');
        console.log(`   ✅ 更新 ${blog.slug}-en.md`);
      }
    } catch(e) {
      console.log(`   ⚠️ 找不到文件: bpp-${blog.slug}-en.md`);
    }
  }
}

// 主函数
function main() {
  console.log('🚀 批量发布 blog...\n');
  
  // 1. 更新 blog.html
  updateBlogHtml();
  
  // 2. 更新 sitemap.xml
  updateSitemap();
  
  console.log('\n📋 Git add & commit...');
  console.log('   运行: git add -A');
  console.log('   运行: git commit -m "feat: add new blog posts"');
  console.log('   运行: git push');
  console.log('\n💡 请手动运行 git 命令，或在下一条消息中让我运行');
  
  // 3. 更新 Obsidian（注释掉，因为需要先 git push）
  // updateObsidian();
}

main();
