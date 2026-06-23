import fs from 'fs';
const files = [
  'baidu-ad-creation-workflow-simplified-creative-upgrade.html',
  'baidu-ad-performance-diagnostic-tool.html',
  'baidu-brand-info-account-level.html',
  'baidu-click-fraud-ipv4-blocking.html',
  'baidu-conversion-tracking-dedup.html',
  'baidu-feed-ads-history-operation-records-upgrade.html',
  'baidu-inactive-keyword-cleanup-2025.html',
  'baidu-landing-page-audit-rejection-reasons.html',
  'baidu-landing-page-report.html',
  'baidu-ocpc-skip-data-accumulation.html',
  'baidu-search-device-bid-coefficient-retirement.html',
  'chinese-consumers-decision-journey.html',
  'faq-international-brands.html',
  'baidu-ads-campaign-upgrade-2025.html',
  'baidu-custom-form-retirement.html'
];
let ok = 0, fail = 0;
for (const f of files) {
  const h = fs.readFileSync('ko/blog/' + f, 'utf8');
  const title = h.match(/<title>([^<]*)<\/title>/)?.[1] || '';
  const ogTitle = (h.match(/og:title[^>]*content="([^"]+)"/i) || [])[1] || '';
  const schema = (h.match(/"headline": "([^"]+)"/) || [])[1] || '';
  const hasKo = s => /[\uac00-\ud7af]/.test(s);
  const t = hasKo(title) ? 'T' : '-';
  const o = hasKo(ogTitle) ? 'O' : '-';
  const s = hasKo(schema) ? 'S' : '-';
  const pass = hasKo(title) && hasKo(ogTitle) && hasKo(schema);
  if (pass) ok++; else fail++;
  console.log(`${pass ? 'OK' : 'FAIL'} ${t}${o}${s} ${f}`);
}
console.log(`\nResult: ${ok} passed, ${fail} failed`);
