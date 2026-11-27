/* Логика книги: навигация, прогресс, подсветка кода, мелкие удобства. */
(function () {
  "use strict";

  const BOOK = window.BOOK;
  const STORE = "assoc-guide-v1";
  const slug = document.body.dataset.slug || "";

  /* ── локальное состояние ───────────────────────────────────── */
  function load() {
    try { return JSON.parse(localStorage.getItem(STORE)) || {}; }
    catch { return {}; }
  }
  function save(state) {
    try { localStorage.setItem(STORE, JSON.stringify(state)); } catch {}
  }
  const state = Object.assign({ checked: {}, done: {} }, load());

  function chapterDone(ch) {
    if (state.done[ch.slug]) return true;
    if (ch.slug !== slug) return false;
    const boxes = [...document.querySelectorAll(".check input")];
    return boxes.length > 0 && boxes.every(b => state.checked[b.dataset.key]);
  }

  /* ── сайдбар ───────────────────────────────────────────────── */
  function sidebarHTML() {
    const parts = BOOK.parts.map(p => {
      const chs = BOOK.chapters.filter(c => c.part === p.n);
      const items = chs.map(c => {
        const soon = !c.ready;
        const act = c.slug === slug ? " active" : "";
        const done = chapterDone(c) ? " done" : "";
        return `<a class="nav-ch${act}${done}${soon ? " soon" : ""}" href="${c.slug}.html">`
          + `<span class="n">${c.n}</span><span>${c.title}</span>`
          + (soon ? `<span class="flag">скоро</span>` : "") + `</a>`;
      }).join("");
      return `<div class="nav-part"><div class="t"><span>${p.n}</span>${p.title}</div>${items}</div>`;
    }).join("");

    const total = BOOK.chapters.length;
    const done = BOOK.chapters.filter(chapterDone).length;
    const pct = Math.round((done / total) * 100);

    const ref = (BOOK.reference || []).filter(r => r.hub).map(r => {
      const act = (slug === r.slug || slug.startsWith("ref-")) ? " active" : "";
      return `<a class="nav-ch${act}" href="${r.file}">`
        + `<span class="n">📖</span><span>${r.title}</span></a>`;
    }).join("");

    return `
      <a class="brand" href="index.html?stay=1">
        <span class="kicker">Обучающий гайд</span>
        <span class="name">Python <em>→</em> pandas <em>→</em> SQL</span>
      </a>
      <div class="progress-wrap">
        <div class="progress-top"><span>Освоено глав</span><span>${done} / ${total}</span></div>
        <div class="progress-bar"><i style="width:${pct}%"></i></div>
      </div>
      <button class="menu-btn" aria-expanded="false">Оглавление</button>
      <div class="nav-wrap">
        <div class="reader-bar"><span>Размер текста</span><button data-rs="-0.05" title="Мельче">А−</button><button data-rs="0.05" title="Крупнее">А+</button></div>
        <div class="nav-part">
          <div class="t"><span>◆</span>Справочник</div>
          ${ref}
        </div>
        ${parts}
        <div class="nav-part">
          <div class="t"><span>◆</span>Инструменты</div>
          <a class="nav-ch${slug === "appendix-snippets" ? " active" : ""}" href="appendix-snippets.html">
            <span class="n">📎</span><span>Файлы лабораторий</span>
          </a>
          <a class="nav-ch${slug === "diagnostic" ? " active" : ""}" href="diagnostic.html">
            <span class="n">20′</span><span>Диагностика коллекций</span>
          </a>
          <a class="nav-ch${slug === "checkpoint-1" ? " active" : ""}" href="checkpoint-1.html">
            <span class="n">60′</span><span>Проверочная: часть I</span>
          </a>
          <a class="nav-ch${slug === "checkpoint-2" ? " active" : ""}" href="checkpoint-2.html">
            <span class="n">60′</span><span>Проверочная: часть II</span>
          </a>
          <a class="nav-ch${slug === "checkpoint-3" ? " active" : ""}" href="checkpoint-3.html">
            <span class="n">60′</span><span>Проверочная: часть III</span>
          </a>
          <a class="nav-ch${slug === "checkpoint-4" ? " active" : ""}" href="checkpoint-4.html">
            <span class="n">60′</span><span>Проверочная: SQL</span>
          </a>
        </div>
      </div>
      <div class="side-foot">
        Демо-выпуск: готовы обложка и глава 02.<br>
        <span class="net" id="net">проверяю офлайн-копию…</span>
      </div>`;
  }

  const sb = document.getElementById("sidebar");
  if (sb) {
    sb.innerHTML = sidebarHTML();
    const btn = sb.querySelector(".menu-btn");
    if (btn) btn.addEventListener("click", () => {
      sb.classList.toggle("open");
      btn.setAttribute("aria-expanded", sb.classList.contains("open"));
    });
  }

  /* ── чек-листы ─────────────────────────────────────────────── */
  const boxes = [...document.querySelectorAll(".check input")];
  boxes.forEach((b, i) => {
    b.dataset.key = `${slug}:${i}`;
    b.checked = !!state.checked[b.dataset.key];
    b.addEventListener("change", () => {
      if (b.checked) state.checked[b.dataset.key] = true;
      else delete state.checked[b.dataset.key];
      const all = boxes.every(x => x.checked);
      if (all) state.done[slug] = true;
      else delete state.done[slug];
      save(state);
      const bar = document.querySelector(".progress-bar > i");
      const cnt = document.querySelector(".progress-top span:last-child");
      const done = BOOK.chapters.filter(chapterDone).length;
      if (bar) bar.style.width = Math.round((done / BOOK.chapters.length) * 100) + "%";
      if (cnt) cnt.textContent = `${done} / ${BOOK.chapters.length}`;
      b.closest("label").classList.toggle("on", b.checked);
    });
  });

  /* ── подсветка кода ────────────────────────────────────────── */
  const PY_KW = new Set(("False None True and as assert async await break class continue def del elif else except finally for from global if import in is lambda nonlocal not or pass raise return try while with yield").split(" "));
  const PY_BI = new Set(("abs all any bool dict dir divmod enumerate filter float format frozenset getattr hasattr hash id input int isinstance iter len list map max min next object open ord pow print range repr reversed round set setattr slice sorted str sum super tuple type zip self cls").split(" "));
  const SQL_KW = new Set(("select from where group by having order limit offset join inner left right full outer on using as distinct insert into values update set delete create table primary key foreign references not null unique check default index drop alter add column and or in between like ilike is exists case when then else end with recursive union all intersect except over partition rows range unbounded preceding following current row asc desc count sum avg min max coalesce nullif cast explain analyse analyze").split(" "));

  const esc = s => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

  function hlPy(src) {
    const re = /("""[\s\S]*?"""|'''[\s\S]*?'''|"(?:[^"\\\n]|\\.)*"|'(?:[^'\\\n]|\\.)*'|f"(?:[^"\\\n]|\\.)*")|(#[^\n]*)|\b(0x[0-9a-fA-F]+|\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\b|\b([A-Za-z_]\w*)\b/g;
    let out = "", last = 0, m;
    while ((m = re.exec(src))) {
      out += esc(src.slice(last, m.index));
      const [tok, str, com, num, word] = m;
      if (str) out += `<span class="tok-s">${esc(str)}</span>`;
      else if (com) out += `<span class="tok-c">${esc(com)}</span>`;
      else if (num) out += `<span class="tok-n">${esc(num)}</span>`;
      else {
        if (PY_KW.has(word)) out += `<span class="tok-k">${esc(word)}</span>`;
        else if (PY_BI.has(word)) out += `<span class="tok-b">${esc(word)}</span>`;
        else out += esc(word);
      }
      last = m.index + tok.length;
    }
    return out + esc(src.slice(last));
  }

  function hlSql(src) {
    const re = /('(?:[^']|'')*')|(--[^\n]*)|\b(\d+(?:\.\d+)?)\b|\b([A-Za-z_]\w*)\b/g;
    let out = "", last = 0, m;
    while ((m = re.exec(src))) {
      out += esc(src.slice(last, m.index));
      const [tok, str, com, num, word] = m;
      if (str) out += `<span class="tok-s">${esc(str)}</span>`;
      else if (com) out += `<span class="tok-c">${esc(com)}</span>`;
      else if (num) out += `<span class="tok-n">${esc(num)}</span>`;
      else if (SQL_KW.has(word.toLowerCase())) out += `<span class="tok-k">${esc(word)}</span>`;
      else out += esc(word);
      last = m.index + tok.length;
    }
    return out + esc(src.slice(last));
  }

  document.querySelectorAll("pre[data-lang]").forEach(pre => {
    const lang = pre.dataset.lang;
    const src = pre.textContent.replace(/^\n+|\s+$/g, "");
    pre.innerHTML = lang === "sql" ? hlSql(src) : hlPy(src);
    const box = pre.closest(".code");
    if (box) {
      const btn = box.querySelector("button.copy");
      if (btn) btn.addEventListener("click", () => {
        navigator.clipboard?.writeText(src).catch(() => {});
        btn.textContent = "скопировано";
        setTimeout(() => (btn.textContent = "копировать"), 1400);
      });
    }
  });

  /* ── клавиатура: ← → ───────────────────────────────────────── */
  document.addEventListener("keydown", e => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const tag = (e.target.tagName || "").toLowerCase();
    if (tag === "input" || tag === "textarea") return;
    const prev = document.querySelector(".pager a.prev:not(.off)");
    const next = document.querySelector(".pager a.next:not(.off)");
    if (e.key === "ArrowLeft" && prev) location.href = prev.href;
    if (e.key === "ArrowRight" && next) location.href = next.href;
  });
})();

