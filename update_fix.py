from pathlib import Path
p = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\fix_article.py')
content = p.read_text(encoding='utf-8')
# Add KO footer fix after the write_text line
old = '    output_path.write_text(html, encoding="utf-8")'
new = '''    # Fix KO footer if needed
    if lang == "ko":
        html = html.replace('Baidu PPC Pro. All rights reserved.', 'Baidu PPC Pro. \\ubb34\\ub2e8\\uc804\\uc7ac\\ub97c \\uae08\\uc9c0\\ud569\\ub2c8\\ub2e4.')
    output_path.write_text(html, encoding="utf-8")'''
content = content.replace(old, new)
p.write_text(content, encoding='utf-8')
print('Updated fix_article.py')
