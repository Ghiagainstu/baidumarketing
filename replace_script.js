const fs = require('fs');
const filePath = 'c:/Users/HYE/WorkBuddy/20260411211839/index.html';

let content = fs.readFileSync(filePath, 'utf8');

// Replace the entire inline script block with external JS reference
const oldBlockStart = '<script>\n';
const oldBlockEnd = '</script>\n';

const newScriptTag = '<script src="/assets/js/main.js" defer></script>\n';

// Find positions
const startIdx = content.indexOf(oldBlockStart);
const endIdx = content.indexOf(oldBlockEnd, startIdx) + oldBlockEnd.length;

if (startIdx !== -1 && endIdx !== -1) {
  content = content.substring(0, startIdx) + newScriptTag + content.substring(endIdx);
  fs.writeFileSync(filePath, content, 'utf8');
  console.log('Successfully replaced inline script with external JS reference');
  console.log('Start position:', startIdx);
  console.log('End position:', endIdx);
} else {
  console.log('Could not find script block');
  console.log('startIdx:', startIdx);
  console.log('endIdx:', endIdx);
}
