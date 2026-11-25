// Скриншоты страниц книги для визуальной проверки.
// node tools/shot.cjs <url> <out.png> [selector|""] [full|""]
const { ROOT, puppeteer, chromePath } = require("./lib.cjs");

(async () => {
  const [url, out, sel, full] = process.argv.slice(2);
  const browser = await puppeteer.launch({
    executablePath: chromePath(), headless: true,
    args: ["--no-sandbox", "--allow-file-access-from-files", "--font-render-hinting=none"],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 1000, deviceScaleFactor: 1.5 });
  const errs = [];
  page.on("console", m => { if (m.type() === "error") errs.push(m.text()); });
  page.on("pageerror", e => errs.push("PAGEERROR: " + e.message));
  page.on("requestfailed", r => errs.push("REQFAIL: " + decodeURIComponent(r.url()).slice(-70)));
  await page.goto(url, { waitUntil: "networkidle0" });
  await new Promise(r => setTimeout(r, 300));

  if (full) await page.screenshot({ path: out, fullPage: true });
  else if (sel) {
    const el = await page.$(sel);
    if (!el) console.log("NO SELECTOR", sel);
    else await el.screenshot({ path: out });
  } else await page.screenshot({ path: out });

  const meta = await page.evaluate(() => ({
    title: document.title,
    height: document.documentElement.scrollHeight,
    navLinks: document.querySelectorAll(".nav-ch").length,
  }));
  console.log(JSON.stringify(meta));
  if (errs.length) console.log("ERRORS:\n" + errs.join("\n"));
  await browser.close();
})();
