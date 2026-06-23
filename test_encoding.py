import sys
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path
p = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\ja\blog\_template-ja.html')
html = p.read_text(encoding='utf-8')
print('Has サービス:', 'サービス' in html)
print('Has 料金:', '料金' in html)
print('Has 日本語:', '日本語' in html)

# Test write
out = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\ja\blog\_test_encoding.html')
out.write_text(html, encoding='utf-8')

# Read back
html2 = out.read_text(encoding='utf-8')
print('Roundtrip サービス:', 'サービス' in html2)
print('Roundtrip 日本語:', '日本語' in html2)
out.unlink()
