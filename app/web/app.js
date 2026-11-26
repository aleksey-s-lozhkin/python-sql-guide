const $ = (id) => document.getElementById(id);

const CHAPTERS = [
  ["ch-01-python-collections", "01 · Карта коллекций", 1],
  ["ch-02-dict", "02 · dict", 1],
  ["ch-03-list-tuple", "03 · list и tuple", 1],
  ["ch-04-set", "04 · set", 1],
  ["ch-05-comprehensions", "05 · Comprehensions", 1],
  ["ch-06-collections", "06 · collections", 1],
  ["ch-07-ndarray", "07 · ndarray", 2],
  ["ch-08-indexing", "08 · Индексация и маски", 2],
  ["ch-09-axis", "09 · axis", 2],
  ["ch-10-broadcasting", "10 · Broadcasting", 2],
  ["ch-11-views-copies", "11 · Views и copies", 2],
  ["ch-12-series-dataframe", "12 · Series и DataFrame", 3],
  ["ch-13-loc-iloc", "13 · loc и iloc", 3],
  ["ch-14-filtering", "14 · Фильтрация", 3],
  ["ch-15-groupby", "15 · groupby", 3],
  ["ch-16-merge", "16 · merge", 3],
  ["ch-17-missing", "17 · Пропуски", 3],
  ["ch-18-dates-reshape", "18 · Даты и reshape", 3],
  ["ch-19-order-of-execution", "19 · Порядок выполнения", 4],
  ["ch-20-select-where-null", "20 · SELECT и NULL", 4],
  ["ch-21-group-by-having", "21 · GROUP BY", 4],
  ["ch-22-subqueries-cte", "22 · Подзапросы и CTE", 4],
  ["ch-23-window-functions", "23 · Оконные функции", 4],
  ["ch-24-indexes-explain", "24 · Индексы и EXPLAIN", 4],
  ["ch-25-sql-vs-pandas", "25 · SQL или pandas", 5],
  ["ch-26-project", "26 · Проект", 5],
];

const state = { user: null, tasks: [], progress: {}, current: null, mode: "login" };

