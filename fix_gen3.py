from pathlib import Path
p = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\gen_blog_html.py')
lines = p.read_text(encoding='utf-8').split('\n')
bt = chr(96)
new_line = "    text = re.sub(r'" + bt + r"([^" + bt + r"]+)" + bt + r"', r'<code>\1</code>', text)"
lines[145] = new_line
p.write_text('\n'.join(lines), encoding='utf-8')
print('Fixed line 146:', new_line)
