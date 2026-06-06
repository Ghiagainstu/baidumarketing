#!/usr/bin/env python3
"""
obsidian_migrate.py — Obsidian 博客文件迁移脚本
将现有的 EN/JA/KO 独立文件重组为父页面+摘要结构。

旧结构：
  01-Market-Insights/
    ✅ bpp-01-baidu-2025-earnings.md      (EN)
    ✅ bpp-01-baidu-2025-earnings-jp.md   (JA)
    ✅ bpp-01-baidu-2025-earnings-ko.md   (KO)

新结构：
  01-Market-Insights/
    baidu-2025-earnings.md              ← 父页面（EN 完整内容）
    baidu-2025-earnings/
      summary-en.md                     ← EN 摘要
      summary-ja.md                     ← JA 摘要
      summary-ko.md                     ← KO 摘要

用法：
  python obsidian_migrate.py              # 预览迁移（不执行）
  python obsidian_migrate.py --execute    # 执行迁移
  python obsidian_migrate.py --dry-run    # 预览迁移（不执行）
"""

import os
import re
import shutil
import sys
from pathlib import Path
from collections import defaultdict

# ============================================================
# 配置
# ============================================================
OBSIDIAN_ROOT = Path("E:/Obsidian/Baidu")
CATEGORY_DIRS = [
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
]


# ============================================================
# 文件名解析
# ============================================================

def parse_filename(filename):
    """
    解析文件名，返回 (slug, lang) 或 None。
    
    支持的格式：
    - ✅ bpp-01-baidu-2025-earnings.md      → (baidu-2025-earnings, en)
    - ✅ bpp-01-baidu-2025-earnings-jp.md   → (baidu-2025-earnings, ja)
    - ✅ bpp-01-baidu-2025-earnings-ko.md   → (baidu-2025-earnings, ko)
    - Jun 5, 2026 - baidu-industry-insights-tool-guide-en.md → (baidu-industry-insights-tool-guide, en)
    - Jun 5, 2026 - baidu-industry-insights-tool-guide-jp.md → (baidu-industry-insights-tool-guide, ja)
    """
    name = filename.replace(".md", "")

    # 格式 1: "✅ bpp-NN-slug.md" 或 "✅ bpp-slug.md"
    m = re.match(r"✅ bpp-(\d+-)?(.+?)(-(en|jp|ko|ja))?$", name)
    if m:
        slug = m.group(2)
        lang_suffix = m.group(4)
        if lang_suffix == "jp":
            lang = "ja"
        elif lang_suffix:
            lang = lang_suffix
        else:
            lang = "en"
        return slug, lang

    # 格式 2: "Jun 5, 2026 - slug-en.md"
    m = re.match(r"[A-Z][a-z]+ \d+, \d+ - (.+?)-(en|jp|ko|ja)$", name)
    if m:
        slug = m.group(1)
        lang_suffix = m.group(2)
        if lang_suffix == "jp":
            lang = "ja"
        else:
            lang = lang_suffix
        return slug, lang

    return None, None


def extract_summary(content, max_chars=200):
    """从完整内容中提取摘要（前 max_chars 个字符）"""
    # 跳过 frontmatter
    lines = content.split("\n")
    in_frontmatter = False
    content_lines = []

    for line in lines:
        if line.strip() == "---":
            in_frontmatter = not in_frontmatter
            continue
        if not in_frontmatter and line.strip():
            content_lines.append(line.strip())

    # 合并内容，截取摘要
    full_text = " ".join(content_lines)
    # 跳过标题
    if full_text.startswith("#"):
        full_text = re.sub(r"^#+\s+", "", full_text)

    if len(full_text) > max_chars:
        # 在句子边界截断
        truncated = full_text[:max_chars]
        last_period = max(truncated.rfind(". "), truncated.rfind("。 "), truncated.rfind("? "), truncated.rfind("? "))
        if last_period > max_chars * 0.6:
            return truncated[:last_period + 1]
        return truncated + "..."
    return full_text


# ============================================================
# 迁移逻辑
# ============================================================

