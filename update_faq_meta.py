#!/usr/bin/env python3
"""
update_faq_meta.py - 更新 ja/faq.html 的 meta 信息为日文
"""

import re

def update_meta(html_file, md_file):
    """更新 HTML 的 meta 信息"""
    # 1. 从 MD 提取 meta 信息
    print("1. 从 MD 提取 meta 信息...")
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # 提取 Title
    title_match = re.search(r'### Title\n```\n(.+?)\n```', md_content)
    title = title_match.group(1).strip() if title_match else None
    
    # 提取 Meta Description
    desc_match = re.search(r'### Meta Description\n```\n(.+?)\n```', md_content, re.DOTALL)
    meta_desc = desc_match.group(1).strip() if desc_match else None
    
    # 提取 OG Title
    og_title_match = re.search(r'### OG Title\n```\n(.+?)\n```', md_content)
    og_title = og_title_match.group(1).strip() if og_title_match else None
    
    # 提取 OG Description
    og_desc_match = re.search(r'### OG Description\n```\n(.+?)\n```', md_content, re.DOTALL)
    og_desc = og_desc_match.group(1).strip() if og_desc_match else None
    
    # 提取 Twitter Title
    tw_title_match = re.search(r'### Twitter Title\n```\n(.+?)\n```', md_content)
    tw_title = tw_title_match.group(1).strip() if tw_title_match else None
    
    # 提取 Twitter Description
    tw_desc_match = re.search(r'### Twitter Description\n```\n(.+?)\n```', md_content, re.DOTALL)
    tw_desc = tw_desc_match.group(1).strip() if tw_desc_match else None
    
    print(f"   Title: {title[:50] if title else '未找到'}...")
    print(f"   Meta Description: {meta_desc[:50] if meta_desc else '未找到'}...")
    print(f"   OG Title: {og_title[:50] if og_title else '未找到'}...")
    print(f"   OG Description: {og_desc[:50] if og_desc else '未找到'}...")
    
    # 2. 读取 HTML
    print("\n2. 读取 HTML 文件...")
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    new_html = html
    
    # 3. 替换 <title>
    if title:
        new_html = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', new_html)
        print("   已替换 <title>")
    
    # 4. 替换 <meta name="description">
    if meta_desc:
        new_html = re.sub(r'<meta name="description" content=".*?" />', f'<meta name="description" content="{meta_desc}" />', new_html)
        print("   已替换 meta description")
    
    # 5. 替换 OG tags
    if og_title:
        new_html = re.sub(r'<meta property="og:title" content=".*?" />', f'<meta property="og:title" content="{og_title}" />', new_html)
        print("   已替换 og:title")
    
    if og_desc:
        new_html = re.sub(r'<meta property="og:description" content=".*?" />', f'<meta property="og:description" content="{og_desc}" />', new_html)
        print("   已替换 og:description")
    
    # 6. 替换 Twitter tags
    if tw_title:
        new_html = re.sub(r'<meta name="twitter:title" content=".*?" />', f'<meta name="twitter:title" content="{tw_title}" />', new_html)
        print("   已替换 twitter:title")
    
    if tw_desc:
        new_html = re.sub(r'<meta name="twitter:description" content=".*?" />', f'<meta name="twitter:description" content="{tw_desc}" />', new_html)
        print("   已替换 twitter:description")
    
    # 7. 写入文件
    print("\n3. 写入文件...")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_html)
    
    print(f"\n完成！{html_file} 已更新")


if __name__ == '__main__':
    md_file = 'ja/faq-ja.md'
    html_file = 'ja/faq.html'
    update_meta(html_file, md_file)
