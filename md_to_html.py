"""
md_to_html.py — 标准化 Obsidian MD → HTML 转换函数
用于 bpp-blog-html skill，禁止手动拼接 HTML。

使用方式:
    from md_to_html import md_to_html, md_to_full_html
    body_html = md_to_html(md_text)        # 只转换正文（article-content 内的内容）
    full_html = md_to_full_html(md_text)   # 包含 article-hero + article-section 结构
"""
import re


def md_to_html(md_text):
    """
    Convert Markdown body text to HTML content for article-content div.
    Input: MD text WITHOUT frontmatter and WITHOUT H1 title.
    Output: HTML string for insertion into <article class="article-content">
    """
    lines = md_text.strip().split('\n')
    result = []
    i = 0
    in_ul = False
    in_ol = False

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            result.append('</ul>')
            in_ul = False
        if in_ol:
            result.append('</ol>')
            in_ol = False

    def inline(text):
        """Apply inline markdown formatting."""
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        return text

    def is_html_block(line):
        """Check if line starts an HTML block."""
        return bool(re.match(r'\s*<(div|table|blockquote|details|figure|section|article)', line.strip()))

    def read_html_block(start_idx):
        """Read a multi-line HTML block and return (lines, next_index)."""
        block = [lines[start_idx]]
        depth = 0
        for tag in ['<div', '<table', '<thead', '<tbody', '<tr', '<blockquote', '<details', '<figure', '<section']:
            if tag in lines[start_idx]:
                depth += 1
        for closing in ['</div>', '</table>', '</blockquote>', '</details>', '</figure>', '</section>']:
            if closing in lines[start_idx]:
                depth -= 1

        idx = start_idx + 1
        while depth > 0 and idx < len(lines):
            block.append(lines[idx])
            for tag in ['<div', '<table', '<thead', '<tbody', '<tr', '<blockquote', '<details', '<figure', '<section']:
                if tag in lines[idx]:
                    depth += 1
            for closing in ['</div>', '</table>', '</blockquote>', '</details>', '</figure>', '</section>']:
                if closing in lines[idx]:
                    depth -= 1
            idx += 1

        return '\n'.join(f'      {bl}' for bl in block), idx

    while i < len(lines):
        line = lines[i]

        # Empty line
        if not line.strip():
            i += 1
            continue

        # H2
        if line.startswith('## '):
            close_lists()
            result.append(f'    <h2>{inline(line[3:])}</h2>')
            i += 1
            continue

        # H3
        if line.startswith('### '):
            close_lists()
            result.append(f'    <h3>{inline(line[4:])}</h3>')
            i += 1
            continue

        # H4
        if line.startswith('#### '):
            close_lists()
            result.append(f'    <h4>{inline(line[5:])}</h4>')
            i += 1
            continue

        # Markdown table (| col | col |)
        if line.strip().startswith('|') and '|' in line.strip()[1:]:
            close_lists()
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i].strip())
                i += 1
            # Parse table
            if len(table_lines) >= 2:
                # First row = header
                headers = [c.strip() for c in table_lines[0].split('|')[1:-1]]
                # Skip separator row (|---|---|)
                data_start = 1
                if len(table_lines) > 1 and re.match(r'^[\s|:-]+$', table_lines[1]):
                    data_start = 2
                result.append('    <table class="comparison-table">')
                result.append('      <thead><tr>' + ''.join(f'<th>{inline(h)}</th>' for h in headers) + '</tr></thead>')
                result.append('      <tbody>')
                for row_line in table_lines[data_start:]:
                    cells = [c.strip() for c in row_line.split('|')[1:-1]]
                    result.append('        <tr>' + ''.join(f'<td>{inline(c)}</td>' for c in cells) + '</tr>')
                result.append('      </tbody>')
                result.append('    </table>')
            continue

        # Horizontal rule
        if line.strip() == '---':
            close_lists()
            i += 1
            continue

        # Callout block (dedicated parser for reliability)
        if re.match(r'\s*<div class="callout', line.strip()):
            close_lists()
            block_lines = [line.strip()]
            depth = 1
            i += 1
            while depth > 0 and i < len(lines):
                l = lines[i].strip()
                block_lines.append(l)
                depth += l.count('<div') - l.count('</div>')
                i += 1
            result.append('    ' + '\n    '.join(block_lines))
            continue

        # Comparison table (dedicated parser)
        if re.match(r'\s*<table class="comparison-table"', line.strip()):
            close_lists()
            block_lines = [line.strip()]
            depth = 1
            i += 1
            while depth > 0 and i < len(lines):
                l = lines[i].strip()
                block_lines.append(l)
                depth += l.count('<table') - l.count('</table>')
                i += 1
            result.append('    ' + '\n    '.join(block_lines))
            continue

        # Stats grid (dedicated parser)
        if re.match(r'\s*<div class="stats-grid"', line.strip()):
            close_lists()
            block_lines = [line.strip()]
            depth = 1
            i += 1
            while depth > 0 and i < len(lines):
                l = lines[i].strip()
                block_lines.append(l)
                depth += l.count('<div') - l.count('</div>')
                i += 1
            result.append('    ' + '\n    '.join(block_lines))
            continue

        # Takeaway box (dedicated parser)
        if re.match(r'\s*<div class="takeaway', line.strip()):
            close_lists()
            block_lines = [line.strip()]
            depth = 1
            i += 1
            while depth > 0 and i < len(lines):
                l = lines[i].strip()
                block_lines.append(l)
                depth += l.count('<div') - l.count('</div>')
                i += 1
            result.append('    ' + '\n    '.join(block_lines))
            continue

        # Generic HTML block (fallback)
        if is_html_block(line):
            close_lists()
            block_html, i = read_html_block(i)
            result.append(block_html)
            continue

        # Pass through standalone HTML tags
        if line.strip().startswith('<') and line.strip().endswith('>'):
            close_lists()
            result.append(f'      {line.strip()}')
            i += 1
            continue

        # Unordered list
        if line.strip().startswith('- '):
            if not in_ul:
                close_lists()
                result.append('    <ul>')
                in_ul = True
            item = inline(line.strip()[2:])
            result.append(f'      <li>{item}</li>')
            i += 1
            continue

        # Ordered list
        if re.match(r'^\d+\.\s', line.strip()):
            if not in_ol:
                close_lists()
                result.append('    <ol>')
                in_ol = True
            item = inline(re.sub(r'^\d+\.\s', '', line.strip()))
            result.append(f'      <li>{item}</li>')
            i += 1
            continue

        # Blockquote (callout)
        if line.strip().startswith('> '):
            close_lists()
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('> '):
                quote_lines.append(lines[i].strip()[2:])
                i += 1
            quote_text = ' '.join(quote_lines)
            quote_text = inline(quote_text)
            result.append(f'    <blockquote><p>{quote_text}</p></blockquote>')
            continue

        # Paragraph
        close_lists()
        para_lines = []
        while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('#') and not lines[i].strip().startswith('<') and not lines[i].strip().startswith('- ') and not re.match(r'^\d+\.\s', lines[i].strip()) and not lines[i].strip() == '---' and not lines[i].strip().startswith('> '):
            para_lines.append(lines[i])
            i += 1

        if para_lines:
            text = ' '.join(p.strip() for p in para_lines)
            text = inline(text)
            result.append(f'    <p>{text}</p>')
            continue

        i += 1

    close_lists()
    return '\n\n'.join(result)


