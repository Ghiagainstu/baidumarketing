from pathlib import Path
p = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\blog_publish.py')
content = p.read_text(encoding='utf-8')

# Replace the grid close detection section
old = '''    after_last = content[grid_content_start + last_article_end + len("</article>"):]
    # Look for grid closing tag (</div> or </section>)
    grid_close_div = after_last.find("</div>")
    grid_close_section = after_last.find("</section>")
    if grid_close_div == -1 and grid_close_section == -1:
        print("grid close not found")
        return False

    # Use whichever close tag was found
    if grid_close_div >= 0 and (grid_close_section < 0 or grid_close_div < grid_close_section):
        grid_close = grid_close_div
        grid_end = grid_content_start + last_article_end + len("</article>") + grid_close + len("</div>")
    else:
        grid_close = grid_close_section
        grid_end = grid_content_start + last_article_end + len("</article>") + grid_close + len("</section>")'''

new = '''    after_last = content[grid_content_start + last_article_end + len("</article>"):]
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

if old in content:
    content = content.replace(old, new)
    p.write_text(content, encoding='utf-8')
    print('Fixed blog_publish.py grid close logic (v3)')
else:
    print('Pattern not found')
