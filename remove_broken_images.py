#!/usr/bin/env python3
"""
删除博客中引用不存在图片的 <img> 标签
- 检查 <img src="..."> 中的图片文件是否存在
- 如果图片不存在，删除整个 <img> 标签
"""
import os
import re
from pathlib import Path

# 配置
BLOG_DIR = r"C:\Users\HYE\WorkBuddy\20260411211839\blog"
ASSETS_DIR = r"C:\Users\HYE\WorkBuddy\20260411211839\assets"

def check_image_exists(src):
    """
    检查图片文件是否存在
    - 如果是 http/https URL，跳过（不检查远程图片）
    - 如果是相对路径或绝对路径，检查本地文件
    """
    if src.startswith('http://') or src.startswith('https://'):
        # 远程图片，跳过检查
        return True
    
    # 提取文件名
    filename = os.path.basename(src)
    local_path = os.path.join(ASSETS_DIR, filename)
    
    return os.path.exists(local_path)

def remove_broken_images(html_content):
    """
    移除引用不存在图片的 <img> 标签
    返回: (修改后的内容, 删除的img标签列表)
    """
    img_pattern = re.compile(r'<img[^>]*src=["\']([^"\']+)["\'][^>]*>', re.IGNORECASE)
    
    broken_imgs = []
    new_content = html_content
    
    # 找到所有 <img> 标签
    for match in img_pattern.finditer(html_content):
        full_tag = match.group(0)
        src = match.group(1)
        
        # 检查图片是否存在
        if not check_image_exists(src):
            broken_imgs.append((src, full_tag))
            # 删除这个 <img> 标签
            new_content = new_content.replace(full_tag, '')
    
    return new_content, broken_imgs

def process_blog_file(filepath):
    """处理单个博客文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有 <img> 标签
        if '<img' not in content:
            return None, []
        
        # 移除损坏的图片
        new_content, broken_imgs = remove_broken_images(content)
        
        # 如果有删除的图片，写回文件
        if broken_imgs:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True, broken_imgs
        
        return False, []
        
    except Exception as e:
        return None, [str(e)]

def main():
    print("=" * 60)
    print("删除博客中引用不存在图片的 <img> 标签")
    print("=" * 60)
    
    # 获取所有博客文件
    blog_files = list(Path(BLOG_DIR).glob("*.html"))
    
    print(f"\n扫描到 {len(blog_files)} 个博客文件")
    print(f"资产目录: {ASSETS_DIR}")
    
    # 检查资产目录中有哪些文件
    assets_files = []
    if os.path.exists(ASSETS_DIR):
        assets_files = os.listdir(ASSETS_DIR)
    print(f"资产目录中有 {len(assets_files)} 个文件")
    
    print("\n开始处理...")
    
    total_files_modified = 0
    total_imgs_removed = 0
    all_broken_imgs = []
    
    for i, filepath in enumerate(blog_files, 1):
        modified, broken_imgs = process_blog_file(str(filepath))
        
        if modified is True:
            total_files_modified += 1
            total_imgs_removed += len(broken_imgs)
            print(f"\n[{i}/{len(blog_files)}] ✅ {filepath.name}")
            for src, tag in broken_imgs:
                print(f"   - 删除: {src}")
                all_broken_imgs.append((filepath.name, src))
        elif modified is False:
            # 有<img>标签但图片都存在
            pass
        else:
            # 没有<img>标签
            pass
    
    # 输出总结
    print("\n" + "=" * 60)
    print("处理完成！")
    print("=" * 60)
    print(f"修改的文件数: {total_files_modified}")
    print(f"删除的 <img> 标签数: {total_imgs_removed}")
    
    if all_broken_imgs:
        print("\n删除的图片列表:")
        for filename, src in all_broken_imgs:
            print(f"  - {filename}: {src}")

if __name__ == "__main__":
    main()
