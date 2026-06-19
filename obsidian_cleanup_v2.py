#!/usr/bin/env python3
"""
Obsidian Vault 清理脚本 - 处理剩余待处理项
1. 合并重复文件夹
2. 处理根目录孤立文件
"""

import os
import shutil
from pathlib import Path

VAULT_PATH = Path("E:/Obsidian/Baidu")
DRY_RUN = False

def merge_folders(source_folder, target_folder, reason):
    """合并文件夹：将 source 中的文件移动到 target"""
    print(f"\n=== 合并: {source_folder.name} -> {target_folder.name} ===")
    print(f"原因: {reason}")
    
    if not source_folder.exists():
        print(f"  源文件夹不存在: {source_folder}")
        return
    
    if not target_folder.exists():
        print(f"  目标文件夹不存在: {target_folder}")
        return
    
    moved = 0
    for source_file in source_folder.glob("*.md"):
        target_file = target_folder / source_file.name
        
        if target_file.exists():
            print(f"  跳过（已存在）: {source_file.name}")
            continue
        
        print(f"  移动: {source_file.name}")
        if not DRY_RUN:
            shutil.move(str(source_file), str(target_file))
        moved += 1
    
    # 删除空的源文件夹
    if not DRY_RUN:
        remaining = list(source_folder.glob("*"))
        if len(remaining) == 0 or (len(remaining) == 1 and remaining[0].name == "readme.md"):
            # 只有 readme.md 或空，可以删除
            if remaining and remaining[0].name == "readme.md":
                remaining[0].unlink()
            source_folder.rmdir()
            print(f"  删除空文件夹: {source_folder.name}")
    
    print(f"  共移动 {moved} 个文件")


def handle_root_orphan_files():
    """处理根目录孤立文件"""
    print("\n=== 处理根目录孤立文件 ===")
    
    # 定义孤立文件的分类映射
    orphan_mapping = {
        "baidu-ad-display-name-update.md": {
            "category": "02-Platform",
            "slug": "05-baidu-display-name-update",
            "lang": "en",
        },
        "baidu-marketing-playbook-appendix-faq-ko.md": {
            "category": "05-Strategy",
            "slug": "faq-international-brands",
            "lang": "ko",
        },
    }
    
    # 索引/MOC 文件保留在根目录
    keep_in_root = [
        "00-Post-Archive-Index.md",
        "00-百度营销博客-MOC.md",
    ]
    
    # 特殊文件，需要手动处理
    special_files = [
        "2020年百度B2B行业洞察报告.md",
        "BPP-品牌Logo设计规范.md",
        "bpp-blog-cards-jp-translated.md",
        "bpp-faq-jp-translated.md",
        "bpp-faq-source-en.md",
    ]
    
    for root_file in VAULT_PATH.glob("*.md"):
        filename = root_file.name
        
        # 跳过保留文件
        if filename in keep_in_root:
            print(f"  保留（索引文件）: {filename}")
            continue
        
        # 检查是否有映射
        if filename in orphan_mapping:
            mapping = orphan_mapping[filename]
            target_folder = VAULT_PATH / mapping["category"] / mapping["slug"]
            new_filename = f"{mapping['slug']}-{mapping['lang']}.md"
            target_path = target_folder / new_filename
            
            if target_path.exists():
                print(f"  跳过（已存在）: {filename}")
                continue
            
            print(f"  移动: {filename} -> {mapping['category']}/{mapping['slug']}/{new_filename}")
            if not DRY_RUN:
                target_folder.mkdir(parents=True, exist_ok=True)
                shutil.move(str(root_file), str(target_path))
        elif filename in special_files:
            print(f"  特殊文件（需手动处理）: {filename}")
        else:
            print(f"  未知文件: {filename}")


def main():
    print("=" * 60)
    print("Obsidian Vault 清理 - 处理剩余待处理项")
    print(f"Vault 路径: {VAULT_PATH}")
    print(f"模式: {'DRY RUN（预览）' if DRY_RUN else '实际执行'}")
    print("=" * 60)
    
    # 1. 合并重复文件夹
    print("\n" + "=" * 60)
    print("Part 1: 合并重复文件夹")
    print("=" * 60)
    
    # 合并 1: baidu-app-ecosystem -> 07-baidu-app-ecosystem
    merge_folders(
        VAULT_PATH / "02-Platform" / "baidu-app-ecosystem",
        VAULT_PATH / "02-Platform" / "07-baidu-app-ecosystem",
        "baidu-app-ecosystem 只有 ja，07-baidu-app-ecosystem 有完整 en/ja/ko"
    )
    
    # 合并 2: baidu-merchant-agent-human-handoff -> bpp-baidu-merchant-agent-human-handoff
    merge_folders(
        VAULT_PATH / "02-Platform" / "baidu-merchant-agent-human-handoff",
        VAULT_PATH / "02-Platform" / "bpp-baidu-merchant-agent-human-handoff",
        "bpp- 前缀版本有完整 en/ja/ko"
    )
    
    # 合并 3: baidu-market-product-updates-june-2026 -> baidu-marketing-product-updates-june-2026
    merge_folders(
        VAULT_PATH / "02-Platform" / "baidu-market-product-updates-june-2026",
        VAULT_PATH / "02-Platform" / "baidu-marketing-product-updates-june-2026",
        "marketing 版本有完整 en/ja/ko"
    )
    
    # 2. 处理根目录孤立文件
    print("\n" + "=" * 60)
    print("Part 2: 处理根目录孤立文件")
    print("=" * 60)
    
    handle_root_orphan_files()
    
    print("\n" + "=" * 60)
    print("清理完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
