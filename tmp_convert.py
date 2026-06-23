import re
from pathlib import Path

PROJECT = Path(r"C:\Users\HYE\WorkBuddy\20260411211839")
SLUG = "b2b-manufacturer-baidu-case-study"
CATEGORY = "strategy"

def md_to_html(md_body):
    html = md_body
    html = re.sub(r"^#### (.+)$", r"<h4>\1</h4>", html, flags=re.MULTILINE)
    html = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
    html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"^# (.+)$", r'<h1 class="article-title">\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html)
    html = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', html)
    html = re.sub(r"`(.+?)`", r"<code>\1</code>", html)
    
    lines = html.split("\n")
    out = []
    in_table = in_ol = in_ul = False
    
    for line in lines:
        t = line.strip()
        if t.startswith("|") and t.endswith("|"):
            if not in_table:
                out.append("<table>")
                in_table = True
            if re.match(r"^\|[\s\-:|]+\|$", t):
                continue
            cells = [c.strip() for c in t.strip("|").split("|")]
            tag = "th" if out[-1] == "<table>" else "td"
            out.append("<tr>" + "".join(f"<{tag}>{c}</{tag}>" for c in cells) + "</tr>")
            continue
        elif in_table:
            out.append("</table>")
            in_table = False
        
        m_ol = re.match(r"^\d+\. (.+)$", t)
        if m_ol:
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{m_ol.group(1)}</li>")
            continue
        elif in_ol and t == "":
            out.append("</ol>")
            in_ol = False
            continue
        
        m_ul = re.match(r"^- (.+)$", t)
        if m_ul:
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{m_ul.group(1)}</li>")
            continue
        elif in_ul and t == "":
            out.append("</ul>")
            in_ul = False
            continue
        
        if t.startswith("<h"):
            out.append(t)
            continue
        if t and not t.startswith("<"):
            out.append(f"<p>{t}</p>")
        elif t:
            out.append(t)
    
    if in_table: out.append("</table>")
    if in_ol: out.append("</ol>")
    if in_ul: out.append("</ul>")
    return "\n".join(out)

def build_html(lang, template_path, md_path, title, slug, date, read_time, author, cta_title, cta_text, cta_btn, cta_link):
    template = template_path.read_text(encoding="utf-8")
    md_content = md_path.read_text(encoding="utf-8")
    fm_end = md_content.index("---", md_content.index("---") + 3) + 3
    body_md = md_content[fm_end:].strip()
    body_html = md_to_html(body_md)
    
    html = template
    html = html.replace("{{TITLE}}", title)
    html = html.replace("{{SLUG}}", slug)
    html = html.replace("{{DATE}}", date)
    html = html.replace("{{READ_TIME}}", read_time)
    html = html.replace("{{AUTHOR}}", author)
    html = html.replace("{{CATEGORY}}", CATEGORY)
    html = html.replace("{{BODY}}", body_html)
    html = html.replace("{{CTA_TITLE}}", cta_title)
    html = html.replace("{{CTA_TEXT}}", cta_text)
    html = html.replace("{{CTA_BTN}}", cta_btn)
    html = html.replace("{{CTA_LINK}}", cta_link)
    return html

# EN
en_html = build_html("en",
    PROJECT / "blog" / "_template-en.html",
    Path(r"E:\Obsidian\Baidu\05-Strategy") / SLUG / f"{SLUG}-en.md",
    "From Zero to 400 Leads Per Month: How a European Manufacturer Cracked the China Market with Baidu PPC",
    SLUG, "Jun 23, 2026", "8 min", "Baidu PPC Pro Team",
    "Want to See What Baidu PPC Could Look Like for Your Company?",
    "Talk to the BPP team. We will analyze your industry, estimate realistic CPCs and lead volumes, and give you an honest assessment.",
    "Contact BPP", "/contact")
(PROJECT / "blog" / f"{SLUG}.html").write_text(en_html, encoding="utf-8")
print(f"✅ EN HTML saved ({len(en_html)} chars)")

# JA
ja_html = build_html("ja",
    PROJECT / "ja" / "blog" / "_template-ja.html",
    Path(r"E:\Obsidian\Baidu\05-Strategy") / SLUG / f"{SLUG}-ja.md",
    "ゼロから月間400件のリード獲得：ヨーロッパメーカーが百度PPCで中国市場を開拓した方法",
    SLUG, "2026年6月23日", "9 min", "Baidu PPC Pro チーム",
    "自社にとって百度PPCがどのような姿になるか見てみたいですか？",
    "BPPチームにお問い合わせください。業界を分析し、現実的なCPCとリードボリュームを推定し、正直な評価をお伝えします。",
    "BPPにお問い合わせ", "/ja/contact")
(PROJECT / "ja" / "blog" / f"{SLUG}.html").write_text(ja_html, encoding="utf-8")
print(f"✅ JA HTML saved ({len(ja_html)} chars)")

# KO
ko_html = build_html("ko",
    PROJECT / "ko" / "blog" / "_template-ko.html",
    Path(r"E:\Obsidian\Baidu\05-Strategy") / SLUG / f"{SLUG}-ko.md",
    "제로에서 월 400건 리드 확보: 유럽 제조사가 바이두 PPC로 중국 시장을 개척한 방법",
    SLUG, "2026년 6월 23일", "9 min", "Baidu PPC Pro 팀",
    "자사에 바이두 PPC가 어떤 모습일지 확인해 보시겠습니까?",
    "BPP 팀에 문의하십시오. 업종을 분석하고, 현실적인 CPC와 리드 볼륨을 추정하며, 솔직한 평가를 제공합니다.",
    "BPP에 문의", "/ko/contact")
(PROJECT / "ko" / "blog" / f"{SLUG}.html").write_text(ko_html, encoding="utf-8")
print(f"✅ KO HTML saved ({len(ko_html)} chars)")
