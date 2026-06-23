from pathlib import Path
p = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\gen_blog_html.py')
content = p.read_text(encoding='utf-8')

# Find and replace the entire build_table function
old_func_start = content.index('def build_table(rows):')
# Find the next def after build_table
next_def = content.index('\ndef ', old_func_start + 1)
old_func = content[old_func_start:next_def]

new_func = '''def build_table(rows):
    """Build HTML table from rows."""
    if len(rows) < 2:
        return ''
    html = '<table class="comparison-table">\\n'
    html += '  <thead><tr>'
    for cell in rows[0]:
        html += f'<th>{process_inline(cell)}</th>'
    html += '</tr></thead>\\n'
    html += '  <tbody>'
    for row in rows[1:]:
        html += '<tr>'
        for cell in row:
            html += f'<td>{process_inline(cell)}</td>'
        html += '</tr>'
    html += '</tbody></table>'
    return html

'''
content = content[:old_func_start] + new_func + content[next_def:]
p.write_text(content, encoding='utf-8')
print('Replaced build_table function')
