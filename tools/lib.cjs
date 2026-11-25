// Общие пути к локальным инструментам проверки гайда.
// Тяжёлые зависимости (puppeteer + Chromium ~600 МБ) живут вне проекта,
// в /tmp/guide-tools, чтобы не засорять рабочую папку.
// Переопределяется переменной окружения GUIDE_TOOLS.
const path = require("path");
const fs = require("fs");

const ROOT = path.resolve(__dirname, "..");
const TOOLS = process.env.GUIDE_TOOLS || "/tmp/guide-tools";
const NPM = path.join(TOOLS, "npm");

function need(p) {
  try { return require(p); } catch (e) {
    console.error(`Не найдено: ${p}\nПоставьте окружение: cd ${NPM} && npm i puppeteer @resvg/resvg-js && npx puppeteer browsers install chrome`);
    process.exit(1);
  }
}

const puppeteer = need(path.join(NPM, "node_modules/puppeteer"));

function chromePath() {
  const base = path.join(NPM, ".puppeteer/chrome");
  for (const v of fs.readdirSync(base)) {
    const p = path.join(base, v, "chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing");
    if (fs.existsSync(p)) return p;
  }
  throw new Error("Chromium не найден в " + base);
}

module.exports = { ROOT, TOOLS, NPM, puppeteer, chromePath, need };
