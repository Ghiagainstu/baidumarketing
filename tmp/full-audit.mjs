import fs from 'fs';
import path from 'path';

const results = [];

function scanFile(filePath, expectedLang) {
  const h = fs.readFileSync(filePath, 'utf8');
  const issues = [];
  const relPath = path.relative('.', filePath).replace(/\\/g, '/');
  const slug = path.basename(filePath, '.html');

  // 1. Obsidian markdown remnants: lines starting with #, ##, ###, -, *, >, ``` etc in article content
  const articleMatch = h.match(/<article[^>]*>([\s\S]*?)<\/article>/i) || 
                        h.match(/<div class="article-content">([\s\S]*?)<\/div>\s*(?:<\/section>|<section)/i);
  
  // Check for raw markdown headings like #, ##, ### that are NOT inside <code> or <pre> tags
  const bodyContent = h.replace(/<pre[\s\S]*?<\/pre>/gi, '').replace(/<code[\s\S]*?<\/code>/gi, '');
  
  // Raw markdown heading remnants (lines starting with # followed by space, not inside HTML tags)
  const mdHeadings = bodyContent.match(/(?:^|\n)\s*#{1,6}\s+[A-Za-z\u3000-\u9fff\uac00-\ud7af]/gm);
  if (mdHeadings) issues.push('obsidian-heading-remnant:' + mdHeadings.length);

  // Raw markdown list remnants: lines starting with "- " or "* " that look like markdown (not in lists)
  // Look for patterns like "\n- text" or "\n* text" outside of <li> tags
  const outsideLi = bodyContent.replace(/<li[\s\S]*?<\/li>/gi, '');
  const mdBullets = outsideLi.match(/(?:^|\n)\s*[-*]\s+[A-Za-z\u3000-\u9fff\uac00-\ud7af](?![\w-]*>)/gm);
  if (mdBullets && mdBullets.length > 2) issues.push('obsidian-bullet-remnant:' + mdBullets.length);

  // Raw markdown blockquote remnants
  const mdBlockquotes = bodyContent.match(/(?:^|\n)\s*>\s+[A-Za-z\u3000-\u9fff\uac00-\ud7af]/gm);
  if (mdBlockquotes && mdBlockquotes.length > 1) issues.push('obsidian-blockquote-remnant:' + mdBlockquotes.length);

  // 2. Language mixing detection
  const textOnly = bodyContent.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ');
  
  const cjkChars = (textOnly.match(/[\u3000-\u9fff\uac00-\ud7af]/g) || []).length;
  const latinChars = (textOnly.match(/[a-zA-Z]/g) || []).length;
  const totalChars = cjkChars + latinChars;
  
  if (expectedLang === 'en') {
    // English page should not have significant CJK
    const cjkRatio = totalChars > 0 ? cjkChars / totalChars : 0;
    if (cjkRatio > 0.15 && cjkChars > 50) issues.push('lang-mix-en-has-cjk:' + Math.round(cjkRatio * 100) + '%');
  } else if (expectedLang === 'ja') {
    // Japanese page should have significant Japanese, check for Korean
    const koreanChars = (textOnly.match(/[\uac00-\ud7af]/g) || []).length;
    if (koreanChars > 30) issues.push('lang-mix-ja-has-ko:' + koreanChars);
    // Check if page is mostly English (untranslated)
    const jaRatio = totalChars > 0 ? cjkChars / totalChars : 0;
    if (jaRatio < 0.05 && totalChars > 200) issues.push('likely-untranslated-ja');
  } else if (expectedLang === 'ko') {
    // Korean page: check for Japanese hiragana/katakana
    const jpSpecific = (textOnly.match(/[\u3040-\u309f\u30a0-\u30ff]/g) || []).length;
    if (jpSpecific > 20) issues.push('lang-mix-ko-has-jp:' + jpSpecific);
    // Check if page is mostly English (untranslated)
    const koreanChars = (textOnly.match(/[\uac00-\ud7af]/g) || []).length;
    const koRatio = totalChars > 0 ? koreanChars / totalChars : 0;
    if (koRatio < 0.05 && totalChars > 200) issues.push('likely-untranslated-ko');
  }

  // 3. Broken/mojibake characters - look for common encoding issues
  const mojibake = h.match(/[\ufffd]|&amp;amp;|&amp;lt;|&amp;gt;/g);
  if (mojibake) issues.push('mojibake:' + mojibake.length);

  // 4. HTML structure issues
  // Duplicate IDs
  const idMatches = h.match(/\bid="([^"]+)"/g) || [];
  const ids = idMatches.map(m => m.match(/"([^"]+)"/)[1]);
  const dupIds = ids.filter((id, i) => ids.indexOf(id) !== i);
  const uniqueDupIds = [...new Set(dupIds)];
  if (uniqueDupIds.length > 0) issues.push('dup-ids:' + uniqueDupIds.join(','));

  // 5. Broken links (internal links to non-existent pages or wrong paths)
  const internalLinks = h.match(/href="\/(?!#)[^"]*"/g) || [];
  // just count, don't check filesystem for performance

  // 6. Empty or broken footer-lang links
  const footerLangMatch = h.match(/<div class="footer-lang">([\s\S]*?)<\/div>/);
  if (footerLangMatch) {
    const langContent = footerLangMatch[1];
    const langLinks = langContent.match(/href="([^"]+)"/g) || [];
    if (langLinks.length < 2) issues.push('footer-lang-too-few-links:' + langLinks.length);
    // Check if href is empty or broken
    for (const link of langLinks) {
      if (link.includes('href=""') || link.includes("href=''")) issues.push('footer-lang-empty-href');
    }
  }

  // 7. Duplicate function definitions
  const funcNames = ['toggleLangMenu', 'toggleTheme', 'handleScroll', 'initBackToTop'];
  for (const fn of funcNames) {
    const count = (h.match(new RegExp('function ' + fn + '\\b', 'g')) || []).length;
    if (count > 1) issues.push('dup-func-' + fn + ':' + count);
  }

  // 8. Obf-email not rendered (empty anchor with obf-email class)
  const obfLinks = h.match(/class="obf-email-link"[\s>][^<]*<\/a>/g) || [];
  for (const link of obfLinks) {
    if (link.replace(/<[^>]+>/g, '').trim() === '') {
      // Empty obf link - check if JS exists to fill it
      if (!h.includes('obf-email')) issues.push('obf-email-no-content');
    }
  }

  // 9. Broken image references (data URIs or missing alt)
  const imgs = h.match(/<img[^>]*>/gi) || [];
  for (const img of imgs) {
    if (!img.includes('alt=')) issues.push('img-missing-alt');
    break; // only report once
  }

  // 10. Extra whitespace issues in article content (multiple blank lines)
  const articleText = h.match(/<article[\s\S]*?<\/article>/i);
  if (articleText) {
    const tripleNewlines = (articleText[0].match(/\n{4,}/g) || []).length;
    if (tripleNewlines > 3) issues.push('excessive-whitespace:' + tripleNewlines);
  }

  // 11. Check for leftover TODO/FIXME/placeholder text
  const placeholders = h.match(/\b(TODO|FIXME|PLACEHOLDER|LOREM|XXX|REPLACE_THIS)\b/gi);
  if (placeholders) issues.push('placeholder-text:' + placeholders.join(','));

  // 12. Check for raw URLs that should be links (http/https not in href/src/content)
  // Skip this - too many false positives

  // 13. Check for broken <style> tags (unclosed)
  const styleOpens = (h.match(/<style[^>]*>/gi) || []).length;
  const styleCloses = (h.match(/<\/style>/gi) || []).length;
  if (styleOpens !== styleCloses) issues.push('unclosed-style-tag:' + styleOpens + 'vs' + styleCloses);

  // 14. Check for broken <script> tags
  const scriptOpens = (h.match(/<script[^>]*>/gi) || []).length;
  const scriptCloses = (h.match(/<\/script>/gi) || []).length;
  if (scriptOpens !== scriptCloses) issues.push('unclosed-script-tag:' + scriptOpens + 'vs' + scriptCloses);

  // 15. Check <title> tag content
  const titleMatch = h.match(/<title>([^<]*)<\/title>/);
  if (titleMatch) {
    const title = titleMatch[1];
    if (title.includes('undefined') || title.includes('null') || title === '') issues.push('broken-title');
    // Check if title is in wrong language
    if (expectedLang === 'ja' && /[a-zA-Z]/.test(title) && !/[\u3000-\u9fff]/.test(title)) issues.push('title-not-in-ja');
    if (expectedLang === 'ko' && /[a-zA-Z]/.test(title) && !/[\uac00-\ud7af]/.test(title)) issues.push('title-not-in-ko');
  } else {
    issues.push('missing-title-tag');
  }

  // 16. Check meta description language
  const metaDesc = h.match(/<meta name="description" content="([^"]*)"/i);
  if (metaDesc) {
    const desc = metaDesc[1];
    if (expectedLang === 'ja' && !/[\u3000-\u9fff]/.test(desc) && desc.length > 20) issues.push('meta-desc-not-in-ja');
    if (expectedLang === 'ko' && !/[\uac00-\ud7af]/.test(desc) && desc.length > 20) issues.push('meta-desc-not-in-ko');
  }

  // 17. Check og:title language
  const ogTitle = h.match(/<meta property="og:title" content="([^"]*)"/i);
  if (ogTitle) {
    const ot = ogTitle[1];
    if (expectedLang === 'ja' && !/[\u3000-\u9fff]/.test(ot) && ot.length > 10) issues.push('og-title-not-in-ja');
    if (expectedLang === 'ko' && !/[\uac00-\ud7af]/.test(ot) && ot.length > 10) issues.push('og-title-not-in-ko');
  }

  // 18. Check schema.org JSON-LD language
  const schemaMatch = h.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/);
  if (schemaMatch) {
    try {
      const schema = JSON.parse(schemaMatch[1]);
      if (expectedLang === 'ja' && schema.headline && !/[\u3000-\u9fff]/.test(schema.headline)) issues.push('schema-headline-not-in-ja');
      if (expectedLang === 'ko' && schema.headline && !/[\uac00-\ud7af]/.test(schema.headline)) issues.push('schema-headline-not-in-ko');
    } catch(e) {
      issues.push('schema-json-parse-error');
    }
  }

  if (issues.length > 0) {
    results.push({ file: relPath, lang: expectedLang, issues });
  }
}

// Scan all blog directories
const dirs = [
  { dir: 'blog', lang: 'en' },
  { dir: 'ja/blog', lang: 'ja' },
  { dir: 'ko/blog', lang: 'ko' }
];

for (const { dir, lang } of dirs) {
  if (!fs.existsSync(dir)) continue;
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html') && !f.startsWith('_'));
  for (const f of files) {
    scanFile(path.join(dir, f), lang);
  }
}

// Print results grouped by issue type
console.log('=== FULL AUDIT RESULTS ===');
console.log('Total files with issues:', results.length);
console.log('');

// Group by issue type
const byType = {};
for (const r of results) {
  for (const issue of r.issues) {
    const type = issue.split(':')[0];
    if (!byType[type]) byType[type] = [];
    byType[type].push(r.file + ' -> ' + issue);
  }
}

const sortedTypes = Object.entries(byType).sort((a, b) => b[1].length - a[1].length);
for (const [type, items] of sortedTypes) {
  console.log(`\n--- ${type} (${items.length} files) ---`);
  items.forEach(item => console.log('  ' + item));
}

// Also print per-file summary
console.log('\n\n=== PER-FILE SUMMARY ===');
for (const r of results) {
  console.log(r.file + ': ' + r.issues.join(' | '));
}
