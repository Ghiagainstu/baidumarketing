import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const blogDir = join(__dirname, 'blog');

const takeaways = {
  'keyword-research-baidu.html': ['Use Baidu Keyword Planner as your primary research tool', 'Leverage 5118.com for competitive keyword analysis', 'Search Zhihu to understand how Chinese users phrase questions', 'Focus on high-intent, mid-tail keywords rather than broad terms', 'Build keyword themes around product type + service + location'],
  'baidu-pricing-models.html': ['Start new campaigns with CPC to gather data, then switch to oCPC', 'oCPC delivers 20-40% lower CPA through AI-powered bid optimization', 'CPM is best for brand awareness and retargeting campaigns', 'oCPC and oCPA use the same underlying AI technology', 'Set realistic CPA targets to let the AI optimize effectively'],
  'ocpc-explained.html': ['oCPC uses AI to predict conversion probability and adjust bids per auction', 'Delivers 20-40% lower CPA compared to manual CPC bidding', 'Requires conversion tracking (phone calls, forms, or purchases)', 'Wait until you have 20+ weekly conversions before switching from CPC', 'Ideal for lead gen, e-commerce, and app install campaigns'],
  'native-ads-vs-feed-ads.html': ['Native advertising is a format (blends into content); feed is a placement (content streams)', 'Baidu feed ads are native in format AND feed in placement', 'Feed ads on Baidu have a unique advantage: search-intent + behavior targeting', 'Most effective campaigns combine search, feed, and display for full-funnel coverage', 'Focus on user intent stage (discovery vs. decision) rather than terminology'],
  'baidu-feed-ads-explained.html': ['Baidu feed has 100M+ DAU with rapid year-over-year growth', 'Feed ads are behavior-targeted, not just keyword-targeted', 'Feed excels at reaching users in discovery mode before they search', 'Pair feed with search for a complete full-funnel Baidu strategy', 'Feed ads perform better than traditional display for brand awareness'],
  'baidu-ads-foreign-business.html': ['Baidu processes 6B+ daily searches with intent-based targeting', 'Search ads convert at higher rates than social ads for B2B lead generation', 'AI-powered bidding (oCPC) automates optimization for better ROI', 'Foreign companies need a Chinese business license or registered agent', 'Full-funnel strategy: feed for awareness, search for conversion'],
  'baidu-user-data-targeting.html': ['Baidu combines search, feed, maps, Wenku, and Netdisk data for targeting', 'Search history is the richest behavioral signal in the Chinese market', 'Map location data captures real-world behavior patterns', 'Wenku reading habits signal professional interests and B2B profiles', 'Multi-signal targeting creates profiles unmatched by other platforms'],
  'baidu-app-ecosystem.html': ['Baidu App (708M MAU) is the primary search and feed surface', 'Baidu Maps captures local intent for geographically targeted campaigns', 'Haokan Video (80 min avg session) is ideal for brand awareness', 'Wenku (230M+ users) reaches professional/B2B audiences effectively', 'One account activates ads across all Baidu surfaces with shared data'],
  'landing-page-bounce-rate.html': ['Host in China or use CDN — page speed is critical from Chinese networks', 'Match landing page headline to ad copy for message continuity', 'Place lead forms above the fold with minimal fields', 'Add phone number and WeChat QR prominently for Chinese B2B buyers', 'Test one variable at a time with data-driven iteration'],
  'digital-marketing-china.html': ['Digital marketing in China reaches 1.1B+ users with real-time data', 'Online channels deliver 60-80% lower cost per qualified lead', 'B2B success requires combining Baidu search, feed ads, and content marketing', 'Same trade show budget can generate 500+ qualified leads on Baidu', 'Digital campaigns are instantly scalable with no long-term contracts'],
};

for (const [file, items] of Object.entries(takeaways)) {
  const filePath = join(blogDir, file);
  let html = readFileSync(filePath, 'utf-8');
  
  // Check if takeaway-box HTML already exists (not CSS)
  if (/class="takeaway-box"/.test(html)) {
    console.log(`⏭️  Has takeaway: ${file}`);
    continue;
  }
  
  const itemsHTML = items.map(item => `              <li>${item}</li>`).join('\n');
  const takeawayHTML = `
        <div class="takeaway-box">
          <h3>📋 Key Takeaways</h3>
          <ul>
${itemsHTML}
          </ul>
        </div>
`;
  
  // Find <div class="cta-section" with flexible whitespace
  const ctaMatch = html.match(/<div\s+class="cta-section">/);
  if (ctaMatch) {
    const idx = ctaMatch.index;
    html = html.substring(0, idx) + takeawayHTML + html.substring(idx);
    writeFileSync(filePath, html, 'utf-8');
    console.log(`✅ Added takeaway: ${file}`);
  } else {
    console.log(`❓ No cta-section found: ${file}`);
  }
}

console.log('\n✨ Takeaway insertion complete!');
