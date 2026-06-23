from pathlib import Path
p = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\gen_blog_html.py')
lines = p.read_text(encoding='utf-8').split('\n')

# Find the md_to_html function and add logic to skip first # heading
new_lines = []
skip_first_h1 = False
for i, line in enumerate(lines):
    if 'def md_to_html(md_text):' in line:
        skip_first_h1 = True
        new_lines.append(line)
        continue
    if skip_first_h1 and 'html_parts = []' in line:
        new_lines.append(line)
        new_lines.append('    first_h1_skipped = False')
        continue
    if skip_first_h1 and "stripped.startswith(\'# \')" not in line and 'if stripped.startswith(' in line and "stripped.startswith('## ')" in line:
        # Found the h2 check, add h1 skip before it
        new_lines.append("        # H1 (skip first occurrence - already in page title)")
        new_lines.append("        if stripped.startswith('# ') and not first_h1_skipped:")
        new_lines.append("            first_h1_skipped = True")
        new_lines.append("            continue")
        new_lines.append("        if stripped.startswith('# '):")
        new_lines.append("            html_parts.append(f'<h2>{process_inline(stripped[2:])}</h2>')")
        new_lines.append("            continue")
    new_lines.append(line)

p.write_text('\n'.join(new_lines), encoding='utf-8')
print('Fixed h1 skip')
