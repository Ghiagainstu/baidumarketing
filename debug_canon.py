#!/usr/bin/env python3
# debug canonical
with open('ja/blog/baidu-ocpc-skip-data-accumulation.html', 'r', encoding='utf-8') as f:
    html = f.read()

slug = 'baidu-ocpc-skip-data-accumulation'
old_str = f'rel="canonical" href="https://www.baidumarketing.com/blog/{slug}"'
new_str = f'rel="canonical" href="https://www.baidumarketing.com/ja/blog/{slug}.html"'

print(f"Searching for: {repr(old_str)}")
print(f"Found: {old_str in html}")

if old_str not in html:
    # Find the canonical line
    for line in html.split('\n'):
        if 'canonical' in line:
            print(f"Actual line: {repr(line.strip())}")
            # Check character by character
            idx = line.find('href=')
            if idx != -1:
                href_part = line[idx:idx+100]
                print(f"href part: {repr(href_part)}")
            break
