#!/usr/bin/env python3
"""
blog_publish.py — BPP 博客自动化发布脚本
从 SKILL.md 提取所有发布规则，100% 自动执行。

用法：python blog_publish.py <slug> --category <cat> --title-en "..." --title-ja "..." --title-ko "..." --excerpt-en "..." --excerpt-ja "..." --excerpt-ko "..." --date "Mon DD, YYYY" --date-ja "YYYY年M月D日" --date-ko "YYYY년 M월 D일" --read-time "N min" --read-time-ja "約N分" --read-time-ko "약N분"

示例：python blog_publish.py baidu-industry-insights-tool-guide \
  --category insights \
  --title-en "📊 How to Use Baidu's New Industry Insights Tool" \
  --title-ja "📊 百度業界インサイトツールの使い方" \
  --title-ko "📊 바이두의 새로운 업종 인사이트 도구 사용법" \
  --excerpt-en "Learn how Baidu's new Industry Insights tool helps advertisers benchmark PPC performance." \
  --excerpt-ja "百度の新「業界インサイト」ツールの活用法を解説。" \
  --excerpt-ko "바이두의 새로운 업종 인사이트 도구로 PPC 성과를 벤치마킹하는 방법을 알아보세요。" \
  --date "Jun 3, 2026" \
  --date-ja "2026年6月3日" \
  --date-ko "2026년 6월 3일" \
  --read-time "8 min" \
  --read-time-ja "約9分" \
  --read-time-ko "약9분"

功能：
  1. 调用 blog_validate.py 验证
  2. 插入 blog 卡片到 blog.html / ja/blog.html / ko/blog.html
  3. 按日期排序所有卡片
  4. 更新 sitemap.xml
  5. Git commit + push
  6. 输出验收报告
"""

import sys
import re
import os
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

# ============================================================
# 配置
# ============================================================
PROJECT_ROOT = Path(__file__).parent
BLOG_VALIDATE = PROJECT_ROOT / "blog_validate.py"

# 多语言配置
LANG_CONFIG = {
    "en": {
        "blog_dir": "blog",
        "listing_file": "blog.html",
        "read_more": "Read more →",
        "date_field": "date",  # 用于排序的字段
    },
    "ja": {
        "blog_dir": "ja/blog",
        "listing_file": "ja/blog.html",
        "read_more": "続きを読む →",
        "date_field": "date_ja",
    },
    "ko": {
        "blog_dir": "ko/blog",
        "listing_file": "ko/blog.html",
        "read_more": "더 보기 →",
        "date_field": "date_ko",
    },
}


# ============================================================
# 卡片模板
# ============================================================

def create_card_html(lang, slug, category, title, excerpt, date, read_time):
    """创建 blog 卡片 HTML"""
    read_more = LANG_CONFIG[lang]["read_more"]

    # 确定链接路径（相对路径，不带语言前缀）
    if lang == "en":
        link_path = f"blog/{slug}"
    else:
        # JA/KO 用相对路径 blog/slug（不是 ja/blog/slug）
        link_path = f"blog/{slug}"

    card = f'''<article class="blog-card" data-category="{category}">
        <a href="{link_path}" class="blog-card-link">
          <div class="blog-card-content">
            <h3 class="blog-card-title">{title}</h3>
            <p class="blog-card-excerpt">{excerpt}</p>
            <div class="blog-card-readmore">{read_more}</div><div class="blog-card-meta"><span>{date}</span><span class="read-time"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg> {read_time}</span></div>
          </div>
        </a></article>'''

    return card


# ============================================================
# 日期解析
# ============================================================

def parse_date_en(date_str):
    """解析英文日期：Mon DD, YYYY"""
    try:
        return datetime.strptime(date_str.strip(), "%b %d, %Y")
    except:
        try:
            return datetime.strptime(date_str.strip(), "%B %d, %Y")
        except:
            return datetime(2020, 1, 1)


def parse_date_ja(date_str):
    """解析日文日期：YYYY年M月D日"""
    m = re.match(r"(\d{4})年(\d{1,2})月(\d{1,2})日", date_str.strip())
    if m:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return datetime(2020, 1, 1)


def parse_date_ko(date_str):
    """解析韩文日期：YYYY년 M월 D일"""
    m = re.match(r"(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일", date_str.strip())
    if m:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return datetime(2020, 1, 1)


def parse_date_auto(date_str, lang):
    """根据语言自动解析日期"""
    if lang == "ja":
        return parse_date_ja(date_str)
    elif lang == "ko":
        return parse_date_ko(date_str)
    else:
        return parse_date_en(date_str)


# ============================================================
# 卡片插入 + 排序
# ============================================================

