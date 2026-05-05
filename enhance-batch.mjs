import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const blogDir = join(__dirname, 'blog');

const files = [
  'keyword-research-baidu.html',
  'baidu-pricing-models.html',
  'ocpc-explained.html',
  'native-ads-vs-feed-ads.html',
  'baidu-feed-ads-explained.html',
  'baidu-ads-foreign-business.html',
  'baidu-user-data-targeting.html',
  'baidu-app-ecosystem.html',
  // landing-page-bounce-rate.html is already structurally correct, only Phase 2
  'digital-marketing-china.html',
];

// Phase 2 enhancement CSS (common for all)
const phase2CSS = `
    /* Phase 2 - Callout Cards */
    .callout { border-radius: 12px; padding: 20px 24px; margin: 24px 0; display: flex; gap: 14px; align-items: flex-start; }
    .callout-warning { background: #FEF3C7; border: 1px solid #FCD34D; }
    .callout-tip { background: #D1FAE5; border: 1px solid #6EE7B7; }
    .callout-insight { background: rgba(41,50,225,.06); border: 1px solid rgba(41,50,225,.18); }
    [data-theme="dark"] .callout-warning { background: rgba(245,158,11,.1); border-color: rgba(245,158,11,.25); }
    [data-theme="dark"] .callout-tip { background: rgba(16,185,129,.1); border-color: rgba(16,185,129,.25); }
    [data-theme="dark"] .callout-insight { background: rgba(41,50,225,.12); border-color: rgba(41,50,225,.3); }
    .callout-icon { font-size: 1.3rem; flex-shrink: 0; line-height: 1.6; }
    .callout div { font-size: .95rem; line-height: 1.6; }
    .callout strong { display: block; margin-bottom: 4px; }

    /* Phase 2 - Stats Grid */
    .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 16px; margin: 24px 0; }
    .stat-card { background: var(--gray-50); border-radius: 12px; padding: 20px; text-align: center; border: 1px solid var(--gray-200); }
    [data-theme="dark"] .stat-card { background: var(--gray-100); border-color: var(--gray-200); }
    .stat-value { font-size: 1.8rem; font-weight: 800; color: var(--blue); }
    .stat-label { font-size: .8rem; color: var(--gray-600); margin-top: 4px; }

    /* Phase 2 - Takeaway Box */
    .takeaway-box { background: linear-gradient(135deg, #EEF0FF 0%, #F5F3FF 100%); border: 1px solid #C7D2FE; border-radius: 12px; padding: 24px; margin: 32px 0; }
    [data-theme="dark"] .takeaway-box { background: linear-gradient(135deg, rgba(41,50,225,.08) 0%, rgba(79,70,229,.08) 100%); border-color: rgba(41,50,225,.25); }
    .takeaway-box h3 { font-size: 1rem; font-weight: 700; margin-bottom: 12px; color: var(--blue); display: flex; align-items: center; gap: 8px; }
    .takeaway-box ul { list-style: none; display: flex; flex-direction: column; gap: 8px; }
    .takeaway-box ul li { font-size: .9rem; line-height: 1.6; padding-left: 20px; position: relative; }
    .takeaway-box ul li::before { content: '\\2713'; position: absolute; left: 0; color: var(--blue); font-weight: 700; }

    /* Phase 2 - Responsive */
    @media (max-width: 768px) {
      .callout { flex-direction: column; gap: 8px; }
      .callout-icon { font-size: 1.1rem; }
      .stats-grid { grid-template-columns: repeat(2, 1fr); }
      .stat-value { font-size: 1.5rem; }
      .takeaway-box { padding: 20px; }
    }`;

// Footer social SVG block
const footerSocialHTML = `
    <div class="footer-social">
      <a href="#" class="obf-email-icon" data-u="baidu" data-d="baidumarketing.com" aria-label="Email">
        <svg viewBox="0 0 24 24" fill="none" stroke="#D1D5DB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="22,4 12,13 2,4"/></svg>
      </a>
    </div>
  </div>
</footer>`;

const footerCopyrightHTML = `&copy; <script>document.write(new Date().getFullYear())</script> Baidu PPC Pro. All rights reserved.</div>`;

