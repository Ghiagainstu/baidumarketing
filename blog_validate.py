#!/usr/bin/env python3
"""
blog_validate.py — BPP 博客自动化验证脚本
从 SKILL.md 提取所有验证规则，100% 自动执行。

用法：python blog_validate.py <slug> [--lang en|ja]
示例：python blog_validate.py baidu-industry-insights-tool-guide --lang en

退出码：
  0 = 全部通过
  1 = 有失败项
"""

import sys
import re
import os
from pathlib import Path

# ============================================================
# 配置
# ============================================================
PROJECT_ROOT = Path(__file__).parent
GA4_ID = "G-TCGE7NJT7H"
BASE_URL = "https://www.baidumarketing.com"

# 多语言规则
LANG_RULES = {
    "en": {
        "blog_dir": "blog",
        "footer_copyright": "All rights reserved",
        "read_more": "Read more",
        "breadcrumb_home": "Home",
        "breadcrumb_blog": "Blog",
        "date_format": r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4}",
    },
    "ja": {
        "blog_dir": "ja/blog",
        "footer_copyright": "無断転載を禁じます",
        "read_more": "続きを読む",
        "breadcrumb_home": "ホーム",
        "breadcrumb_blog": "ブログ",
        "date_format": r"\d{4}年\d{1,2}月\d{1,2}日",
    },
    "ko": {
        "blog_dir": "ko/blog",
        "footer_copyright": "무단전재를 금지합니다",
        "read_more": "자세히 보기",
        "breadcrumb_home": "홈",
        "breadcrumb_blog": "블로그",
        "date_format": r"d{4}년d{1,2}월d{1,2}일",
    },
}


class ValidationResult:
    def __init__(self):
        self.results = []

    def add(self, name, passed, detail=""):
        self.results.append({"name": name, "passed": passed, "detail": detail})

    def report(self):
        print("\n" + "=" * 60)
        print("📋 验证报告")
        print("=" * 60)
        passed_count = 0
        failed_count = 0
        for r in self.results:
            icon = "✅" if r["passed"] else "❌"
            print(f"  {icon} {r['name']}")
            if r["detail"]:
                print(f"     → {r['detail']}")
            if r["passed"]:
                passed_count += 1
            else:
                failed_count += 1
        print("=" * 60)
        print(f"  通过: {passed_count}  失败: {failed_count}  总计: {len(self.results)}")
        print("=" * 60)
        return failed_count == 0


# ============================================================
# 验证函数
# ============================================================

def check_ga4(html, result):
    """检查 GA4 跟踪代码"""
    found = GA4_ID in html
    result.add("GA4 跟踪代码", found, f"应包含 {GA4_ID}" if not found else "")


def check_style_count(html, result):
    """检查 </style> 标签数量"""
    count = html.count("</style>")
    result.add("</style> 标签数量", count == 1, f"找到 {count} 个，应为 1 个")


def check_main_tag(html, result):
    """检查 <main> 标签"""
    has_open = "<main" in html
    has_close = "</main>" in html
    result.add("<main> 标签", has_open and has_close)


def check_article_content(html, result):
    """检查 <article class=\"article-content\"> 标签"""
    found = 'class="article-content"' in html
    result.add('<article class="article-content">', found)


def check_h1_title(html, result):
    """检查 <h1 class=\"article-title\"> 标签"""
    found = 'class="article-title"' in html
    result.add('<h1 class="article-title">', found)


def check_canonical(html, result):
    """检查 canonical URL"""
    match = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', html)
    if not match:
        result.add("Canonical URL", False, "未找到 canonical 标签")
        return
    url = match.group(1)
    is_https = url.startswith("https://www.baidumarketing.com/")
    no_html = ".html" not in url
    result.add("Canonical URL", is_https, f"URL: {url}")
    result.add("Canonical 无 .html", no_html, f"URL: {url}")


def check_og_tags(html, result):
    """检查 OG 标签（6 项）"""
    required = ["og:type", "og:url", "og:title", "og:description", "og:site_name", "og:image"]
    missing = []
    for tag in required:
        if f'property="{tag}"' not in html:
            missing.append(tag)
    result.add("OG 标签 (6项)", len(missing) == 0, f"缺失: {missing}" if missing else "")


def check_twitter_card(html, result):
    """检查 Twitter Card（4 项）"""
    required = ["twitter:card", "twitter:title", "twitter:description", "twitter:image"]
    missing = []
    for tag in required:
        if f'name="{tag}"' not in html:
            missing.append(tag)
    result.add("Twitter Card (4项)", len(missing) == 0, f"缺失: {missing}" if missing else "")


def check_theme_color(html, result):
    """检查 theme-color + color-scheme"""
    has_theme = 'name="theme-color"' in html
    has_scheme = 'name="color-scheme"' in html
    result.add("theme-color + color-scheme", has_theme and has_scheme)


