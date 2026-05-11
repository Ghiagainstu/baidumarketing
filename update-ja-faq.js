/**
 * update-ja-faq.js v7
 * 纯字符串操作，从后往前替换
 * 通过正则定位每个 faq-answer 并填入日文答案
 */

const fs = require('fs');
const path = require('path');

const MD = path.join(__dirname, 'ja', 'faq-ja.md');
const HTML = path.join(__dirname, 'ja', 'faq.html');

// ========== 解析翻译文件 ==========
function parseFaqMd(md) {
  const qas = [];
  const lines = md.split('\n');
  let cur = null;

  for (let i = 0; i < lines.length; i++) {
    const t = lines[i].trim();

    if (/^\*\*Q\d+\*\*/.test(t)) {
      if (cur) qas.push(cur);
      cur = { q: t.replace(/^\*\*Q\d+\*\*\s*/, '').trim(), a: '' };
    } else if (cur && /^\*\*A\d+\*\*/.test(t)) {
      const aLines = [];
      i++;
      while (i < lines.length &&
             !/^\*\*Q\d+\*\*/.test(lines[i]) &&
             !lines[i].trim().startsWith('###') &&
             !lines[i].trim().startsWith('##')) {
        aLines.push(lines[i]);
        i++;
      }
      i--;
      cur.a = aLines.join('\n').trim();
    }
  }
  if (cur) qas.push(cur);
  console.log(`解析到 ${qas.length} 个 Q&A`);
  return qas;
}

// ========== 找到第 n 个 faq-answer 的位置 ==========
// 返回 { startContent: number, endContent: number }
// startContent: `<div class="faq-answer">` 之后的位置
// endContent: 对应的 `</div>` 的位置
function findAnswerPos(s, n) {
  let count = 0;
  let pos = 0;

  while ((pos = s.indexOf('<div class="faq-answer">', pos)) !== -1) {
    if (count === n) {
      const contentStart = pos + '<div class="faq-answer">'.length;
      // 找匹配的 </div>
      let depth = 1;
      let j = contentStart;
      while (j < s.length && depth > 0) {
        const nextOpen = s.indexOf('<div', j);
        const nextClose = s.indexOf('</div>', j);
        if (nextClose === -1) return null;
        if (nextOpen !== -1 && nextOpen < nextClose) {
          depth++;
          j = nextOpen + 1;
        } else {
          depth--;
          if (depth === 0) return { startContent: contentStart, endContent: nextClose };
          j = nextClose + 1;
        }
      }
      return null;
    }
    count++;
    pos += 1;
  }
  return null;
}

