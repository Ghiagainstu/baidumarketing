/**
 * Comprehensive fix for baidu-brand-info-account-level.html
 * Fixes: HTML structure (article-hero/article-section),
 *         garbage <p> tag, footer structure, missing CTA and Related Articles
 */
const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, 'blog/baidu-brand-info-account-level.html');
let html = fs.readFileSync(filePath, 'utf8');

// 1. Fix nav-logo href: "index" -> "/"
html = html.replace(/<a href="index"/, '<a href="/"');

// 2. Fix nav-cta href: "contact" -> "/contact"
html = html.replace(/<a href="contact" class="nav-cta">/, '<a href="/contact" class="nav-cta">');

// 3. Fix footer links: add missing "/" prefix
html = html.replace(/<li><a href="features">/, '<li><a href="/features">');
html = html.replace(/<li><a href="pricing">/, '<li><a href="/pricing">');
html = html.replace(/<li><a href="clients">/, '<li><a href="/clients">');
html = html.replace(/<li><a href="about">/, '<li><a href="/about">');
html = html.replace(/<li><a href="faq">/, '<li><a href="/faq">');
html = html.replace(/<li><a href="blog">/, '<li><a href="/blog">');
html = html.replace(/<li><a href="privacy">/, '<li><a href="/privacy">');
html = html.replace(/<li><a href="terms">/, '<li><a href="/terms">');
html = html.replace(/<li><a href="contact">/, '<li><a href="/contact">');

// 4. Fix footer-brand h3: replace "4️⃣ BPP Baidu PPC Pro" with SVG logo version
html = html.replace(
  /<h3>4️⃣ BPP Baidu PPC Pro<\/h3>/,
  '<h3><svg width="28" height="28" viewBox="0 0 32 32" fill="none"><defs><linearGradient id="fLogo2" x1="0" y1="0" x2="32" y2="32"><stop offset="0%" stop-color="#2932E1"/><stop offset="100%" stop-color="#4F46E5"/></linearGradient></defs><rect width="32" height="32" rx="8" fill="url(#fLogo2)"/><text x="16" y="21" text-anchor="middle" font-size="12" font-weight="800" fill="white">BPP</text></svg> Baidu PPC Pro</h3>'
);