// Per-file Phase 2 content enhancements
const enhancements = {
  'keyword-research-baidu.html': {
    h2Emojis: { 'Baidu\'s Built-In Tools': '🔍 Baidu\'s Built-In Tools', 'Third-Party Tools': '🛠️ Third-Party Tools', 'Best Practices': '✅ Best Practices' },
    callouts: [
      { after: 'Direct translations of English keywords often miss the mark.', type: 'warning', icon: '⚠️', title: 'Common Mistake:', text: 'Translating English keywords directly often fails. Chinese users search using industry-specific jargon, regional terms, and colloquial phrases that don\'t map cleanly from English.' },
      { after: 'Baidu Index shows trending searches and topic popularity.', type: 'insight', icon: '💡', title: 'Pro Insight:', text: 'Cross-referencing Baidu Index with Baidu Keyword Planner gives you both volume data and trend direction — ideal for timing campaign launches around seasonal demand.' },
    ],
    takeaway: { items: ['Use Baidu Keyword Planner as your primary research tool', 'Leverage 5118.com for competitive keyword analysis', 'Search Zhihu to understand how Chinese users phrase questions', 'Focus on high-intent, mid-tail keywords rather than broad terms', 'Build keyword themes around product type + service + location'] },
  },
  'baidu-pricing-models.html': {
    h2Emojis: { 'Which Should You Use?': '🎯 Which Pricing Model Should You Use?' },
    callouts: [
      { after: 'Set a realistic CPA target (based on your historical data or industry benchmarks) and let the system optimize.', type: 'tip', icon: '✅', title: 'Pro Tip:', text: 'Start with CPC for 2-3 weeks to gather conversion data, then switch to oCPC. The more conversion data Baidu has, the better its AI performs — typically 20+ conversions per week is the sweet spot.' },
      { after: 'CPM or video view optimization makes sense when you\'re not optimizing for immediate conversions.', type: 'insight', icon: '💡', title: 'Strategic Note:', text: 'Many successful B2B campaigns use a layered approach: CPM for brand awareness, CPC for keyword testing, and oCPC for conversion optimization — all running simultaneously across different campaigns.' },
    ],
    takeaway: { items: ['Start new campaigns with CPC to gather data, then switch to oCPC', 'oCPC delivers 20-40% lower CPA through AI-powered bid optimization', 'CPM is best for brand awareness and retargeting campaigns', 'oCPC and oCPA use the same underlying AI technology', 'Set realistic CPA targets — too low and the system can\'t find enough conversions'] },
  },
  'ocpc-explained.html': {
    h2Emojis: { 'How oCPC Works': '⚙️ How oCPC Works', 'oCPC vs Manual CPC': '📊 oCPC vs Manual CPC', 'What You Need to Get Started': '📋 What You Need to Get Started', 'When oCPC Makes Sense': '🎯 When oCPC Makes Sense' },
    callouts: [
      { after: 'It delivers 20-40% lower cost per acquisition compared to manual CPC bidding.', type: 'insight', icon: '💡', title: 'Why It Works:', text: 'Baidu processes 6B+ daily searches. That volume means the AI has enormous data to train on — it can predict conversion probability with high accuracy and adjust bids in milliseconds.' },
      { after: 'Baidu recommends 20+ conversions per week for optimal performance', type: 'warning', icon: '⚠️', title: 'Don\'t Switch Too Early:', text: 'Starting oCPC with fewer than 20 weekly conversions can lead to unstable bidding. The AI needs enough signal to differentiate between high-value and low-value clicks. Be patient with the CPC learning phase.' },
    ],
    takeaway: { items: ['oCPC uses AI to predict conversion probability and adjust bids per auction', 'Delivers 20-40% lower CPA compared to manual CPC bidding', 'Requires conversion tracking (phone calls, forms, or purchases)', 'Wait until you have 20+ weekly conversions before switching from CPC', 'Ideal for lead gen, e-commerce, and app install campaigns'] },
  },
  'native-ads-vs-feed-ads.html': {
    h2Emojis: { 'For Most Advertisers': '🎯 For Most Advertisers', 'The Practical Answer': '💡 The Practical Answer' },
    callouts: [
      { after: 'It bridges the gap between search (high intent) and social (discovery).', type: 'tip', icon: '✅', title: 'Pro Tip:', text: 'Baidu feed ads combine search-intent data (which WeChat and Douyin don\'t have) with content-consumption behavior. This dual-signal targeting is unique to Baidu\'s ecosystem.' },
      { after: 'Most effective Baidu campaigns combine all three, with feed ads serving as the discovery layer that feeds users into the search pipeline.', type: 'insight', icon: '💡', title: 'Key Insight:', text: 'Think of it as a funnel: feed ads generate awareness and discovery, search ads capture high-intent users, and display/video ads reinforce brand messaging. Each plays a distinct role.' },
    ],
    takeaway: { items: ['Native advertising is a format (blends into content); feed is a placement (content streams)', 'Baidu feed ads are native in format AND feed in placement', 'Feed ads on Baidu have a unique advantage: search-intent + behavior targeting', 'Most effective campaigns combine search, feed, and display for full-funnel coverage', 'Focus on user intent stage (discovery vs. decision) rather than terminology'] },
  },
  'baidu-feed-ads-explained.html': {
    h2Emojis: { 'How Feed Ads Are Different from Search Ads': '🔍 How Feed Ads Differ from Search Ads', 'The Targeting Advantage': '🎯 The Targeting Advantage', 'When to Use Feed Ads': '📋 When to Use Feed Ads' },
    callouts: [
      { after: 'They\'re targeted using search history, browsing patterns, and behavioral signals.', type: 'insight', icon: '💡', title: 'Key Insight:', text: 'Unlike social platforms where targeting is based purely on demographics and interests, Baidu feed ads leverage actual search behavior — what users have actively looked for. This creates a much stronger purchase intent signal.' },
      { after: 'Feed builds awareness and captures discovery, search captures high-intent users ready to convert.', type: 'tip', icon: '✅', title: 'Pro Tip:', text: 'Run feed and search campaigns simultaneously with shared negative keywords. Users who convert via search likely saw your feed ad first — the combination creates a multiplier effect on brand recall.' },
    ],
    takeaway: { items: ['Baidu feed has 100M+ DAU with rapid year-over-year growth', 'Feed ads are behavior-targeted, not just keyword-targeted', 'Feed excels at reaching users in discovery mode before they search', 'Pair feed with search for a complete full-funnel Baidu strategy', 'Feed ads perform better than traditional display for brand awareness'] },
  },
  'baidu-ads-foreign-business.html': {
    h2Emojis: { 'Why Baidu Works Better Than Social Platforms': '🥊 Why Baidu Beats Social for Lead Gen', 'Getting Started as a Foreign Company': '🚀 Getting Started as a Foreign Company' },
    callouts: [
      { after: 'The conversion rate on Baidu search ads typically exceeds social platforms because you\'re reaching people at the moment of decision.', type: 'insight', icon: '💡', title: 'Key Insight:', text: 'Social ads generate interest; search ads capture intent. For B2B lead generation where the sales cycle involves research and comparison, Baidu search captures users at the decision point — when they\'re ready to engage.' },
      { after: 'Foreign companies need a Chinese business license or a registered agent.', type: 'warning', icon: '⚠️', title: 'Compliance Note:', text: 'Without a Chinese business entity, you can\'t directly open a Baidu advertising account. Working with a registered agent (like us) handles the compliance layer while you focus on strategy and creative.' },
    ],
    takeaway: { items: ['Baidu processes 6B+ daily searches with intent-based targeting', 'Search ads convert at higher rates than social ads for B2B lead generation', 'AI-powered bidding (oCPC) automates optimization for better ROI', 'Foreign companies need a Chinese business license or registered agent', 'Full-funnel strategy: feed for awareness, search for conversion'] },
  },
  'baidu-user-data-targeting.html': {
    h2Emojis: { 'Where Baidu\'s Data Comes From': '🔍 Where Baidu\'s Data Comes From', 'What This Means for Advertisers': '🎯 What This Means for Advertisers' },
    callouts: [
      { after: 'Google can\'t replicate this in China, which means Baidu offers targeting capabilities that simply aren\'t available through other platforms.', type: 'insight', icon: '💡', title: 'Key Insight:', text: 'Baidu\'s data advantage is structural — it comes from owning search, maps, feed, documents, and cloud storage in China. No other platform (including Google) can replicate this multi-signal data ecosystem in the Chinese market.' },
      { after: 'The combination creates targeting profiles that other platforms simply can\'t match in the Chinese market.', type: 'tip', icon: '✅', title: 'Pro Tip:', text: 'Combine multiple data signals in your targeting: users who searched for logistics keywords AND read supply chain documents on Wenku AND visited industrial zone locations on Maps are extremely high-value B2B prospects.' },
    ],
    takeaway: { items: ['Baidu combines search, feed, maps, Wenku, and Netdisk data for targeting', 'Search history is the richest behavioral signal in the Chinese market', 'Map location data captures real-world behavior patterns', 'Wenku reading habits signal professional interests and B2B profiles', 'Multi-signal targeting creates profiles unmatched by other platforms'] },
  },
  'baidu-app-ecosystem.html': {
    h2Emojis: { 'One Account, Multiple Surfaces': '🔗 One Account, Multiple Surfaces', 'Which Platforms Should You Use?': '🎯 Which Platforms Should You Use?' },
    callouts: [
      { after: 'YouTube, Search, and Display often require separate account structures and have limited data sharing between properties.', type: 'insight', icon: '💡', title: 'Key Insight:', text: 'Baidu\'s unified account structure means your targeting data, creative assets, and performance insights flow across all surfaces. One campaign setup can reach users on search, feed, maps, and video — a level of integration Google doesn\'t offer.' },
      { after: 'If you\'re targeting professionals or B2B audiences.', type: 'tip', icon: '✅', title: 'Pro Tip:', text: 'Wenku reaches 230M+ users who are actively consuming professional and educational content. For B2B campaigns targeting decision-makers, Wenku ads are an overlooked channel with high engagement and lower competition than search.' },
    ],
    takeaway: { items: ['Baidu App (708M MAU) is the primary search and feed surface', 'Baidu Maps captures local intent for geographically targeted campaigns', 'Haokan Video (80 min avg session) is ideal for brand awareness', 'Wenku (230M+ users) reaches professional/B2B audiences effectively', 'One account activates ads across all Baidu surfaces with shared data'] },
  },
  'digital-marketing-china.html': {
    h2Emojis: { 'Online vs Traditional: The Comparison': '📊 Online vs Traditional: The Comparison', 'For B2B Companies Specifically': '🎯 For B2B Companies Specifically', 'The ROI Math': '💰 The ROI Math' },
    callouts: [
      { after: 'Online advertising runs 24/7, reaches nationwide, and — unlike TV or print — gives you real-time data on what\'s working.', type: 'insight', icon: '💡', title: 'Key Insight:', text: 'With 80% internet penetration and 1.1B+ users, China\'s digital landscape offers unparalleled scale. Real-time performance data means you can test, optimize, and scale campaigns in days — not months like traditional media.' },
      { after: 'This covers both ends of the funnel: search captures high-intent buyers, feed builds awareness with prospects who aren\'t searching yet.', type: 'tip', icon: '✅', title: 'Pro Tip:', text: 'The winning digital strategy combines search ads (for high-intent buyers), feed ads (for awareness), and content marketing (for long-term authority). Together they cover the full B2B funnel.' },
      { after: 'A well-optimized Baidu campaign with the same budget might generate 500+ qualified leads with full performance data.', type: 'warning', icon: '⚠️', title: 'Don\'t Ignore the Numbers:', text: 'A single trade show booth can cost ¥100,000+ with limited leads and zero performance tracking. The same budget on Baidu could generate 500+ qualified leads with full analytics.' },
    ],
    statsGrid: {
      replace: 'stat-highlight',
      cards: [
        { value: '1.1B+', label: 'Online Users in China' },
        { value: '80%', label: 'Internet Penetration' },
        { value: '60-80%', label: 'Lower Cost Per Lead' },
        { value: '24/7', label: 'Always-On Reach' },
      ]
    },
    takeaway: { items: ['Digital marketing in China reaches 1.1B+ users with real-time data', 'Online channels deliver 60-80% lower cost per qualified lead', 'B2B success requires combining Baidu search, feed ads, and content marketing', 'Same trade show budget can generate 500+ qualified leads on Baidu', 'Digital campaigns are instantly scalable with no long-term contracts'] },
  },
};