/* ── оглавление на обложке ─────────────────────────────────── */
(function renderTOC() {
  const host = document.getElementById("toc");
  if (!host) return;
  host.innerHTML = BOOK.parts.map(p => {
    const items = BOOK.chapters.filter(c => c.part === p.n).map(c => {
      const inner = `<span class="n">${c.n}</span><span class="t">${c.title}</span><span class="d">${c.desc}</span>`;
      return `<li><a class="${c.ready ? "" : "off"}" href="${c.slug}.html">${inner}</a></li>`;
    }).join("");
    return `<div class="part"><h3><b>${p.n}</b>${p.title}<span style="margin-left:auto;text-transform:none;letter-spacing:0;color:var(--muted)">${p.range}</span></h3><ol>${items}</ol></div>`;
  }).join("");
})();

/* ── PWA: офлайн-копия для чтения в дороге ─────────────────── */
(function pwa() {
  const net = document.getElementById("net");
  const setNet = (txt, cls) => {
    if (!net) return;
    net.textContent = txt;
    net.className = "net " + (cls || "");
  };

  if (!("serviceWorker" in navigator) || !/^https?:$/.test(location.protocol)) {
    setNet("кэш недоступен при открытии файлом", "warn");
    return;
  }

  const ready = () =>
    navigator.onLine
      ? setNet("офлайн-копия готова", "ok")
      : setNet("вы офлайн — книга открывается", "off");

  navigator.serviceWorker
    .register("./sw.js")
    .then(() => {
      if (navigator.serviceWorker.controller) ready();
      else navigator.serviceWorker.addEventListener("controllerchange", ready);
    })
    .catch(() => setNet("офлайн-копия не включилась", "warn"));

  window.addEventListener("offline", ready);
  window.addEventListener("online", ready);
  ready();
})();

