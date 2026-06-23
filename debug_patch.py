from pathlib import Path
p = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\fix_article.py')
content = p.read_text(encoding='utf-8')
old = '    html = html.replace("{{TITLE}}", title)'
new = '''    print(f"DEBUG: title=[{title}], has_placeholder={' + chr(123) + 'chr(123) + 'TITLE' + chr(125) + chr(125) + ' in html}")
    html = html.replace("{{TITLE}}", title)
    h1_check = re.search(r'<h1[^>]*>(.*?)</h1>', html)
    print(f"DEBUG: h1 after replace=[{h1_check.group(1) if h1_check else 'NONE'}]")'''
content = content.replace(old, new)
p.write_text(content, encoding='utf-8')
print('Added debug')
