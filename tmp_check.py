from pathlib import Path
content = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\blog.html').read_text(encoding='utf-8')
marker = '<div class="blog-grid" id="blogGrid">'
start = content.find(marker)
# Find the next </section> or </div> that closes the grid
after_grid = content[start+1000:]
# Look for the first non-article tag
lines = after_grid.split('\n')
for i, line in enumerate(lines[:5]):
    print(f'Line {i}: {repr(line[:100])}')
