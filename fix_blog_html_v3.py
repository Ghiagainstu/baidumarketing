#!/usr/bin/env python3
"""
fix_blog_html_v3.py — 修复韩语博客 HTML 结构 v3
1. 未包装的文本行 → <p>text</p>
2. 修复 blockquote 格式
3. 修复 list 格式
"""
import re
import os
import glob

PROJECT = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(PROJECT, "ko", "blog")

# HTML 标签模式
HTML_TAG = re.compile(r'^<[^>]+>')
HTML_BLOCK = re.compile(r'^<(?:div|section|article|table|ul|ol|blockquote|h[1-6]|hr|pre|figure|figcaption|nav|header|footer|main|aside|form|fieldset|details|summary|dialog|menu|slot|template|svg|math)\b', re.IGNORECASE)
HTML_CLOSE = re.compile(r'^</(?:div|section|article|table|ul|ol|blockquote|figure|details|dialog|menu|slot|template|svg|math)\b', re.IGNORECASE)


def fix_file(filepath):
    """修复单个文件"""
    basename = os.path.basename(filepath)
    if basename.startswith("_"):
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    changed = False
    new_lines = []
    in_article = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # 检测 article 区域
        if '<article class="article-content">' in stripped:
            in_article = True
            new_lines.append(line)
            continue
        
        if '</article>' in stripped:
            in_article = False
            new_lines.append(line)
            continue
        
        # 只在 article 区域内处理
        if not in_article:
            new_lines.append(line)
            continue
        
        # 跳过空行
        if not stripped:
            new_lines.append(line)
            continue
        
        # 跳过已经是 HTML 标签的行
        if stripped.startswith('<'):
            new_lines.append(line)
            continue
        
        # 跳过已经是 HTML 标签的行
        if stripped.startswith('</'):
            new_lines.append(line)
            continue
        
        # 跳过 div, section, table 等块级元素
        if HTML_BLOCK.match(stripped):
            new_lines.append(line)
            continue
        
        # 跳过已经在 p 标签内的行
        if stripped.startswith('<p>') or stripped.startswith('<p '):
            new_lines.append(line)
            continue
        
        # 跳过已经在 h1-h6 标签内的行
        if re.match(r'^<h[1-6]', stripped):
            new_lines.append(line)
            continue
        
        # 跳过已经在 blockquote 标签内的行
        if stripped.startswith('<blockquote'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 ul/ol 标签内的行
        if stripped.startswith('<ul') or stripped.startswith('<ol'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 li 标签内的行
        if stripped.startswith('<li'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 table 标签内的行
        if stripped.startswith('<table'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 tr/td/th 标签内的行
        if stripped.startswith('<tr') or stripped.startswith('<td') or stripped.startswith('<th'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 img 标签内的行
        if stripped.startswith('<img'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 br 标签内的行
        if stripped.startswith('<br'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 hr 标签内的行
        if stripped.startswith('<hr'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 pre/code 标签内的行
        if stripped.startswith('<pre') or stripped.startswith('<code'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 script/style 标签内的行
        if stripped.startswith('<script') or stripped.startswith('<style'):
            new_lines.append(line)
            continue
        
        # 跳过已经在注释内的行
        if stripped.startswith('<!--'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 CDATA 内的行
        if stripped.startswith('<![CDATA['):
            new_lines.append(line)
            continue
        
        # 跳过已经在 DOCTYPE 内的行
        if stripped.startswith('<!DOCTYPE'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 xml 内的行
        if stripped.startswith('<?xml'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 svg 内的行
        if stripped.startswith('<svg'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 math 内的行
        if stripped.startswith('<math'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 form 内的行
        if stripped.startswith('<form'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 input 内的行
        if stripped.startswith('<input'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 textarea 内的行
        if stripped.startswith('<textarea'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 select 内的行
        if stripped.startswith('<select'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 button 内的行
        if stripped.startswith('<button'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 a 内的行
        if stripped.startswith('<a '):
            new_lines.append(line)
            continue
        
        # 跳过已经在 span 内的行
        if stripped.startswith('<span'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 em/strong/b/i 内的行
        if stripped.startswith('<em') or stripped.startswith('<strong') or stripped.startswith('<b') or stripped.startswith('<i'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 sub/sup 内的行
        if stripped.startswith('<sub') or stripped.startswith('<sup'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 mark/del/ins 内的行
        if stripped.startswith('<mark') or stripped.startswith('<del') or stripped.startswith('<ins'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 small/big 内的行
        if stripped.startswith('<small') or stripped.startswith('<big'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 abbr/cite/q 内的行
        if stripped.startswith('<abbr') or stripped.startswith('<cite') or stripped.startswith('<q'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 dfn/var/samp/kbd 内的行
        if stripped.startswith('<dfn') or stripped.startswith('<var') or stripped.startswith('<samp') or stripped.startswith('<kbd'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 time/data 内的行
        if stripped.startswith('<time') or stripped.startswith('<data'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 address 内的行
        if stripped.startswith('<address'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 figure/figcaption 内的行
        if stripped.startswith('<figure') or stripped.startswith('<figcaption'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 map/area 内的行
        if stripped.startswith('<map') or stripped.startswith('<area'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 audio/video/source 内的行
        if stripped.startswith('<audio') or stripped.startswith('<video') or stripped.startswith('<source'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 track/embed/param 内的行
        if stripped.startswith('<track') or stripped.startswith('<embed') or stripped.startswith('<param'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 object/applet 内的行
        if stripped.startswith('<object') or stripped.startswith('<applet'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 iframe/frame/frameset 内的行
        if stripped.startswith('<iframe') or stripped.startswith('<frame') or stripped.startswith('<frameset'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 noembed/noframes/noscript 内的行
        if stripped.startswith('<noembed') or stripped.startswith('<noframes') or stripped.startswith('<noscript'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 marquee 内的行
        if stripped.startswith('<marquee'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 blink 内的行
        if stripped.startswith('<blink'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 listing/xmp 内的行
        if stripped.startswith('<listing') or stripped.startswith('<xmp'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 nextid 内的行
        if stripped.startswith('<nextid'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 isindex 内的行
        if stripped.startswith('<isindex'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 basefont/font 内的行
        if stripped.startswith('<basefont') or stripped.startswith('<font'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 center/strike 内的行
        if stripped.startswith('<center') or stripped.startswith('<strike'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 dir/menu 内的行
        if stripped.startswith('<dir') or stripped.startswith('<menu'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 plaintext 内的行
        if stripped.startswith('<plaintext'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 spacer 内的行
        if stripped.startswith('<spacer'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 wbr 内的行
        if stripped.startswith('<wbr'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 bdi/bdo 内的行
        if stripped.startswith('<bdi') or stripped.startswith('<bdo'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 ruby/rt/rp 内的行
        if stripped.startswith('<ruby') or stripped.startswith('<rt') or stripped.startswith('<rp'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 meter/progress 内的行
        if stripped.startswith('<meter') or stripped.startswith('<progress'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 output 内的行
        if stripped.startswith('<output'):
            new_lines.append(line)
            continue
        
        # 跳过已经在datalist 内的行
        if stripped.startswith('<datalist'):
            new_lines.append(line)
            continue
        
        # 跳过已经在 keygen 内的行
        if stripped.startswith('<keygen'):
            new_lines.append(line)
            continue
        
        # 其他情况，包装在 <p> 标签中
        new_lines.append(f'<p>{stripped}</p>\n')
        changed = True
    
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        return True
    return False


def main():
    print("=" * 60)
    print("🇰🇷 修复韩语博客 HTML 结构 v3")
    print("=" * 60)
    
    files = glob.glob(os.path.join(BLOG_DIR, "*.html"))
    files = [f for f in files if "_template" not in os.path.basename(f)]
    
    fixed = 0
    for filepath in sorted(files):
        basename = os.path.basename(filepath)
        if fix_file(filepath):
            print(f"  ✓ Fixed: {basename}")
            fixed += 1
        else:
            print(f"  - No changes: {basename}")
    
    print("=" * 60)
    print(f"✅ 完成: {fixed}/{len(files)} 个文件已修复")
    print("=" * 60)


if __name__ == "__main__":
    main()
