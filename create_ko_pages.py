#!/usr/bin/env python3
"""
create_ko_pages.py — 批量创建韩语核心页面
从 EN 页面复制，翻译关键文本，更新链接
"""
import re
import os
import shutil

PROJECT = os.path.dirname(os.path.abspath(__file__))

# 韩语翻译映射
TRANSLATIONS = {
    # 页面标题
    "Privacy Policy — How We Protect Your Data — Baidu PPC Pro": "개인정보 처리방침 — 데이터 보호 방법 — Baidu PPC Pro",
    "Terms of Service — Baidu PPC Pro": "이용약관 — Baidu PPC Pro",
    "About Us — Baidu PPC Pro": "회사 소개 — Baidu PPC Pro",
    "Features — Baidu PPC Pro": "서비스 — Baidu PPC Pro",
    "Pricing — Baidu PPC Pro": "요금 — Baidu PPC Pro",
    "Clients — Baidu PPC Pro": "도입 사례 — Baidu PPC Pro",
    "Contact Us — Baidu PPC Pro": "문의하기 — Baidu PPC Pro",
    "Why Baidu PPC Pro — Baidu PPC Pro": "바이두 PPC Pro란 — Baidu PPC Pro",
    "China Geo — Baidu PPC Pro": "중국 지리 — Baidu PPC Pro",
    "Baidu PPC Pro — China Digital Advertising": "Baidu PPC Pro — 중국 디지털 광고",
    
    # 导航链接
    "Why Baidu PPC Pro": "바이두 PPC Pro란",
    "Services": "서비스",
    "Pricing": "요금",
    "Clients": "도입 사례",
    "FAQ": "자주 묻는 질문",
    "About": "회사 소개",
    "Blog": "블로그",
    "Contact": "문의하기",
    "Get Started": "지금 시작하기",
    
    # Footer
    "Quick Links": "바로가기",
    "Legal": "법적 고지",
    "About Us": "회사 소개",
    "Submit a Request": "문의 접수",
    "Privacy Policy": "개인정보 처리방침",
    "Terms of Service": "이용약관",
    "All rights reserved": "무단전재를 금지합니다",
    
    # 面包屑
    "Home": "홈",
    
    # 常见文本
    "Read more": "더 보기",
    "Learn more": "자세히 보기",
    "Contact us": "문의하기",
    "Get in touch": "연락하기",
    
    # Hero 区域
    "Your Gateway to China's Biggest Search Engine": "중국 최대 검색 엔진으로의 관문",
    "Without the": "없이",
    "Barrier": "장벽",
    "Open Your Account Today": "오늘 계정을 열기",
    "View Pricing": "요금 보기",
    
    # 功能区域
    "Account Activation": "계정 활성화",
    "Top 3 Placement": "상위 3위 배치",
    "Campaign Dashboard": "캠페인 대시보드",
    "Total Spend": "총 지출",
    "Conversions": "전환",
    "Avg. CPC": "평균 CPC",
    "CTR": "CTR",
    "Click Trend": "클릭 추세",
    "Active Campaigns": "활성 캠페인",
    "Brand Keywords": "브랜드 키워드",
    "Search Ads": "검색 광고",
    "Clicks": "클릭",
    "CPC": "CPC",
    
    # 数据展示
    "We Help International Brands": "해외 브랜드를 돕습니다",
    "Advertise on Baidu": "바이두에 광고하기",
    "China's #1 Search Engine": "중국 1위 검색 엔진",
    "Monthly Active Users": "월간 활성 사용자",
    "Market Share": "시장 점유율",
    "Daily Searches": "일일 검색",
    
    # 服务区域
    "What We Do": "우리가 하는 일",
    "End-to-End Baidu Advertising": "엔드투엔드 바이두 광고",
    "Account Setup": "계정 설정",
    "Campaign Management": "캠페인 관리",
    "Creative Production": "크리에이티브 제작",
    "Landing Pages": "랜딩 페이지",
    "Analytics & Reporting": "분석 및 리포팅",
    "Compliance": "컴플라이언스",
    
    # 客户区域
    "Trusted by Global Brands": "글로벌 브랜드가 신뢰",
    "Our Clients": "우리의 고객",
    "Case Studies": "사례 연구",
    "Results": "결과",
    
    # CTA 区域
    "Ready to Get Started?": "시작할 준비가 되셨나요?",
    "Talk to Our Team": "팀에 문의하기",
    "Schedule a Call": "통화 예약",
    "Free Consultation": "무료 상담",
    
    # 联系区域
    "Get in Touch": "연락하기",
    "Send us a Message": "메시지 보내기",
    "Your Name": "이름",
    "Your Email": "이메일",
    "Company Name": "회사명",
    "Phone Number": "전화번호",
    "Message": "메시지",
    "Send Message": "메시지 보내기",
    
    # 价格区域
    "Simple, Transparent Pricing": "간단하고 투명한 요금",
    "No Hidden Fees": "숨겨진 수수료 없음",
    "Monthly": "월간",
    "Annual": "연간",
    "per month": "월",
    "per year": "연",
    "Most Popular": "가장 인기",
    "Get Started": "시작하기",
    "Contact Sales": "영업팀 문의",
    
    # 关于区域
    "Our Story": "우리의 이야기",
    "Our Team": "우리의 팀",
    "Our Values": "우리의 가치",
    "Mission": "미션",
    "Vision": "비전",
    
    # FAQ 区域
    "Frequently Asked Questions": "자주 묻는 질문",
    "Still have questions?": "아직 질문이 있으신가요?",
    
    # 语言切换器
    "Language": "언어",
    "English": "English",
    "日本語": "日本語",
    "한국어": "한국어",
}

