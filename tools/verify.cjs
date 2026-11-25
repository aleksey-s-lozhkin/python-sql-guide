// Визуальная проверка книги: десктоп, планшет, мобильный, светлая и тёмная темы.
// node tools/verify.cjs [light|dark]
const path = require("path");
const { ROOT, puppeteer, chromePath } = require("./lib.cjs");

const base = "file://" + path.join(ROOT, "guide") + "/";
const out = process.env.OUT_DIR || "/tmp/guide-shots";

(async () => {
  const scheme = process.argv[2] || "light";
  const browser = await puppeteer.launch({
    executablePath: chromePath(), headless: true,
    args: ["--no-sandbox", "--allow-file-access-from-files", "--font-render-hinting=none"],
  });
  const errs = [];
  const page = await browser.newPage();
  page.on("pageerror", e => errs.push("PAGEERROR: " + e.message));
  page.on("requestfailed", r => errs.push("REQFAIL: " + decodeURIComponent(r.url()).slice(-70)));
  await page.emulateMediaFeatures([{ name: "prefers-color-scheme", value: scheme }]);

  await page.setViewport({ width: 1440, height: 1000, deviceScaleFactor: 1.5 });
  await page.goto(base + "index.html", { waitUntil: "networkidle0" });
  await page.screenshot({ path: `${out}/index-top-${scheme}.png` });
  await page.evaluate(() => document.querySelector(".toc").scrollIntoView());
  await new Promise(r => setTimeout(r, 200));
  await page.screenshot({ path: `${out}/index-toc-${scheme}.png` });

  await page.goto(base + "ch-02-dict.html", { waitUntil: "networkidle0" });
  await page.screenshot({ path: `${out}/chapter-top-${scheme}.png` });
  await page.evaluate(() => { document.querySelector(".qa details").open = true; });
  await (await page.$(".qa")).screenshot({ path: `${out}/qa-open-${scheme}.png` });
  await (await page.$(".chain")).screenshot({ path: `${out}/chain-${scheme}.png` });

  await page.goto(base + "ch-15-groupby.html", { waitUntil: "networkidle0" });
  await page.screenshot({ path: `${out}/stub-${scheme}.png` });

  for (const [name, w, h] of [["tablet", 1024, 900], ["mobile", 390, 844]]) {
    const p = await browser.newPage();
    await p.setViewport({ width: w, height: h, deviceScaleFactor: 2 });
    await p.emulateMediaFeatures([{ name: "prefers-color-scheme", value: scheme }]);
    await p.goto(base + "ch-02-dict.html", { waitUntil: "networkidle0" });
    await p.screenshot({ path: `${out}/${name}-${scheme}.png` });
    await p.close();
  }

  console.log(errs.length ? "ERRORS:\n" + errs.join("\n") : "no errors");
  await browser.close();
})();
