/**
 * Fix baidu-brand-info-account-level.html to match baseline standard
 * Issues: incomplete CSS vars, corrupted dark mode CSS, missing HTML structure,
 *         garbage in meta tags, empty JSON-LD fields, wrong callout classes
 */
const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, 'blog/baidu-brand-info-account-level.html');
let html = fs.readFileSync(filePath, 'utf8');

// 1. Fix meta description (line 5) - garbage content
html = html.replace(
  /<meta name="description" content="[^"]*">/,
  '<meta name="description" content="Baidu moved brand info from unit/plan level to account level starting Dec 2024. Learn why this matters for ad relevance and CTR." />'
);

// 2. Add missing canonical link (after line 7)
if (!html.includes('rel="canonical"')) {
  html = html.replace(
    /<link rel="alternate" hreflang="x-default"[^>]*>/,
    '<link rel="alternate" hreflang="x-default" href="https://www.baidumarketing.com/blog/baidu-brand-info-account-level">\n  <link rel="canonical" href="https://www.baidumarketing.com/blog/baidu-brand-info-account-level" />'
  );
}

// 3. Fix og:url to remove .html
html = html.replace(
  /<meta property="og:url" content="[^"]*\.html">/,
  '<meta property="og:url" content="https://www.baidumarketing.com/blog/baidu-brand-info-account-level" />'
);

// 4. Fix og:description (garbage)
html = html.replace(
  /<meta property="og:description" content="[^"]*">/,
  '<meta property="og:description" content="Baidu moved brand info from unit/plan level to account level starting Dec 2024. Learn why this matters for ad relevance and CTR." />'
);

// 5. Fix twitter:description (garbage)
html = html.replace(
  /<meta name="twitter:description" content="[^"]*">/,
  '<meta name="twitter:description" content="Baidu moved brand info from unit/plan level to account level starting Dec 2024. Learn why this matters for ad relevance and CTR." />'
);

// 6. Fix JSON-LD url and @id (empty fields)
html = html.replace(/"url":\s*""\s*,/, '"url": "https://www.baidumarketing.com/blog/baidu-brand-info-account-level",');
html = html.replace(/"@id":\s*""\s*/, '"@id": "https://www.baidumarketing.com/blog/baidu-brand-info-account-level" ');
// Fix datePublished to match the actual date
html = html.replace(/"datePublished":\s*"[^"]*"/, '"datePublished": "2026-05-17"');
html = html.replace(/"dateModified":\s*"[^"]*"/, '"dateModified": "2026-05-17"');

// 7. Fix callout class in HTML: "callout tip" -> "callout callout-tip"
html = html.replace(/class="callout tip"/g, 'class="callout callout-tip"');

// 8. Fix takeaway heading: h3 -> strong (baseline style)
html = html.replace(
  /<div class="takeaway">\s*<h3>([^<]*)<\/h3>/,
  '<div class="takeaway">\n      <strong>Key Takeaway</strong>\n      <p>$1</p>'
);

fs.writeFileSync(filePath, html, 'utf8');
console.log('Part 1 fixes applied (meta tags, JSON-LD, callout class, takeaway)');