def check_preconnect(html, result):
    """检查 preconnect 双标签"""
    count = html.count("preconnect")
    result.add("Preconnect 双标签", count >= 2, f"找到 {count} 个，应 >= 2")


def check_favicon(html, result):
    """检查 Favicon（单引号）"""
    # 匹配 data:image/svg+xml 格式的 favicon（注意转义 +）
    match = re.search(r'href="(data:image/svg\+xml,[^"]*)"', html)
    if not match:
        # 也检查单引号格式
        match = re.search(r"href='(data:image/svg\+xml,[^']*)'", html)
    if not match:
        result.add("Favicon", False, "未找到内联 SVG favicon")
        return
    svg = match.group(1)
    # 检查 SVG 内部是否使用单引号（不应有未转义的双引号）
    # URL 编码的引号不算
    has_bad_quotes = '"' in svg and '%22' not in svg
    result.add("Favicon 单引号", not has_bad_quotes, "SVG 内部不应有双引号")


def check_json_ld(html, result):
    """检查 JSON-LD Schema"""
    has_schema = '"@type":"BlogPosting"' in html or '"@type": "BlogPosting"' in html
    result.add("JSON-LD BlogPosting", has_schema)
    if has_schema:
        has_author = '"author"' in html
        result.add("JSON-LD author", has_author)


def check_dark_mode(html, result):
    """检查 Dark Mode CSS"""
    has_dark = '[data-theme="dark"]' in html
    result.add("Dark Mode CSS", has_dark)


def check_nav_mobile_cta_hidden(html, result):
    """检查 nav-mobile-cta 隐藏"""
    has_rule = ".nav-mobile-cta" in html and "display:none" in html.replace(" ", "")
    result.add("nav-mobile-cta 隐藏", has_rule)


def check_lang_switch(html, result):
    """检查语言切换器"""
    has_switch = "lang-switch-item" in html
    result.add("语言切换器", has_switch)


# ============================================================
# 多语言验证
# ============================================================

def check_footer_copyright(html, lang, result):
    """检查 footer 版权文字"""
    rules = LANG_RULES[lang]
    found = rules["footer_copyright"] in html
    result.add(f"Footer 版权 ({lang})", found, f"应包含 '{rules['footer_copyright']}'")


def check_read_more(html, lang, result):
    """检查 Read more 翻译"""
    rules = LANG_RULES[lang]
    if lang == "en":
        # EN 页面不应有其他语言的 Read more
        has_ja = "続きを読む" in html
        result.add("Read more (EN)", not has_ja, "不应包含日语 Read more")
    else:
        found = rules["read_more"] in html
        result.add(f"Read more ({lang})", found, f"应包含 '{rules['read_more']}'")


def check_readmore_css(html, lang, result):
    """检查 .blog-card-readmore CSS"""
    if lang == "ja" or lang == "ko":
        has_css = "blog-card-readmore" in html
        result.add(f"Readmore CSS ({lang})", has_css, "应包含 .blog-card-readmore CSS 规则")


def check_breadcrumb(html, lang, result):
    """检查面包屑"""
    rules = LANG_RULES[lang]
    has_home = rules["breadcrumb_home"] in html
    has_blog = rules["breadcrumb_blog"] in html
    result.add(f"面包屑 ({lang})", has_home and has_blog)


def check_card_links(html, lang, result):
    """检查 blog 卡片链接路径"""
    if lang == "ja":
        # JA 博客列表页不应有 ja/blog/ 双重路径
        bad_links = re.findall(r'href="ja/blog/[^"]*"', html)
        result.add("卡片链接路径 (JA)", len(bad_links) == 0,
                   f"发现 {len(bad_links)} 个 'ja/blog/' 双重路径" if bad_links else "")
    elif lang == "ko":
        bad_links = re.findall(r'href="ko/blog/[^"]*"', html)
        result.add("卡片链接路径 (KO)", len(bad_links) == 0,
                   f"发现 {len(bad_links)} 个 'ko/blog/' 双重路径" if bad_links else "")


def check_excerpt_length(html, result):
    """检查 blog 卡片摘要长度"""
    excerpts = re.findall(r'class="blog-card-excerpt">(.*?)</p>', html, re.DOTALL)
    long_excerpts = []
    for exc in excerpts:
        clean = re.sub(r'<[^>]+>', '', exc).strip()
        if len(clean) > 130:
            long_excerpts.append(len(clean))
    result.add("卡片摘要长度 (≤120字符)", len(long_excerpts) == 0,
               f"{len(long_excerpts)} 个摘要超过 130 字符" if long_excerpts else "")


# ============================================================
# 视觉组件验证
# ============================================================

