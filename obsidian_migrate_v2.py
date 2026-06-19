#!/usr/bin/env python3
"""
Obsidian Vault 标准化迁移脚本
将 BPP 博客文件迁移到统一格式：

E:/Obsidian/Baidu/[分类]/[slug]/
  readme.md           ← 三语摘要（EN/JA/KO）
  [slug]-en.md        ← EN 完整文章
  [slug]-ja.md        ← JA 完整文章
  [slug]-ko.md        ← KO 完整文章（如适用）
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# 配置
VAULT_PATH = Path("E:/Obsidian/Baidu")
LOG_PATH = Path("c:/Users/HYE/WorkBuddy/20260411211839/migration-log.md")
DRY_RUN = False  # 设为 True 只预览不执行

# 分类文件夹映射
CATEGORY_FOLDERS = {
    "01-Market-Insights",
    "02-Platform",
    "03-Search-Ads",
    "04-Feed-Ads",
    "05-Strategy",
    "06-Landing-Page",
    "07-Pricing-Models",
    "08-Baidu-Basics",
    "09-China-Search-Landscape",
    "10-ByteDance-Douyin",
    "11-Offline-Traditional",
    "12-Operations-Compliance",
    "13-Special-Topics",
}

# 迁移日志
migration_log = []


def log_action(action, old_path, new_path, note=""):
    """记录迁移操作"""
    migration_log.append({
        "action": action,
        "old": str(old_path),
        "new": str(new_path),
        "note": note,
    })


def extract_slug_from_filename(filename):
    """从文件名提取 slug"""
    # 去掉 ✅ 前缀
    name = filename.replace("✅ ", "")
    # 去掉 bpp- 前缀
    name = re.sub(r'^bpp-', '', name)
    # 去掉语言后缀
    name = re.sub(r'-(en|ja|ko)$', '', name)
    # 去掉 .md 扩展名
    name = name.replace('.md', '')
    return name


def extract_lang_from_filename(filename):
    """从文件名提取语言"""
    match = re.search(r'-(en|ja|ko)\.md$', filename)
    if match:
        return match.group(1)
    return None


def get_summary_excerpt(filepath, max_chars=200):
    """从 markdown 文件提取摘要"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 跳过 frontmatter
        content = re.sub(r'^---\n.*?\n---\n*', '', content, flags=re.DOTALL)
        
        # 提取第一段非空内容
        lines = content.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('---'):
                return line[:max_chars]
    except:
        pass
    return ""


def step1_rename_summary_files():
    """Step 2: 重命名 summary-{lang}.md 文件"""
    print("\n=== Step 1: 重命名 summary-{lang}.md 文件 ===")
    count = 0
    
    for category_folder in VAULT_PATH.iterdir():
        if not category_folder.is_dir():
            continue
        
        for subfolder in category_folder.iterdir():
            if not subfolder.is_dir():
                continue
            
            slug = subfolder.name
            
            for summary_file in subfolder.glob("summary-*.md"):
                lang = extract_lang_from_filename(summary_file.name)
                if not lang:
                    continue
                
                new_name = f"{slug}-{lang}.md"
                new_path = subfolder / new_name
                
                if new_path.exists():
                    print(f"  跳过（已存在）: {summary_file.name} -> {new_name}")
                    log_action("skip", summary_file, new_path, "目标已存在")
                    continue
                
                print(f"  重命名: {summary_file.name} -> {new_name}")
                if not DRY_RUN:
                    summary_file.rename(new_path)
                log_action("rename", summary_file, new_path)
                count += 1
    
    print(f"  共处理 {count} 个文件")
    return count


def step2_move_checkmark_files():
    """Step 1: 移动 ✅ 前缀文件到子文件夹"""
    print("\n=== Step 2: 移动 ✅ 前缀文件到子文件夹 ===")
    count = 0
    
    for category_folder in VAULT_PATH.iterdir():
        if not category_folder.is_dir():
            continue
        if category_folder.name not in CATEGORY_FOLDERS:
            continue
        
        for checkmark_file in category_folder.glob("✅ *.md"):
            if not checkmark_file.is_file():
                continue
            
            filename = checkmark_file.name
            slug = extract_slug_from_filename(filename)
            lang = extract_lang_from_filename(filename)
            
            if not lang:
                print(f"  跳过（无语言后缀）: {filename}")
                log_action("skip", checkmark_file, None, "无语言后缀")
                continue
            
            # 目标子文件夹
            target_folder = category_folder / slug
            new_filename = f"{slug}-{lang}.md"
            new_path = target_folder / new_filename
            
            # 如果目标已存在，跳过
            if new_path.exists():
                print(f"  跳过（已存在）: {filename}")
                log_action("skip", checkmark_file, new_path, "目标已存在")
                continue
            
            # 创建子文件夹（如果不存在）
            print(f"  移动: {filename} -> {slug}/{new_filename}")
            if not DRY_RUN:
                target_folder.mkdir(exist_ok=True)
                shutil.move(str(checkmark_file), str(new_path))
            log_action("move", checkmark_file, new_path)
            count += 1
    
    print(f"  共处理 {count} 个文件")
    return count


