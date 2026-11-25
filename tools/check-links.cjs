// Проверка целостности: все ссылки, картинки и скрипты в guide/*.html существуют.
// node tools/check-links.cjs
const fs = require("fs");
const path = require("path");
const { ROOT } = require("./lib.cjs");

const dir = path.join(ROOT, "guide");
const files = fs.readdirSync(dir).filter(f => f.endsWith(".html"));
let bad = 0, total = 0;

for (const f of files) {
  const html = fs.readFileSync(path.join(dir, f), "utf8");
  const refs = [...html.matchAll(/(?:href|src)="([^"]+)"/g)].map(m => m[1]);
  for (const ref of refs) {
    if (/^(https?:|mailto:|data:|#)/.test(ref)) continue;
    total++;
    const clean = decodeURIComponent(ref.split("#")[0].split("?")[0]);
    if (!clean) continue;
    const target = path.resolve(dir, clean);
    if (!fs.existsSync(target)) { console.log(`✗ ${f} → ${ref}`); bad++; }
  }
}

// каждая глава из оглавления должна иметь файл
const toc = fs.readFileSync(path.join(dir, "assets/toc.js"), "utf8");
const slugs = [...toc.matchAll(/slug:\s*"([^"]+)"/g)].map(m => m[1]);
for (const s of slugs) {
  if (!fs.existsSync(path.join(dir, s + ".html"))) { console.log(`✗ нет страницы для ${s}`); bad++; }
}

console.log(bad ? `\n${bad} битых ссылок из ${total}` : `все ${total} ссылок целы, ${files.length} страниц`);
process.exit(bad ? 1 : 0);
