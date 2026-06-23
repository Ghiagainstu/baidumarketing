import fs from 'fs';
const files = [
  'ai-marketing-whitepapers-2026-baidu-insights.html',
  'b2b-lead-generation-framework.html',
  'baidu-ad-creation-workflow-simplified-creative-upgrade.html',
  'baidu-ad-performance-diagnostic-tool.html',
  'baidu-ads-campaign-upgrade-2025.html',
  'baidu-brand-info-account-level.html',
  'baidu-click-fraud-ipv4-blocking.html',
  'baidu-conversion-tracking-dedup.html',
  'baidu-feed-ads-history-operation-records-upgrade.html',
  'baidu-inactive-keyword-cleanup-2025.html',
  'baidu-industry-insights-tool-guide.html',
  'baidu-landing-page-audit-rejection-reasons.html',
  'baidu-landing-page-report.html',
  'baidu-ocpc-skip-data-accumulation.html',
  'baidu-search-ads-1-1-desktop-images.html',
  'baidu-search-device-bid-coefficient-retirement.html',
  'chinese-consumers-decision-journey.html',
  'faq-international-brands.html',
  'baidu-2026-international-brands.html',
  'baidu-app-ecosystem.html',
  'baidu-custom-form-retirement.html',
  'baidu-six-updates-june-2026.html'
];

for (const f of files) {
  const h = fs.readFileSync('ko/blog/' + f, 'utf8');
  // Get text inside <p> tags only
  const pTexts = (h.match(/<p[^>]*>([\s\S]*?)<\/p>/gi) || [])
    .map(t => t.replace(/<[^>]+>/g, ''))
    .join(' ');
  const ko = (pTexts.match(/[\uac00-\ud7af]/g) || []).length;
  const en = (pTexts.match(/[a-zA-Z]{3,}/g) || []).length;
  const ratio = ko + en > 0 ? Math.round(ko / (ko + en) * 100) : 0;
  const status = ratio > 30 ? 'BODY_KO' : ratio > 10 ? 'PARTIAL' : 'BODY_EN';
  console.log(`${f}: ${status} (${ratio}% ko, ${ko} ko chars, ${en} en words)`);
}