// Process landing-page-bounce-rate separately (it has different structure)
const lpEnhancements = {
  h2Emojis: { 'The Common Causes': '⚠️ The Common Causes', 'The Fix Checklist': '🔧 The Fix Checklist', 'Quick Wins That Move the Needle': '🚀 Quick Wins That Move the Needle' },
  callouts: [
    { after: 'No trust signals — who are you? why should I trust you?', type: 'warning', icon: '⚠️', title: 'China-Specific Issue:', text: 'Overseas-hosted landing pages often load in 5-10 seconds from China. Every extra second of load time increases bounce rate by 20-30%. Hosting in China or using a China CDN is non-negotiable.' },
    { after: 'Data-driven iteration beats guesswork.', type: 'tip', icon: '✅', title: 'Quick Win:', text: 'Chinese B2B buyers often prefer phone calls over form fills. Adding a prominent phone number and WeChat QR code can increase conversion rates by 30-50% for Baidu campaigns.' },
  ],
  takeaway: { items: ['Host in China or use CDN — page speed is critical from Chinese networks', 'Match landing page headline to ad copy for message continuity', 'Place lead forms above the fold with minimal fields', 'Add phone number and WeChat QR prominently for Chinese B2B buyers', 'Test one variable at a time with data-driven iteration'] },
};

