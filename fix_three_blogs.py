import re

files = [
    'blog/baidu-conversion-tracking-dedup.html',
    'blog/baidu-ad-performance-diagnostic-tool.html',
    'blog/baidu-ocpc-skip-data-accumulation.html'
]

for filepath in files:
    f = open(filepath, encoding='utf-8').read()
    original = f

    # 1. Upgrade stats-grid CSS to v2
    old_stats = '/* Stats Grid */\n.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 40px 0; }\n.stat-card { background: var(--gray-50); padding: 28px 20px; border-radius: var(--radius); text-align: center; border: 1px solid var(--gray-200); }\n.stat-number { font-size: 2.2rem; font-weight: 800; color: var(--blue); margin-bottom: 6px; }\n.stat-label { font-size: .85rem; color: var(--gray-600); }'

    new_stats = """/* Stats Grid - Enhanced v2 */
.stats-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; margin: 40px 0; }
.stat-card {
  background: linear-gradient(180deg, #FFFFFF 0%, #EEF0FF 100%);
  padding: 28px 16px 28px; border-radius: 16px; text-align: center;
  border: 1.5px solid #E5E7EB; position: relative; overflow: hidden;
  transition: transform .3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow .3s ease, border-color .3s ease;
}
.stat-card::before {
  content: ''; position: absolute; top: 0; left: 50%; transform: translateX(-50%);
  width: 60%; height: 4px; border-radius: 0 0 4px 4px;
  background: linear-gradient(135deg, #2932E1, #4F46E5); opacity: 0;
  transition: opacity .3s ease, width .3s cubic-bezier(0.16, 1, 0.3, 1);
}
.stat-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(41,50,225,.22); border-color: #2932E1;
}
.stat-card:hover::before { opacity: 1; width: 85%; }
.stat-value {
  font-size: 2rem; font-weight: 900; line-height: 1.15;
  background: linear-gradient(135deg, #2932E1 0%, #4F46E5 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text; margin-bottom: 6px; letter-spacing: -.02em;
  word-break: break-word; overflow-wrap: break-word;
}
.stat-card:nth-child(1) .stat-value { background: linear-gradient(135deg, #2932E1, #4F46E5); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.stat-card:nth-child(2) .stat-value { background: linear-gradient(135deg, #4F46E5, #7C3AED); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.stat-label { font-size: .92rem; font-weight: 700; color: #111827; margin-bottom: 5px; text-transform: uppercase; letter-spacing: .04em; }
@media (max-width: 768px) { .stats-grid { grid-template-columns: 1fr; } }"""

    f = f.replace(old_stats, new_stats)

    # 2. Fix takeaway-box CSS
    old_takeaway = """/* Takeaway */
.takeaway-box { background: var(--gradient-brand); color: #fff; padding: 28px 32px; border-radius: var(--radius-lg); margin: 40px 0; }
.takeaway-box h3 { font-size: 1.1rem; font-weight: 700; margin-bottom: 12px; color: #fff; }
.takeaway-box strong { display: block; font-size: .9rem; text-transform: uppercase; letter-spacing: .5px; margin-bottom: 10px; color: #fff; }
.takeaway-box p { margin-bottom: 0 !important; color: #fff !important; font-size: 1.05rem !important; line-height: 1.7 !important; }
.takeaway-box ul { margin: 12px 0 0 0; padding-left: 20px; color: #fff !important; }
.takeaway-box ul li { color: #fff !important; margin-bottom: 6px; }"""

    new_takeaway = """/* Takeaway - Enhanced */
.takeaway-box {
  background: linear-gradient(180deg, #FFFFFF 0%, #EEF0FF 100%);
  border: 1.5px solid #E5E7EB; border-radius: 16px; padding: 28px 32px; margin: 32px 0;
  position: relative; overflow: hidden;
  transition: transform .25s ease, box-shadow .25s ease;
}
.takeaway-box::before {
  content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%;
  background: linear-gradient(135deg, #2932E1, #4F46E5); border-radius: 4px 0 0 4px;
}
.takeaway-box:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(41,50,225,.15); }
.takeaway-box h3 { font-size: 1.1rem; font-weight: 700; margin-bottom: 12px; color: #2932E1; display: flex; align-items: center; gap: 8px; }
.takeaway-box ul { list-style: none; display: flex; flex-direction: column; gap: 8px; padding-left: 0; margin: 12px 0 0 0; }
.takeaway-box ul li { font-size: .9rem; line-height: 1.6; padding-left: 24px; position: relative; color: #374151; }
.takeaway-box ul li::before { content: '\\2713'; position: absolute; left: 0; color: #2932E1; font-weight: 700; }
.takeaway-box ul li strong { color: #111827; font-weight: 700; }"""

    f = f.replace(old_takeaway, new_takeaway)

    # 3. Fix CTA box CSS variables
    old_cta = """/* CTA Box */
.cta-box { background: var(--gradient-brand); color: #fff; padding: 48px; border-radius: var(--radius-xl); text-align: center; margin: 50px 0; }
.cta-box h2, .cta-box h3 { font-size: 2rem !important; font-weight: 700 !important; margin-bottom: 16px !important; color: #fff !important; }
.cta-box p { font-size: 1.05rem !important; margin-bottom: 30px !important; opacity: .9; color: #fff !important; }
.cta-btn { display: inline-block; background: #fff; color: var(--blue); padding: 14px 36px; border-radius: 8px; font-weight: 600; font-size: 1rem; transition: transform var(--transition-base), box-shadow var(--transition-base); }
.cta-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,.2); }"""

    new_cta = """/* CTA Box */
.cta-box { background: linear-gradient(135deg, #2932E1 0%, #4F46E5 100%); color: #fff; padding: 48px; border-radius: 16px; text-align: center; margin: 50px 0; }
.cta-box h2, .cta-box h3 { font-size: 2rem !important; font-weight: 700 !important; margin-bottom: 16px !important; color: #fff !important; }
.cta-box p { font-size: 1.05rem !important; margin-bottom: 30px !important; opacity: .9; color: #fff !important; }
.cta-btn { display: inline-block; background: #fff; color: #2932E1; padding: 14px 36px; border-radius: 8px; font-weight: 600; font-size: 1rem; transition: transform .2s, box-shadow .2s; }
.cta-btn:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,.2); }"""

    f = f.replace(old_cta, new_cta)

    # 4. Fix dark mode overrides for stat-card
    old_dark = '[data-theme="dark"] .stat-card { background: var(--gray-100); border-color: var(--gray-200); }'
    new_dark = """[data-theme="dark"] .stat-card { background: linear-gradient(180deg, var(--gray-100) 0%, rgba(99,102,241,.06) 100%); border-color: var(--gray-200); }
[data-theme="dark"] .stat-label { color: var(--gray-700); }
[data-theme="dark"] .stat-value { background: linear-gradient(135deg, #818CF8, #A78BFA); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }"""

    f = f.replace(old_dark, new_dark)

    # 5. Fix dark mode for takeaway-box-box -> takeaway-box
    f = f.replace('[data-theme="dark"] .takeaway-box-box {', '[data-theme="dark"] .takeaway-box {')
    f = f.replace('[data-theme="dark"] .takeaway-box-box ul li', '[data-theme="dark"] .takeaway-box ul li')

    # 6. Fix HTML: stat-number -> stat-value
    f = f.replace('class="stat-number"', 'class="stat-value"')

    # 7. Remove dead takeaway-box-box CSS block
    old_dead = """    .takeaway-box-box { background: linear-gradient(135deg, #EEF0FF 0%, #F5F3FF 100%); border: 1px solid #C7D2FE; border-radius: 12px; padding: 24px; margin: 32px 0; }
    .takeaway-box-box h3 { font-size: 1rem; font-weight: 700; margin-bottom: 12px; color: var(--blue); display: flex; align-items: center; gap: 8px; }
    .takeaway-box-box ul { list-style: none; display: flex; flex-direction: column; gap: 8px; padding-left: 0; margin: 0; }
    .takeaway-box-box ul li { font-size: .9rem; line-height: 1.6; padding-left: 20px; position: relative; }
    .takeaway-box-box ul li::before { content: '\\2713'; position: absolute; left: 0; color: var(--blue); font-weight: 700; }"""
    f = f.replace(old_dead, '')

    if f != original:
        open(filepath, 'w', encoding='utf-8').write(f)
        print(f'Fixed: {filepath}')
    else:
        print(f'No changes: {filepath}')