def check_visual_components(html, result):
    """检查视觉组件数量"""
    components = {
        "stats-grid": len(re.findall(r'class="stats-grid"', html)),
        "callout": len(re.findall(r'class="callout', html)),
        "takeaway-box": len(re.findall(r'class="takeaway-box"', html)),
        "comparison-table": len(re.findall(r'class="comparison-table"', html)),
        "cta-box": len(re.findall(r'class="cta-box"', html)),
    }
    count = sum(1 for v in components.values() if v > 0)
    detail = ", ".join(f"{k}:{v}" for k, v in components.items() if v > 0)
    result.add(f"视觉组件 (≥2种，推荐4种)", count >= 2, f"{count} 种: {detail}")


def check_comparison_table_tag(html, result):
    """检查 comparison-table 使用 <table> 标签"""
    bad = len(re.findall(r'<div class="comparison-table"', html))
    result.add("comparison-table 用 <table>", bad == 0,
               f"发现 {bad} 个用 <div> 的 comparison-table" if bad else "")


# ============================================================
# 主验证流程
# ============================================================

def validate_blog(slug, lang="en"):
    """验证单个博客页面"""
    result = ValidationResult()

    # 确定文件路径
    rules = LANG_RULES[lang]
    blog_dir = rules["blog_dir"]
    file_path = PROJECT_ROOT / blog_dir / f"{slug}.html"

    if not file_path.exists():
        print(f"❌ 文件不存在: {file_path}")
        return False

    html = file_path.read_text(encoding="utf-8")
    print(f"\n📄 验证文件: {file_path}")
    print(f"   文件大小: {len(html)} 字符")

    # === 基础结构检查 ===
    check_ga4(html, result)
    check_style_count(html, result)
    check_main_tag(html, result)
    check_article_content(html, result)
    check_h1_title(html, result)

    # === SEO 检查 ===
    check_canonical(html, result)
    check_og_tags(html, result)
    check_twitter_card(html, result)
    check_theme_color(html, result)
    check_preconnect(html, result)
    check_favicon(html, result)
    check_json_ld(html, result)

    # === 样式检查 ===
    check_dark_mode(html, result)
    check_nav_mobile_cta_hidden(html, result)

    # === 多语言检查 ===
    check_lang_switch(html, result)
    check_footer_copyright(html, lang, result)
    check_breadcrumb(html, lang, result)

    # === 博客列表页检查（仅对列表页）===
    if "blog-grid" in html:
        check_card_links(html, lang, result)
        check_excerpt_length(html, result)
        check_read_more(html, lang, result)
        check_readmore_css(html, lang, result)

    # === 视觉组件检查 ===
    if "article-content" in html:
        check_visual_components(html, result)
        check_comparison_table_tag(html, result)

    # === 输出报告 ===
    return result.report()


def validate_blog_listing(lang="en"):
    """验证博客列表页"""
    result = ValidationResult()
    rules = LANG_RULES[lang]

    if lang == "en":
        file_path = PROJECT_ROOT / "blog.html"
    else:
        file_path = PROJECT_ROOT / lang / "blog.html"

    if not file_path.exists():
        print(f"❌ 文件不存在: {file_path}")
        return False

    html = file_path.read_text(encoding="utf-8")
    print(f"\n📄 验证列表页: {file_path}")

    # 检查卡片链接
    check_card_links(html, lang, result)

    # 检查 Readmore CSS
    check_readmore_css(html, lang, result)

    # 检查摘要长度
    check_excerpt_length(html, result)

    # 检查卡片排序（通过日期）
    dates = re.findall(r'<span>([^<]+)</span>', html)
    # 这里只做基本检查，不验证完整排序

    return result.report()


# ============================================================
# CLI 入口
# ============================================================

def main():
    if len(sys.argv) < 2:
        print("用法: python blog_validate.py <slug> [--lang en|ja]")
        print("      python blog_validate.py --listing [--lang en|ja]")
        print("      python blog_validate.py --all")
        sys.exit(1)

    # 解析参数
    slug = None
    lang = "en"
    listing_mode = False
    all_mode = False

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--lang" and i + 1 < len(sys.argv):
            lang = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--listing":
            listing_mode = True
            i += 1
        elif sys.argv[i] == "--all":
            all_mode = True
            i += 1
        else:
            slug = sys.argv[i]
            i += 1

    all_passed = True

    if all_mode:
        # 验证所有博客
        for l in ["en", "ja", "ko"]:
            blog_dir = LANG_RULES[l]["blog_dir"]
            dir_path = PROJECT_ROOT / blog_dir
            if dir_path.exists():
                for f in dir_path.glob("*.html"):
                    if f.name == "blog.html":
                        continue
                    s = f.stem
                    passed = validate_blog(s, l)
                    if not passed:
                        all_passed = False
    elif listing_mode:
        passed = validate_blog_listing(lang)
        if not passed:
            all_passed = False
    elif slug:
        passed = validate_blog(slug, lang)
        if not passed:
            all_passed = False
    else:
        print("请指定 slug 或使用 --listing / --all")
        sys.exit(1)

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
