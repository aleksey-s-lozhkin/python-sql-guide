// Проверка офлайн-режима: кэш, регистрация SW, открытие главы без сети.
// Для работы нужен локальный сервер: python3 -m http.server 8899
const { puppeteer, chromePath } = require("./lib.cjs");

const url = process.env.BASE || "http://127.0.0.1:8899/guide/";

(async () => {
  const browser = await puppeteer.launch({
    executablePath: chromePath(), headless: true,
    args: ["--no-sandbox"],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 1000 });

  await page.goto(url + "index.html", { waitUntil: "networkidle0" });
  await page.evaluate(() => navigator.serviceWorker.ready);
  await new Promise(r => setTimeout(r, 800));

  const state = await page.evaluate(async () => {
    const keys = await caches.keys();
    const cache = await caches.open(keys[0]);
    const reqs = await cache.keys();
    return {
      controlled: !!navigator.serviceWorker.controller,
      cache: keys[0],
      files: reqs.length,
      hasChapter: reqs.some(r => r.url.endsWith("ch-25-sql-vs-pandas.html")),
      net: document.getElementById("net")?.textContent,
      manifest: document.querySelector('link[rel="manifest"]')?.href,
    };
  });
  console.log(state);

  // офлайн: всё, что в кэше, должно открываться
  await page.reload({ waitUntil: "networkidle0" });
  await page.setOfflineMode(true);
  await page.goto(url + "ch-02-dict.html", { waitUntil: "domcontentloaded" });
  const offline = await page.evaluate(() => ({
    title: document.title,
    h1: document.querySelector("h1")?.textContent.trim().slice(0, 40),
    styled: getComputedStyle(document.body).backgroundColor,
    net: document.getElementById("net")?.textContent,
  }));
  console.log("OFFLINE:", offline);

  await page.setOfflineMode(false);
  await browser.close();
})();