def post_process(html):
    """
    Final safety net: convert any remaining raw Markdown to HTML.
    Call AFTER md_to_html or md_to_full_html to catch edge cases.
    """
    # Raw ## / ### that slipped through
    html = re.sub(r'^## ([^<].*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### ([^<].*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### ([^<].*?)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    # Raw **bold** / *italic* / [link](url) / `code`
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', html)
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
    return html


def md_to_full_html(md_text, date_str, read_time, category, author, cta_title, cta_text, cta_btn, cta_link, lang='en', wrap_main=True):
    """
    Convert full MD text (with frontmatter) to complete article HTML structure.
    Returns the full <section class="article-hero"> + <main>...</main> block.
    """
    # Extract body (skip frontmatter + H1)
    body = md_text
    if body.startswith('---'):
        fm_end = body.find('---', 3)
        if fm_end > 0:
            body = body[fm_end + 3:].strip()

    # Extract title from H1
    title = ''
    if body.startswith('# '):
        nl = body.find('\n')
        title = body[2:nl] if nl > 0 else body[2:]
        body = body[nl + 1:].strip() if nl > 0 else ''

    # Breadcrumb
    if lang == 'ja':
        breadcrumb = '<a href="/ja">ホーム</a> / <a href="/ja/blog">ブログ</a>'
        date_label = date_str
        cat_label = category
    elif lang == 'ko':
        breadcrumb = '<a href="/ko">홈</a> / <a href="/ko/blog">블로그</a>'
        date_label = date_str
        cat_label = category
    else:
        breadcrumb = '<a href="/">Home</a> / <a href="/blog">Blog</a>'
        date_label = date_str
        cat_label = category

    body_html = post_process(md_to_html(body))

    return f'''  <section class="article-hero">
    <div class="container">
      <div class="breadcrumb">{breadcrumb}</div>
      <h1 class="article-title">{title}</h1>
      <div class="article-meta">
        <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg> {date_label}</span>
        <span><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> {read_time}</span>
        <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/></svg> {cat_label}</span>
        <span><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg> By {author}</span>
      </div>
    </div>
  </section>

  {'<main>' if wrap_main else ''}
  <section class="article-section">
    <div class="container">
      <article class="article-content">

{body_html}

      </article>
    </div>
  </section>

  <div class="cta-box">
    <div class="container">
      <h3>{cta_title}</h3>
      <p>{cta_text}</p>
      <a href="{cta_link}" class="btn-primary">{cta_btn}</a>
    </div>
  </div>
  {'</main>' if wrap_main else ''}'''
