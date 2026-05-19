// fix-css-variables.js
// 以 baidu-brand-protection-guide.html 为基准，修复 CSS 变量不完整的 blog 页面
// 用法: node fix-css-variables.js

const fs = require('fs');
const path = require('path');

const BLOG_DIR = path.join(__dirname, 'blog');
const BASELINE = path.join(BLOG_DIR, 'baidu-brand-protection-guide.html');

// 从基准页面提取完整 :root 和 [data-theme="dark"] 的 CSS 变量定义
function extractCssVariables(html) {
  const styleMatch = html.match(/<style>([\s\S]*?)<\/style>/);
  if (!styleMatch) return null;
  const styleContent = styleMatch[1];
  
  // 提取 :root { ... } 块
  const rootMatch = styleContent.match(/:root\s*\{[\s\S]*?\}/);
  // 提取 [data-theme="dark"] { ... } 块（第一个，变量定义块）
  const darkMatches = styleContent.matchAll(/\[data-theme="dark"\]\s*\{[\s\S]*?\}/g);
  const darkBlocks = [...darkMatches];
  
  return {
    rootBlock: rootMatch ? rootMatch[0] : null,
    // 取第一个[data-theme="dark"]块（变量定义），不包含后续样式覆盖
    darkBlock: darkBlocks.length > 0 ? darkBlocks[0][0] : null,
  };
}

// 读取基准页面
const baselineHtml = fs.readFileSync(BASELINE, 'utf8');
const baselineVars = extractCssVariables(baselineHtml);

if (!baselineVars.rootBlock || !baselineVars.darkBlock) {
  console.error('无法从基准页面提取 CSS 变量');
  process.exit(1);
}

console.log('基准页面 CSS 变量提取成功');
console.log('Root block length:', baselineVars.rootBlock.length);
console.log('Dark block length:', baselineVars.darkBlock.length);

// 需要修复的页面
const pagesToFix = [
  path.join(BLOG_DIR, 'ai-assistants-vs-baidu.html'),
  path.join(BLOG_DIR, 'china-internet-numbers-2025.html'),
];

for (const pagePath of pagesToFix) {
  if (!fs.existsSync(pagePath)) {
    console.log('文件不存在:', pagePath);
    continue;
  }
  
  let html = fs.readFileSync(pagePath, 'utf8');
  
  // 替换 :root { ... } 块
  html = html.replace(/:root\s*\{[\s\S]*?\}/, baselineVars.rootBlock);
  
  // 替换第一个 [data-theme="dark"] { ... } 块（变量定义块）
  // 需要小心：只替换变量定义块，不替换后续样式覆盖块
  // 策略：找到第一个[data-theme="dark"] {，然后找到对应的结束 }
  // 但是简单的正则无法处理嵌套括号
  
  // 更安全的策略：在 <style> 标签内，找到第一个 [data-theme="dark"] { ... }
  // 然后替换到第一个 } 之前（假设变量定义块没有嵌套）
  
  // 实际上，观察发现 [data-theme="dark"] 变量定义块之后有空白行，然后是样式覆盖
  // 我们可以用更精确的正则：匹配从 [data-theme="dark"] { 到第一个单独的 }
  
  // 但是变量定义块内可能有嵌套（实际上没有，都是变量定义）
  // 所以可以用：\[data-theme="dark"\]\s*\{[^}]*\}
  // 但是 [^}]* 无法匹配多行
  
  // 用这个函数来替换第一个 [data-theme="dark"] 块
  function replaceFirstDarkBlock(content, newBlock) {
    const idx = content.indexOf('[data-theme="dark"]');
    if (idx === -1) return content;
    
    // 找到 { 的位置
    const braceStart = content.indexOf('{', idx);
    if (braceStart === -1) return content;
    
    // 找到匹配的结束 }
    let depth = 1;
    let pos = braceStart + 1;
    while (pos < content.length && depth > 0) {
      if (content[pos] === '{') depth++;
      if (content[pos] === '}') depth--;
      pos++;
    }
    // pos 现在是结束 } 之后的位置
    
    // 替换从 idx 到 pos 的内容
    return content.substring(0, idx) + newBlock + content.substring(pos);
  }
  
  html = replaceFirstDarkBlock(html, baselineVars.darkBlock);
  
  fs.writeFileSync(pagePath, html, 'utf8');
  console.log('修复完成:', path.basename(pagePath));
}

console.log('所有页面修复完成');
