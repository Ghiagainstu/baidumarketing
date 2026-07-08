import sys

lang = sys.argv[1]
prefix = sys.argv[2]

path = f'{prefix}/blog/waic-2026-preview-china-ai-direction.html'
with open(path, encoding='utf-8') as f:
    c = f.read()

# Add platform-pills CSS
if 'platform-pills' not in c:
    c = c.replace('</style>', '''
    .platform-pills { display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0; }
    .platform-pill { display: flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: 999px; font-size: .8rem; font-weight: 600; border: 1px solid; }
    .platform-pill.baidu { background: #EEF0FF; border-color: #A5B4FC; color: #3730A3; }
    .platform-pill.wenxin { background: #ECFDF5; border-color: #6EE7B7; color: #065F46; }
    .platform-pill.deepseek { background: #F5F3FF; border-color: #C4B5FD; color: #5B21B6; }
    .platform-pill.douyin { background: #FFF1F2; border-color: #FDA4AF; color: #9F1239; }
    [data-theme="dark"] .platform-pill.baidu { background: rgba(55,48,163,.15); border-color: #6366F1; color: #A5B4FC; }
    [data-theme="dark"] .platform-pill.wenxin { background: rgba(6,95,70,.15); border-color: #10B981; color: #6EE7B7; }
    [data-theme="dark"] .platform-pill.deepseek { background: rgba(91,33,182,.15); border-color: #8B5CF6; color: #C4B5FD; }
    [data-theme="dark"] .platform-pill.douyin { background: rgba(159,18,57,.15); border-color: #E11D48; color: #FDA4AF; }
  </style>''')

if lang == 'ja':
    c = c.replace('<h2>数字が示すもの</h2>', '<h2>\U0001f4ca 数字が示すもの</h2>')
    c = c.replace('<h2>広告にとってなぜ重要か</h2>', '<h2>\U0001f50d 広告にとってなぜ重要か</h2>')
    c = c.replace('<h2>カレンダーの収束</h2>', '<h2>\U0001f4c5 カレンダーの収束</h2>')
    c = c.replace('<h2>海外ブランドが注目すべきこと</h2>', '<h2>\u26a0\ufe0f 海外ブランドが注目すべきこと</h2>')
    c = c.replace('<h2>BPPがそれに対して行うこと</h2>', '<h2>\u2705 BPPがそれに対して行うこと</h2>')
    
    pills = '<div class="platform-pills"><span class="platform-pill baidu">\U0001f50d 百度</span><span class="platform-pill deepseek">\U0001f9e0 DeepSeek</span><span class="platform-pill douyin">\U0001f3b5 抖音</span><span class="platform-pill wenxin">\U0001f4da 騰訊</span></div>'
    
    after_ad = '<p>WAICには「広告トラック」はありません。しかし、WAICで展示されるテクノロジー——マルチモーダルAI、インテリジェントエージェント、レコメンデーションシステム、生成検索——は、今日中国の消費者にブランドがどのように見えるかを定義するのと同じテクノロジーです。</p>'
    c = c.replace(after_ad, after_ad + '\n\n    ' + pills)
    
    # callout
    signal3 = '<p><strong>シグナル3：政府支援のAIインフラが急速に拡大している。</strong> 10の国家省庁がWAICを共催しています。この会議は商業イベントではなく、戦略的方向性の国家支援シグナルです。これほどのコミットメントを持つ政府がAIインフラ——計算能力、モデル登録、アプリケーションシナリオ——に投資するとき、広告主が無視できないプラットフォームレベルの変化の条件が生まれます。</p>'
    callout = signal3 + '\n\n    <div class="callout callout-insight">\n      <strong>インサイト：WAICは、今年中国のAIプラットフォームの方向性について得られる最も強力なシグナルです。</strong> 10の国家省庁が共催。300以上の製品が世界初公開。1,100社以上の出展企業。これは技術会議ではなく、政府支援の方向性声明です。中国のプラットフォームで広告を出す広告主にとって、WAICで発表されるテクノロジーは、6ヶ月後の広告の動作を決定します。\n    </div>'
    c = c.replace(signal3, callout)
    
    # takeaway
    c = c.replace('WAIC 2026は10日後に開幕します。',
                  'WAIC 2026は10日後に開幕します。\n\n    <div class="takeaway-box">\n      <strong>重要なポイント：</strong> WAIC 2026（7月17-20日、上海）は今年の中国AIプラットフォームの方向性を示す最も重要なシグナル。1,100社以上の出展企業、300以上のグローバル初公開、10の国家省庁。3つのシグナル：マルチモーダルAI、インテリジェントエージェント、政府支援インフラ。百度のWAIC発表、AI検索の進化、規制後の規制シグナルに注目。\n    </div>')