def insert_and_sort_cards(lang, slug, category, title, excerpt, date, read_time):
    """插入新卡片并按日期排序"""
    config = LANG_CONFIG[lang]
    listing_path = PROJECT_ROOT / config["listing_file"]

    if not listing_path.exists():
        print(f"❌ 列表页不存在: {listing_path}")
        return False

    content = listing_path.read_text(encoding="utf-8")

    # 检查是否已存在
    if f'blog/{slug}' in content:
        print(f"⚠️  卡片已存在: {slug}，跳过插入")
        return True

    # 创建新卡片
    new_card = create_card_html(lang, slug, category, title, excerpt, date, read_time)

    # 找到 blog-grid 位置
    grid_marker = '<div class="blog-grid" id="blogGrid">'
    grid_start = content.find(grid_marker)
    if grid_start == -1:
        print(f"❌ 未找到 blog-grid")
        return False

    grid_content_start = grid_start + len(grid_marker)

    # 插入新卡片
    content = content[:grid_content_start] + new_card + content[grid_content_start:]

    # 重新定位 grid
    grid_start = content.find(grid_marker)
    grid_content_start = grid_start + len(grid_marker)

    # 提取所有卡片
    cards = re.findall(
        r'<article class="blog-card"[^>]*>.*?</article>',
        content[grid_content_start:],
        re.DOTALL
    )

    if not cards:
        print(f"❌ 未找到任何卡片")
        return False

    # 按日期排序
    def sort_key(card):
        m = re.search(r"<span>([^<]+)</span>", card)
        if m:
            date_str = m.group(1)
            return parse_date_auto(date_str, lang)
        return datetime(2020, 1, 1)

    sorted_cards = sorted(cards, key=sort_key, reverse=True)

    # 替换 grid 内容
    new_grid_content = "".join(sorted_cards)

    # 找到 grid 结束位置（最后一个 </article> 之后的 </div>）
    last_article_end = content[grid_content_start:].rfind("</article>")
    if last_article_end == -1:
        print(f"❌ 未找到 </article> 结束标签")
        return False

    after_last = content[grid_content_start + last_article_end + len("</article>"):]
    grid_close = after_last.find("</div>")
    if grid_close == -1:
        print(f"❌ 未找到 grid 关闭标签")
        return False

    grid_end = grid_content_start + last_article_end + len("</article>") + grid_close + len("</div>")

    # 写入新内容
    new_content = content[:grid_content_start] + new_grid_content + content[grid_end:]
    listing_path.write_text(new_content, encoding="utf-8")

    print(f"✅ 卡片已插入并排序: {listing_path}")
    return True


# ============================================================
# Sitemap 更新
# ============================================================

