from pathlib import Path
p = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\gen_blog_html.py')
content = p.read_text(encoding='utf-8')

old = """    # Build date string
    date_str = date  # Will be like 2026-06-23"""

new = """    # Build date string per language
    from datetime import datetime
    try:
        dt = datetime.strptime(date, '%Y-%m-%d')
        if lang == 'ja':
            date_str = f'{dt.year}年{dt.month}月{dt.day}日'
        elif lang == 'ko':
            date_str = f'{dt.year}년 {dt.month}월 {dt.day}일'
        else:
            date_str = dt.strftime('%b %d, %Y')
    except ValueError:
        date_str = date"""

if old in content:
    content = content.replace(old, new)
    p.write_text(content, encoding='utf-8')
    print('Fixed date formatting')
else:
    print('Pattern not found')