def scan_existing_files():
    """扫描现有文件，按 slug 分组"""
    groups = defaultdict(dict)

    for cat_dir in CATEGORY_DIRS:
        cat_path = OBSIDIAN_ROOT / cat_dir
        if not cat_path.exists():
            continue

        for filename in os.listdir(cat_path):
            if not filename.endswith(".md"):
                continue
            if filename.startswith("00-") or filename.startswith("BPP-"):
                continue

            slug, lang = parse_filename(filename)
            if slug and lang:
                filepath = cat_path / filename
                groups[(cat_dir, slug)][lang] = filepath

    return groups


def create_migration_plan(groups):
    """创建迁移计划"""
    plan = []

    for (cat_dir, slug), lang_files in groups.items():
        # 确定父页面文件（EN）
        en_file = lang_files.get("en")
        if not en_file:
            # 如果没有 EN 文件，跳过
            continue

        # 新目录结构
        parent_dir = OBSIDIAN_ROOT / cat_dir
        summary_dir = parent_dir / slug

        # 父页面路径
        parent_file = parent_dir / f"{slug}.md"

        # 摘要文件路径
        summary_files = {}
        for lang, filepath in lang_files.items():
            summary_files[lang] = summary_dir / f"summary-{lang}.md"

        plan.append({
            "cat_dir": cat_dir,
            "slug": slug,
            "lang_files": lang_files,
            "parent_file": parent_file,
            "summary_dir": summary_dir,
            "summary_files": summary_files,
        })

    return plan


def execute_migration(plan, dry_run=True):
    """执行迁移"""
    print("=" * 60)
    print("📁 Obsidian 博客文件迁移")
    print("=" * 60)

    for item in plan:
        slug = item["slug"]
        cat_dir = item["cat_dir"]
        lang_files = item["lang_files"]
        parent_file = item["parent_file"]
        summary_dir = item["summary_dir"]
        summary_files = item["summary_files"]

        print(f"\n📄 {cat_dir}/{slug}")
        print(f"  语言: {', '.join(lang_files.keys())}")

        if dry_run:
            print(f"  [DRY RUN] 将创建:")
            print(f"    父页面: {parent_file.name}")
            print(f"    摘要目录: {summary_dir.name}/")
            for lang, sfile in summary_files.items():
                print(f"      {sfile.name}")
        else:
            # 创建摘要目录
            summary_dir.mkdir(exist_ok=True)

            # 复制 EN 文件作为父页面
            en_file = lang_files.get("en")
            if en_file and en_file.exists():
                shutil.copy2(en_file, parent_file)
                print(f"  ✅ 父页面: {parent_file.name}")

            # 创建摘要文件
            for lang, filepath in lang_files.items():
                if filepath.exists():
                    content = filepath.read_text(encoding="utf-8")
                    summary = extract_summary(content)

                    # 创建摘要文件
                    summary_file = summary_files[lang]
                    summary_content = f"""---
title: "{slug}"
slug: {slug}
language: {lang}
type: summary
parent: "[[{slug}]]"
---

# {slug}

{summary}

→ [[{slug}|阅读全文]]
"""
                    summary_file.write_text(summary_content, encoding="utf-8")
                    print(f"  ✅ 摘要: {summary_file.name}")

    if dry_run:
        print("\n" + "=" * 60)
        print("⚠️  这是预览模式。使用 --execute 执行迁移。")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("✅ 迁移完成！")
        print("=" * 60)
        print("注意：原始文件未删除。确认迁移正确后可手动删除。")


# ============================================================
# CLI 入口
# ============================================================

def main():
    dry_run = True

    if "--execute" in sys.argv:
        dry_run = False
    elif "--dry-run" in sys.argv:
        dry_run = True

    # 扫描现有文件
    groups = scan_existing_files()

    if not groups:
        print("❌ 未找到任何博客文件")
        sys.exit(1)

    print(f"📊 找到 {len(groups)} 组博客文件")

    # 创建迁移计划
    plan = create_migration_plan(groups)

    # 执行迁移
    execute_migration(plan, dry_run=dry_run)


if __name__ == "__main__":
    main()