# 页面配置
PAGES = [
    {"slug": "privacy", "title": "Privacy Policy — How We Protect Your Data — Baidu PPC Pro"},
    {"slug": "terms", "title": "Terms of Service — Baidu PPC Pro"},
    {"slug": "about", "title": "About Us — Baidu PPC Pro"},
    {"slug": "features", "title": "Features — Baidu PPC Pro"},
    {"slug": "pricing", "title": "Pricing — Baidu PPC Pro"},
    {"slug": "clients", "title": "Clients — Baidu PPC Pro"},
    {"slug": "contact", "title": "Contact Us — Baidu PPC Pro"},
    {"slug": "why-baidu-ppc-pro", "title": "Why Baidu PPC Pro — Baidu PPC Pro"},
    {"slug": "china-geo", "title": "China Geo — Baidu PPC Pro"},
    {"slug": "index", "title": "Baidu PPC Pro — China Digital Advertising"},
]


def translate_text(text):
    """翻译文本"""
    for en, ko in TRANSLATIONS.items():
        text = text.replace(en, ko)
    return text


def update_links(html):
    """更新内部链接为韩语路径"""
    # 更新导航链接
    html = re.sub(r'href="/about"', 'href="/ko/about"', html)
    html = re.sub(r'href="/features"', 'href="/ko/features"', html)
    html = re.sub(r'href="/pricing"', 'href="/ko/pricing"', html)
    html = re.sub(r'href="/clients"', 'href="/ko/clients"', html)
    html = re.sub(r'href="/faq"', 'href="/ko/faq"', html)
    html = re.sub(r'href="/contact"', 'href="/ko/contact"', html)
    html = re.sub(r'href="/blog"', 'href="/ko/blog"', html)
    html = re.sub(r'href="/why-baidu-ppc-pro"', 'href="/ko/why-baidu-ppc-pro"', html)
    html = re.sub(r'href="/privacy"', 'href="/ko/privacy"', html)
    html = re.sub(r'href="/terms"', 'href="/ko/terms"', html)
    html = re.sub(r'href="/china-geo"', 'href="/ko/china-geo"', html)
    
    # 更新 canonical
    html = re.sub(r'href="https://www\.baidumarketing\.com/privacy"', 'href="https://www.baidumarketing.com/ko/privacy"', html)
    html = re.sub(r'href="https://www\.baidumarketing\.com/terms"', 'href="https://www.baidumarketing.com/ko/terms"', html)
    html = re.sub(r'href="https://www\.baidumarketing\.com/about"', 'href="https://www.baidumarketing.com/ko/about"', html)
    html = re.sub(r'href="https://www\.baidumarketing\.com/features"', 'href="https://www.baidumarketing.com/ko/features"', html)
    html = re.sub(r'href="https://www\.baidumarketing\.com/pricing"', 'href="https://www.baidumarketing.com/ko/pricing"', html)
    html = re.sub(r'href="https://www\.baidumarketing\.com/clients"', 'href="https://www.baidumarketing.com/ko/clients"', html)
    html = re.sub(r'href="https://www\.baidumarketing\.com/contact"', 'href="https://www.baidumarketing.com/ko/contact"', html)
    html = re.sub(r'href="https://www\.baidumarketing\.com/why-baidu-ppc-pro"', 'href="https://www.baidumarketing.com/ko/why-baidu-ppc-pro"', html)
    html = re.sub(r'href="https://www\.baidumarketing\.com/china-geo"', 'href="https://www.baidumarketing.com/ko/china-geo"', html)
    
    # 更新 OG URL
    html = re.sub(r'content="https://www\.baidumarketing\.com/privacy"', 'content="https://www.baidumarketing.com/ko/privacy"', html)
    html = re.sub(r'content="https://www\.baidumarketing\.com/terms"', 'content="https://www.baidumarketing.com/ko/terms"', html)
    html = re.sub(r'content="https://www\.baidumarketing\.com/about"', 'content="https://www.baidumarketing.com/ko/about"', html)
    html = re.sub(r'content="https://www\.baidumarketing\.com/features"', 'content="https://www.baidumarketing.com/ko/features"', html)
    html = re.sub(r'content="https://www\.baidumarketing\.com/pricing"', 'content="https://www.baidumarketing.com/ko/pricing"', html)
    html = re.sub(r'content="https://www\.baidumarketing\.com/clients"', 'content="https://www.baidumarketing.com/ko/clients"', html)
    html = re.sub(r'content="https://www\.baidumarketing\.com/contact"', 'content="https://www.baidumarketing.com/ko/contact"', html)
    html = re.sub(r'content="https://www\.baidumarketing\.com/why-baidu-ppc-pro"', 'content="https://www.baidumarketing.com/ko/why-baidu-ppc-pro"', html)
    html = re.sub(r'content="https://www\.baidumarketing\.com/china-geo"', 'content="https://www.baidumarketing.com/ko/china-geo"', html)
    
    # 更新 hreflang
    html = re.sub(r'hreflang="ko" href="https://www\.baidumarketing\.com/ko/[^"]*"', 
                  lambda m: m.group(0), html)  # 保留现有的 ko hreflang
    
    return html