else:
    c = c.replace('<h2>숫자가 말하는 것</h2>', '<h2>\U0001f4ca 숫자가 말하는 것</h2>')
    c = c.replace('<h2>광고에 중요한 이유</h2>', '<h2>\U0001f50d 광고에 중요한 이유</h2>')
    c = c.replace('<h2>캘린더의 수렴</h2>', '<h2>\U0001f4c5 캘린더의 수렴</h2>')
    c = c.replace('<h2>해외 브랜드가 주목해야 할 것</h2>', '<h2>\u26a0\ufe0f 해외 브랜드가 주목해야 할 것</h2>')
    c = c.replace('<h2>BPP가 이에 대해 하는 일</h2>', '<h2>\u2705 BPP가 이에 대해 하는 일</h2>')
    
    pills = '<div class="platform-pills"><span class="platform-pill baidu">\U0001f50d 바이두</span><span class="platform-pill deepseek">\U0001f9e0 DeepSeek</span><span class="platform-pill douyin">\U0001f3b5 더우인</span><span class="platform-pill wenxin">\U0001f4da 텐센트</span></div>'
    
    after_ad = '<p>WAIC에는 "광고 트랙"이 없습니다. 그러나 WAIC에서 전시되는 기술——멀티모달 AI, 지능형 에이전트, 추천 시스템, 생성 검색——은 오늘날 중국 소비자에게 브랜드가 어떻게 보이는지를 정의하는 동일한 기술입니다.</p>'
    c = c.replace(after_ad, after_ad + '\n\n    ' + pills)
    
    signal3 = '<p><strong>신호 3: 정부 지원 AI 인프라가 빠르게 확장되고 있습니다.</strong> 10개의 국가 부처가 WAIC를 공동 주최합니다. 이 회의는 상업 이벤트가 아니라 전략적 방향성의 국가 지원 신호입니다. 이 수준의 헌신을 가진 정부가 AI 인프라——컴퓨팅 파워, 모델 등록, 애플리케이션 시나리오——에 투자할 때, 광고주가 무시할 수 없는 플랫폼 수준의 변화 조건이 만들어집니다.</p>'
    callout = signal3 + '\n\n    <div class="callout callout-insight">\n      <strong>인사이트: WAIC는 올해 중국 AI 플랫폼 방향에 대해 얻을 수 있는 가장 강력한 신호입니다.</strong> 10개 국가 부처가 공동 주최. 300개 이상 제품 세계 첫 공개. 1,100개 이상 전시업체. 이는 기술 컨퍼런스가 아니라 정부 지원 방향성 성명입니다. 중국 플랫폼에서 광고하는 광고주에게 WAIC에서 발표되는 기술은 6개월 후 광고의 작동 방식을 결정할 것입니다.\n    </div>'
    c = c.replace(signal3, callout)
    
    c = c.replace('WAIC 2026이 10일 후 개막합니다.',
                  'WAIC 2026이 10일 후 개막합니다.\n\n    <div class="takeaway-box">\n      <strong>핵심 요점:</strong> WAIC 2026(7월 17-20일, 상하이)은 올해 중국 AI 플랫폼 방향의 가장 중요한 신호. 1,100개 이상 전시업체, 300개 이상 글로벌 첫 공개, 10개 국가 부처. 3가지 신호: 멀티모달 AI, 지능형 에이전트, 정부 지원 인프라. 바이두 WAIC 발표, AI 검색 진화, 규제 후 규제 신호에 주목.\n    </div>')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print(f'{lang} done')
