import fs from 'fs';
const htmlPath = process.argv[2];
const bodyPath = process.argv[3];
let html = fs.readFileSync(htmlPath, 'utf8');
const newBody = fs.readFileSync(bodyPath, 'utf8');
const startTag = '<article class="article-content">';
const endTag = '</article>';
const startIdx = html.indexOf(startTag);
const endIdx = html.indexOf(endTag, startIdx);
if (startIdx === -1 || endIdx === -1) { console.error('article not found'); process.exit(1); }
html = html.substring(0, startIdx) + newBody + '\n    ' + html.substring(endIdx + endTag.length);
// Update meta
const titleKo = '\uc544\uc774 \ub9c8\ucf00\ud305 \ubc31\uc11c 2026: \ubc14\uc774\ub4dc \uad11\uace0 \ub370\uc774\ud130 \ubc0f \ud574\uc678 \ube0c\ub79c\ub4dc \ud65c\uc6a9\ubc95';
const descKo = 'iResearch\uc640 iMedia \ubc31\uc11c\ub85c \ubd84\uc11d\ud55c 2026\ub144 AI \ub9c8\ucf00\ud305 \ud2b8\ub80c\ub4dc. GEO \uc2dc\uc7a5 70%+\uc131\uc7a5, 8\uc5b5 AI \uac80\uc0c9 \uc0ac\uc6a9\uc790, \uc804\ud1b5 SEO 30%+\ud558\ub77d. \ud574\uc678 \uad11\uace0\uc8fc\ub97c \uc704\ud55c \uc2e4\uc804 \uac00\uc774\ub4dc.';
html = html.replace(/<title>[^<]*<\/title>/, '<title>' + titleKo + ' \u2014 Baidu PPC Pro Blog</title>');
html = html.replace(/<h1[^>]*>[^<]*<\/h1>/, '<h1 class="article-title">' + titleKo + '</h1>');
html = html.replace(/og:title[^>]*content="[^"]*"/, 'og:title" content="' + titleKo + '"');
html = html.replace(/"headline": "[^"]*"/, '"headline": "' + titleKo + '"');
html = html.replace(/og:description[^>]*content="[^"]*"/, 'og:description" content="' + descKo + '"');
html = html.replace(/<meta name="description" content="[^"]*"/, '<meta name="description" content="' + descKo + '"');
fs.writeFileSync(htmlPath, html, 'utf8');
console.log('Updated ' + htmlPath + ' (' + html.length + ' bytes)');
