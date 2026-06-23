from pathlib import Path
p = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\gen_blog_html.py')
lines = p.read_text(encoding='utf-8').split('\n')
# Line 146 (0-indexed 145) has the broken regex
# Replace it with a working version using chr(96) for backtick
lines[145] = "    text = re.sub(r'{}([^{}]+){}', r'<code>\\1</code>', text)".format(chr(96), chr(96))
p.write_text('\n'.join(lines), encoding='utf-8')
print('Fixed line 146')
