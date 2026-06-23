from pathlib import Path
p = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\fix_article.py')
content = p.read_text(encoding='utf-8')

old = '    html = html.replace("{{DATE}}", date)'
new = '''    # Format date per language
    from datetime import datetime
    try:
        dt = datetime.strptime(date, '%Y-%m-%d')
        if lang == 'ja':
            date_display = f'{dt.year}年{dt.month}月{dt.day}日'
        elif lang == 'ko':
            date_display = f'{dt.year}년 {dt.month}월 {dt.day}일'
        else:
            date_display = dt.strftime('%b %d, %Y')
    except ValueError:
        date_display = date
    html = html.replace("{{DATE}}", date_display)'''

if old in content:
    content = content.replace(old, new)
    p.write_text(content, encoding='utf-8')
    print('Fixed date formatting in fix_article.py')
else:
    print('Pattern not found')
