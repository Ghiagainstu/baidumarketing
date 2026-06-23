import fs from 'fs';
import path from 'path';

function checkTranslation(filePath, lang) {
  const h = fs.readFileSync(filePath, 'utf8');
  
  // Extract article text from <p>, <h1>-<h6>, <li>, <td> tags only
  const contentTags = h.match(/<(?:p|h[1-6]|li|td|th|blockquote|figcaption|div class="callout[^"]*")[^>]*>([\s\S]*?)<\/(?:p|h[1-6]|li|td|th|blockquote|figcaption|div)>/gi) || [];
  let articleText = contentTags.map(t => t.replace(/<[^>]+>/g, ' ')).join(' ');
  
  // Remove CSS/script noise
  articleText = articleText.replace(/\{[^}]*\}/g, '');
  
  const ko = (articleText.match(/[\uac00-\ud7af]/g) || []).length;
  const ja = (articleText.match(/[\u3040-\u309f\u30a0-\u30ff]/g) || []).length;
  const cjk = (articleText.match(/[\u3000-\u9fff]/g) || []).length;
  const en = (articleText.match(/[a-zA-Z]{2,}/g) || []).length;
  const total = ko + ja + cjk + en;
  
  // Also check title and meta
  const title = h.match(/<title>([^<]*)<\/title>/)?.[1] || '';
  const metaDesc = h.match(/content="([^"]*)"[^>]*>\s*$/m) || '';
  const ogTitle = h.match(/og:title[^>]*content="([^"]*)"/)?.[1] || '';
  const schemaHeadline = h.match(/"headline":\s*"([^"]*)"/)?.[1] || '';
  
  const relPath = path.relative('.', filePath).replace(/\\/g, '/');
  const issues = [];
  
  if (lang === 'ko') {
    const koRatio = total > 0 ? ko / total : 0;
    if (koRatio < 0.1 && total > 50) issues.push('body-mostly-english-ko:' + Math.round(koRatio*100) + '%');
    if (title && !/[\uac00-\ud7af]/.test(title) && /[a-zA-Z]/.test(title)) issues.push('title-en-not-ko');
    if (ogTitle && !/[\uac00-\ud7af]/.test(ogTitle) && /[a-zA-Z]/.test(ogTitle)) issues.push('og-title-en-not-ko');
    if (schemaHeadline && !/[\uac00-\ud7af]/.test(schemaHeadline) && /[a-zA-Z]/.test(schemaHeadline)) issues.push('schema-headline-en-not-ko');
  }
  
  if (lang === 'ja') {
    const jaTotal = ja + cjk; // Japanese uses kanji too
    const jaRatio = total > 0 ? jaTotal / total : 0;
    if (jaRatio < 0.1 && total > 50) issues.push('body-mostly-english-ja:' + Math.round(jaRatio*100) + '%');
    if (title && !/[\u3000-\u9fff]/.test(title) && /[a-zA-Z]/.test(title)) issues.push('title-en-not-ja');
  }
  
  if (issues.length > 0) {
    return { file: relPath, ko: ko, en: en, ja: ja, cjk: cjk, issues };
  }
  return null;
}

const results = [];

for (const dir of ['blog', 'ja/blog', 'ko/blog']) {
  if (!fs.existsSync(dir)) continue;
  const lang = dir.startsWith('ko') ? 'ko' : dir.startsWith('ja') ? 'ja' : 'en';
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html') && !f.startsWith('_'));
  for (const f of files) {
    const r = checkTranslation(path.join(dir, f), lang);
    if (r) results.push(r);
  }
}

console.log('=== TRANSLATION CHECK ===');
console.log('Files with issues:', results.length);
results.forEach(r => {
  console.log('\n' + r.file);
  console.log('  ko:' + r.ko + ' en:' + r.en + ' ja:' + r.ja + ' cjk:' + r.cjk);
  console.log('  ISSUES: ' + r.issues.join(' | '));
});
