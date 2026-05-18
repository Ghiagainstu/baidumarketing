const fs = require('fs');
const filePath = 'c:/Users/HYE/WorkBuddy/20260411211839/index.html';

let lines = fs.readFileSync(filePath, 'utf8').split('\n');

// Lines to remove: 2047-2320 (1-indexed) => indices 2046-2319
// Replace line 2047 (index 2046) with new script tag
// Remove lines 2048-2320 (indices 2047-2319)

const startIdx = 2046; // 0-indexed, line 2047
const endIdx = 2319; // 0-indexed, line 2320

// Replace the <script> line with new tag
lines[startIdx] = '<script src="/assets/js/main.js" defer></script>';

// Remove lines from startIdx+1 to endIdx
lines.splice(startIdx + 1, endIdx - startIdx);

const result = lines.join('\n');
fs.writeFileSync(filePath, result, 'utf8');

console.log('Successfully replaced inline script with external JS reference');
console.log('Removed lines from', startIdx + 1, 'to', endIdx + 1);