def step3_create_readme_files():
    """Step 3: 创建 readme.md 文件"""
    print("\n=== Step 3: 创建 readme.md 文件 ===")
    count = 0
    
    for category_folder in VAULT_PATH.iterdir():
        if not category_folder.is_dir():
            continue
        
        for subfolder in category_folder.iterdir():
            if not subfolder.is_dir():
                continue
            
            readme_path = subfolder / "readme.md"
            if readme_path.exists():
                continue
            
            # 收集各语言版本的摘要
            slug = subfolder.name
            summaries = {}
            
            for lang in ['en', 'ja', 'ko']:
                lang_file = subfolder / f"{slug}-{lang}.md"
                if lang_file.exists():
                    excerpt = get_summary_excerpt(lang_file)
                    if excerpt:
                        summaries[lang] = excerpt
            
            if not summaries:
                continue
            
            # 生成 readme.md 内容
            content = f"# {slug}\n\n"
            
            if 'en' in summaries:
                content += f"## EN\n{summaries['en']}\n\n"
            if 'ja' in summaries:
                content += f"## JA\n{summaries['ja']}\n\n"
            if 'ko' in summaries:
                content += f"## KO\n{summaries['ko']}\n\n"
            
            print(f"  创建: {subfolder.relative_to(VAULT_PATH)}/readme.md")
            if not DRY_RUN:
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            log_action("create", None, readme_path)
            count += 1
    
    print(f"  共创建 {count} 个 readme.md")
    return count


def step4_handle_root_files():
    """Step 4: 处理根目录孤立文件"""
    print("\n=== Step 4: 处理根目录孤立文件 ===")
    count = 0
    
    # 根目录文件分类映射
    root_file_mapping = {
        "baidu-marketing-blog": "02-Platform",
        "baidu-marketing-blog-ja": "02-Platform",
        "baidu-marketing-blog-ko": "02-Platform",
        "faq-b2b-market-insights": "01-Market-Insights",
        "faq-b2b-market-insights-en": "01-Market-Insights",
        "faq-b2b-market-insights-ja": "01-Market-Insights",
        "faq-b2b-market-insights-ko": "01-Market-Insights",
    }
    
    for root_file in VAULT_PATH.glob("*.md"):
        if not root_file.is_file():
            continue
        
        filename = root_file.name
        name = filename.replace('.md', '')
        
        # 跳过特殊文件
        if filename in ['00-Post-Archive-Index.md', '00-百度营销博客-MOC.md']:
            continue
        
        # 检查是否在映射中
        if name in root_file_mapping:
            category = root_file_mapping[name]
            slug = name.replace('-en', '').replace('-ja', '').replace('-ko', '')
            lang = extract_lang_from_filename(filename)
            
            target_folder = VAULT_PATH / category / slug
            new_filename = f"{slug}-{lang}.md" if lang else filename
            new_path = target_folder / new_filename
            
            if new_path.exists():
                print(f"  跳过（已存在）: {filename}")
                log_action("skip", root_file, new_path, "目标已存在")
                continue
            
            print(f"  移动: {filename} -> {category}/{slug}/{new_filename}")
            if not DRY_RUN:
                target_folder.mkdir(parents=True, exist_ok=True)
                shutil.move(str(root_file), str(new_path))
            log_action("move", root_file, new_path)
            count += 1
        else:
            print(f"  跳过（无映射）: {filename}")
            log_action("skip", root_file, None, "无分类映射")
    
    print(f"  共处理 {count} 个文件")
    return count


