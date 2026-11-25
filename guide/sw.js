// Сгенерировано tools/gen_sw.cjs — не править руками.
const CACHE = "assoc-guide-v81e16f55";
const PRECACHE = [
  "./assets/app.js",
  "./assets/icons/favicon.svg",
  "./assets/icons/icon-180.png",
  "./assets/icons/icon-192.png",
  "./assets/icons/icon-512.png",
  "./assets/icons/icon.svg",
  "./assets/maps/alias-vs-copy.svg",
  "./assets/maps/comprehension-vs-generator.svg",
  "./assets/maps/dict-hash.svg",
  "./assets/maps/list-as-train.svg",
  "./assets/maps/one-model-three-worlds.svg",
  "./assets/maps/set-operations.svg",
  "./assets/style.css",
  "./assets/toc.js",
  "./ch-01-python-collections.html",
  "./ch-02-dict.html",
  "./ch-03-list-tuple.html",
  "./ch-04-set.html",
  "./ch-05-comprehensions.html",
  "./ch-06-collections.html",
  "./ch-07-ndarray.html",
  "./ch-08-indexing.html",
  "./ch-09-axis.html",
  "./ch-10-broadcasting.html",
  "./ch-11-views-copies.html",
  "./ch-12-series-dataframe.html",
  "./ch-13-loc-iloc.html",
  "./ch-14-filtering.html",
  "./ch-15-groupby.html",
  "./ch-16-merge.html",
  "./ch-17-missing.html",
  "./ch-18-dates-reshape.html",
  "./ch-19-order-of-execution.html",
  "./ch-20-select-where-null.html",
  "./ch-21-group-by-having.html",
  "./ch-22-subqueries-cte.html",
  "./ch-23-window-functions.html",
  "./ch-24-indexes-explain.html",
  "./ch-25-sql-vs-pandas.html",
  "./ch-26-project.html",
  "./diagnostic.html",
  "./index.html",
  "./manifest.webmanifest",
  "./snippets/01_dict_lab.py",
  "./snippets/03_list_tuple_lab.py",
  "./snippets/04_set_lab.py",
  "./snippets/05_comprehensions_lab.py"
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