function fixFavicon(html) {
  // Remove leaked SVG after the closing >" of the correct favicon
  // Pattern: correct favicon ends with "...>BPP</text></svg>" /> then has leaked SVG content
  const correctFaviconEnd = `</text></svg>" />`;
  const idx = html.indexOf(correctFaviconEnd);
  if (idx === -1) return html;
  
  const afterCorrect = idx + correctFaviconEnd.length;
  const beforeNextLine = html.indexOf('\n', afterCorrect);
  
  // Check if there's leaked SVG on the same line
  const restOfLine = html.substring(afterCorrect, beforeNextLine);
  if (restOfLine.trim().startsWith('<') && restOfLine.includes('width')) {
    // There's leaked SVG on the same line
    html = html.substring(0, afterCorrect) + '\n' + html.substring(beforeNextLine + 1);
  }
  return html;
}

function fixFooter(html) {
  // Check if footer already has </footer> (landing-page-bounce-rate does)
  if (html.includes('</footer>')) return html;
  
  // Fix: replace broken footer end
  // Current: <div class="footer-copy">&copy; \n<script>...
  // Need: <div class="footer-copy">&copy; <script>document.write(new Date().getFullYear())</script> Baidu PPC Pro. All rights reserved.</div>\n    <div class="footer-social">...SVG...</div>\n  </div>\n</footer>
  
  const brokenFooterCopy = `<div class="footer-copy">&copy; \n<script>`;
  const footerSocialStart = `<script>
  // Mobile nav toggle`;
  
  if (html.includes(brokenFooterCopy)) {
    html = html.replace(brokenFooterCopy, `<div class="footer-copy">${footerCopyrightHTML}\n    ${footerSocialHTML.split('\n').slice(0, -1).join('\n')}\n\n${footerSocialStart}`);
    // Remove the extra blank line
    html = html.replace(/\n\n\n/, '\n\n');
  }
  
  return html;
}

