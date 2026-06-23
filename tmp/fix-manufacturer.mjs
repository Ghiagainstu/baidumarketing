import fs from 'fs';
const f = 'ko/blog/b2b-manufacturer-baidu-case-study.html';
let h = fs.readFileSync(f, 'utf8');

const title = '\uc81c\ub85c\uc5d0\uc11c \uc6d8 400\uac74 \ub9ac\ub4dc \ud655\ubcf4: \uc720\ub7fd \uc81c\uc870\uc0ac\uac00 \ubc14\uc774\ub4dc PPC\ub85c \uc911\uad6d \uc2dc\uc7a5\uc744 \uac1c\ud1a0\ud55c \ubc29\ubc95';
const desc = '\uc720\ub7fd \uc0b0\uc5c5 \uc790\ub3d9\ud654 \ubd80\ud488 \uc81c\uc870\uc0ac\uac00 \ubc14\uc774\ub4dc PPC\ub85c 90\uc77c \ub0b4\uc5d0 \ud655\uc778 \ub9ac\ub4dc 47\uac74\uc744 \uc0dd\uc131\ud55c \ubc29\ubc95';

// Fix title
h = h.replace(/<title>\[TITLE\][^<]*<\/title>/, '<title>' + title + ' \u2014 Baidu PPC Pro Blog</title>');
h = h.replace(/og:title[^>]*content="\[TITLE\]"/, 'og:title" content="' + title + '"');
h = h.replace(/twitter:title[^>]*content="\[TITLE\]"/, 'twitter:title" content="' + title + '"');

// Fix JSON-LD placeholders
h = h.replace(/"headline":"\[TITLE\]"/, '"headline":"' + title + '"');
h = h.replace(/"description":"\[DESCRIPTION\]"/, '"description":"' + desc + '"');
h = h.replace(/"datePublished":"\[DATE\]"/, '"datePublished":"2026-06-23"');
h = h.replace(/"dateModified":"\[DATE\]"/, '"dateModified":"2026-06-23"');
h = h.replace(/ko\/blog\/\[SLUG\]/, 'ko/blog/b2b-manufacturer-baidu-case-study');

// Remove duplicate <h1> (line 295) and bare --- (line 297)
h = h.replace(/\n<h1 class="article-title">\uuc81c\ub85c\uc5d0\uc11c \uc6d8 400\uac74 \ub9ac\ub4dc \ud655\ubcf4.*?<\/h1>/, '');
h = h.replace(/<p>---<\/p>/, '');

fs.writeFileSync(f, h, 'utf8');
console.log('Fixed:', f);
