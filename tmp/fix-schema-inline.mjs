import fs from 'fs';

function fixFile(f, oldHeadline, newHeadline, oldDesc, newDesc) {
  let h = fs.readFileSync(f, 'utf8');
  if (oldHeadline) h = h.replace(oldHeadline, newHeadline);
  if (oldDesc) h = h.replace(oldDesc, newDesc);
  fs.writeFileSync(f, h, 'utf8');
  console.log('Fixed: ' + f);
}

fixFile(
  'ko/blog/ai-marketing-whitepapers-2026-baidu-insights.html',
  '"headline":"AI Marketing White Papers 2026: What the Data Says About Baidu Advertising \u2014 And What Overseas Brands Should Do"',
  '"headline":"\uc544\uc774 \ub9c8\ucf00\ud305 \ubc31\uc11c 2026: \ubc14\uc774\ub4dc \uad11\uace0 \ub370\uc774\ud130 \ubc0f \ud574\uc678 \ube0c\ub79c\ub4dc \ud65c\uc6a9\ubc95"',
  '"description":"AI-driven marketing, private domain traffic, and automation are reshaping China\'s digital landscape in 2026. Here is what overseas advertisers need to know."',
  '"description":"iResearch\uc640 iMedia \ubc31\uc11c\ub85c \ubd84\uc11d\ud55c 2026\ub144 AI \ub9c8\ucf00\ud305 \ud2b8\ub80c\ub4dc"'
);

fixFile(
  'ko/blog/b2b-lead-generation-framework.html',
  '"headline":"The 5-Step B2B Lead Generation Framework on Baidu: A Practical Guide for Overseas Companies"',
  '"headline":"\ubc14\uc774\ub4dc B2B \ub9ac\ub4dc \uc0dd\uc131 \ud504\ub808\uc784\uc6cc\ud06c: \ud574\uc678 \uae30\uc5c5\uc744 \uc704\ud55c 5\ub2e8\uacc4 \uac00\uc774\ub4dc"',
  null, null
);

fixFile(
  'ko/blog/baidu-industry-insights-tool-guide.html',
  '"headline":"How to Use Baidu\'s New Industry Insights Tool to Benchmark Your PPC Performance"',
  '"headline":"\ubc14\uc774\ub4dc \uc5c5\uacc4 \uc778\uc0ac\uc774\uce20 \ub3c4\uad6c \uac00\uc774\ub4dc: \uacbd\uc7c1 \ubca0\uce58\ub9c8\ud06c \ud65c\uc6a9\ubc95"',
  '"description":"Baidu\'s new Industry Insights tool (June 3, 2026) gives advertisers real industry benchmarks. Learn how to use it to optimize your Baidu PPC campaigns with data, not guesswork."',
  '"description":"\ubc14\uc774\ub4dc\uc758 \uc5c5\uacc4 \uc778\uc0ac\uc774\uce20 \ub3c4\uad6c\ub85c \uc2e4\uc81c \uc5c5\uacc4 \ubca0\uce58\ub9c8\ud06c\ub97c \ud65c\uc6a9\ud558\uc5ec \uce90\ud398\uc778\uc744 \ucd5c\uc801\ud654\ud558\ub294 \ubc29\ubc95"'
);

fixFile(
  'ko/blog/b2b-manufacturer-baidu-case-study.html',
  '"headline":"How a European Industrial Manufacturer Generated 47 Qualified Leads in 90 Days with Baidu PPC"',
  '"headline":"\uc720\ub7fd \uc0b0\uc5c5 \uc81c\uc870\uc5c5\uccb4\uac00 \ubc14\uc774\ub4dc PPC\ub85c 90\uc77c \ub0b4\uc5d0 \ud655\uc778 \ub9ac\ub4dc 47\uac74\uc744 \uc0dd\uc131\ud55c \ubc29\ubc95"',
  null, null
);

fixFile(
  'ko/blog/baidu-account-opening-foreign-companies.html',
  '"headline":"How Foreign Companies Open a Baidu Ads Account: Complete 2026 Guide"',
  '"headline":"\ud574\uc678 \ud68c\uc0ac\ub97c \uc704\ud55c \ubc14\uc774\ub4dc \uad11\uace0 \uacc4\uc815 \uac1c\uc120 \uac00\uc774\ub4dc 2026"',
  '"description":"Step-by-step guide to opening a Baidu advertising account for foreign companies without a Chinese business license."',
  '"description":"\uc911\uad6d \uc0ac\uc5c5\uc790\ub4f1\ub85d\uc774 \uc5c6\ub294 \ud574\uc678 \ud68c\uc0ac\ub97c \uc704\ud55c \ubc14\uc774\ub4dc \uad11\uace0 \uacc4\uc815 \uac1c\uc120 \ub2e8\uacc4\ubcc4 \uac00\uc774\ub4dc"'
);

fixFile(
  'ko/blog/baidu-account-opening-foreign-companies.html',
  '"og:title" content="How Foreign Companies Open a Baidu Ads Account"',
  '"og:title" content="\ud574\uc678 \ud68c\uc0ac\ub97c \uc704\ud55c \ubc14\uc774\ub4dc \uad11\uace0 \uacc4\uc815 \uac1c\uc120 \uac00\uc774\ub4dc"',
  null, null
);
