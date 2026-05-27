#!/usr/bin/env python3
"""为缺失 GA4 代码的 HTML 文件插入 G-TCGE7NJT7H"""
import os
import re

PROJECT_DIR = r"c:\Users\HYE\WorkBuddy\20260411211839"
GA4_CODE = """  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-TCGE7NJT7H"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-TCGE7NJT7H');
  </script>
"""

def find_html_files(root):
    """找出所有 HTML 文件"""
    html_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # 跳过 .workbuddy 和 node_modules
        dirnames[:] = [d for d in dirnames if d not in ('.workbuddy', 'node_modules', '.git')]
        for f in filenames:
            if f.endswith('.html'):
                html_files.append(os.path.join(dirpath, f))
    return html_files

def has_ga4(filepath):
    """检查文件是否已有 GA4 代码"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return 'G-TCGE7NJT7H' in content

def insert_ga4(filepath):
    """在 <head> 后插入 GA4 代码"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 在 <head> 或 <head> 后紧跟换行处插入
    # 匹配 <head> 后面紧跟换行，然后插入 GA4 代码
    pattern = r'(<head>\s*\n)'
    replacement = r'\1' + GA4_CODE
    
    new_content = re.sub(pattern, replacement, content, count=1)
    
    if new_content == content:
        # 尝试另一种格式：<head> 在同一行
        pattern2 = r'(<head>)'
        replacement2 = r'\1\n' + GA4_CODE
        new_content = re.sub(pattern2, replacement2, content, count=1)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    html_files = find_html_files(PROJECT_DIR)
    print(f"扫描到 {len(html_files)} 个 HTML 文件")
    
    missing = [f for f in html_files if not has_ga4(f)]
    print(f"缺失 GA4 代码：{len(missing)} 个文件")
    
    success = 0
    failed = 0
    for f in missing:
        relpath = os.path.relpath(f, PROJECT_DIR)
        try:
            if insert_ga4(f):
                print(f"  ✓ {relpath}")
                success += 1
            else:
                print(f"  ✗ {relpath} (插入失败)")
                failed += 1
        except Exception as e:
            print(f"  ✗ {relpath} (错误: {e})")
            failed += 1
    
    print(f"\n完成：成功 {success}，失败 {failed}")

if __name__ == '__main__':
    main()
