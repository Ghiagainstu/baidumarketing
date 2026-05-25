#!/usr/bin/env python3
"""Fix blog datePublished and display dates from Obsidian source files."""

import re
import os
from pathlib import Path

# Complete mapping: blog slug → correct date (from Obsidian KO/EN files)
# Format: slug → (iso_date, display_date)
DATE_MAP = {
    "ai-assistants-vs-baidu": ("2026-04-20", "Apr 20, 2026"),
    "baidu-2025-earnings-geo": ("2026-04-15", "Apr 15, 2026"),
    "baidu-ad-performance-diagnostic-tool": ("2022-06-24", "Jun 24, 2022"),
    "baidu-ads-campaign-upgrade-2025": ("2025-10-16", "Oct 16, 2025"),
    "baidu-app-ecosystem": ("2025-04-12", "Apr 12, 2025"),
    "baidu-click-fraud-ipv4-blocking": ("2020-12-31", "Dec 31, 2020"),
    "baidu-conversion-tracking-dedup": ("2021-08-17", "Aug 17, 2021"),
    "baidu-creative-url-retirement-migration": ("2025-05-22", "May 22, 2025"),
    "baidu-custom-form-retirement": ("2024-07-24", "Jul 24, 2024"),
    "baidu-ecosystem-numbers": ("2025-04-01", "Apr 2025"),
    "baidu-feed-account-structure": ("2024-11-25", "Nov 25, 2024"),
    "baidu-feed-ads-explained": ("2025-01-20", "Jan 20, 2025"),
    "baidu-feed-ads-history-operation-records-upgrade": ("2020-11-30", "Nov 30, 2020"),
    "baidu-inactive-keyword-cleanup-2025": ("2025-12-08", "Dec 8, 2025"),
    "baidu-landing-page-audit-rejection-reasons": ("2021-01-06", "Jan 6, 2021"),
    "baidu-landing-page-report": ("2021-03-31", "Mar 31, 2021"),
    "baidu-ocpc-skip-data-accumulation": ("2021-12-22", "Dec 22, 2021"),
    "baidu-pricing-models": ("2024-12-12", "Dec 12, 2024"),
    "baidu-search-ads-1-1-desktop-images": ("2025-10-27", "Oct 27, 2025"),
    "baidu-search-device-bid-coefficient-retirement": ("2022-09-14", "Sep 14, 2022"),
    "baidu-user-data-targeting": ("2025-04-15", "Apr 15, 2025"),
    "baidu-vs-google-ppc-differences": ("2026-04-30", "Apr 30, 2026"),
    "china-internet-numbers-2025": ("2026-04-22", "Apr 22, 2026"),
    "digital-consumer-9trillion": ("2026-04-01", "Apr 2026"),
    "digital-marketing-china": ("2024-12-01", "Dec 2024"),
    "faq-international-brands": ("2026-05-10", "May 10, 2026"),
    "feed-landing-page-optimization": ("2024-11-20", "Nov 20, 2024"),
    "keyword-research-baidu": ("2024-12-05", "Dec 5, 2024"),
    "landing-page-bounce-rate": ("2024-12-08", "Dec 8, 2024"),
    "native-ads-vs-feed-ads": ("2024-12-15", "Dec 15, 2024"),
    "ocpc-explained": ("2024-12-10", "Dec 10, 2024"),
    "search-vs-ai-usage": ("2026-04-01", "Apr 2026"),
    # Blogs that already have correct dates but let's verify
    "baidu-ads-foreign-business": ("2025-01-01", "Jan 2025"),
}

def fix_file(filepath, iso_date, display_date):
    """Fix datePublished in JSON-LD and display date in article-meta."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix JSON-LD datePublished (both formats: with and without spaces)
    # Pattern 1: "datePublished": "2025-01-01"
    content = re.sub(
        r'"datePublished"\s*:\s*"2025-01-01"',
        f'"datePublished": "{iso_date}"',
        content
    )
    # Pattern 2: "datePublished":"2025-01-01"
    content = re.sub(
        r'"datePublished"\s*:\s*"2025-01-01"',
        f'"datePublished":"{iso_date}"',
        content
    )
    
    # Fix dateModified if it's also 2025-01-01
    content = re.sub(
        r'"dateModified"\s*:\s*"2025-01-01"',
        f'"dateModified": "{iso_date}"',
        content
    )
    
    # Fix display date in article-meta
    # Pattern: <span>January 2025</span> or <span>April 2025</span> etc.
    # We need to replace the first <span>...</span> in article-meta that contains a date
    
    # For blogs with display dates like "January 2025", "April 2025" etc.
    month_pattern = r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}'
    if re.search(month_pattern, content):
        # Replace the month year pattern in article-meta
        content = re.sub(
            f'<span>{month_pattern}</span>',
            f'<span>{display_date}</span>',
            content,
            count=1
        )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    blog_dir = Path("blog")
    fixed = 0
    skipped = 0
    
    for slug, (iso_date, display_date) in DATE_MAP.items():
        filepath = blog_dir / f"{slug}.html"
        if filepath.exists():
            if fix_file(filepath, iso_date, display_date):
                print(f"✅ Fixed: {slug} → {iso_date} / {display_date}")
                fixed += 1
            else:
                print(f"⏭️  Skipped (no change needed): {slug}")
                skipped += 1
        else:
            print(f"❌ Not found: {slug}.html")
    
    print(f"\n📊 Summary: {fixed} fixed, {skipped} skipped")

if __name__ == "__main__":
    main()
