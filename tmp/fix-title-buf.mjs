import fs from 'fs';
const f = 'ko/blog/b2b-manufacturer-baidu-case-study.html';
let h = fs.readFileSync(f, 'utf8');

const title = '???? ? 400? ?? ??: ?? ???? ??? PPC? ?? ??? ??? ??';

// The title tag currently has corrupted bytes, use regex to replace the whole tag
h = h.replace(/<title>.*?<\/title>/, '<title>' + title + ' ¡ª Baidu PPC Pro Blog</title>');

// Write as Buffer to ensure UTF-8
const buf = Buffer.from(h, 'utf8');
fs.writeFileSync(f, buf);
console.log('Fixed title with Buffer write');

// Verify
const verify = fs.readFileSync(f, 'utf8');
const t = verify.match(/<title>([^<]*)<\/title>/)[1];
console.log('Verify title:', t.slice(0, 60));
