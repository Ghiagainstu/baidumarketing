#!/usr/bin/env python3
"""
translate_index_ko.py — 翻译 index.html 为韩语
"""
import re
import os

PROJECT = os.path.dirname(os.path.abspath(__file__))

# 完整翻译映射
TRANSLATIONS = {
    # Skip to main content
    "Skip to main content": "메인 콘텐츠로 건너뛰기",
    
    # Hero 区域
    "Your Gateway to China's Biggest Search Engine": "중국 최대 검색 엔진으로의 관문",
    "Without the": "없이",
    "Barrier": "장벽",
    "Open Your Account Today": "오늘 계정을 열기",
    "View Pricing": "요금 보기",
    
    # 数据仪表板
    "Account Activation": "계정 활성화",
    "Top 3 Placement": "상위 3위 배치",
    "Campaign Dashboard": "캠페인 대시보드",
    "Mar 1 – Mar 31, 2026": "2026년 3월 1일 – 3월 31일",
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
    "Active": "활성",
    "Product Pages": "상품 페이지",
    "oCPC": "oCPC",
    "Generic Keywords": "일반 키워드",
    
    # 时间范围
    "7D": "7일",
    "30D": "30일",
    "90D": "90일",
    
    # 功能区域
    "Why Baidu PPC Pro": "바이두 PPC Pro란",
    "The Platform": "플랫폼",
    "The Problem": "문제",
    "The Solution": "해결책",
    "We Handle Everything": "모든 것을 처리합니다",
    "From account setup to campaign management, we handle the entire process so you can focus on your business.": "계정 설정부터 캠페인 관리까지, 전체 프로세스를 처리하므로 비즈니스에 집중할 수 있습니다.",
    
    # 服务区域
    "What We Do": "우리가 하는 일",
    "End-to-End Baidu Advertising": "엔드투엔드 바이두 광고",
    "Account Setup": "계정 설정",
    "We handle the entire account setup process, including verification, payment methods, and compliance requirements.": "전체 계정 설정 프로세스를 처리하며, 인증, 결제 방법, 컴플라이언스 요구 사항을 포함합니다.",
    "Campaign Management": "캠페인 관리",
    "Our team manages your campaigns daily, optimizing bids, keywords, and ad copy for maximum ROI.": "팀이 매일 캠페인을 관리하며, 입찰, 키워드, 광고 문구를 최적화하여 최대 ROI를 달성합니다.",
    "Creative Production": "크리에이티브 제작",
    "We create culturally appropriate ad copy and landing pages that resonate with Chinese audiences.": "중국 고객에게 공감되는 문화적으로 적절한 광고 문구와 랜딩 페이지를 제작합니다.",
    "Landing Pages": "랜딩 페이지",
    "We design and optimize landing pages for Chinese users, ensuring fast load times and mobile responsiveness.": "중국 사용자를 위한 랜딩 페이지를 설계하고 최적화하며, 빠른 로딩 시간과 모바일 반응성을 보장합니다.",
    "Analytics & Reporting": "분석 및 리포팅",
    "Get detailed reports in English, with insights and recommendations to improve your campaign performance.": "영어로 된 상세 보고서와 캠페인 성과 향상을 위한 인사이트와 권장 사항을 제공합니다.",
    "Compliance": "컴플라이언스",
    "We ensure all your ads comply with Chinese advertising regulations and platform policies.": "모든 광고가 중국 광고 규정 및 플랫폼 정책을 준수하도록 보장합니다.",
    
    # 数据展示
    "We Help International Brands": "해외 브랜드를 돕습니다",
    "Advertise on Baidu": "바이두에 광고하기",
    "China's #1 Search Engine": "중국 1위 검색 엔진",
    "Monthly Active Users": "월간 활성 사용자",
    "Market Share": "시장 점유율",
    "Daily Searches": "일일 검색",
    "600M+": "6억+",
    "75%": "75%",
    "6B+": "60억+",
    
    # 客户区域
    "Trusted by Global Brands": "글로벌 브랜드가 신뢰",
    "Our Clients": "우리의 고객",
    "Case Studies": "사례 연구",
    "Results": "결과",
    "What Our Clients Say": "고객의 말",
    "Testimonials": "추천사",
    
    # FAQ 区域
    "Frequently Asked Questions": "자주 묻는 질문",
    "Still have questions?": "아직 질문이 있으신가요?",
    "Contact us": "문의하기",
    
    # CTA 区域
    "Ready to Get Started?": "시작할 준비가 되셨나요?",
    "Talk to Our Team": "팀에 문의하기",
    "Schedule a Call": "통화 예약",
    "Free Consultation": "무료 상담",
    "Get Started": "시작하기",
    "Contact Sales": "영업팀 문의",
    
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
    "Get in touch": "연락하기",
    
    # 语言切换器
    "Language": "언어",
    
    # 价格
    "Pricing": "요금",
    "per month": "월",
    "per year": "연",
    "Monthly": "월간",
    "Annual": "연간",
    "Most Popular": "가장 인기",
    
    # 客户案例
    "Clients": "도입 사례",
    "About": "회사 소개",
    "FAQ": "자주 묻는 질문",
    "Blog": "블로그",
    "Contact": "문의하기",
    "Services": "서비스",
    
    # 导航
    "Get Started →": "지금 시작하기 →",
    
    # 特殊文本
    "We help international agencies and brands access China's $100B+ digital advertising market with compliance, clarity, and zero guesswork — one platform, end to end.": "1000억 달러 규모의 중국 디지털 광고 시장에 해외 기업이 진출할 수 있도록 컴플라이언스, 투명성, 명확한 가이드를 제공합니다. 하나의 플랫폼, 엔드투엔드.",
    "Baidu PPC Pro": "Baidu PPC Pro",
    "Pro": "Pro",
}


def translate_text(text):
    """翻译文本"""
    for en, ko in TRANSLATIONS.items():
        text = text.replace(en, ko)
    return text


def main():
    en_path = os.path.join(PROJECT, "index.html")
    ko_path = os.path.join(PROJECT, "ko", "index.html")
    
    # 读取 EN 页面
    with open(en_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 更新 lang 属性
    html = html.replace('lang="en"', 'lang="ko"')
    
    # 翻译文本
    html = translate_text(html)
    
    # 更新链接
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
    html = re.sub(r'href="https://www\.baidumarketing\.com/"', 'href="https://www.baidumarketing.com/ko/"', html)
    
    # 更新 OG URL
    html = re.sub(r'content="https://www\.baidumarketing\.com/"', 'content="https://www.baidumarketing.com/ko/"', html)
    
    # 修复语言切换器
    html = re.sub(
        r'<button class="lang-switch-btn"[^>]*>.*?</button>',
        '<button class="lang-switch-btn" onclick="toggleLangMenu()" aria-label="Language">🇰🇷 <svg width="10" height="6" viewBox="0 0 10 6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M1 1l4 4 4-4"/></svg></button>',
        html,
        flags=re.DOTALL
    )
    
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
    
    # 写入文件
    os.makedirs(os.path.dirname(ko_path), exist_ok=True)
    with open(ko_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 翻译完成: ko/index.html ({len(html)} bytes)")


if __name__ == "__main__":
    main()
