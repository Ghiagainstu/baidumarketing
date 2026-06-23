from pathlib import Path
p = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\gen_blog_html.py')
lines = p.read_text(encoding='utf-8').split('\n')

# Find the build_table function and fix it
new_lines = []
in_build_table = False
for i, line in enumerate(lines):
    if 'def build_table' in line:
        in_build_table = True
        new_lines.append(line)
        continue
    if in_build_table:
        if line.strip().startswith('html = '):
            # Replace the opening div with table
            new_lines.append('    html = \'<table class="comparison-table">\'')
            new_lines.append('    html += \'<thead><tr>\'')
            # Skip the next 2 lines (old html= and html +=)
            continue
        if 'for cell in rows[0]:' in line:
            new_lines.append(line)
            continue
        if "html += f'<th>" in line:
            new_lines.append(line)
            continue
        if "html += '</tr></thead>" in line:
            new_lines.append(line)
            new_lines.append("    html += '<tbody>'")
            continue
        if "html += '<tbody>'" in line:
            continue  # Skip old tbody line
        if '</tbody></table></div>' in line:
            new_lines.append("    html += '</tbody></table>'")
            in_build_table = False
            continue
    new_lines.append(line)

p.write_text('\n'.join(new_lines), encoding='utf-8')
print('Fixed build_table')
