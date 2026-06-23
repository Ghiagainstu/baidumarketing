# BPP Website Project Files

This directory contains all files needed for Codex to take over BPP website changes.

## Directory Structure
```
U:\AI BPP\
├── CODING_GUIDE.md          # Complete coding guide for Codex
├── README.md                # This file
├── .workbuddy/
│   ├── memory/
│   │   └── MEMORY.md        # Project history and lessons learned
│   └── skills/
│       ├── bpp-template-ultimate/  # Page creation template
│       ├── bpp-blog-html/         # Blog pipeline
│       ├── bpp-blog-write/        # Blog content creation
│       ├── bpp-新语言-nav/        # Language nav sync
│       ├── blog-enhance/          # Visual enhancement
│       └── blog-summary-enhance/  # Blog card summary
├── index.html               # Homepage
├── about.html               # About page
├── features.html            # Features page
├── pricing.html             # Pricing page
├── clients.html             # Clients page
├── faq.html                 # FAQ page
├── contact.html             # Contact page
├── blog.html                # Blog listing page
├── privacy.html             # Privacy policy
├── terms.html               # Terms of service
├── why-baidu-ppc-pro.html   # Why Baidu PPC Pro page
├── china-geo.html           # China GEO page
├── 404.html                 # 404 error page
├── build.mjs                # Build script for nav/footer sync
├── vercel.json              # Vercel deployment config
├── package.json             # Package config
├── robots.txt               # Crawler config
├── sitemap.xml              # Auto-generated sitemap
├── blog/
│   ├── _template-en.html    # Blog post template
│   ├── 8-ways-lower-baidu-cpc.html
│   └── saas-companies-baidu-ppc-china.html
├── ja/                      # Japanese translations
│   ├── index.html
│   ├── blog/
│   └── ...
├── ko/                      # Korean translations
│   ├── index.html
│   ├── blog/
│   └── ...
├── locales/                 # Translation JSON files
│   ├── nav-ja.json
│   ├── nav-ko.json
│   ├── footer-ja.json
│   ├── footer-ko.json
│   └── languages.json
└── assets/
    ├── js/main.js
    ├── og-brand-default.png
    └── team/
```

## Quick Start for Codex
1. Read `CODING_GUIDE.md` first - it contains all critical rules
2. Check `.workbuddy/memory/MEMORY.md` for full project history
3. Use skills in `.workbuddy/skills/` for specific tasks
4. Always use clean URLs (no .html) for internal links
5. Always include `www` in all URLs
6. Follow the navigation order: Why Baidu PPC Pro → Services → Pricing → Clients → FAQ → About → Blog → Contact

## Deployment
- Push to GitHub: `git push origin main`
- Vercel auto-deploys within ~1 minute
- Verify on https://www.baidumarketing.com/

## Key Commands
```bash
node build.mjs sync all    # Sync all language nav/footer
node build.mjs ls          # List all page status
node build.mjs site        # Update sitemap.xml
```

## Contact
- GitHub: https://github.com/Ghiagainstu/baidumarketing.git
- Domain: baidumarketing.com
