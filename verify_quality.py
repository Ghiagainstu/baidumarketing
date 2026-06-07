"""
Translation Quality Check: compare EN vs JA vs KO
Samples articles that exist in all 3 languages
"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

VAULT = 'E:/Obsidian/Baidu'
PROJECT = 'c:/Users/HYE/WorkBuddy/20260411211839'

def extract_body(content):
    """Extract body after frontmatter"""
    if content.startswith('---'):
        end = content.find('---', 3)
        if end > 0:
            return content[end+3:].strip()
    return content.strip()

def count_words(text):
    return len(text.split())

def count_chars(text):
    return len(text.replace(' ', '').replace('\n', ''))

def check_key_terms(text, terms, language):
    """Check if key terms are translated/kept correctly"""
    found = {}
    for en_term, (ja_term, ko_term) in terms.items():
        idx = 'ja' if language == 'ja' else 'ko'
        expected = ja_term if language == 'ja' else ko_term
        if en_term.lower() in text.lower():
            found[en_term] = 'EN_term_found_in_translation'
    return found

def check_brand_voice(text, language):
    """Check BPP brand voice compliance"""
    issues = []
    
    # AI-typical words
    ai_words = ['delve', 'robust', 'leverage', 'game-changer', 'crucial', 
                'seamless', 'revolutionize', 'unlock', 'harness', 'empower']
    for w in ai_words:
        if w.lower() in text.lower():
            issues.append(f'AI word: "{w}"')
    
    # CTA check
    if language == 'ja':
        if '/contact' in text:
            issues.append('JA uses /contact instead of /ja/contact')
    elif language == 'ko':
        if '/contact' in text and '/ko/contact' not in text:
            issues.append('KO uses /contact instead of /ko/contact')
    
    return issues

# Sample articles with all 3 languages
samples = [
    # From subfolders (✅ bpp- prefix)
    ('03-Search-Ads', '✅ bpp-10-why-baidu-ads-work'),
    ('03-Search-Ads', '✅ bpp-11-ocpc-explained'),
    ('03-Search-Ads', '✅ bpp-12-cpm-ocpm-ecpm'),
    ('04-Feed-Ads', '✅ bpp-22-how-baidu-feed-ads-work'),
    ('05-Strategy', '✅ bpp-26-keyword-research-baidu'),
    ('08-Baidu-Basics', '✅ bpp-01-can-i-do-baidu-ppc'),
    ('10-ByteDance-Douyin', '✅ bpp-01-major-shift-ocean-engine'),
    ('12-Operations-Compliance', '✅ bpp-04-invalid-click-protection'),
]

print("=" * 100)
print("TRANSLATION QUALITY SAMPLE CHECK")
print("=" * 100)

for folder, base_name in samples:
    print(f"\n{'─' * 100}")
    print(f"SAMPLE: {base_name}")
    print(f"{'─' * 100}")
    
    # Read EN
    en_path = os.path.join(VAULT, folder, f'{base_name}.md')
    if not os.path.exists(en_path):
        en_path = os.path.join(VAULT, folder, f'{base_name}-en.md')
    
    ja_path = os.path.join(VAULT, folder, f'{base_name}-ja.md')
    ko_path = os.path.join(VAULT, folder, f'{base_name}-ko.md')
    
    texts = {}
    for lang, path in [('EN', en_path), ('JA', ja_path), ('KO', ko_path)]:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            body = extract_body(content)
            texts[lang] = body
        else:
            texts[lang] = None
    
    # Basic stats
    print(f"\n  {'Language':<8s} {'Words/Chars':<15s} {'Paragraphs':<12s} {'Lines':<8s} {'File exists':<12s}")
    print(f"  {'─'*8} {'─'*15} {'─'*12} {'─'*8} {'─'*12}")
    
    for lang in ['EN', 'JA', 'KO']:
        if texts[lang]:
            paras = len([p for p in texts[lang].split('\n\n') if p.strip()])
            lines = len(texts[lang].split('\n'))
            if lang == 'EN':
                count = f"{count_words(texts[lang])} words"
            else:
                count = f"{count_chars(texts[lang])} chars"
            print(f"  {lang:<8s} {count:<15s} {paras:<12d} {lines:<8d} ✓")
        else:
            print(f"  {lang:<8s} {'─':<15s} {'─':<12s} {'─':<8s} ✗ MISSING")
    
    # Translation ratio check (JA/EN, KO/EN char ratio)
    if texts['EN'] and texts['JA']:
        en_words = count_words(texts['EN'])
        ja_chars = count_chars(texts['JA'])
        ratio = ja_chars / max(en_words, 1)
        status = 'OK' if 1.0 <= ratio <= 2.5 else ('SHORT' if ratio < 1.0 else 'LONG')
        print(f"  JA/EN ratio: {ja_chars}/{en_words} = {ratio:.1f} [{status}]")
    
    if texts['EN'] and texts['KO']:
        en_words = count_words(texts['EN'])
        ko_chars = count_chars(texts['KO'])
        ratio = ko_chars / max(en_words, 1)
        status = 'OK' if 1.0 <= ratio <= 2.5 else ('SHORT' if ratio < 1.0 else 'LONG')
        print(f"  KO/EN ratio: {ko_chars}/{en_words} = {ratio:.1f} [{status}]")
    
    # Brand voice check
    if texts['JA']:
        ja_issues = check_brand_voice(texts['JA'], 'ja')
        if ja_issues:
            print(f"  JA Issues: {ja_issues}")
        else:
            print(f"  JA Brand Voice: OK")
    
    if texts['KO']:
        ko_issues = check_brand_voice(texts['KO'], 'ko')
        if ko_issues:
            print(f"  KO Issues: {ko_issues}")
        else:
            print(f"  KO Brand Voice: OK")
    
    # Quick check: does translation preserve key structure elements?
    if texts['EN']:
        en_has_h2 = texts['EN'].count('\n## ') 
        en_has_list = texts['EN'].count('\n- ')
        en_has_bold = texts['EN'].count('**')
        
        if texts['JA']:
            ja_has_h2 = texts['JA'].count('\n## ')
            ja_has_list = texts['JA'].count('\n- ')
            ja_has_bold = texts['JA'].count('**')
            h2_diff = abs(en_has_h2 - ja_has_h2)
            list_diff = abs(en_has_list - ja_has_list)
            issues = []
            if h2_diff > 1: issues.append(f'H2 mismatch ({en_has_h2} vs {ja_has_h2})')
            if list_diff > 3: issues.append(f'List mismatch ({en_has_list} vs {ja_has_list})')
            if issues:
                print(f"  JA Structure: {', '.join(issues)}")
            else:
                print(f"  JA Structure: OK (H2: {en_has_h2}/{ja_has_h2}, Lists: {en_has_list}/{ja_has_list})")
        
        if texts['KO']:
            ko_has_h2 = texts['KO'].count('\n## ')
            ko_has_list = texts['KO'].count('\n- ')
            h2_diff = abs(en_has_h2 - ko_has_h2)
            list_diff_ko = abs(en_has_list - ko_has_list)
            issues = []
            if h2_diff > 1: issues.append(f'H2 mismatch ({en_has_h2} vs {ko_has_h2})')
            if list_diff_ko > 3: issues.append(f'List mismatch ({en_has_list} vs {ko_has_list})')
            if issues:
                print(f"  KO Structure: {', '.join(issues)}")
            else:
                print(f"  KO Structure: OK (H2: {en_has_h2}/{ko_has_h2}, Lists: {en_has_list}/{ko_has_list})")

print("\n" + "=" * 100)
print("SUMMARY")
print("=" * 100)