def step5_handle_date_prefix_files():
    """Step 5: 处理日期前缀文件"""
    print("\n=== Step 5: 处理日期前缀文件 ===")
    count = 0
    
    # 查找 "Jun 5, 2026 - " 前缀的文件
    for category_folder in VAULT_PATH.iterdir():
        if not category_folder.is_dir():
            continue
        
        for date_file in category_folder.glob("Jun 5, 2026 - *.md"):
            filename = date_file.name
            # 提取 slug
            slug = filename.replace("Jun 5, 2026 - ", "").replace('.md', '')
            lang = extract_lang_from_filename(slug)
            
            if lang:
                slug = slug.replace(f'-{lang}', '')
            
            # 目标子文件夹
            target_folder = category_folder / slug
            new_filename = f"{slug}-{lang}.md" if lang else f"{slug}.md"
            new_path = target_folder / new_filename
            
            if new_path.exists():
                print(f"  跳过（已存在）: {filename}")
                log_action("skip", date_file, new_path, "目标已存在")
                continue
            
            print(f"  移动: {filename} -> {slug}/{new_filename}")
            if not DRY_RUN:
                target_folder.mkdir(exist_ok=True)
                shutil.move(str(date_file), str(new_path))
            log_action("move", date_file, new_path)
            count += 1
    
    print(f"  共处理 {count} 个文件")
    return count


def step6_handle_duplicate_folders():
    """Step 6: 处理疑似重复子文件夹"""
    print("\n=== Step 6: 检查疑似重复子文件夹 ===")
    
    duplicates = [
        ("02-Platform/baidu-app-ecosystem", "02-Platform/07-baidu-app-ecosystem"),
        ("02-Platform/bpp-baidu-merchant-agent-human-handoff", "02-Platform/baidu-merchant-agent-human-handoff"),
        ("02-Platform/baidu-market-product-updates-june-2026", "02-Platform/baidu-marketing-product-updates-june-2026"),
    ]
    
    for folder1, folder2 in duplicates:
        path1 = VAULT_PATH / folder1
        path2 = VAULT_PATH / folder2
        
        if path1.exists() and path2.exists():
            print(f"  重复: {folder1} vs {folder2}")
            # 比较文件数量
            files1 = list(path1.glob("*.md"))
            files2 = list(path2.glob("*.md"))
            print(f"    {folder1}: {len(files1)} 个文件")
            print(f"    {folder2}: {len(files2)} 个文件")
            log_action("duplicate", path1, path2, f"{len(files1)} vs {len(files2)} files")
        elif path1.exists():
            print(f"  仅存在: {folder1}")
        elif path2.exists():
            print(f"  仅存在: {folder2}")


def generate_migration_log():
    """生成迁移日志"""
    print("\n=== 生成迁移日志 ===")
    
    content = f"""# Obsidian Vault 迁移日志

**迁移日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**模式**: {'DRY RUN（预览）' if DRY_RUN else '实际执行'}

## 迁移统计

| 操作 | 数量 |
|------|------|
| 重命名 | {len([l for l in migration_log if l['action'] == 'rename'])} |
| 移动 | {len([l for l in migration_log if l['action'] == 'move'])} |
| 创建 | {len([l for l in migration_log if l['action'] == 'create'])} |
| 跳过 | {len([l for l in migration_log if l['action'] == 'skip'])} |
| 重复 | {len([l for l in migration_log if l['action'] == 'duplicate'])} |

## 详细日志

"""
    
    for entry in migration_log:
        old = entry['old'] or '-'
        new = entry['new'] or '-'
        note = f" ({entry['note']})" if entry['note'] else ""
        content += f"- **{entry['action']}**: `{old}` -> `{new}`{note}\n"
    
    if not DRY_RUN:
        with open(LOG_PATH, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  日志已保存到: {LOG_PATH}")
    else:
        print(f"  预览模式，日志未保存")


def main():
    """主函数"""
    print("=" * 60)
    print("Obsidian Vault 标准化迁移")
    print(f"Vault 路径: {VAULT_PATH}")
    print(f"模式: {'DRY RUN（预览）' if DRY_RUN else '实际执行'}")
    print("=" * 60)
    
    # 检查 vault 路径
    if not VAULT_PATH.exists():
        print(f"错误: Vault 路径不存在: {VAULT_PATH}")
        return
    
    # 执行迁移步骤
    step1_rename_summary_files()
    step2_move_checkmark_files()
    step3_create_readme_files()
    step4_handle_root_files()
    step5_handle_date_prefix_files()
    step6_handle_duplicate_folders()
    
    # 生成迁移日志
    generate_migration_log()
    
    print("\n" + "=" * 60)
    print("迁移完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
