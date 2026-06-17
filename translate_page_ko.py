#!/usr/bin/env python3
"""
translate_page_ko.py — 提取页面所有英文文本，供一次性翻译
用法：python translate_page_ko.py <slug>
输出：extracted_texts_<slug>.txt（带行号和上下文）
"""
import re
import os
import sys

PROJECT = os.path.dirname(os.path.abspath(__file__))

def extract_texts(html):
    """提取所有需要翻译的英文文本"""
    texts = []
    seen = set()
    
    # 移除 JSON-LD 和 script 标签内容
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    
    # 移除 style 标签内容
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    
    # 移除注释
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    
    # 匹配 >text< 格式（标签之间的文本）
    pattern = r'>([^<]+)<'
    for m in re.finditer(pattern, html):
        text = m.group(1).strip()
        # 跳过：空文本、纯数字、纯符号、CSS/JS、品牌名
        if not text or len(text) < 2:
            continue
        if re.match(r'^[\d\s\.\,\%\+\-\*\/\=\(\)\[\]\{\}\$\@\#\!\?\:\;]+$', text):
            continue
        if any(x in text for x in ['var ', 'function ', 'const ', 'let ', 'document.', 'window.', 'console.', 'return ', 'if (', 'else {', '===', '!==', '&&', '||', '{', '}']):
            continue
        if text in seen:
            continue
        seen.add(text)
        texts.append(text)
    
    return texts


def main():
    if len(sys.argv) < 2:
        print("用法: python translate_page_ko.py <slug>")
        sys.exit(1)
    
    slug = sys.argv[1]
    en_path = os.path.join(PROJECT, f"{slug}.html")
    
    if not os.path.exists(en_path):
        print(f"✗ 文件不存在: {en_path}")
        sys.exit(1)
    
    with open(en_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    texts = extract_texts(html)
    
    # 输出到文件
    output_path = os.path.join(PROJECT, f"extracted_texts_{slug}.txt")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"# {slug} 页面英文文本提取\n")
        f.write(f"# 共 {len(texts)} 条\n")
        f.write(f"# 格式: 序号|原文\n\n")
        for i, text in enumerate(texts, 1):
            f.write(f"{i}|{text}\n")
    
    print(f"✅ 提取完成: {len(texts)} 条文本")
    print(f"📄 输出文件: {output_path}")
    print(f"\n下一步:")
    print(f"1. 打开 {output_path}")
    print(f"2. 将所有英文文本翻译为韩语")
    print(f"3. 运行 apply_translations_ko.py 应用翻译")


if __name__ == "__main__":
    main()
