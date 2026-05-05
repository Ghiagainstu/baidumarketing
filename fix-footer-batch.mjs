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
  'digital-marketing-china.html',
];

const footerSocialSVG = `<a href="#" class="obf-email-icon" data-u="baidu" data-d="baidumarketing.com" aria-label="Email">
        <svg viewBox="0 0 24 24" fill="none" stroke="#D1D5DB" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><polyline points="22,4 12,13 2,4"/></svg>
      </a>
    </div>
  </div>
</footer>`;

const copyrightJS = `<script>document.write(new Date().getFullYear())</script> Baidu PPC Pro. All rights reserved.</div>
    <div class="footer-social">
      ${footerSocialSVG}`;

for (const file of files) {
  const filePath = join(blogDir, file);
  let html = readFileSync(filePath, 'utf-8');
  const original = html;

  // Check if footer is already fixed (has </footer>)
  if (html.includes('</footer>')) {
    console.log(`⏭️  Already fixed: ${file}`);
    continue;
  }

  // Replace the broken footer pattern: &copy; [whitespace] <script>  // Mobile nav toggle
  // with proper copyright + social SVG + script
  const brokenPattern = /&copy;[\s\r\n]+<script>\s*\n\s*\/\/\s*Mobile\s+nav\s+toggle/;
  
  if (brokenPattern.test(html)) {
    html = html.replace(brokenPattern, `&copy; ${copyrightJS}\n<script>\n  // Mobile nav toggle`);
    writeFileSync(filePath, html, 'utf-8');
    console.log(`✅ Fixed footer: ${file}`);
  } else {
    console.log(`❓ Pattern not found: ${file}`);
    // Debug: show what's around &copy;
    const idx = html.indexOf('&copy;');
    if (idx !== -1) {
      console.log(`   Context: ${JSON.stringify(html.substring(idx, idx + 50))}`);
    }
  }
}

console.log('\n✨ Footer fix complete!');
