import re

path = 'C:/Users/HYE/WorkBuddy/20260411211839/ja/china-geo.html'
content = open(path, encoding='utf-8').read()

replacements = [
    # 1. Section sub: What is GEO
    ("ジェネレーティブエンジン最適化 (GEO) is the practice of optimizing content so AI-powered search engines — like Baidu's ERNIE, ByteDance（字节跳动）'s Doubao, DeepSeek, and Alibaba's Tongyi Qianwen — reference your brand in their answers.",
     "ジェネレーティブエンジン最適化（GEO）とは、百度のERNIE、ByteDance（字節跳動）のDoubao、DeepSeek、阿里巴巴の通義千問など、AI搭載の検索エンジンが回答の中であなたのブランドを引用するようコンテンツを最適化する実践です。"),

    # 2. Intro card paragraph 1
    ("Think of GEO as the evolution of SEO. Traditional search engines return a list of blue links. Generative engines return a <strong>curated answer</strong> — a paragraph, a comparison, a recommendation — written by AI in real time. If your brand is not in that answer, you are invisible to 660 million monthly active users.",
     "GEOはSEOの進化形と考えてください。従来の検索エンジンは青いリンクのリストを返します。ジェネレーティブエンジンは、AIがリアルタイムで作成した<strong>厳選された回答</strong>——段落、比較、おすすめ——を返します。もしその回答にあなたのブランドが含まれていなければ、6億6,000万人の月間アクティブユーザーから見もらえません。"),

    # 3. Intro card paragraph 2
    ("For international brands targeting China, GEO is particularly critical. Chinese consumers are early and enthusiastic adopters of AI tools. They ask AI for product recommendations, brand comparisons, and purchasing advice — often before ever visiting a search engine. If your brand's content is not optimized for AI retrieval, you lose the battle before the first click.",
     "中国をターゲットとする海外ブランドにとって、GEOは特に重要です。中国の消費者はAIツールの熱心なアーリーアダプターです。検索エンジンを訪れる前に、AIに製品推薦、ブランド比較、購入アドバイスを求めます。もしあなたのブランドのコンテンツがAI検索向けに最適化されていなければ、最初のクリックの前に戦いに負けてしまいます。"),

    # 4. Stat labels
    ("of Chinese Users Trust AI Answers for Purchases",
     "の中国ユーザーが購入判断にAIの回答を信頼"),
    ("of Gen Z in China Use AI Assistants Weekly",
     "の中国Z世代が毎週AIアシスタントを利用"),

    # 5. China AI Trends section-sub
    ("China has emerged as a global leader in generative AI adoption. Here are the trends shaping the landscape for advertisers and brands.",
     "中国はジェネレーティブAI採用の世界的リーダーとして台頭しました。広告主とブランドの展望を形作るトレンドを紹介します。"),

    # 6. Trend items
    ("Explosive User Growth",
     "爆発的なユーザー成長"),
    ("China's AI-native app user base grew from virtually zero to 660M+ MAU in less than 3 years. The speed of adoption outpaces any previous technology wave — mobile, social, or e-commerce.",
     "中国のAIネイティブアプリのユーザーは、わずか3年でほぼゼロから6億6,000万MAU以上に成長しました。モバイル、ソーシャル、Eコマースいずれの技術波よりも採用スピードが速いです。"),

    ("Tech Giants Compete",
     "テック巨頭の競争"),
    ("Baidu, ByteDance（字节跳动）, Alibaba, and Tencent are all racing to dominate the AI assistant market. Each brings a unique ecosystem advantage — Baidu's search data, ByteDance（字节跳动）'s content, Alibaba's commerce.",
     "百度、ByteDance（字節跳動）、阿里巴巴、騰訊がAIアシスタント市場の支配を競っています。それぞれ独自のエコシステム優位性を持ちます——百度の検索データ、ByteDanceのコンテンツ、阿里巴巴のコマース。"),

    ("AI-First Consumer Behavior",
     "AIファーストの消費者行動"),
    ("Chinese consumers increasingly start their purchase journey with an AI prompt rather than a search query. For brands, appearing in AI answers is becoming as important as ranking #1 on Baidu.",
     "中国の消費者は検索クエリではなく、AIプロンプトから購入ジャーニーを始めることが増えてきました。ブランドにとって、AI回答に表示されることが百度で1位にランクインすることと同じくらい重要になりつつあります。"),

    ("GEO Becomes a Budget Line",
     "GEOが予算項目に"),
    ("Forward-looking brands are allocating 10-15% of their China digital marketing budget to GEO content production and AI answer optimization — a line item that did not exist 18 months ago.",
     "先進的なブランドは、中国デジタルマーケティング予算の10〜15%をGEOコンテンツ制作とAI回答最適化に割り当てています——18ヶ月前には存在しなかった予算項目です。"),

    # 7. Key Insight callout
    ("💡 Key Insight",
     "💡 重要な洞察"),
    ("GEO is not a replacement for traditional Baidu SEM and SEO — it is a complement. The most effective China digital strategies invest across all three channels to capture users at every stage of the AI-funnel.",
     "GEOは従来の百度SEMやSEOの代替ではなく、補完です。最も効果的な中国デジタル戦略は、AIファネルの各段階でユーザーを獲得するために3つのチャネルすべてに投資します。"),

    # 8. Platform section-sub
    ("Each platform has unique strengths, user demographics, and content preferences. Understanding these differences is the foundation of an effective GEO strategy.",
     "各プラットフォームには独自の強み、ユーザー層、コンテンツ嗜好があります。この違いを理解することが、効果的なGEO戦略の基盤です。"),

    # 9. Platform card descriptions
    ("Deeply integrated with Baidu Search. ERNIE generates answers powered by real-time search data. Best platform for <strong>brand awareness</strong> and <strong>purchase intent</strong> queries. Users often ask ERNIE for product comparisons, reviews, and brand recommendations.",
     "百度検索と深く統合されています。ERNIEはリアルタイムの検索データを活用した回答を生成します。<strong>ブランド認知</strong>や<strong>購入意図</strong>のクエリに最適なプラットフォームです。ユーザーは製品比較、レビュー、ブランド推薦をERNIEによく質問します。"),

    ("ByteDance（字节跳动）'s flagship AI assistant, integrated with Douyin (TikTok China). 226M MAU makes it China's most popular standalone AI app. 最適化d for <strong>entertainment</strong>, <strong>lifestyle</strong>, and <strong>shopping</strong> queries. Voice interaction is a key differentiator.",
     "ByteDance（字節跳動）のフラッグシップAIアシスタントで、Douyin（TikTok中国版）と統合されています。2億2,600万MAUは中国で最も人気のスタンドアロンAIアプリです。<strong>エンターテインメント</strong>、<strong>ライフスタイル</strong>、<strong>ショッピング</strong>クエリに最適化。音声インタラクションが大きな差別化要因です。"),

    ("The open-source reasoning model that took China by storm. DeepSeek excels at <strong>logical reasoning</strong>, <strong>technical analysis</strong>, and <strong>in-depth research</strong> queries. Popular among professionals, developers, and educated users making complex purchasing decisions.",
     "中国を席巻したオープンソース推論モデルです。DeepSeekは<strong>論理的推論</strong>、<strong>技術分析</strong>、<strong>詳細なリサーチ</strong>クエリに優れています。プロフェッショナル、開発者、複雑な購入判断を行う教育レベルの高いユーザーに人気です。"),

    ("Alibaba's multi-modal AI model, integrated with Taobao and Tmall. Uniquely positioned for <strong>product discovery</strong> and <strong>e-commerce</strong> queries. Users ask Tongyi for product recommendations, price comparisons, and shopping guidance.",
     "阿里巴巴のマルチモーダルAIモデルで、淘宝と天猫と統合されています。<strong>製品発見</strong>と<strong>Eコマース</strong>クエリに独自のポジションを持ちます。ユーザーは通義に製品推薦、価格比較、ショッピングガイドを求めます。"),

    # 10. Comparison table headers
    ("<th>Platform</th>", "<th>プラットフォーム</th>"),
    ("<th>Company</th>", "<th>運営会社</th>"),
    ("<th>Best For</th>", "<th>最適用途</th>"),
    ("<th>Content Preference</th>", "<th>コンテンツ嗜好</th>"),

    # Table rows
    ("<td>Brand awareness, purchase intent</td>", "<td>ブランド認知、購入意図</td>"),
    ("<td>Factual, authoritative, structured data</td>", "<td>事実ベース、権威性、構造化データ</td>"),
    ("<td>Entertainment, lifestyle, shopping</td>", "<td>エンターテインメント、ライフスタイル、ショッピング</td>"),
    ("<td>Engaging, visual, conversational</td>", "<td>魅力的、ビジュアル、対話型</td>"),
    ("<td>Technical analysis, research</td>", "<td>技術分析、リサーチ</td>"),
    ("<td>In-depth, logical, citation-rich</td>", "<td>詳細、論理的、引用豊富</td>"),
    ("<td>E-commerce, product discovery</td>", "<td>Eコマース、製品発見</td>"),
    ("<td>Product specs, reviews, comparisons</td>", "<td>製品スペック、レビュー、比較</td>"),
    ("<td>Independent</td>", "<td>独立系</td>"),

    # 11. What This Means callout
    ("✅ What This Means for Your Brand",
     "✅ あなたのブランドへの影響"),
    ("Each platform pulls content from different sources. Baidu ERNIE favors Baidu-indexed pages. Doubao favors Douyin/ByteDance（字节跳动） content. Tongyi leverages Alibaba's product database. An effective GEO strategy must distribute brand content across all four ecosystems — not just your website.",
     "各プラットフォームは異なるソースからコンテンツを取得します。百度ERNIEは百度インデックスページを優先し、DoubaoはDouyin/ByteDanceのコンテンツを優先し、通義は阿里巴巴の製品データベースを活用します。効果的なGEO戦略は、ウェブサイトだけでなく4つのエコシステム全体にブランドコンテンツを配布する必要があります。"),

    # 12. How We Help section
    ("Our Approach", "私たちのアプローチ"),
    ("How We Help Brands Win at GEO",
     "GEOでブランドが勝つための支援方法"),
    ("Our GEO service combines content optimization, platform-specific distribution, and performance tracking to ensure your brand appears in AI answers across China's top generative engines.",
     "GEOサービスはコンテンツ最適化、プラットフォーム別の配信、パフォーマンス追跡を組み合わせ、中国の主要ジェネレーティブエンジン全体でブランドがAI回答に表示されるようにします。"),

    # 13. Four steps
    ("1. Content 監査 &amp; Gap Analysis", "1. コンテンツ監査＆ギャップ分析"),
    ("We analyze your existing content against the types of questions each AI platform answers. We identify gaps where your brand is invisible and prioritize content production.",
     "各AIプラットフォームが回答する質問の種類に対して既存のコンテンツを分析し、ブランドが表示されていないギャップを特定し、コンテンツ制作の優先順位を付けます。"),

    ("2. Platform-Specific Optimization", "2. プラットフォーム別最適化"),
    ("Each AI platform has unique source preferences and answer formats. We optimize your content for Baidu's structured data preferences, Doubao's conversational style, DeepSeek's citation requirements, and Tongyi's product focus.",
     "各AIプラットフォームには独自のソース嗜好と回答形式があります。百度の構造化データ嗜好、Doubaoの会話型スタイル、DeepSeekの引用要件、通義の製品焦点に合わせてコンテンツを最適化します。"),

    ("3. Multi-Channel Distribution", "3. マルチチャネル配信"),
    ("We distribute your brand content across the ecosystems each AI platform trusts: Baidu Zhidao, Baidu Baike, Douyin, Taobao product pages, and authoritative third-party review sites.",
     "各AIプラットフォームが信頼するエコシステム全体にブランドコンテンツを配布します：百度知道、百度百科、Douyin、淘宝製品ページ、および権威ある第三者レビューサイト。"),

    ("4. 監視ing &amp; Iteration", "4. 監視＆改善"),
    ("AI answer formats evolve rapidly. We track which queries trigger your brand mentions, measure AI answer sentiment, and adjust content strategy monthly.",
     "AIの回答形式は急速に進化します。ブランド言及をトリガーするクエリの追跡、AI回答のセンチメント測定、コンテンツ戦略の月次調整を行います。"),

    # 14. Key Takeaways
    ("📋 Key Takeaways", "📋 重要ポイント"),
    ("China's top 4 AI platforms serve 660M+ monthly active users — a market no international brand can afford to ignore",
     "中国のトップ4 AIプラットフォームは6億6,000万MAU以上のユーザーにサービス——海外ブランドが無視できない市場"),
    ("GEO (ジェネレーティブエンジン最適化) is the practice of optimizing brand content to appear in AI-generated answers",
     "GEO（ジェネレーティブエンジン最適化）は、AI生成回答にブランドコンテンツを表示させるための最適化実践"),
    ("Each platform has unique content preferences — a one-size-fits-all approach does not work",
     "各プラットフォームには独自のコンテンツ嗜好がある——ワンサイズフィッツオールは機能しない"),
    ("GEO complements traditional Baidu SEM and SEO, not replaces them",
     "GEOは従来の百度SEMやSEOを補完し、代替するものではない"),
    ("The most effective strategy combines content optimization across all four platforms with paid search visibility",
     "最も効果的な戦略は、4つのプラットフォーム全体でのコンテンツ最適化と有料検索の可視性を組み合わせるもの"),
    ("AI consumption behavior in China is growing faster than any previous digital channel — early movers gain disproportionate advantage",
     "中国でのAI消費行動は従来のデジタルチャネルよりも速く成長——アーリームーバーが大きな優位性を獲得"),
]