// 5. Fix the footer-copy section (the script tag is misplaced)
html = html.replace(
  /<div class="footer-copy">© <script>document\.write\(new Date\(\)\.getFullYear\(\)\)\n\(function\(\)\{const t=document\.getElementById\('backToTop'\);if\(t\)window\.addEventListener\('scroll',\(\)=>\{t\.classList\.toggle\('visible',window\.scrollY>400\)\}\)\)\(\);\n  <\/script> Baidu PPC Pro\. All rights reserved\.<\/div>/,
  '<div class="footer-copy">&copy; <script>document.write(new Date().getFullYear())</script> Baidu PPC Pro. All rights reserved.</div>'
);

// 6. Fix the missing </li> for Terms of Service link
html = html.replace(
  /<li><a href="\/terms">Terms of Service<\/a><\/li>/,
  '<li><a href="/terms">Terms of Service</a></li>'
);
// The original HTML (line 441) has: <li><a href="terms">Terms of Service</a></li></ul>
// but it's missing the <li> wrapper for the privacy link too
// Let me re-check... Actually line 441 is: <div class="footer-col"><h4>Legal</h4><ul><li><a href="privacy">Privacy Policy</a></li><li><a href="terms">Terms of Service</a></li></ul></div>
// The second <li> is missing. Let me fix that properly.
html = html.replace(
  /<li><a href="\/privacy">Privacy Policy<\/a><\/li><li><a href="\/terms">Terms of Service<\/a><\/li>/,
  '<li><a href="/privacy">Privacy Policy</a></li>\n        <li><a href="/terms">Terms of Service</a></li>'
);

// 7. Remove the garbage <p> tag (line 373)
html = html.replace(/<p>--- status: published title: [^<]*<\/p>\s*\n/, '');

// 8. Fix the article-meta to include SVG icons (like baseline)
// Current: <div class="article-meta"><span>2026-05-17</span>...
// Should have: date icon, clock icon, category icon, author icon
const oldMeta = `<div class="article-meta">
        <span>2026-05-17</span>
        <span>·</span>
        <span>4 min read</span>
        <span>·</span>
        <span>Baidu PPC Pro Team</span>
      </div>`;
const newMeta = `      <div class="article-meta">
          <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg> May 17, 2026</span>
          <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> 4 min read</span>
          <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg> Search Ads</span>
          <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg> By Baidu PPC Pro Team</span>
        </div>`;

if (html.includes(oldMeta)) {
  html = html.replace(oldMeta, newMeta);
  console.log('Fixed article-meta with SVG icons');
} else {
  console.log('WARNING: Could not find old article-meta to replace');
}

// 9. Restructure the HTML: add article-hero and article-section wrappers
// The current structure from <main> to </main>:
//   <main>
//     <article class="article-content">
//       <div class="article-meta">...</div>
//       <h1 class="article-title">...</h1>
//       ... content ...
//       <div class="takeaway">...</div>
//     </article>
//   </main>
// Should become:
//   <main>
//     <section class="article-hero">
//       <div class="container">
//         <h1 class="article-title">...</h1>
//         <div class="article-meta">...</div>
//       </div>
//     </section>
//     <section class="article-section">
//       <div class="container">
//         <article class="article-content">
//           ... content (without h1 and meta) ...
//         </article>
//       </div>
//     </section>
//   </main>

// This is complex string manipulation. Let me extract the content and rebuild.
const mainMatch = html.match(/<main>([\s\S]*?)<\/main>/);
if (mainMatch) {
  const mainContent = mainMatch[1];
  
  // Extract h1
  const h1Match = mainContent.match(/<h1 class="article-title">([^<]*)<\/h1>/);
  const h1Text = h1Match ? h1Match[1] : 'Baidu Moves Brand Info to Account Level';
  
  // Extract article-meta (new version with SVG icons)
  const metaSection = newMeta;
  
  // Extract content from first h2 to end of takeaway
  const contentStart = mainContent.match(/<h2>📊 What Changed<\/h2>/);
  const contentEnd = mainContent.match(/<\/div><\/article>/);
  
  if (contentStart && contentEnd) {
    const content = mainContent.substring(contentStart.index, contentEnd.index + '</div></article>'.length);
    // Remove the closing </article> tag from content since we'll add it in the new structure
    const contentBody = content.replace(/<\/article>\s*$/, '');
    
    const newMain = `<main>
    <section class="article-hero">
      <div class="container">
        <h1 class="article-title">${h1Text}</h1>
${metaSection.replace(/^      /gm, '        ')}
      </div>
    </section>

    <section class="article-section">
      <div class="container">
        <article class="article-content">
${contentBody.replace(/^<h2>/gm, '          <h2>').replace(/^<\/div><\/article>/, '          </div></article>')}
        </article>
      </div>
    </section>
  </main>`;

    html = html.replace(/<main>[\s\S]*?<\/main>/, newMain);
    console.log('Restructured HTML with article-hero and article-section');
  } else {
    console.log('WARNING: Could not find content start/end markers for restructuring');
  }
}

// 10. Add CTA section and Related Articles section before <footer>
const ctaAndRelated = `
  <section class="cta-box" style="margin:50px auto;max-width:800px;">
    <h2 style="font-size:2rem;font-weight:700;margin-bottom:16px;color:#fff;">Need Help With Baidu Account Setup?</h2>
    <p style="font-size:1.05rem;margin-bottom:30px;opacity:.9;color:#fff;">BPP manages brand information and account setup for overseas clients. We handle the technical details so you can focus on your business.</p>
    <a href="/contact" class="cta-btn">Get Started with BPP &rarr;</a>
  </section>

  <section class="related-section">
    <div class="container">
      <h2 style="font-size:1.5rem;font-weight:700;margin-bottom:8px;color:var(--gray-900);">Related Articles</h2>
      <p style="color:var(--gray-600);font-size:.95rem;margin-bottom:24px;">More insights on Baidu advertising and account management</p>
      <div class="related-grid">
        <a href="/blog/baidu-brand-protection-guide" class="related-card">
          <h4>🛡️ How to Protect Your Brand on Baidu PPC</h4>
          <p>Step-by-step guide to protecting your brand from competitor misuse in Baidu PPC ads.</p>
        </a>
        <a href="/blog/baidu-keyword-match-types-guide" class="related-card">
          <h4>🔑 Baidu Keyword Match Types: Why You Need So Many Similar Keywords</h4>
          <p>Understand the 5 match types on Baidu and how to use them strategically for lower CPC.</p>
        </a>
        <a href="/blog/how-much-does-baidu-ppc-cost" class="related-card">
          <h4>💰 How Much Does Baidu PPC Cost? Pricing, CPC, and Budget Guide</h4>
          <p>The CPC formula and how Quality Score directly impacts your actual cost per click.</p>
        </a>
      </div>
    </div>
  </section>
`;

html = html.replace(/(\s*<footer>)/, ctaAndRelated + '$1');

fs.writeFileSync(filePath, html, 'utf8');
console.log('Done! File has been fixed.');