/* ── размер текста для чтения с телефона ───────────────────── */
(function reader() {
  const KEY = "assoc-rs";
  const root = document.documentElement;
  let scale = parseFloat(localStorage.getItem(KEY) || "1");
  const apply = () => {
    root.style.setProperty("--rs", scale.toFixed(2));
    document.querySelectorAll(".reader-bar [data-rs]").forEach((b) => {
      const d = parseFloat(b.dataset.rs);
      b.disabled = (d < 0 && scale <= 0.9) || (d > 0 && scale >= 1.35);
    });
  };
  apply();
  document.querySelectorAll(".reader-bar [data-rs]").forEach((b) =>
    b.addEventListener("click", () => {
      scale = Math.min(1.35, Math.max(0.9, +(scale + parseFloat(b.dataset.rs)).toFixed(2)));
      try { localStorage.setItem(KEY, scale); } catch {}
      apply();
    })
  );
})();

/* ── место чтения и закладки ─────────────────────────────── */
(function reading() {
  const LAST = "assoc-reader";
  const MARKS = "assoc-bookmarks";
  const AUTO = "assoc-autoresume";
  const pageSlug = document.body.dataset.slug || "";
  const isIndex = pageSlug === "index";
  const isChapter = /^ch-/.test(pageSlug);
  let saved = null;
  try { saved = JSON.parse(localStorage.getItem(LAST) || "null"); } catch {}

  if ("scrollRestoration" in history) history.scrollRestoration = "manual";

  function escText(value) {
    return String(value).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function headings() {
    const hs = [...document.querySelectorAll(".wrap h2, .wrap h3")];
    hs.forEach((h, i) => { if (!h.id) h.id = "sec-" + i; });
    return hs;
  }

  function position() {
    const y = Math.round(window.scrollY);
    const max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
    let best = null;
    headings().forEach((h) => {
      const top = h.getBoundingClientRect().top + y;
      if (top <= y + 60) best = { id: h.id, top };
    });
    const h1 = document.querySelector("h1");
    return {
      slug: pageSlug,
      y,
      ratio: Math.min(1, Math.max(0, y / max)),
      anchor: best ? best.id : "",
      offset: best ? Math.max(0, y - best.top) : y,
      title: h1 ? (h1.firstChild ? h1.firstChild.textContent.trim() : h1.textContent.trim()) : document.title,
      updatedAt: Date.now(),
    };
  }

  function storePosition() {
    if (!isChapter) return;
    try { localStorage.setItem(LAST, JSON.stringify(position())); } catch {}
  }

  function readMarks() {
    try { return JSON.parse(localStorage.getItem(MARKS) || "[]") || []; } catch { return []; }
  }
  function writeMarks(list) {
    try { localStorage.setItem(MARKS, JSON.stringify(list.slice(0, 30))); } catch {}
  }

  function targetFrom(s) {
    if (s.anchor) {
      const el = document.getElementById(s.anchor);
      if (el) return Math.round(el.getBoundingClientRect().top + window.scrollY + (s.offset || 0));
    }
    return Math.round(s.y || 0);
  }

  function restore(s) {
    const max = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
    const target = Math.max(0, Math.min(max, targetFrom(s)));
    if (target < 80) return;
    const apply = () => window.scrollTo(0, target);
    requestAnimationFrame(() => requestAnimationFrame(apply));
    setTimeout(apply, 140);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(() => setTimeout(apply, 80));
  }

  if (saved && saved.slug === pageSlug && !isIndex && !location.hash) {
    restore(saved);
  }

  let timer = null;
  const saveSoon = () => {
    if (timer) return;
    timer = setTimeout(() => { timer = null; storePosition(); }, 300);
  };
  window.addEventListener("scroll", saveSoon, { passive: true });
  window.addEventListener("pagehide", storePosition);
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "hidden") storePosition();
  });

  function toast(text) {
    let el = document.querySelector(".toast");
    if (!el) {
      el = document.createElement("div");
      el.className = "toast";
      el.setAttribute("role", "status");
      document.body.appendChild(el);
    }
    el.textContent = text;
    el.classList.add("show");
    clearTimeout(el._t);
    el._t = setTimeout(() => el.classList.remove("show"), 2400);
  }

  if (isChapter) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "bookmark-fab";
    btn.id = "bookmark-fab";
    btn.title = "Поставить закладку на этом месте";
    btn.setAttribute("aria-label", "Поставить закладку на этом месте");
    btn.textContent = "🔖";
    document.body.appendChild(btn);
    btn.classList.toggle("on", readMarks().some((m) => m.slug === pageSlug));
    btn.addEventListener("click", () => {
      const list = readMarks();
      const idx = list.findIndex((m) => m.slug === pageSlug);
      if (idx >= 0) {
        list.splice(idx, 1);
        btn.classList.remove("on");
        toast("Закладка снята");
      } else {
        list.unshift(Object.assign(position(), { createdAt: Date.now() }));
        btn.classList.add("on");
        toast("Закладка сохранена — она есть на обложке");
      }
      writeMarks(list);
      renderMarks();
    });
  }

  const host = document.getElementById("resume");
  const marksHost = document.getElementById("bookmarks");
  const autoOn = () => localStorage.getItem(AUTO) !== "0";
  const standalone = window.matchMedia("(display-mode: standalone)").matches || navigator.standalone === true;
  const params = new URLSearchParams(location.search);

  function renderMarks() {
    if (!isIndex || !marksHost) return;
    const list = readMarks();
    if (!list.length) { marksHost.innerHTML = ""; return; }
    marksHost.innerHTML = '<div class="marks-head"><span>Закладки</span><span class="muted">' + list.length + '</span></div>' +
      list.map((m, i) => '<div class="mark-row">' +
        '<a class="resume mark-link" href="' + escText(m.slug) + '.html?continue=1">' +
          '<span class="k">Закладка</span><span class="t">' + escText(m.title) + '</span>' +
          '<span class="p">' + Math.round((m.ratio || 0) * 100) + '%</span></a>' +
        '<button type="button" class="mark-del" data-i="' + i + '" aria-label="Удалить закладку">×</button></div>').join("");
    marksHost.querySelectorAll(".mark-link").forEach((a, i) => {
      a.addEventListener("click", () => {
        try { localStorage.setItem(LAST, JSON.stringify(readMarks()[i])); } catch {}
      });
    });
    marksHost.querySelectorAll(".mark-del").forEach((b) =>
      b.addEventListener("click", () => {
        const list2 = readMarks();
        list2.splice(Number(b.dataset.i), 1);
        writeMarks(list2);
        renderMarks();
      })
    );
  }

  if (isIndex) {
    if (saved && saved.slug && saved.slug !== "index" && saved.title && host) {
      const pct = Math.round((saved.ratio || 0) * 100);
      host.innerHTML = '<a class="resume resume-main" href="' + escText(saved.slug) + '.html?continue=1">' +
        '<span class="k">Продолжить чтение</span>' +
        '<span class="t">' + escText(saved.title) + '</span>' +
        '<span class="p">' + pct + '%</span></a>' +
        '<label class="autoresume"><input type="checkbox" id="auto-resume"' + (autoOn() ? " checked" : "") + '> открывать сразу с этого места при запуске</label>';
      const box = document.getElementById("auto-resume");
      if (box) box.addEventListener("change", () => localStorage.setItem(AUTO, box.checked ? "1" : "0"));
      const fab = document.createElement("a");
      fab.className = "resume-fab";
      fab.href = saved.slug + ".html?continue=1";
      fab.innerHTML = '<span class="k">Продолжить</span><span class="p">' + pct + '%</span>';
      document.body.appendChild(fab);
      const card = document.querySelector(".resume-main");
      if (card && "IntersectionObserver" in window) {
        new IntersectionObserver(([entry]) => { fab.hidden = entry.isIntersecting; }, { threshold: 0.55 }).observe(card);
      }
      let firstLaunch = false;
      try {
        firstLaunch = !sessionStorage.getItem("assoc-pwa-launched");
        sessionStorage.setItem("assoc-pwa-launched", "1");
      } catch (e) { firstLaunch = true; }
      const cameFromInside = document.referrer && document.referrer.startsWith(location.origin);
      if (standalone && autoOn() && firstLaunch && !cameFromInside && !params.has("stay") && !params.has("continue")) {
        location.replace(saved.slug + ".html?continue=1");
        return;
      }
    } else if (host) {
      host.innerHTML = '<a class="resume resume-main" href="ch-01-python-collections.html">' +
        '<span class="k">Начало</span><span class="t">Глава 01 · Карта коллекций</span><span class="p">0%</span></a>';
    }
    renderMarks();
  }
})();