def fix_language_switcher(html):
    """修复语言切换器"""
    # 修复语言切换器按钮（显示韩国国旗）
    html = re.sub(
        r'<button class="lang-switch-btn"[^>]*>.*?</button>',
        '<button class="lang-switch-btn" onclick="toggleLangMenu()" aria-label="Language">🇰🇷 <svg width="10" height="6" viewBox="0 0 10 6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M1 1l4 4 4-4"/></svg></button>',
        html,
        flags=re.DOTALL
    )
    
    # 修复语言切换器菜单
    html = re.sub(
        r'<div class="lang-switch-menu"[^>]*>.*?</div>',
        '''<div class="lang-switch-menu" id="langSwitchMenu">
          <a href="/" lang="en" class="lang-switch-item">🇺🇸 English</a>
          <a href="/ja" lang="ja" class="lang-switch-item">🇯🇵 日本語</a>
          <a href="/ko" lang="ko" class="lang-switch-item">🇰🇷 한국어</a>
        </div>''',
        html,
        flags=re.DOTALL
    )
    
    return html


def create_ko_page(slug):
    """创建韩语页面"""
    en_path = os.path.join(PROJECT, f"{slug}.html")
    ko_path = os.path.join(PROJECT, "ko", f"{slug}.html")
    
    if not os.path.exists(en_path):
        print(f"  ✗ EN page not found: {en_path}")
        return False
    
    # 读取 EN 页面
    with open(en_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 更新 lang 属性
    html = html.replace('lang="en"', 'lang="ko"')
    
    # 翻译文本
    html = translate_text(html)
    
    # 修复语言切换器
    html = fix_language_switcher(html)
    
    # 更新链接
    html = update_links(html)
    
    # 添加韩语 hreflang
    if 'hreflang="ko"' not in html:
        # 在 x-default 之前添加 ko hreflang
        html = re.sub(
            r'(<link rel="alternate" hreflang="x-default"[^>]*>)',
            r'<link rel="alternate" hreflang="ko" href="https://www.baidumarketing.com/ko/' + slug + '" />\n  \1',
            html
        )
    
    # 写入文件
    os.makedirs(os.path.dirname(ko_path), exist_ok=True)
    with open(ko_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"  ✓ Created ko/{slug}.html ({len(html)} bytes)")
    return True


def main():
    print("=" * 60)
    print("🇰🇷 批量创建韩语核心页面")
    print("=" * 60)
    
    success = 0
    failed = 0
    
    for page in PAGES:
        if create_ko_page(page["slug"]):
            success += 1
        else:
            failed += 1
    
    print("=" * 60)
    print(f"✅ 完成: {success} 成功, {failed} 失败")
    print("=" * 60)


if __name__ == "__main__":
    main()