function addPhase2CSS(html) {
  // Insert Phase 2 CSS before </style>
  const styleClose = '</style>';
  if (!html.includes(styleClose)) return html;
  
  // Check if Phase 2 CSS already exists
  if (html.includes('.callout {')) return html;
  
  const idx = html.indexOf(styleClose);
  html = html.substring(0, idx) + phase2CSS + '\n  ' + styleClose + html.substring(idx + styleClose.length);
  return html;
}

function addH2Emojis(html, emojis) {
  for (const [original, replacement] of Object.entries(emojis)) {
    // Only replace if emoji not already present
    if (!html.includes(replacement.substring(0, 3))) {
      html = html.replace(`<h2>${original}</h2>`, `<h2>${replacement}</h2>`);
    }
  }
  return html;
}

function addCallouts(html, callouts) {
  for (const callout of callouts) {
    const calloutHTML = `\n        <div class="callout callout-${callout.type}">
              <span class="callout-icon">${callout.icon}</span>
              <div><strong>${callout.title}</strong> ${callout.text}</div>
            </div>`;
    
    // Find the paragraph containing the trigger text
    const pIdx = html.indexOf(callout.after);
    if (pIdx === -1) continue;
    
    // Find the end of this paragraph
    const pCloseIdx = html.indexOf('</p>', pIdx);
    if (pCloseIdx === -1) continue;
    
    const insertPos = pCloseIdx + 4;
    // Check if a callout is already nearby
    const nearby = html.substring(insertPos, insertPos + 20);
    if (nearby.includes('callout')) continue;
    
    html = html.substring(0, insertPos) + calloutHTML + html.substring(insertPos);
  }
  return html;
}