async function api(path, options = {}) {
  const res = await fetch(path, {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  let data = null;
  try { data = await res.json(); } catch (e) { /* пусто */ }
  if (!res.ok) {
    const err = new Error((data && data.detail) || "HTTP " + res.status);
    err.status = res.status;
    throw err;
  }
  return data;
}

function esc(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function showAuth() {
  $("auth-view").hidden = false;
  $("app-view").hidden = true;
  $("who").textContent = "";
  $("logout").hidden = true;
}

function showApp() {
  $("auth-view").hidden = true;
  $("app-view").hidden = false;
  $("who").textContent = state.user.email;
  $("logout").hidden = false;
}

async function boot() {
  try {
    const cfg = await api("/api/config");
    if (cfg.book_url) $("book-link").href = cfg.book_url;
  } catch (e) { /* не критично */ }

  try {
    state.user = await api("/api/me");
  } catch (e) {
    showAuth();
    return;
  }
  showApp();
  await Promise.all([loadProgress(), loadTasks()]);
}

async function loadProgress() {
  const data = await api("/api/progress");
  state.progress = {};
  data.items.forEach((item) => { state.progress[item.slug] = item.status; });
  renderProgress();
}

function renderProgress() {
  const box = $("progress");
  box.innerHTML = "";
  let part = 0;
  CHAPTERS.forEach(([slug, title, chapterPart]) => {
    if (chapterPart !== part) {
      part = chapterPart;
      const divider = document.createElement("div");
      divider.className = "muted small";
      divider.style.margin = "8px 0 2px";
      divider.textContent = ["I · Python", "II · NumPy", "III · pandas", "IV · SQL", "V · Интеграция"][part - 1];
      box.appendChild(divider);
    }
    const label = document.createElement("label");
    const input = document.createElement("input");
    input.type = "checkbox";
    input.checked = state.progress[slug] === "done";
    input.addEventListener("change", () => toggleProgress(slug, input.checked));
    label.appendChild(input);
    label.appendChild(document.createTextNode(title));
    box.appendChild(label);
  });
}

async function toggleProgress(slug, done) {
  try {
    if (done) {
      await api("/api/progress/" + encodeURIComponent(slug), {
        method: "PUT",
        body: JSON.stringify({ status: "done" }),
      });
      state.progress[slug] = "done";
    } else {
      await api("/api/progress/" + encodeURIComponent(slug), { method: "DELETE" });
      delete state.progress[slug];
    }
  } catch (e) {
    alert("Не удалось сохранить прогресс: " + e.message);
  }
}

async function loadTasks() {
  const data = await api("/api/tasks");
  state.tasks = data.items;
  renderTasks();
}

function renderTasks() {
  const box = $("task-list");
  box.innerHTML = "";
  state.tasks.forEach((task) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "task-btn";
    btn.innerHTML =
      "<strong>" + esc(task.title) + "</strong>" +
      "<span>глава " + esc(task.chapter || "—") + " · " + esc(task.difficulty || "задача") + "</span>";
    btn.addEventListener("click", () => openTask(task.slug));
    box.appendChild(btn);
  });
}

async function openTask(slug) {
  $("task-empty").hidden = true;
  $("task-view").hidden = false;
  $("result").hidden = true;
  const task = await api("/api/tasks/" + encodeURIComponent(slug));
  state.current = task;
  $("task-title").textContent = task.title;
  $("task-meta").textContent = "глава " + (task.chapter || "—");
  $("task-prompt").textContent = task.prompt;
  $("hints-list").innerHTML = "";
  if (task.hints && task.hints.length) {
    $("task-hints").hidden = false;
    task.hints.forEach((hint) => {
      const li = document.createElement("li");
      li.textContent = hint;
      $("hints-list").appendChild(li);
    });
  } else {
    $("task-hints").hidden = true;
  }
  $("sql").value = "";
  $("sql").focus();
}

async function runTask() {
  if (!state.current) return;
  const sql = $("sql").value.trim();
  if (!sql) {
    $("run-status").textContent = "Сначала напишите запрос.";
    return;
  }
  const button = $("run");
  button.disabled = true;
  $("run-status").textContent = "Выполняем…";
  try {
    const result = await api("/api/tasks/" + encodeURIComponent(state.current.slug) + "/check", {
      method: "POST",
      body: JSON.stringify({ sql }),
    });
    renderResult(result);
  } catch (e) {
    renderResult({ ok: false, error: e.message });
  } finally {
    button.disabled = false;
    $("run-status").textContent = "";
  }
}

function renderResult(result) {
  const box = $("result");
  box.hidden = false;
  box.className = "result " + (result.ok ? "ok" : "bad");
  const rows = result.rows || [];
  let html = "<h3>" + (result.ok ? "Верно" : "Пока не совпало") + "</h3>";
  if (result.error) html += "<p class='error'>" + esc(result.error) + "</p>";
  if (result.expected_count !== undefined) {
    html += "<p class='note'>Строк: получено " + result.got_count + ", ожидалось " + result.expected_count + ".</p>";
  }
  if (rows.length) {
    html += "<table><thead><tr>";
    (result.columns || []).forEach((col) => { html += "<th>" + esc(col) + "</th>"; });
    html += "</tr></thead><tbody>";
    rows.forEach((row) => {
      html += "<tr>";
      row.forEach((value) => {
        html += "<td>" + (value === null ? "NULL" : esc(value)) + "</td>";
      });
      html += "</tr>";
    });
    html += "</tbody></table>";
  }
  if (result.missing && result.missing.length) {
    html += "<p class='note'>Не хватает: " + result.missing.map(esc).join("; ") + "</p>";
  }
  if (result.extra && result.extra.length) {
    html += "<p class='note'>Лишние: " + result.extra.map(esc).join("; ") + "</p>";
  }
  box.innerHTML = html;
}

function setMode(mode) {
  state.mode = mode;
  $("tab-login").classList.toggle("active", mode === "login");
  $("tab-register").classList.toggle("active", mode === "register");
  $("auth-submit").textContent = mode === "login" ? "Войти" : "Зарегистрироваться";
  $("password").autocomplete = mode === "login" ? "current-password" : "new-password";
  $("auth-error").hidden = true;
}

async function submitAuth(event) {
  event.preventDefault();
  const email = $("email").value.trim();
  const password = $("password").value;
  $("auth-error").hidden = true;
  try {
    await api("/api/auth/" + state.mode, {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
    state.user = await api("/api/me");
    showApp();
    await Promise.all([loadProgress(), loadTasks()]);
  } catch (e) {
    $("auth-error").textContent = e.message;
    $("auth-error").hidden = false;
  }
}

async function logout() {
  try { await api("/api/auth/logout", { method: "POST" }); } catch (e) { /* пусто */ }
  state.user = null;
  showAuth();
}

$("tab-login").addEventListener("click", () => setMode("login"));
$("tab-register").addEventListener("click", () => setMode("register"));
$("auth-form").addEventListener("submit", submitAuth);
$("logout").addEventListener("click", logout);
$("run").addEventListener("click", runTask);
$("sql").addEventListener("keydown", (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key === "Enter") runTask();
});

boot();
