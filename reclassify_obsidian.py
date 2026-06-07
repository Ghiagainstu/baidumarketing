"""
Reclassify all Obsidian Baidu blog articles to official categories.
Official: insights / platform / search / feed / strategy / landing / pricing
"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

VAULT = 'E:/Obsidian/Baidu'

# Official categories (EN for all languages)
OFFICIAL = ['insights', 'platform', 'search', 'feed', 'strategy', 'landing', 'pricing']

# === MAPPING RULES ===
# 1. Folder-based mapping (folders 08-13 and special cases)
FOLDER_MAP = {
    '01-Market-Insights': 'insights',
    '02-Platform': 'platform',
    '03-Search-Ads': 'search',
    '04-Feed-Ads': 'feed',
    '05-Strategy': 'strategy',
    '06-Landing-Page': 'landing',
    '07-Pricing-Models': 'pricing',
    '08-Baidu-Basics': 'strategy',      # Getting started / account basics
    '09-China-Search-Landscape': 'insights',  # Market landscape
    '10-ByteDance-Douyin': 'insights',  # Competitive landscape
    '11-Offline-Traditional': 'strategy',  # Marketing approach
    '12-Operations-Compliance': 'search',  # Search ad operations
    '13-Special-Topics': 'strategy',    # Special topics / tips
}

# 2. Chinese category → EN official
CN_MAP = {
    '市场洞察': 'insights',
    '平台生态': 'platform',
    '搜索广告': 'search',
    '信息流广告': 'feed',
    '策略': 'strategy',
    '落地页': 'landing',
    '定价模型': 'pricing',
    '百度基础': 'strategy',
    '中国搜索': 'insights',
    '字节跳动': 'insights',
    '线下广告': 'strategy',
    '运营合规': 'search',
    '专题': 'strategy',
}

# 3. Korean category → EN official
KO_MAP = {
    '인사이트': 'insights',
    '플랫폼': 'platform',
}

# 4. Other known categories
OTHER_MAP = {
    'bpp-perspective': 'insights',
    'bpp-faq': 'strategy',
    'B2B Marketing on Baidu': 'insights',
    'platform': 'platform',
    'search': 'search',
    'feed': 'feed',
    'strategy': 'strategy',
    'landing': 'landing',
    'insights': 'insights',
}

# 5. Root files slug-based mapping (for ✅ bpp-baidu-* files without proper category)
SLUG_MAP = {
    'baidu-ad-creation-flow-simplified': 'search',
    'baidu-ad-performance-diagnostic-tool': 'search',
    'baidu-ads-campaign-upgrade-2025': 'platform',
    'baidu-brand-info-account-level': 'search',
    'baidu-brand-zone-pre-review': 'search',
    'baidu-click-fraud-ipv4-blocking': 'search',
    'baidu-conflicting-negative-keywords': 'search',
    'baidu-conversion-tracking-dedup': 'search',
    'baidu-creative-url-retirement-migration': 'platform',
    'baidu-custom-form-retirement': 'platform',
    'baidu-feed-ads-history-operation-records-upgrade': 'feed',
    'baidu-inactive-keyword-cleanup-2025': 'search',
    'baidu-keyword-zero-impression-diagnosis': 'search',
    'baidu-landing-page-audit-rejection-reasons': 'landing',
    'baidu-landing-page-report': 'landing',
    'baidu-ocpc-skip-data-accumulation': 'search',
    'baidu-search-ads-1-1-desktop-images': 'search',
    'baidu-search-device-bid-coefficient-retirement': 'search',
    'faq-international-brands': 'strategy',
    'baidu-merchant-agent-human-handoff': 'platform',
}

def extract_frontmatter(content):
    """Return (fm_dict, fm_raw_text, fm_start, fm_end)"""
    if not content.startswith('---'):
        return {}, '', 0, 0
    end = content.find('---', 3)
    if end < 0:
        return {}, '', 0, 0
    fm_text = content[3:end]
    fm = {}
    for line in fm_text.strip().split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip().strip('"')
    return fm, fm_text, 3, end

def determine_category(fm, folder, filename):
    """Determine the correct official category for a file."""
    current_cat = fm.get('category', 'NONE')
    lang = fm.get('language', 'en')
    slug = fm.get('slug', filename.replace('.md', ''))
    
    # 1. If already an official EN category, keep it
    if current_cat in OFFICIAL:
        return current_cat, 'already_official'
    
    # 2. Chinese category mapping
    if current_cat in CN_MAP:
        return CN_MAP[current_cat], 'cn_mapped'
    
    # 3. Korean category mapping
    if current_cat in KO_MAP:
        return KO_MAP[current_cat], 'ko_mapped'
    
    # 4. Other known categories
    if current_cat in OTHER_MAP:
        return OTHER_MAP[current_cat], 'other_mapped'
    
    # 5. Folder-based mapping
    if folder in FOLDER_MAP:
        return FOLDER_MAP[folder], 'folder_mapped'
    
    # 6. Slug-based mapping (for ROOT files)
    # Extract base slug from filename
    base_slug = filename.replace('.md', '')
    for prefix in ['✅ bpp-', '✅ ']:
        if base_slug.startswith(prefix):
            base_slug = base_slug[len(prefix):]
    # Remove language suffix
    base_slug = re.sub(r'-(en|ja|ko)$', '', base_slug)
    
    if base_slug in SLUG_MAP:
        return SLUG_MAP[base_slug], 'slug_mapped'
    
    # 7. Summary files in subfolders - inherit from parent folder
    if 'summary-' in filename:
        if folder in FOLDER_MAP:
            return FOLDER_MAP[folder], 'summary_inherited'
    
    return None, 'UNKNOWN'

def update_frontmatter_category(content, new_cat):
    """Replace category value in frontmatter."""
    if not content.startswith('---'):
        return content
    end = content.find('---', 3)
    if end < 0:
        return content
    
    fm_text = content[3:end]
    # Replace category line
    new_fm = re.sub(
        r'^category:\s*.*$',
        f'category: {new_cat}',
        fm_text,
        flags=re.MULTILINE
    )
    
    # If no category line existed, add one after language or tags
    if 'category:' not in new_fm:
        lines = new_fm.strip().split('\n')
        insert_idx = 0
        for i, line in enumerate(lines):
            if line.startswith('language:') or line.startswith('tags:'):
                insert_idx = i + 1
                break
        lines.insert(insert_idx, f'category: {new_cat}')
        new_fm = '\n'.join(lines)
    
    return content[:3] + new_fm + content[end:]

# === MAIN ===
skip_dirs = {'charts', 'pages', 'templates', '.obsidian', 'OCR_Results'}
changes = []
skipped = []
unknowns = []

for root, dirs, files in os.walk(VAULT):
    dirs[:] = [d for d in dirs if d not in skip_dirs]
    
    for f in files:
        if not f.endswith('.md'):
            continue
        
        full = os.path.join(root, f)
        rel = os.path.relpath(full, VAULT)
        folder = rel.split(os.sep)[0] if os.sep in rel else 'ROOT'
        
        with open(full, 'r', encoding='utf-8') as fh:
            content = fh.read()
        
        fm, fm_text, _, _ = extract_frontmatter(content)
        current_cat = fm.get('category', 'NONE')
        
        new_cat, reason = determine_category(fm, folder, f)
        
        if new_cat is None:
            unknowns.append((rel, current_cat, reason))
            continue
        
        if new_cat == current_cat:
            skipped.append((rel, current_cat, 'no_change'))
            continue
        
        # Update
        new_content = update_frontmatter_category(content, new_cat)
        
        with open(full, 'w', encoding='utf-8') as fh:
            fh.write(new_content)
        
        changes.append((rel, current_cat, new_cat, reason))

# Report
print("=" * 100)
print("RECLASSIFICATION REPORT")
print("=" * 100)
print(f"\nFiles changed: {len(changes)}")
print(f"Files unchanged: {len(skipped)}")
print(f"Unknown/needs manual review: {len(unknowns)}")

if changes:
    print(f"\n{'─' * 100}")
    print("CHANGED FILES:")
    print(f"{'─' * 100}")
    print(f"{'File':70s} {'Old Category':20s} {'New Category':12s} {'Reason'}")
    print(f"{'─' * 70} {'─' * 20} {'─' * 12} {'─' * 15}")
    for rel, old, new, reason in sorted(changes):
        print(f"{rel[:69]:70s} {old:20s} {new:12s} {reason}")

if unknowns:
    print(f"\n{'─' * 100}")
    print("UNKNOWN (needs manual review):")
    print(f"{'─' * 100}")
    for rel, cat, reason in unknowns:
        print(f"  {rel}  [current: {cat}]  ({reason})")

# Summary by new category
print(f"\n{'─' * 100}")
print("SUMMARY BY NEW CATEGORY:")
print(f"{'─' * 100}")
from collections import Counter
cat_counts = Counter()
for rel, old, new, reason in changes:
    cat_counts[new] += 1
for rel, cat, reason in skipped:
    cat_counts[cat] += 1
for cat in OFFICIAL:
    print(f"  {cat:12s}: {cat_counts.get(cat, 0):3d} files")
