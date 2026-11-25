// Сборка service worker: кэширует всю книгу, чтобы читать офлайн с телефона.
// node tools/gen_sw.cjs  (пересобирает guide/sw.js после добавления глав)
const fs = require("fs");
const path = require("path");

const dir = path.join(__dirname, "..", "guide");
const walk = (p) => {
  const out = [];
  for (const e of fs.readdirSync(p, { withFileTypes: true })) {
    const full = path.join(p, e.name);
    if (e.isDirectory()) out.push(...walk(full));
    else out.push(full);
  }
  return out;
};

const files = walk(dir)
  .filter(f => !f.endsWith("sw.js") && !f.endsWith(".DS_Store"))
  .map(f => path.relative(dir, f).split(path.sep).join("/"))
  .sort();

// версия = хеш содержимого: любая правка главы или стиля обновляет кэш
const crypto = require("crypto");
const h = crypto.createHash("sha1");
for (const f of files) h.update(f).update(fs.readFileSync(path.join(dir, f)));
const version = process.env.SW_VERSION || h.digest("hex").slice(0, 8);
const list = files.map(f => `  "./${f}"`).join(",\n");

const sw = `// Сгенерировано tools/gen_sw.cjs — не править руками.
const CACHE = "assoc-guide-v${version}";
const PRECACHE = [
${list}
];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE)
      .then((c) => c.addAll(PRECACHE))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

const isHTML = (req) =>
  req.mode === "navigate" || (req.headers.get("accept") || "").includes("text/html");

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;

  // Страницы: сначала кэш (офлайн важнее свежести), обновление — фоном.
  if (isHTML(req)) {
    e.respondWith((async () => {
      const c = await caches.open(CACHE);
      const cached = await c.match(req, { ignoreSearch: true });
      const fresh = fetch(req)
        .then((res) => { if (res && res.ok) c.put(req, res.clone()); return res; })
        .catch(() => cached);
      return cached || fresh;
    })());
    return;
  }

  // Остальное: кэш, затем сеть.
  e.respondWith((async () => {
    const c = await caches.open(CACHE);
    const hit = await c.match(req);
    if (hit) return hit;
    try {
      const res = await fetch(req);
      if (res && res.ok && req.url.startsWith(self.location.origin)) c.put(req, res.clone());
      return res;
    } catch {
      return new Response("Офлайн: файл не в кэше", { status: 503, headers: { "Content-Type": "text/plain; charset=utf-8" } });
    }
  })());
});
`;

fs.writeFileSync(path.join(dir, "sw.js"), sw);
console.log(`sw.js собран: ${files.length} файлов в кэше`);
