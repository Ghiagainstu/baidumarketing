#!/usr/bin/env python3
"""
fix_blog_ko.py — 批量修复韩语博客页面中的英文文本
"""
import re
import os
import glob

PROJECT = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(PROJECT, "ko", "blog")

# 批量替换映射
REPLACEMENTS = {
    # 导航链接
    '>Why Baidu PPC Pro<': '>바이두 PPC Pro란<',
    '>Services<': '>서비스<',
    '>Pricing<': '>요금<',
    '>Clients<': '>도입 사례<',
    '>FAQ<': '>자주 묻는 질문<',
    '>About<': '>회사 소개<',
    '>Blog<': '>블로그<',
    '>Contact<': '>문의하기<',
    '>Get Started →<': '>지금 시작하기 →<',
    
    # Footer
    '>Quick Links<': '>바로가기<',
    '>About Us<': '>회사 소개<',
    '>Submit a Request<': '>문의 접수<',
    '>Legal<': '>법적 고지<',
    '>Privacy Policy<': '>개인정보 처리방침<',
    '>Terms of Service<': '>이용약관<',
    
    # Footer 描述
    '>We help international agencies and brands access China\'s digital advertising market.<':
        '>1000억 달러 규모의 중국 디지털 광고 시장에 해외 기업이 진출할 수 있도록 지원합니다.<',
    '>We help international agencies and brands access China\'s digital advertising market with compliance, clarity, and zero guesswork.<':
        '>컴플라이언스, 투명성, 명확한 가이드로 해외 기업이 중국 디지털 광고 시장에 진출할 수 있도록 지원합니다.<',
    
    # CTA
    '>Ready to get started?': '>시작할 준비가 되셨나요?',
    'Ready to get started?': '시작할 준비가 되셨나요?',
    
    # Read time
    '>2 min read<': '>2분 읽기<',
    '>3 min read<': '>3분 읽기<',
    '>4 min read<': '>4분 읽기<',
    '>5 min read<': '>5분 읽기<',
    '>6 min read<': '>6분 읽기<',
    '>7 min read<': '>7분 읽기<',
    '>8 min read<': '>8분 읽기<',
    '>9 min read<': '>9분 읽기<',
    '>10 min read<': '>10분 읽기<',
    
    # Category
    '>feed<': '>피드 광고<',
    '>search<': '>검색 광고<',
    '>strategy<': '>전략<',
    '>platform<': '>플랫폼<',
    '>landing<': '>랜딩 페이지<',
    
    # 面包屑
    '>Home<': '>홈<',
    '/ Blog': '/ 블로그',
    
    # 常见短语
    'Professional management ensures compliance and optimal performance':
        '전문적인 관리가 컴플라이언스와 최적의 성과를 보장합니다',
    'Overseas advertisers can benefit from these updates with the right partner':
        '해외 광고주는 적절한 파트너와 함께 이러한 업데이트의 이점을 누릴 수 있습니다',
}


def fix_file(filepath):
    """修复单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 应用替换
    for old, new in REPLACEMENTS.items():
        content = content.replace(old, new)
    
    # 修复 min read（带数字的）
    content = re.sub(r'>(\d+) min read<', r'>\1분 읽기<', content)
    
    # 修复 Ready to get started
    content = content.replace('Ready to get started?', '시작할 준비가 되셨나요?')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    print("=" * 60)
    print("🇰🇷 批量修复韩语博客页面")
    print("=" * 60)
    
    files = glob.glob(os.path.join(BLOG_DIR, "*.html"))
    files = [f for f in files if "_template" not in f]
    
    fixed = 0
    for filepath in sorted(files):
        basename = os.path.basename(filepath)
        if fix_file(filepath):
            print(f"  ✓ Fixed: {basename}")
            fixed += 1
        else:
            print(f"  - No changes: {basename}")
    
    print("=" * 60)
    print(f"✅ 完成: {fixed}/{len(files)} 个文件已修复")
    print("=" * 60)


if __name__ == "__main__":
    main()
