from pathlib import Path
p = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\blog_publish.py')
content = p.read_text(encoding='utf-8')

old = '''    after_last = content[grid_content_start + last_article_end + len("</article>"):]
    # Look for grid closing tag - try </div>, </section>, </footer> in order
    grid_close = -1
    grid_close_len = 0
    for tag in ["</div>", "</section>", "</footer>"]:
        idx = after_last.find(tag)
        if idx >= 0:
            grid_close = idx
            grid_close_len = len(tag)
            break
    if grid_close == -1:
        print("grid close not found")
        return False
    grid_end = grid_content_start + last_article_end + len("</article>") + grid_close + grid_close_len'''

new = '''    after_last = content[grid_content_start + last_article_end + len("</article>"):]
    # Find the boundary after the last article - look for </div>, </section>, </footer>
    boundary = -1
    for tag in ["</div>", "</section>", "</footer>"]:
        idx = after_last.find(tag)
        if idx >= 0:
            # boundary is the START of the close tag (we want to keep it)
            boundary = idx
            break
    if boundary == -1:
        print("grid close not found")
        return False
    # grid_end points to the start of the close tag - we keep the close tag and everything after
    grid_end = grid_content_start + last_article_end + len("</article>") + boundary'''

if old in content:
    content = content.replace(old, new)
    p.write_text(content, encoding='utf-8')
    print('Fixed blog_publish.py (v4)')
else:
    print('Pattern not found')
