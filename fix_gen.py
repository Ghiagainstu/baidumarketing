from pathlib import Path
p = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\gen_blog_html.py')
content = p.read_text(encoding='utf-8')
# Find and fix the broken inline code regex
# The issue is the backtick character got corrupted
lines = content.split('\n')
new_lines = []
for line in lines:
    if 'process_inline' in line and 're.sub' in line and 'code>' in line:
        # This is the broken line - replace it
        new_lines.append("    text = re.sub(r'\\x60([^\\x60]+)\\x60', r'<code>\\1</code>', text)")
    else:
        new_lines.append(line)
content = '\n'.join(new_lines)
p.write_text(content, encoding='utf-8')
print('Fixed inline code regex')