// ========== 更新 HTML ==========
function updateHTML(html, qas) {
  let s = html;
  let okQ = 0, okA = 0, fail = 0;

  // 1. 更新 meta
  s = s.replace(/<title>[^<]*<\/title>/, '<title>百度広告に関するよくある質問 — Baidu PPC Pro</title>');
  s = s.replace(
    /<meta name="description" content="[^"]*"\s*\/>/,
    '<meta name="description" content="海外企業のアカウント開設からコンプライアンス要件まで、百度広告アカウントの開設・運用に必要なすべてを解説します。" />'
  );
  s = s.replace(
    /<meta property="og:title" content="[^"]*"\s*\/>/,
    '<meta property="og:title" content="百度広告に関するよくある質問 — Baidu PPC Pro" />'
  );
  s = s.replace(
    /<meta property="og:description" content="[^"]*"\s*\/>/,
    '<meta property="og:description" content="海外企業のアカウント開設からコンプライアンス要件まで、百度広告アカウントの開設・運用に必要なすべてを解説します。" />'
  );
  s = s.replace(
    /<meta name="twitter:title" content="[^"]*"\s*\/>/,
    '<meta name="twitter:title" content="百度広告に関するよくある質問 — Baidu PPC Pro" />'
  );
  s = s.replace(
    /<meta name="twitter:description" content="[^"]*"\s*\/>/,
    '<meta name="twitter:description" content="海外企業のアカウント開設からコンプライアンス要件まで、百度広告アカウントの開設・運用に必要なすべてを解説します。" />'
  );
  console.log('  meta 更新完成');

  // 2. 更新 hero
  s = s.replace(
    /(<h1>)[^<]*<em>[^<]*<\/em>[^<]*(<\/h1>)/,
    '$1百度広告 <em>よくある質問</em> 💡$2'
  );
  s = s.replace(
    /(<p>)[^<]*(<\/p>)/,
    '$1' + '海外企業のアカウント開設からコンプライアンス要件まで、百度広告アカウントの開設・運用に必要なすべてを解説します。' + '$2'
  );
  console.log('  hero 更新完成');

  // 3. 更新 Q&A（从后往前，保护索引）
  const n = qas.length;

  // 先定位所有 faq-item 块的位置
  const positions = [];
  let p = 0;
  while ((p = s.indexOf('<div class="faq-item">', p)) !== -1) {
    positions.push(p);
    p += 1;
  }
  console.log(`  找到 ${positions.length} 个 faq-item`);

  if (positions.length !== n) {
    console.log(`  ⚠ 数量不匹配：HTML=${positions.length}, MD=${n}`);
  }

  // 从后往前处理
  const m = Math.min(positions.length, n);
  for (let i = m - 1; i >= 0; i--) {
    const pos = positions[i];
    const nextPos = (i < positions.length - 1) ? positions[i + 1] : s.length;
    const block = s.substring(pos, nextPos);

    // 替换问题
    const qRe = /(<button class="faq-question" onclick="toggleFaq\(this\)">\s*)([\s\S]*?)(\s*<span class="faq-icon">\+<\/span>\s*<\/button>)/;
    const qM = block.match(qRe);
    if (!qM) { console.log(`  ✗ Q${i+1} 未找到 question`); fail++; continue; }
    const newQ = qM[1] + qas[i].q + qM[3];
    let newBlock = block.replace(qRe, newQ);

    // 替换答案——用 findAnswerPos 在 newBlock 中定位
    const aStart = newBlock.indexOf('<div class="faq-answer">');
    if (aStart === -1) { console.log(`  ✗ Q${i+1} 未找到 answer 开始`); fail++; continue; }
    const pos2 = findAnswerPos(newBlock, 0);  // 在 block 中找第 0 个 answer
    if (!pos2) { console.log(`  ✗ Q${i+1} 未找到 answer 结束`); fail++; continue; }
    const beforeA = newBlock.substring(0, pos2.startContent);
    const afterA = newBlock.substring(pos2.endContent + '</div>'.length);
    newBlock = beforeA + qas[i].a + afterA;

    // 替换原块
    s = s.substring(0, pos) + newBlock + s.substring(nextPos);
    okQ++; okA++;
  }
  console.log(`  Q&A 更新：问题 ${okQ}/${n}，答案 ${okA}/${n}，失败 ${fail}`);

  // 4. 更新 CTA 统计
  s = s.replace(
    /(<div class="faq-cta-num">)[^<]*(<\/div>)/g,
    (match, p1, p2, offset) => {
      // 依次替换 51 / 8 / 24/7
      const first = s.indexOf('51', offset - 100);
      // 简单处理：直接替换 3 个统计数字
      return match;
    }
  );
  console.log('  CTA 统计需手动确认');

  return s;
}

// ========== main ==========
function main() {
  console.log('读取翻译文件...');
  const md = fs.readFileSync(MD, 'utf8');

  console.log('解析...');
  const qas = parseFaqMd(md);

  console.log('读取 HTML...');
  let html = fs.readFileSync(HTML, 'utf8');

  console.log('备份...');
  fs.writeFileSync(HTML + '.bak6', html, 'utf8');

  console.log('更新...');
  const updated = updateHTML(html, qas);

  fs.writeFileSync(HTML, updated, 'utf8');
  console.log(`\n完成！备份至 ${HTML}.bak6`);
}

main();
