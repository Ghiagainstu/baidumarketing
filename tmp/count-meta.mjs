import fs from 'fs';
const dir = 'ko/blog';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html') && !f.startsWith('_'));

let schemaEn = [], metaEn = [], ogEn = [];

for (const f of files) {
  const h = fs.readFileSync(dir + '/' + f, 'utf8');
  
  const sh = h.match(/"headline":\s*"([^"]+)"/);
  if (sh && !/[\uac00-\ud7af]/.test(sh[1])) schemaEn.push(f);
  
  const md = h.match(/content="([^"]+)"[^>]*name="description"/i) || h.match(/name="description"[^>]*content="([^"]+)"/i);
  if (md && !/[\uac00-\ud7af]/.test(md[1]) && md[1].length > 20) metaEn.push(f);
  
  const og = h.match(/og:title[^>]*content="([^"]+)"/i);
  if (og && !/[\uac00-\ud7af]/.test(og[1]) && og[1].length > 10) ogEn.push(f);
}

const allFiles = new Set([...schemaEn, ...metaEn, ...ogEn]);
console.log('Schema headline still EN:', schemaEn.length, schemaEn);
console.log('Meta desc still EN:', metaEn.length, metaEn);
console.log('og:title still EN:', ogEn.length, ogEn);
console.log('Total unique files:', allFiles.size);
