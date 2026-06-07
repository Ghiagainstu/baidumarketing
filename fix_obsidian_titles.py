import re, os, glob
from datetime import datetime

obsidian_dir = 'E:/Obsidian/Baidu/'
# Find all .md files in subdirectories (blog files)
patterns = [
    obsidian_dir + '01-Market-Insights/*.md',
    obsidian_dir + '02-Platform/*.md',
    obsidian_dir + '03-Search-Ads/*.md',
    obsidian_dir + '04-Feed-Ads/*.md',
    obsidian_dir + '05-Strategy/*.md',
    obsidian_dir + '06-Landing-Page/*.md',
    obsidian_dir + '07-Pricing-Models/*.md',
    obsidian_dir + '08-Baidu-Basics/*.md',
    obsidian_dir + '09-China-Search-Landscape/*.md',
]

files = []
for p in patterns:
    files.extend(glob.glob(p))

fixed = 0
for f in sorted(files):
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    basename = os.path.basename(f)
    
    # Extract date from frontmatter or bold field
    date_match = re.search(r'^date:\s*(\d{4}-\d{2}-\d{2})', content, re.MULTILINE)
    if not date_match:
        date_match = re.search(r'\*\*Date\*\*:\s*(\d{4}-\d{2}-\d{2})', content)
    
    if not date_match:
        continue
    
    # Extract H1 title (first # line)
    h1_match = re.search(r'^(# .+)$', content, re.MULTILINE)
    if not h1_match:
        continue
    
    date_str = date_match.group(1)
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    day = str(dt.day)
    date_prefix = f'{dt.strftime("%b")} {day}, {dt.year}'
    
    title_line = h1_match.group(1)
    title_text = title_line[2:].strip()  # Remove '# '
    
    # Check if already has date prefix
    if re.match(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+', title_text):
        continue
    
    # Add date prefix
    new_title = f'# {date_prefix} — {title_text}'
    new_content = content.replace(title_line, new_title, 1)
    
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(new_content)
    
    fixed += 1
    print(f'Fixed: {basename}')
    print(f'  -> {new_title[:80]}')

print(f'\nTotal fixed: {fixed}')
