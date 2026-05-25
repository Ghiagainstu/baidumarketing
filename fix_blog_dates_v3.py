#!/usr/bin/env python3
"""Fix blog display dates - handle all HTML structures."""

import re
from pathlib import Path

# Blogs that need display date fixes (those with broken/empty date spans)
FIXES = {
    "baidu-ad-performance-diagnostic-tool": ("2022-06-24", "Jun 24, 2022"),
    "baidu-ads-campaign-upgrade-2025": ("2025-10-16", "Oct 16, 2025"),
    "baidu-click-fraud-ipv4-blocking": ("2020-12-31", "Dec 31, 2020"),
    "baidu-conversion-tracking-dedup": ("2021-08-17", "Aug 17, 2021"),
    "baidu-creative-url-retirement-migration": ("2025-05-22", "May 22, 2025"),
    "baidu-custom-form-retirement": ("2024-07-24", "Jul 24, 2024"),
    "baidu-feed-ads-history-operation-records-upgrade": ("2020-11-30", "Nov 30, 2020"),
    "baidu-inactive-keyword-cleanup-2025": ("2025-12-08", "Dec 8, 2025"),
    "baidu-landing-page-audit-rejection-reasons": ("2021-01-06", "Jan 6, 2021"),
    "baidu-landing-page-report": ("2021-03-31", "Mar 31, 2021"),
    "baidu-ocpc-skip-data-accumulation": ("2021-12-22", "Dec 22, 2021"),
    "baidu-search-ads-1-1-desktop-images": ("2025-10-27", "Oct 27, 2025"),
    "baidu-search-device-bid-coefficient-retirement": ("2022-09-14", "Sep 14, 2022"),
    "baidu-user-data-targeting": ("2025-04-15", "Apr 15, 2025"),
    "baidu-vs-google-ppc-differences": ("2026-04-30", "Apr 30, 2026"),
    "faq-international-brands": ("2026-05-10", "May 10, 2026"),
    "feed-landing-page-optimization": ("2024-11-20", "Nov 20, 2024"),
    "keyword-research-baidu": ("2024-12-05", "Dec 5, 2024"),
    "landing-page-bounce-rate": ("2024-12-08", "Dec 8, 2024"),
    "native-ads-vs-feed-ads": ("2024-12-15", "Dec 15, 2024"),
    "ocpc-explained": ("2024-12-10", "Dec 10, 2024"),
    "digital-consumer-9trillion": ("2026-04-01", "Apr 2026"),
    "search-vs-ai-usage": ("2026-04-01", "Apr 2026"),
    "baidu-ads-foreign-business": ("2025-01-01", "Jan 2025"),
    "baidu-pricing-models": ("2024-12-12", "Dec 12, 2024"),
    "baidu-feed-account-structure": ("2024-11-25", "Nov 25, 2024"),
    "baidu-feed-ads-explained": ("2025-01-20", "Jan 20, 2025"),
    "digital-marketing-china": ("2024-12-01", "Dec 2024"),
}

def fix_file(filepath, iso_date, display_date):
    """Fix both JSON-LD datePublished and display date."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Fix JSON-LD datePublished
    content = re.sub(
        r'"datePublished"\s*:\s*"2025-01-01"',
        f'"datePublished": "{iso_date}"',
        content
    )
    content = re.sub(
        r'"datePublished"\s*:\s*"2025-01-01"',
        f'"datePublished":"{iso_date}"',
        content
    )

    # Fix display date - multiple patterns
    # Pattern 1: <span>Month YYYY</span> or <span>Mon DD, YYYY</span> in article-meta
    # Look for the date pattern after article-meta
    date_patterns = [
        # Empty date span: <span></span>
        (r'(<div class="article-meta">\s*<span>)\s*(</span>\s*<span>·</span>)', f'\\1{display_date}\\2'),
        # Month YYYY format: <span>Apr 2025</span>
        (r'<span>(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}</span>', f'<span>{display_date}</span>'),
        # Mon DD, YYYY format: <span>Apr 12, 2025</span>
        (r'<span>(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s*\d{4}</span>', f'<span>{display_date}</span>'),
    ]

    for pattern, replacement in date_patterns:
        new_content = re.sub(pattern, replacement, content, count=1)
        if new_content != content:
            content = new_content
            break

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    blog_dir = Path("blog")
    fixed = 0

    for slug, (iso_date, display_date) in FIXES.items():
        filepath = blog_dir / f"{slug}.html"
        if filepath.exists():
            if fix_file(filepath, iso_date, display_date):
                print(f"✅ Fixed: {slug} → {display_date}")
                fixed += 1
            else:
                print(f"⏭️  Skipped: {slug}")

    print(f"\n📊 Fixed {fixed} files")

if __name__ == "__main__":
    main()
