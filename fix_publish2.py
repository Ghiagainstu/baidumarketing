from pathlib import Path
p = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\blog_publish.py')
content = p.read_text(encoding='utf-8')

# Find and replace the broken section
old = '''    after_last = content[grid_content_start + last_article_end + len("</article>"):]
    # Look for grid closing tag (</div> or </section>)
    grid_close_div = after_last.find("</div>")
    grid_close_section = after_last.find("</section>")
    if grid_close_div == -1 and grid_close_section == -1:
    if grid_close == -1:
        return False

    # Use whichever close tag was found
    if grid_close_div >= 0 and (grid_close_section < 0 or grid_close_div < grid_close_section):
        grid_close = grid_close_div
        grid_end = grid_content_start + last_article_end + len("</article>") + grid_close + len("</div>")
    else:
        grid_close = grid_close_section
        grid_end = grid_content_start + last_article_end + len("</article>") + grid_close + len("</section>")'''

new = '''    after_last = content[grid_content_start + last_article_end + len("</article>"):]
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

if old in content:
    content = content.replace(old, new)
    p.write_text(content, encoding='utf-8')
    print('Fixed blog_publish.py')
else:
    print('Pattern not found - trying alternative fix')
    # Just fix the broken if/if line
    content = content.replace(
        '    if grid_close_div == -1 and grid_close_section == -1:\n    if grid_close == -1:',
        '    if grid_close_div == -1 and grid_close_section == -1:\n        print("grid close not found")'
    )
    # Remove the orphan "return False" if it exists
    content = content.replace(
        '        print("grid close not found")\n        return False',
        '        print("grid close not found")\n        return False'
    )
    p.write_text(content, encoding='utf-8')
    print('Applied alternative fix')
