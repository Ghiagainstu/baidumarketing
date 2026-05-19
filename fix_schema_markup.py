#!/usr/bin/env python3
"""
Fix SEO tags for BPP website - Batch 2: Schema Markup (JSON-LD)
Usage: python fix_schema_markup.py
"""

import os
import json
from pathlib import Path

WORKSPACE = r"C:\Users\HYE\WorkBuddy\20260411211839"

def add_organization_schema():
    """Add Organization schema to index.html"""
    filepath = os.path.join(WORKSPACE, 'index.html')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if schema already exists
    if 'application/ld+json' in content and 'Organization' in content:
        print(f"  ✓ Organization schema already exists: index.html")
        return False
    
    # Organization schema
    schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Baidu PPC Pro",
        "url": "https://www.baidumarketing.com",
        "description": "Baidu advertising services for global companies",
        "logo": "https://www.baidumarketing.com/assets/logo.png",
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "sales",
            "availableLanguage": ["English", "Chinese", "Japanese"]
        },
        "sameAs": [
            "https://www.linkedin.com/company/baidu-ppc-pro"
        ]
    }
    
    schema_script = f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>\n'
    
    # Insert before </head>
    head_close_idx = content.find('</head>')
    
    if head_close_idx == -1:
        print(f"  ✗ Could not find </head>: index.html")
        return False
    
    new_content = content[:head_close_idx] + schema_script + content[head_close_idx:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✓ Added Organization schema: index.html")
    return True

def add_faq_schema():
    """Add FAQPage schema to faq.html"""
    filepath = os.path.join(WORKSPACE, 'faq.html')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if schema already exists
    if 'application/ld+json' in content and 'FAQPage' in content:
        print(f"  ✓ FAQPage schema already exists: faq.html")
        return False
    
    # Extract FAQ items from HTML (simplified - need to parse actual FAQ content)
    # This is a placeholder - actual implementation needs to parse FAQ content
    print(f"  ⚠ FAQPage schema requires manual review: faq.html")
    return False

def add_blog_posting_schema(filepath, blog_slug):
    """Add BlogPosting schema to blog HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if schema already exists
    if 'application/ld+json' in content and 'BlogPosting' in content:
        print(f"  ✓ BlogPosting schema already exists: {os.path.basename(filepath)}")
        return False
    
    # Extract metadata from HTML
    import re
    
    # Get title
    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1) if title_match else ''
    
    # Get description
    desc_match = re.search(r'<meta name="description" content="(.*?)"', content)
    description = desc_match.group(1) if desc_match else ''
    
    # Get date (placeholder - need to extract from HTML or filename)
    date_published = "2026-01-01"  # Placeholder
    
    # Determine if it's JA blog
    is_ja = '\ja\blog' in filepath or '\ja/blog' in filepath
    
    if is_ja:
        url = f"https://www.baidumarketing.com/ja/blog/{blog_slug}"
    else:
        url = f"https://www.baidumarketing.com/blog/{blog_slug}"
    
    # BlogPosting schema
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": description,
        "url": url,
        "datePublished": date_published,
        "dateModified": date_published,
        "author": {
            "@type": "Person",
            "name": "Benny Cheuk",
            "url": "https://www.baidumarketing.com/about#benny-cheuk"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Baidu PPC Pro",
            "logo": {
                "@type": "ImageObject",
                "url": "https://www.baidumarketing.com/assets/logo.png"
            }
        }
    }
    
    schema_script = f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>\n'
    
    # Insert before </head>
    head_close_idx = content.find('</head>')
    
    if head_close_idx == -1:
        print(f"  ✗ Could not find </head>: {os.path.basename(filepath)}")
        return False
    
    new_content = content[:head_close_idx] + schema_script + content[head_close_idx:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✓ Added BlogPosting schema: {os.path.basename(filepath)}")
    return True

def main():
    import re
    
    print("="*80)
    print("Batch 2: Adding Schema Markup (JSON-LD)")
    print("="*80)
    
    # 1. Add Organization schema to index.html
    print("\n[1/3] Adding Organization schema to index.html...")
    add_organization_schema()
    
    # 2. Add FAQPage schema to faq.html (requires manual review)
    print("\n[2/3] Adding FAQPage schema to faq.html...")
    add_faq_schema()
    
    # 3. Add BlogPosting schema to blog files
    print("\n[3/3] Adding BlogPosting schema to blog files...")
    blog_dir = os.path.join(WORKSPACE, 'blog')
    
    if os.path.exists(blog_dir):
        for filename in os.listdir(blog_dir):
            if filename.endswith('.html'):
                filepath = os.path.join(blog_dir, filename)
                blog_slug = filename.replace('.html', '')
                add_blog_posting_schema(filepath, blog_slug)
    
    print("\n" + "="*80)
    print("Batch 2 completed! (FAQPage schema requires manual review)")
    print("="*80)

if __name__ == '__main__':
    main()
