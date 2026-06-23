from pathlib import Path
p = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\get_publish_args.py')
content = p.read_text(encoding='utf-8')
old = 'kv = re.match(r\'^(\\w+):\\s*"?([^"]*)"?$\', line)'
new = 'kv = re.match(r\'^(\\w+):\\s*"?(.*?)"?\\s*$\', line)'
content = content.replace(old, new)
p.write_text(content, encoding='utf-8')
print('Fixed regex')
