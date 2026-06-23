from pathlib import Path
p = Path(r'C:\Users\HYE\WorkBuddy\20260411211839\blog_publish.py')
lines = p.read_text(encoding='utf-8').split('\n')

# Find the grid close logic and fix it
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # Fix the grid close detection
    if 'grid_close = after_last.find("</div>")' in line:
        # Replace with logic that handles both </div> and </section>
        new_lines.append('    # Look for grid closing tag (</div> or </section>)')
        new_lines.append('    grid_close_div = after_last.find("</div>")')
        new_lines.append('    grid_close_section = after_last.find("</section>")')
        new_lines.append('    if grid_close_div == -1 and grid_close_section == -1:')
        i += 1
        continue
    if 'print(f\u274c \u672a\u627e\u5230 grid \u5173\u95ed\u6807\u7b7e")' in line or '\u672a\u627e\u5230 grid' in line:
        # This is the error message line - skip it (we already handle it above)
        i += 1
        continue
    if 'grid_end = grid_content_start + last_article_end + len("</article>") + grid_close + len("</div>")' in line:
        new_lines.append('    # Use whichever close tag was found')
        new_lines.append('    if grid_close_div >= 0 and (grid_close_section < 0 or grid_close_div < grid_close_section):')
        new_lines.append('        grid_close = grid_close_div')
        new_lines.append('        grid_end = grid_content_start + last_article_end + len("</article>") + grid_close + len("</div>")')
        new_lines.append('    else:')
        new_lines.append('        grid_close = grid_close_section')
        new_lines.append('        grid_end = grid_content_start + last_article_end + len("</article>") + grid_close + len("</section>")')
        i += 1
        continue
    new_lines.append(line)
    i += 1

p.write_text('\n'.join(new_lines), encoding='utf-8')
print('Fixed blog_publish.py grid close logic')
