# -*- coding: utf-8 -*-
"""为三语 blog 列表页 (blog.html / ja/blog.html / ko/blog.html) 的卡片标题
批量补齐语义 emoji 前缀。

规范:
- emoji 只用于「列表卡片标题 blog-card-title」和「正文 H2」(blog-enhance),
  绝不进入 <title> / og:title / 文章 H1。
- 三语按 slug 共用同一 emoji, 数据源: blog_emoji_map.json (slug -> emoji)。
- 已有 leading emoji 会先剥离再加, 避免重复。

新增文章后:
1. 在 blog_emoji_map.json 里为新 slug 补一个 emoji;
2. 运行 python add_blog_list_emoji.py 即可给三语列表补齐。
或发布时用 blog_publish.py 的 --title-* 直接在标题前带 emoji。
"""
import re, json, os

BASE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE, 'blog_emoji_map.json'), encoding='utf-8') as f:
    EMOJI = json.load(f)

LEAD_EMOJI = re.compile(
    r'^[\U0001F000-\U0001FAFF\u2600-\u27BF\u2190-\u21FF\u2B00-\u2BFF\uFE0F\u200D]+\s*'
)

def process(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()
    count, missing = 0, []

    def repl(m):
        block = m.group(0)
        href_m = re.search(r'href="blog/([^"]+)"', block)
        if not href_m:
            return block
        slug = href_m.group(1)
        emo = EMOJI.get(slug)
        if not emo:
            missing.append(slug)
            return block
        def title_repl(tm):
            nonlocal count
            clean = LEAD_EMOJI.sub('', tm.group(1))
            count += 1
            return f'<h3 class="blog-card-title">{emo} {clean}</h3>'
        return re.sub(r'<h3 class="blog-card-title">(.*?)</h3>', title_repl, block, flags=re.S)

    html = re.sub(r'<article class="blog-card" data-category="[^"]+">.*?</article>',
                  repl, html, flags=re.S)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    return count, missing

if __name__ == '__main__':
    for lang, rel in [('EN', 'blog.html'), ('JA', 'ja/blog.html'), ('KO', 'ko/blog.html')]:
        c, miss = process(os.path.join(BASE, rel))
        print(f"{lang}: {c} titles updated; missing slugs: {len(miss)}")
        if miss:
            print("   MISSING (add to blog_emoji_map.json):", miss)