def update_sitemap():
    """更新 sitemap.xml"""
    try:
        result = subprocess.run(
            ["node", "build.mjs", "site"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print("✅ sitemap.xml 已更新")
            return True
        else:
            print(f"❌ sitemap 更新失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ sitemap 更新异常: {e}")
        return False


# ============================================================
# Git 操作
# ============================================================

def git_commit_and_push(slug):
    """Git commit + push"""
    files = [
        "blog.html",
        "ja/blog.html",
        "ko/blog.html",
        "sitemap.xml",
    ]

    # 添加新博客文件
    for lang_config in LANG_CONFIG.values():
        blog_dir = lang_config["blog_dir"]
        blog_file = PROJECT_ROOT / blog_dir / f"{slug}.html"
        if blog_file.exists():
            files.append(f"{blog_dir}/{slug}.html")

    # 检查是否有变更
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )
        if not result.stdout.strip():
            print("⚠️  没有变更需要提交")
            return True
    except Exception as e:
        print(f"❌ git status 失败: {e}")
        return False

    # Git add
    try:
        subprocess.run(
            ["git", "add"] + files,
            cwd=PROJECT_ROOT,
            check=True
        )
    except Exception as e:
        print(f"❌ git add 失败: {e}")
        return False

    # Git commit
    try:
        subprocess.run(
            ["git", "commit", "-m", f"blog: add {slug}"],
            cwd=PROJECT_ROOT,
            check=True
        )
        print("✅ git commit 完成")
    except Exception as e:
        print(f"❌ git commit 失败: {e}")
        return False

    # Git push
    try:
        result = subprocess.run(
            ["git", "push"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            print("✅ git push 完成")
            return True
        else:
            print(f"❌ git push 失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ git push 异常: {e}")
        return False


# ============================================================
# 验证调用
# ============================================================

def run_validation(slug):
    """调用 blog_validate.py 验证"""
    print("\n" + "=" * 60)
    print("🔍 开始验证...")
    print("=" * 60)

    # 验证 EN
    result_en = subprocess.run(
        [sys.executable, str(BLOG_VALIDATE), slug, "--lang", "en"],
        cwd=PROJECT_ROOT,
        capture_output=False
    )

    # 验证 JA
    result_ja = subprocess.run(
        [sys.executable, str(BLOG_VALIDATE), slug, "--lang", "ja"],
        cwd=PROJECT_ROOT,
        capture_output=False
    )

    # 验证 KO
    result_ko = subprocess.run(
        [sys.executable, str(BLOG_VALIDATE), slug, "--lang", "ko"],
        cwd=PROJECT_ROOT,
        capture_output=False
    )

    if result_en.returncode != 0 or result_ja.returncode != 0 or result_ko.returncode != 0:
        print("\n❌ 验证失败，请修复后重试")
        return False

    print("\n✅ 验证通过")
    return True


# ============================================================
# 主流程
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="BPP 博客自动化发布")
    parser.add_argument("slug", help="博客 slug")
    parser.add_argument("--category", required=True, help="分类：insights/search/feed/strategy/platform/landing")
    parser.add_argument("--title-en", required=True, help="英文标题")
    parser.add_argument("--title-ja", required=True, help="日文标题")
    parser.add_argument("--title-ko", help="韩文标题")
    parser.add_argument("--excerpt-en", required=True, help="英文摘要 (≤120字符)")
    parser.add_argument("--excerpt-ja", required=True, help="日文摘要 (≤120字符)")
    parser.add_argument("--excerpt-ko", help="韩文摘要 (≤120字符)")
    parser.add_argument("--date", required=True, help="英文日期：Mon DD, YYYY")
    parser.add_argument("--date-ja", required=True, help="日文日期：YYYY年M月D日")
    parser.add_argument("--date-ko", help="韩文日期：YYYY년 M월 D일")
    parser.add_argument("--read-time", required=True, help="英文阅读时间：N min")
    parser.add_argument("--read-time-ja", required=True, help="日文阅读时间：約N分")
    parser.add_argument("--read-time-ko", help="韩文阅读时间：약N분")
    parser.add_argument("--skip-validation", action="store_true", help="跳过验证")
    parser.add_argument("--skip-push", action="store_true", help="跳过 git push")

    args = parser.parse_args()

    print("=" * 60)
    print("📝 BPP 博客自动化发布")
    print("=" * 60)
    print(f"  Slug: {args.slug}")
    print(f"  Category: {args.category}")
    print(f"  EN Title: {args.title_en}")
    print(f"  JA Title: {args.title_ja}")
    if args.title_ko:
        print(f"  KO Title: {args.title_ko}")
    print("=" * 60)

    # Step 1: 验证
    if not args.skip_validation:
        if not run_validation(args.slug):
            sys.exit(1)

    # Step 2: 插入卡片 + 排序
    print("\n" + "=" * 60)
    print("📋 插入卡片...")
    print("=" * 60)

    # EN 卡片
    if not insert_and_sort_cards(
        "en", args.slug, args.category,
        args.title_en, args.excerpt_en,
        args.date, args.read_time
    ):
        sys.exit(1)

    # JA 卡片
    if not insert_and_sort_cards(
        "ja", args.slug, args.category,
        args.title_ja, args.excerpt_ja,
        args.date_ja, args.read_time_ja
    ):
        sys.exit(1)

    # KO 卡片（可选）
    if args.title_ko and args.excerpt_ko and args.date_ko and args.read_time_ko:
        if not insert_and_sort_cards(
            "ko", args.slug, args.category,
            args.title_ko, args.excerpt_ko,
            args.date_ko, args.read_time_ko
        ):
            sys.exit(1)

    # Step 3: 更新 sitemap
    print("\n" + "=" * 60)
    print("🗺️  更新 sitemap...")
    print("=" * 60)
    if not update_sitemap():
        sys.exit(1)

    # Step 4: Git commit + push
    if not args.skip_push:
        print("\n" + "=" * 60)
        print("🚀 Git 部署...")
        print("=" * 60)
        if not git_commit_and_push(args.slug):
            sys.exit(1)

    # 完成
    print("\n" + "=" * 60)
    print("✅ 发布完成！")
    print("=" * 60)
    print(f"  EN: https://www.baidumarketing.com/blog/{args.slug}")
    print(f"  JA: https://www.baidumarketing.com/ja/blog/{args.slug}")
    if args.title_ko:
        print(f"  KO: https://www.baidumarketing.com/ko/blog/{args.slug}")
    print("=" * 60)


if __name__ == "__main__":
    main()