// Now fix the CSS - replace the incomplete base CSS with proper one
// This is done via a separate pass to keep it manageable
const baselineCSS = `    :root {
      --blue: #2932E1;
      --blue-dark: #1E25AF;
      --blue-deep: #151B8A;
      --blue-light: #EEF0FF;
      --blue-glow: #D4D8FF;
      --blue-subtle: #F5F6FF;
      --gray-50: #F9FAFB;
      --gray-100: #F3F4F6;
      --gray-200: #E5E7EB;
      --gray-300: #D1D5DB;
      --gray-400: #9CA3AF;
      --gray-600: #4B5563;
      --gray-700: #374151;
      --gray-800: #1F2937;
      --gray-900: #111827;
      --radius: 12px;
      --radius-lg: 16px;
      --radius-xl: 24px;
      --shadow-sm: 0 1px 3px rgba(0,0,0,.08);
      --shadow-md: 0 4px 16px rgba(0,0,0,.10);
      --shadow-lg: 0 12px 40px rgba(0,0,0,.12);
      --shadow-blue: 0 8px 32px rgba(41,50,225,.18);
      --gradient-brand: linear-gradient(135deg, #2932E1 0%, #4F46E5 50%, #7C3AED 100%);
      --gradient-hero: linear-gradient(160deg, #ffffff 30%, #EEF0FF 60%, #E0E7FF 100%);
      --gradient-surface: linear-gradient(135deg, #F9FAFB 0%, #F3F4FF 100%);
      --font-display: 'Inter', system-ui, -apple-system, sans-serif;
      --transition-base: 0.2s cubic-bezier(0.4, 0, 0.2, 1);
      --transition-smooth: 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    [data-theme="dark"] {
      --blue: #6366F1;
      --blue-dark: #818CF8;
      --blue-deep: #4F46E5;
      --blue-light: rgba(99,102,241,.12);
      --blue-glow: rgba(99,102,241,.15);
      --blue-subtle: rgba(99,102,241,.06);
      --gray-50: #0B0F1A;
      --gray-100: #111827;
      --gray-200: #1F2937;
      --gray-300: #374151;
      --gray-400: #6B7280;
      --gray-600: #9CA3AF;
      --gray-700: #D1D5DB;
      --gray-800: #E5E7EB;
      --gray-900: #F9FAFB;
      --shadow-sm: 0 1px 3px rgba(0,0,0,.3);
      --shadow-md: 0 4px 16px rgba(0,0,0,.4);
      --shadow-lg: 0 12px 40px rgba(0,0,0,.5);
      --shadow-blue: 0 8px 32px rgba(99,102,241,.2);
      --gradient-hero: linear-gradient(160deg, #0F172A 30%, #131C38 60%, #1E1B4B 100%);
      --gradient-surface: linear-gradient(135deg, #111827 0%, #1E1B4B 100%);
      background-color: #0B0F1A;
      color: #E5E7EB;
    }
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body { font-family: var(--font-display); color: var(--gray-900); background: #ffffff; line-height: 1.6; -webkit-font-smoothing: antialiased; }
    [data-theme="dark"] body { background-color: #0B0F1A; color: #E5E7EB; }
    a { color: inherit; text-decoration: none; }
    .container { max-width: 1140px; margin: 0 auto; padding: 0 24px; }

    /* Nav */
    nav { position: sticky; top: 0; z-index: 100; background: rgba(255,255,255,.92); backdrop-filter: blur(12px); border-bottom: 1px solid var(--gray-200); }
    .nav-inner { display: flex; align-items: center; justify-content: space-between; height: 64px; }
    .nav-logo { display: flex; align-items: center; gap: 10px; font-weight: 700; font-size: 1.1rem; color: var(--gray-800); transition: color var(--transition-base);
      white-space: nowrap;
      flex-shrink: 0; }
    .nav-logo:hover { color: var(--blue); }
    .nav-logo svg { flex-shrink: 0; }
    .nav-links { display: flex; gap: 28px; font-size: .9rem; color: var(--gray-600); }
    .nav-links a { position: relative; transition: color var(--transition-base); }
    .nav-links a::after { content: ''; position: absolute; bottom: -4px; left: 50%; width: 0; height: 2px; background: var(--blue); border-radius:1px; transition: width var(--transition-smooth), left var(--transition-smooth); }
    .nav-links a:hover { color: var(--blue); }
    .nav-links a:hover::after { width: 100%; left: 0; }
    .nav-links a.active { color: var(--blue); font-weight: 600; }
    .nav-links a.active::after { width: 100%; left: 0; }
    .nav-mobile-cta,.nav-mobile-theme{display:none}
    .nav-cta { background: var(--gradient-brand); color: #fff; padding: 10px 22px; border-radius: 8px; font-size: .9rem; font-weight: 600; transition: transform var(--transition-base), box-shadow var(--transition-base); position: relative; overflow: hidden; }
    .nav-cta:hover { transform: translateY(-1px); box-shadow: 0 4px 16px rgba(41,50,225,.35); }
    .nav-cta:active { transform: translateY(0) scale(.97); }
    .nav-mobile-toggle { display: none; background: none; border: none; cursor: pointer; }
    .nav-mobile-cta, .nav-mobile-theme { display: none; }
    .nav-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.4); backdrop-filter: blur(2px); z-index: 99; opacity: 0; pointer-events: none; transition: opacity .3s; }
    .nav-overlay.active { opacity: 1; pointer-events: auto; }

    [data-theme="dark"] nav { background: rgba(11,15,26,.85); border-bottom-color: var(--gray-200); }
    [data-theme="dark"] .nav-logo { color: #818CF8; }
    [data-theme="dark"] .nav-links { color: var(--gray-600); }
    [data-theme="dark"] .hamburger-icon rect { fill: #D1D5DB; }
    [data-theme="dark"] .close-icon line { stroke: #D1D5DB; }
    [data-theme="dark"] .nav-overlay { background: rgba(0,0,0,.7); }

    /* Article Hero */
    .article-hero { padding: 120px 0 60px; background: var(--gradient-hero); }
    .article-title { font-size: 2.5rem; font-weight: 800; color: var(--gray-900); line-height: 1.2; margin-bottom: 20px; }
    .article-meta { display: flex; gap: 20px; font-size: .85rem; color: var(--gray-600); margin-bottom: 40px; flex-wrap: wrap; }
    .article-meta span { display: inline-flex; align-items: center; gap: 6px; }
    .article-section { padding: 60px 0; }
    .article-content { max-width: 800px; margin: 0 auto; }

    [data-theme="dark"] .article-hero { background: var(--gradient-hero); }
    [data-theme="dark"] .article-title { color: #F9FAFB; }
    [data-theme="dark"] .article-meta { color: var(--gray-600); }

    .article-content h2 { font-size: 1.8rem; font-weight: 700; color: var(--gray-900); margin: 40px 0 20px; line-height: 1.3; }
    .article-content h3 { font-size: 1.4rem; font-weight: 600; color: var(--gray-900); margin: 30px 0 15px; }
    .article-content p { margin-bottom: 20px; color: var(--gray-700); line-height: 1.8; font-size: 1.05rem; }
    .article-content ul, .article-content ol { margin-bottom: 20px; padding-left: 24px; color: var(--gray-700); line-height: 1.8; }
    .article-content li { margin-bottom: 10px; }

    [data-theme="dark"] .article-content h2, [data-theme="dark"] .article-content h3 { color: #F9FAFB; }
    [data-theme="dark"] .article-content p, [data-theme="dark"] .article-content li { color: var(--gray-600); }

    /* Stats Grid */
    .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 40px 0; }
    .stat-card { background: var(--gray-50); padding: 28px 20px; border-radius: var(--radius); text-align: center; border:1px solid var(--gray-200); }
    .stat-number { font-size: 2.2rem; font-weight: 800; color: var(--blue); margin-bottom: 6px; }
    .stat-label { font-size: .85rem; color: var(--gray-600); }
    [data-theme="dark"] .stat-card { background: var(--gray-100); border-color: var(--gray-200); }

    /* Comparison Table */
    .comparison-table { width: 100%; border-collapse: separate; border-spacing: 0; margin: 40px 0; background: #fff; border-radius: var(--radius); overflow: hidden; box-shadow: var(--shadow-md); }
    .comparison-table th { background: var(--blue); color: #fff; padding: 16px; text-align: left; font-weight: 600; font-size: .95rem; }
    .comparison-table td { padding: 14px 16px; border-bottom: 1px solid var(--gray-200); color: var(--gray-700); font-size: .95rem; }
    .comparison-table tr:last-child td { border-bottom: none; }
    .comparison-table .check-col { text-align: center; font-size: 1.2rem; }
    .check-yes { color: #10B981; }
    .check-no { color: #EF4444; }
    [data-theme="dark"] .comparison-table { background: var(--gray-100); }
    [data-theme="dark"] .comparison-table td { border-bottom-color: var(--gray-200); color: var(--gray-600); }

    /* Callout */
    .callout { padding: 20px 24px; border-radius: var(--radius); margin: 30px 0; border-left: 4px solid; display: flex; gap: 14px; align-items: flex-start; }
    .callout-tip { background: #D1FAE5; border-color: #6EE7B7; }
    .callout-warning { background: #FEF3C7; border-color: #FCD34D; }
    .callout-insight { background: rgba(41,50,225,.06); border-color: rgba(41,50,225,.18); }
    .callout-icon { font-size: 1.3rem; flex-shrink: 0; line-height: 1.6; }

    /* Takeaway */
    .takeaway { background: var(--gradient-brand); color: #fff; padding: 28px 32px; border-radius: var(--radius-lg); margin: 40px 0; }
    .takeaway strong { display: block; font-size: .9rem; text-transform: uppercase; letter-spacing: .5px; margin-bottom: 10px; opacity: .85; }
    .takeaway p { margin-bottom: 0 !important; color: #fff !important; font-size: 1.05rem !important; line-height: 1.7 !important; }
    .takeaway ul { margin: 12px 0 0 0; padding-left: 20px; color: #fff !important; }
    .takeaway ul li { color: #fff !important; margin-bottom: 6px; }

    /* Blockquote */
    .article-content blockquote { margin: 30px 0; padding: 20px 24px; border-left: 4px solid var(--blue); background: var(--gray-50); border-radius: 0 var(--radius) var(--radius) 0; }
    .article-content blockquote p { margin-bottom: 0 !important; font-style: italic; color: var(--gray-700) !important; font-size: 1.05rem !important; }
    .article-content blockquote cite { display: block; margin-top: 10px; font-style: normal; font-size: .85rem; color: var(--gray-400); }
    [data-theme="dark"] .article-content blockquote { background: var(--gray-100); }
    [data-theme="dark"] .article-content blockquote p { color: var(--gray-600) !important; }

    /* SVG Chart */
    .chart-container { margin: 40px 0; padding: 24px; background: var(--gray-50); border-radius: var(--radius-lg); border:1px solid var(--gray-200); overflow-x: auto; }
    .chart-container svg { display: block; width: 100%; height: auto; }
    .chart-title { text-align: center; font-size: .9rem; font-weight: 600; color: var(--gray-600); margin-bottom: 16px; }
    [data-theme="dark"] .chart-container { background: var(--gray-100); border-color: var(--gray-200); }
    [data-theme="dark"] .chart-title { color: var(--gray-600); }

    /* CTA Box */
    .cta-box { background: var(--gradient-brand); color: #fff; padding: 48px; border-radius: var(--radius-xl); text-align: center; margin: 50px 0; }
    .cta-box h2 { font-size: 2rem !important; font-weight: 700 !important; margin-bottom: 16px !important; color: #fff !important; }
    .cta-box p { font-size: 1.05rem !important; margin-bottom: 30px !important; opacity: .9; color: #fff !important; }
    .cta-btn { display: inline-block; background: #fff; color: var(--blue); padding: 14px 36px; border-radius: 8px; font-weight: 600; font-size: 1rem; transition: transform var(--transition-base), box-shadow var(--transition-base); }
    .cta-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,.2); }
    [data-theme="dark"] .cta-box h2 { color: #fff !important; }

    /* Related */
    .related-section { padding: 60px 0; background: var(--gray-50); }
    .related-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-top: 30px; }
    .related-card { background: #fff; border-radius: var(--radius); padding: 24px; border: 1px solid var(--gray-200); transition: transform var(--transition-base), box-shadow var(--transition-base); }
    .related-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-md); }
    .related-card h4 { font-size: 1rem; font-weight: 600; margin-bottom: 8px; color: var(--gray-900); }
    .related-card p { font-size: .85rem; color: var(--gray-600); }
    [data-theme="dark"] .related-section { background: var(--gray-50); }
    [data-theme="dark"] .related-card { background: var(--gray-100); border-color: var(--gray-200); }
    [data-theme="dark"] .related-card h4 { color: #F9FAFB; }

    /* Footer */
    footer { background: var(--gray-800); color: #D1D5DB; padding: 56px 0 24px; }
    .footer-top { display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 40px; padding-bottom: 40px; border-bottom: 1px solid rgba(255,255,255,.1); }
    .footer-brand h3 { color: #fff; font-size: 1.1rem; font-weight: 700; margin-bottom: 12px; display: flex; align-items: center; gap: 10px; }
    .footer-brand h3 svg { flex-shrink: 0; }
    .footer-brand p { font-size: .85rem; line-height: 1.7; color: #9CA3AF; max-width: 280px; }
    .footer-col h4 { color: #fff; font-size: .85rem; font-weight: 600; margin-bottom: 14px; }
    .footer-col ul { list-style: none; display: flex; flex-direction: column; gap: 8px; }
    .footer-col ul li a { font-size: .85rem; color: #9CA3AF; transition: color .2s; }
    .footer-col ul li a:hover { color: #fff; }
    .footer-bottom { display: flex; justify-content: space-between; align-items: center; padding-top: 24px; flex-wrap: wrap; gap: 12px; }
    .footer-copy { font-size: .82rem; color: #6B7280; }
    .footer-social { display: flex; gap: 14px; align-items: center; }
    .footer-social a { width: 36px; height: 36px; border-radius: 8px; background: rgba(255,255,255,.08); display: grid; place-items: center; transition: background .2s, transform .2s; }
    .footer-social a:hover { background: var(--blue); transform: translateY(-2px); }
    .footer-social a:hover svg { fill: #fff !important; stroke: #fff !important; }
    .footer-social a svg { width: 18px; height: 18px; }
    [data-theme="dark"] footer { background: #070B14; }

    /* Theme Toggle */
    .theme-toggle { display: inline-flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%; border:1px solid var(--gray-200); background: transparent; cursor: pointer; transition: all var(--transition-base); color: var(--gray-600); }
    .theme-toggle:hover { border-color: var(--blue); color: var(--blue); transform: rotate(15deg); }
    .theme-toggle svg { width: 18px; height: 18px; }
    [data-theme="dark"] .theme-toggle .icon-sun { display: block; }
    [data-theme="dark"] .theme-toggle .icon-moon { display: none; }
    .theme-toggle .icon-sun { display: none; }
    .theme-toggle .icon-moon { display: block; }
    @media (max-width: 900px) {
      .nav-links { display: none; flex-direction: column; position: fixed; top: 0; right: 0; width: 280px; height: 100vh; background: #fff; padding: 80px 32px 32px; box-shadow: -4px 0 24px rgba(0,0,0,.15); z-index: 100; gap: 8px; }
      .nav-links.open { display: flex; }
      .nav-mobile-toggle { display: block; }
      .stats-grid { grid-template-columns: repeat(2, 1fr); }
      .related-grid { grid-template-columns: 1fr; }
      .footer-top { grid-template-columns: 1fr 1fr; gap: 30px; }
    }
    @media (max-width: 640px) {
      .article-title { font-size: 1.8rem; }
      .stats-grid { grid-template-columns: 1fr; }
      .footer-top { grid-template-columns: 1fr; }
      .cta-box { padding: 32px 24px; }
      .cta-box h2 { font-size: 1.5rem !important; }
    }
  /* ===== Added by standardize-blog-pages.js ===== */`;

