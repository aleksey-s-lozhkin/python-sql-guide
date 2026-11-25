// Проверка «читалки»: размер текста, продолжение чтения, мобильное меню.
const { puppeteer, chromePath } = require("./lib.cjs");
const url = process.env.BASE || "http://127.0.0.1:8899/guide/";
const out = process.env.OUT_DIR || "/tmp/guide-shots";

(async () => {
  const browser = await puppeteer.launch({ executablePath: chromePath(), headless: true, args: ["--no-sandbox"] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 1000, deviceScaleFactor: 1.5 });
  await page.emulateMediaFeatures([{ name: "prefers-color-scheme", value: "light" }]);

  // 1. читаем главу до середины, уходим на обложку — должна появиться карточка «продолжить»
  await page.goto(url + "ch-02-dict.html", { waitUntil: "networkidle0" });
  await page.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight * 0.45));
  await new Promise(r => setTimeout(r, 600));
  await page.goto(url + "index.html", { waitUntil: "networkidle0" });
  await new Promise(r => setTimeout(r, 200));
  const resume = await page.evaluate(() => {
    const a = document.querySelector(".resume");
    return a ? { text: a.textContent.replace(/\s+/g, " ").trim(), href: a.getAttribute("href") } : null;
  });

  // 2. размер текста: +2 шага, проверка и сохранение
  await page.evaluate(() => document.querySelectorAll("[data-rs]").forEach(b => { if (b.dataset.rs > 0) b.click(); }));
  const size1 = await page.evaluate(() => getComputedStyle(document.documentElement).fontSize);
  await page.reload({ waitUntil: "networkidle0" });
  const size2 = await page.evaluate(() => getComputedStyle(document.documentElement).fontSize);

  // 3. мобильное меню с читалкой
  const m = await browser.newPage();
  await m.setViewport({ width: 390, height: 844, deviceScaleFactor: 2 });
  await m.emulateMediaFeatures([{ name: "prefers-color-scheme", value: "dark" }]);
  await m.goto(url + "ch-02-dict.html", { waitUntil: "networkidle0" });
  await m.screenshot({ path: `${out}/m-1-top.png` });
  await m.click(".menu-btn");
  await new Promise(r => setTimeout(r, 250));
  await m.screenshot({ path: `${out}/m-2-menu.png` });

  // 4. обложка с карточкой «продолжить»
  await page.evaluate(() => localStorage.setItem("assoc-reader", JSON.stringify({ slug: "ch-02-dict", y: 1800, ratio: 0.42, title: "dict: шкаф с номерками" })));
  await page.reload({ waitUntil: "networkidle0" });
  await page.screenshot({ path: `${out}/index-resume.png` });

  console.log({ resume, fontSizeDefault: "16px", afterPlus: size1, afterReload: size2 });
  await browser.close();
})();
