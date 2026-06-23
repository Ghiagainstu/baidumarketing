import fs from 'fs';
const f = 'ko/blog/b2b-manufacturer-baidu-case-study.html';
const buf = fs.readFileSync(f);

// Find <title> and </title> in raw bytes
const startMarker = Buffer.from('<title>');
const endMarker = Buffer.from('</title>');
const startIdx = buf.indexOf(startMarker);
const endIdx = buf.indexOf(endMarker);

if (startIdx === -1 || endIdx === -1) { console.error('title tag not found'); process.exit(1); }

const title = '???? ? 400? ?? ??: ?? ???? ??? PPC? ?? ??? ??? ?? ¡ª Baidu PPC Pro Blog';
const newTitleBuf = Buffer.from('<title>' + title + '</title>', 'utf8');

const newBuf = Buffer.concat([
  buf.subarray(0, startIdx),
  newTitleBuf,
  buf.subarray(endIdx + endMarker.length)
]);

fs.writeFileSync(f, newBuf);
console.log('Fixed title bytes');

// Verify
const verify = fs.readFileSync(f, 'utf8');
const t = verify.match(/<title>([^<]*)<\/title>/)[1];
console.log('Verify:', t.slice(0, 80));