function addTakeaway(html, takeaway) {
  if (html.includes('takeaway-box')) return html;
  
  const ctaSection = '<div class="cta-section">';
  const ctaIdx = html.indexOf(ctaSection);
  if (ctaIdx === -1) return html;
  
  const itemsHTML = takeaway.items.map(item => `                <li>${item}</li>`).join('\n');
  const takeawayHTML = `
        <div class="takeaway-box">
              <h3>📋 Key Takeaways</h3>
              <ul>
${itemsHTML}
              </ul>
            </div>

`;
  
  html = html.substring(0, ctaIdx) + takeawayHTML + html.substring(ctaIdx);
  return html;
}

function replaceStatsGrid(html, config) {
  if (!config || html.includes('stats-grid')) return html;
  
  const oldDiv = `<div class="stat-highlight">
          <div class="big">60-80%</div>
          <div class="label">Lower cost per qualified lead vs offline channels</div>
        </div>`;
  
  if (html.includes(oldDiv)) {
    const cardsHTML = config.cards.map(c => `              <div class="stat-card">
                <div class="stat-value">${c.value}</div>
                <div class="stat-label">${c.label}</div>
              </div>`).join('\n');
    
    const newDiv = `<div class="stats-grid">
${cardsHTML}
            </div>`;
    
    html = html.replace(oldDiv, newDiv);
  }
  return html;
}

// Process each file
for (const file of files) {
  const filePath = join(blogDir, file);
  let html = readFileSync(filePath, 'utf-8');
  const original = html;
  
  // Phase 1 fixes
  html = fixFavicon(html);
  html = fixFooter(html);
  
  // Phase 2 CSS
  html = addPhase2CSS(html);
  
  // Phase 2 content
  const enh = enhancements[file];
  if (enh) {
    html = addH2Emojis(html, enh.h2Emojis);
    html = addCallouts(html, enh.callouts);
    html = addTakeaway(html, enh.takeaway);
    if (enh.statsGrid) {
      html = replaceStatsGrid(html, enh.statsGrid);
    }
  }
  
  if (html !== original) {
    writeFileSync(filePath, html, 'utf-8');
    console.log(`✅ Enhanced: ${file}`);
  } else {
    console.log(`⏭️  No changes: ${file}`);
  }
}

// Process landing-page-bounce-rate.html separately
{
  const filePath = join(blogDir, 'landing-page-bounce-rate.html');
  let html = readFileSync(filePath, 'utf-8');
  const original = html;
  
  html = addPhase2CSS(html);
  html = addH2Emojis(html, lpEnhancements.h2Emojis);
  html = addCallouts(html, lpEnhancements.callouts);
  html = addTakeaway(html, lpEnhancements.takeaway);
  
  if (html !== original) {
    writeFileSync(filePath, html, 'utf-8');
    console.log('✅ Enhanced: landing-page-bounce-rate.html');
  } else {
    console.log('⏭️  No changes: landing-page-bounce-rate.html');
  }
}

console.log('\n🎉 All done!');