# Apply replacements
count = 0
unmatched = []
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        count += 1
    else:
        unmatched.append(old[:60])

print(f'Applied {count}/{len(replacements)} translations')
if unmatched:
    print(f'Unmatched ({len(unmatched)}):')
    for u in unmatched:
        print(f'  - {u}')

# Fix JSON-LD: the script tag has JS code inside it (lines 730-752)
# Find the broken JSON-LD and fix it
jsonld_pattern = re.compile(
    r'(<script type="application/ld\+json">.*?)function toggleLangMenu',
    re.DOTALL
)
m = jsonld_pattern.search(content)
if m:
    jsonld_content = m.group(1).strip()
    # Close the JSON-LD script, then start a new script for the JS
    content = content[:m.start()] + jsonld_content + '\n</script>\n\n<script>\nfunction toggleLangMenu' + content[m.end():]
    print('Fixed JSON-LD script tag (separated JS code)')

# Fix JSON-LD url
content = content.replace(
    '"url": "https://www.baidumarketing.com/china-geo"',
    '"url": "https://www.baidumarketing.com/ja/china-geo"'
)

# Fix JSON-LD description
old_desc = '"description": "China\'s AI platforms reach over 660M monthly active users. Learn how ジェネレーティブエンジン最適化 (GEO) helps your brand appear in AI answers."'
new_desc = '"description": "中国のAIプラットフォームは6億6,000万以上のMAUにリーチ。ジェネレーティブエンジン最適化（GEO）がどのようにブランドをAI回答に表示させるかを解説します。"'
content = content.replace(old_desc, new_desc)

open(path, 'w', encoding='utf-8').write(content)
print('File saved.')
