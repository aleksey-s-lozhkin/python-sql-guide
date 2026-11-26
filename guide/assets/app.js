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

    return `
      <a class="brand" href="index.html">
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
        ${parts}
        <div class="nav-part">
          <div class="t"><span>◆</span>Инструменты</div>
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

/* ── место чтения: продолжить с того же места ──────────────── */
(function reading() {
  const KEY = "assoc-reader";
  const pageSlug = document.body.dataset.slug || "";
  let saved = null;
  try { saved = JSON.parse(localStorage.getItem(KEY) || "null"); } catch {}

  if (saved && saved.slug === pageSlug && !location.hash && saved.y > 240) {
    setTimeout(() => window.scrollTo(0, saved.y), 40);
  }

  let timer = null;
  const save = () => {
    const doc = document.documentElement;
    const max = doc.scrollHeight - window.innerHeight;
    const y = Math.round(window.scrollY);
    const h1 = document.querySelector("h1");
    try {
      localStorage.setItem(KEY, JSON.stringify({
        slug: pageSlug,
        y,
        ratio: max > 0 ? Math.min(1, y / max) : 0,
        title: h1 ? h1.firstChild.textContent.trim() : document.title,
      }));
    } catch {}
  };
  window.addEventListener("scroll", () => {
    if (timer) return;
    timer = setTimeout(() => { timer = null; save(); }, 400);
  }, { passive: true });

  const host = document.getElementById("resume");
  if (host && saved && saved.slug && saved.slug !== "index" && saved.title) {
    host.innerHTML = `<a class="resume" href="${saved.slug}.html">
      <span class="k">Продолжить чтение</span>
      <span class="t">${saved.title}</span>
      <span class="p">${Math.round((saved.ratio || 0) * 100)}%</span></a>`;
  }
})();
