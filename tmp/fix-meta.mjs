import fs from 'fs';
const f = process.argv[2];
const title = process.argv[3];
const desc = process.argv[4];
let h = fs.readFileSync(f, 'utf8');

// meta description
h = h.replace(/(<meta name="description" content=")[^"]*(")/, '$1' + desc + '$2');
// og:title
h = h.replace(/(<meta property="og:title" content=")[^"]*(")/, '$1' + title + '$2');
// og:description
h = h.replace(/(<meta property="og:description" content=")[^"]*(")/, '$1' + desc + '$2');
// twitter:title
h = h.replace(/(<meta name="twitter:title" content=")[^"]*(")/, '$1' + title + '$2');
// twitter:description
h = h.replace(/(<meta name="twitter:description" content=")[^"]*(")/, '$1' + desc + '$2');
// JSON-LD headline
h = h.replace(/("headline": ")[^"]*(")/, '$1' + title + '$2');
// JSON-LD description
h = h.replace(/("description": ")[^"]*(")/, '$1' + desc + '$2');

fs.writeFileSync(f, h, 'utf8');
console.log('Fixed: ' + f);
