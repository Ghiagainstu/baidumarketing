import os

base = "C:/Users/HYE/WorkBuddy/20260411211839"
pages = [
    "blog/b2b-lead-generation-framework.html",
    "blog/baidu-2026-international-brands.html",
    "blog/baidu-ads-campaign-upgrade-2025.html",
    "blog/baidu-brand-info-account-level.html",
    "blog/baidu-custom-form-retirement.html",
    "blog/chinese-consumers-decision-journey.html",
    "blog/faq-international-brands.html",
    "blog/why-b2b-baidu-search.html",
    "ja/blog/b2b-lead-generation-framework.html",
    "ja/blog/baidu-2026-international-brands.html",
]

print(f"{'文件':<65} {'canonical':<10} {'hreflang':<10} {'x-default':<12} {'JSON-LD':<8}")
print("-" * 120)

for relpath in pages:
    fpath = os.path.join(base, relpath)
    try:
        content = open(fpath, encoding='utf-8').read()
    except Exception as e:
        print(f"{relpath:<65} 读取失败: {e}")
        continue

    has_canonical = 'rel="canonical"' in content
    has_hreflang = 'hreflang' in content
    has_xdefault = 'hreflang="x-default"' in content
    has_jsonld = 'application/ld+json' in content

    c = "OK" if has_canonical else "缺失"
    h = "OK" if has_hreflang else "缺失"
    xd = "OK" if has_xdefault else "缺失"
    j = "OK" if has_jsonld else "缺失"
    print(f"{relpath:<65} {c:<10} {h:<10} {xd:<12} {j:<8}")
