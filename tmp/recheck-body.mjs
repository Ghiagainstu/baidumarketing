import fs from 'fs';
const files = [
  'baidu-search-ads-1-1-desktop-images.html',
  'baidu-app-ecosystem.html',
  'baidu-2026-international-brands.html',
  'baidu-six-updates-june-2026.html',
  'baidu-industry-insights-tool-guide.html',
  'b2b-lead-generation-framework.html'
];
for (const f of files) {
  const h = fs.readFileSync('ko/blog/' + f, 'utf8');
  const pTags = (h.match(/<p[^>]*>([\s\S]*?)<\/p>/gi) || []);
  const first3 = pTags.slice(0, 3).map(t => t.replace(/<[^>]+>/g, '').trim().slice(0, 100));
  const ko = (pTags.join('').match(/[\uac00-\ud7af]/g) || []).length;
  const jp = (pTags.join('').match(/[\u3040-\u309f\u30a0-\u30ff]/g) || []).length;
  const cn = (pTags.join('').match(/[\u4e00-\u9fff]/g) || []).length;
  console.log('\n=== ' + f + ' (ko:' + ko + ' jp:' + jp + ' cn:' + cn + ') ===');
  first3.forEach((t, i) => console.log('  p' + (i+1) + ': ' + t));
}
