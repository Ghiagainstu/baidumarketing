#!/usr/bin/env python3
"""
fix_residual_ko.py — 修复 index.html 中残留的英文文本
"""
import re
import os

PROJECT = os.path.dirname(os.path.abspath(__file__))

# 残留文本翻译
RESIDUAL_TRANSLATIONS = {
    # 带空格的文本
    "Without the ": "없이 ",
    " Active": " 활성",
    "From ": "시작가 ",
    "Over ": "이상 ",
    " of combined experience in Chinese digital advertising. Based in Shanghai, working with clients worldwide.": "년 이상의 중국 디지털 광고 경험. 상하이 기반, 전 세계 고객과 협력.",
    " in programmatic advertising, specializing in DSP technology. Trilingual in English, Mandarin, and Cantonese. He bridges European and Chinese markets, helping international companies navigate China's programmatic buying with practical, culturally-aware strategies.": "년 이상의 프로그래매틱 광고 경험, DSP 기술 전문. 영어, 중국어, 광둥어 삼중언어. 유럽과 중국 시장을 연결하며, 실용적이고 문화적으로 인식된 전략으로 국제 기업이 중국의 프로그래매틱 바잉을 탐색하도록 돕습니다.",
    " helping international companies navigate China's digital advertising landscape. Fluent English, expert at bridging cultural and technical gaps between global brands and Chinese platforms.": "년 이상의 국제 기업이 중국의 디지털 광고 환경을 탐색하도록 지원. 유창한 영어, 글로벌 브랜드와 중국 플랫폼 사이의 문화적/기술적 격차를 연결하는 전문가.",
    " minimum CNY 2,400": " 최소 2,400위안",
    " starting from USD 100, which includes document translation, document review, and submission handling": " USD 100부터, 서류 번역, 서류 검토, 제출 처리 포함",
    " You are charged only when a user clicks your ad.": " 사용자가 광고를 클릭할 때만 과금됩니다.",
    " Regulated industries such as healthcare and finance must:": " 의료 및 금융과 같은 규제 산업은 다음을 해야 합니다:",
    "All prices in USD. Custom enterprise quotes available for budgets over $50,000/month. ": "모든 가격은 USD입니다. 월 $50,000 이상 예산에 대한 맞춤형 기업 견적 가능. ",
    "Thank you for reaching out. Our team will review your request and reply to ": "연락해 주셔서 감사합니다. 팀이 요청을 검토하고 응답합니다 ",
    " within one business day.": " 1영업일 이내에.",
    
    # 其他残留
    "8.2K": "8.2K",
    "평균 CPC": "평균 CPC",
    "CTR": "CTR",
    "CPC": "CPC",
    "oCPC": "oCPC",
    "JM": "JM",
    "James Mitchell": "James Mitchell",
    "Benny Cheuk": "Benny Cheuk",
    "Yan Huo": "Yan Huo",
}


def main():
    ko_path = os.path.join(PROJECT, "ko", "index.html")
    
    with open(ko_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 应用残留翻译
    for original, translated in RESIDUAL_TRANSLATIONS.items():
        # 转义特殊字符
        escaped = re.escape(original)
        # 替换标签之间的文本
        html = re.sub(r'>' + escaped + r'<', '>' + translated + '<', html)
    
    with open(ko_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 残留文本修复完成: ko/index.html ({len(html)} bytes)")


if __name__ == "__main__":
    main()
