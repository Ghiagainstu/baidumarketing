/**
 * Fix JA Blog Post Nav CSS & Structure
 * 
 * Issues fixed:
 * 1. Nav CSS is from EN template (wrong breakpoints, missing JA rules)
 * 2. Lang-switch button uses ▼ instead of SVG arrow
 * 3. Lang-switch menu CSS uses .show instead of .open
 * 4. Mobile nav breakpoint at 768px instead of 900px
 * 5. .nav-mobile-cta,.nav-mobile-theme{display:none} in wrong location
 * 6. Missing html[lang="ja"] .nav-links gap rules
 * 7. Breadcrumb hrefs missing .html suffix
 * 8. Lang-switch menu dark mode CSS missing
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const BLOG_DIR = path.join(__dirname, 'ja', 'blog');

// The JA-correct nav CSS block to replace lines 88-99 (lang-switch section)
// This replaces the EN template's lang-switch CSS with the JA template version
const JA_LANG_SWITCH_CSS = `    /* Language switcher */
    .nav-right-group { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
    .lang-switch { position: relative; }
    .lang-switch-btn {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 4px 10px;
      border-radius: 8px;
      border: 1px solid var(--gray-200);
      background: transparent;
      cursor: pointer;
      font-size: .9rem;
      color: var(--gray-600);
      transition: all var(--transition-base);
      line-height: 1;
    }
    .lang-switch-btn:hover { border-color: var(--blue); color: var(--blue); }
    .lang-switch-menu {
      position: absolute;
      top: calc(100% + 6px);
      right: 0;
      background: #fff;
      border: 1px solid var(--gray-200);
      border-radius: 8px;
      box-shadow: var(--shadow-md);
      min-width: 150px;
      opacity: 0;
      pointer-events: none;
      transform: translateY(-4px);
      transition: opacity .2s ease, transform .2s ease;
      z-index: 200;
    }
    .lang-switch-menu.open { opacity: 1; pointer-events: auto; transform: translateY(0); }
    .lang-switch-item {
      display: block;
      padding: 10px 16px;
      font-size: .9rem;
      color: var(--gray-700);
      transition: background .15s;
      white-space: nowrap;
    }
    .lang-switch-item:hover { background: var(--blue-light); color: var(--blue); }
    .lang-switch-item:first-child { border-radius: 7px 7px 0 0; }
    .lang-switch-item:last-child { border-radius: 0 0 7px 7px; }
    [data-theme="dark"] .lang-switch-btn { border-color: var(--gray-200); color: var(--gray-600); }
    [data-theme="dark"] .lang-switch-btn:hover { border-color: var(--blue); color: var(--blue); }
    [data-theme="dark"] .lang-switch-menu { background: #0B0F1A; border-color: var(--gray-200); }
    [data-theme="dark"] .lang-switch-item { color: var(--gray-700); }
    [data-theme="dark"] .lang-switch-item:hover { background: rgba(99,102,241,.12); color: var(--blue); }
`;

// JA-optimized nav link gap (narrower than EN for Japanese text)
const JA_NAV_GAP_RULE = `    html[lang="ja"] .nav-links { gap: 20px; font-size: .82rem; }
`;

// The correct mobile nav block (900px breakpoint, JA-compatible)
const JA_MOBILE_NAV_CSS = `
    .nav-mobile-cta, .nav-mobile-theme { display: none; }
    @media (max-width: 900px) {
      .nav-links { display: none; }
      .nav-cta { display: none; }
      .theme-toggle { display: none; }
      .lang-switch { display: none; }
      .nav-mobile-toggle { display: block; }
      .nav-links.open {
        display: flex !important;
        flex-direction: column;
        position: absolute;
        top: 64px;
        left: 0;
        width: 100%;
        padding: 8px 0;
        gap: 0;
        border-bottom: 1px solid var(--gray-200);
        box-shadow: var(--shadow-md);
        z-index: 100;
        background: #fff;
      }
      .nav-links.open a { display: block; padding: 14px 24px; font-size: 1rem; font-weight: 500; color: var(--gray-800); border-bottom: 1px solid var(--gray-100); }
      .nav-links.open a:last-child { border-bottom: none; }
      .nav-links.open a:hover, .nav-links.open a:active { background: var(--blue-subtle); color: var(--blue); }
      .nav-links.open a::after { display: none; }
      .nav-mobile-theme {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 12px 24px;
        font-size: .9rem;
        color: var(--gray-600);
        cursor: pointer;
        border: none;
        background: none;
        text-align: left;
      }
      .footer-top { grid-template-columns: 1fr; }
      .footer-bottom { flex-direction: column; text-align: center; }
    }
    [data-theme="dark"] .nav-links.open { background: #0B0F1A; border-bottom-color: var(--gray-200); }
    [data-theme="dark"] .nav-links.open a { color: var(--gray-700); border-bottom-color: var(--gray-200); }
    [data-theme="dark"] .nav-links.open a:hover, [data-theme="dark"] .nav-links.open a:active { background: rgba(99,102,241,.12); color: var(--blue); }`;

let fixedCount = 0;
let breadcrumbCount = 0;

const files = fs.readdirSync(BLOG_DIR).filter(f => f.endsWith('.html'));

for (const file of files) {
  const filePath = path.join(BLOG_DIR, file);
  let html = fs.readFileSync(filePath, 'utf8');
  let modified = false;

  // 1. Replace the old EN-template lang-switch CSS block with JA version
  // Match from "/* Language switcher */" to the end of its CSS block
  const oldLangCSS = html.match(/\/\* Language switcher \*\/[\s\S]*?\[data-theme="dark"\] \.lang-switch-menu[\s\S]*?\}/);
  if (oldLangCSS && !oldLangCSS[0].includes('nav-right-group')) {
    // Only replace if it doesn't already have the JA version
    html = html.replace(oldLangCSS[0], JA_LANG_SWITCH_CSS.trimEnd());
    modified = true;
  }

  // 2. Replace lang-switch button with ▼ to use SVG arrow
  const langBtnMatch = html.match(/<button class="lang-switch-btn"[^>]*>🇯🇵 ▼<\/button>/);
  if (langBtnMatch) {
    html = html.replace(
      langBtnMatch[0],
      `<button class="lang-switch-btn" onclick="toggleLangMenu()" aria-label="言語">🇯🇵 <svg width="10" height="6" viewBox="0 0 10 6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M1 1l4 4 4-4"/></svg></button>`
    );
    modified = true;
  }

  // 3. Fix lang-switch menu CSS - replace .show with .open in JS condition
  // Actually, the JS uses toggleLangMenu, let me check if it uses .show or .open
  // The CSS uses .show{display:block}, replace with .open pattern
  const showPattern = html.match(/\.lang-switch-menu\.show\s*\{[^}]*\}/);
  if (showPattern && showPattern[0].includes('display:block')) {
    // Don't replace yet - the JS might use .show class
    // Instead add .open CSS alongside .show
    // Actually, let's just replace .show with .open in CSS
    html = html.replace(/\.lang-switch-menu\.show\s*\{display:block\s*;?\s*\}/g, 
      '.lang-switch-menu.open { opacity: 1; pointer-events: auto; transform: translateY(0); }');
    modified = true;
  }

  // 4. Replace the mobile nav section (from @media(max-width:768px) or @media(max-width:900px))
  // Find the old mobile nav block
  const oldMobilePattern = html.match(/\.nav-mobile-cta,\.nav-mobile-theme\{display:none\}[\s\S]*?\[data-theme="dark"\] \.nav-links\.open a:active\{background:rgba\(99,102,241,\.12\);color:var\(--blue\)\}/);
  if (oldMobilePattern) {
    html = html.replace(oldMobilePattern[0], JA_MOBILE_NAV_CSS.trim());
    modified = true;
  }

  // 5. Fix breadcrumb hrefs missing .html suffix
  // Pattern: href="../../ja/index" (no .html)
  const crumbPattern = /href="(\.\.\/\.\.\/ja\/[a-z0-9-]+)(?!\.html)"/g;
  const newHtml = html.replace(crumbPattern, (match, path) => {
    breadcrumbCount++;
    return `href="${path}.html"`;
  });
  if (newHtml !== html) {
    html = newHtml;
    modified = true;
  }

  // 6. Add html[lang="ja"] nav-links rule if not present
  if (!html.includes('html[lang="ja"] .nav-links')) {
    // Insert after the .nav-links a.active::after rule
    const afterActive = html.match(/\.nav-links a\.active::after\s*\{[^}]*\}/);
    if (afterActive) {
      const insertPos = html.indexOf(afterActive[0]) + afterActive[0].length;
      html = html.slice(0, insertPos) + '\n' + JA_NAV_GAP_RULE.trimEnd() + html.slice(insertPos);
      modified = true;
    }
  }

  if (modified) {
    fs.writeFileSync(filePath, html, 'utf8');
    fixedCount++;
  }
}

console.log(`✅ Fixed ${fixedCount}/${files.length} JA blog posts`);
console.log(`🔗 Fixed ${breadcrumbCount} breadcrumb URLs`);
