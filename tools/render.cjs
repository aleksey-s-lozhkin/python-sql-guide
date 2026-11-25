// SVG → PNG (для проверки схем глазами и для вставки в DOCX/PDF).
// Использование: node tools/render.cjs guide/assets/maps/*.svg
const fs = require("fs");
const path = require("path");
const { NPM, need } = require("./lib.cjs");
const { Resvg } = need(path.join(NPM, "node_modules/@resvg/resvg-js"));

const outDir = process.env.OUT_DIR || "/tmp/svg-preview";
fs.mkdirSync(outDir, { recursive: true });

for (const f of process.argv.slice(2)) {
  const svg = fs.readFileSync(f, "utf8");
  const r = new Resvg(svg, { fitTo: { mode: "width", value: 1400 }, background: process.env.BG || "#fbf8f2" });
  const out = path.join(outDir, path.basename(f).replace(/\.svg$/, ".png"));
  fs.writeFileSync(out, r.render().asPng());
  console.log("ok", out);
}
