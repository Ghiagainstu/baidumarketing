import fs from 'fs';
import path from 'path';

const issues = [];
for (const dir of ['blog', 'ja/blog', 'ko/blog']) {
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.html') && !f.startsWith('_'));
  for (const f of files) {
    const h = fs.readFileSync(path.join(dir, f), 'utf8');
    const matches = [...h.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)];
    for (const m of matches) {
      try {
        JSON.parse(m[1]);
      } catch(e) {
        const content = m[1].trim();
        // Check if JS leaked into JSON
        if (content.includes('(function') || content.includes('const ') || content.includes('document.get')) {
          issues.push({ file: dir + '/' + f, type: 'js-leaked-into-schema', snippet: content.slice(0, 100) });
        } else {
          issues.push({ file: dir + '/' + f, type: 'invalid-json', snippet: content.slice(0, 100) });
        }
      }
    }
  }
}
console.log('Schema issues:', issues.length);
issues.forEach(i => console.log(i.file + ': ' + i.type + ' -> ' + i.snippet.slice(0, 80)));