// Read file again and do full CSS replacement
let html2 = fs.readFileSync(filePath, 'utf8');

// Find the start and end of the <style> block's base CSS (before the "Added by standardize" comment)
// The corrupted CSS starts at line 9 and the base CSS (before line 79's comment) needs replacing
// Strategy: replace from "    :root {" (line 11) to just before "/* ===== Added by standardize-blog-pages.js ===== */" (line 79)
// But the current file's CSS is very different from baseline, so let's just replace the entire <style> content

const styleMatch = html2.match(/<style>([\s\S]*?)<\/style>/);
if (styleMatch) {
  const oldStyleContent = styleMatch[1];
  // Keep the standardize additions (lines 79-144 in original), replace everything before it
  const standardizeMarker = '/* ===== Added by standardize-blog-pages.js ===== */';
  const markerIndex = oldStyleContent.indexOf(standardizeMarker);
  
  let newStyleContent;
  if (markerIndex !== -1) {
    // Keep the standardize additions, replace base CSS
    const standardizePart = oldStyleContent.substring(markerIndex);
    newStyleContent = baselineCSS + '\n' + standardizePart;
  } else {
    // No marker, replace entire CSS
    newStyleContent = baselineCSS;
  }
  
  html2 = html2.replace(/<style>([\s\S]*?)<\/style>/, '<style>' + newStyleContent + '</style>');
  fs.writeFileSync(filePath, html2, 'utf8');
  console.log('Part 2: CSS fixed');
} else {
  console.log('ERROR: Could not find <style> block');
}
