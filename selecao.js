/* selecao.js — "Minha seleção": estrela ☆/★ em cada card + botão flutuante.
   Fica no aparelho (localStorage), na mesma chave dos "guardados" do Tinder (ngh-T-sim). */
(function () {
  "use strict";
  var K = "ngh-T-sim";
  function ler() { try { var v = JSON.parse(localStorage.getItem(K) || "{}"); return v && typeof v === "object" && !Array.isArray(v) ? v : {}; } catch (e) { return {}; } }
  function gravar(v) { try { localStorage.setItem(K, JSON.stringify(v)); } catch (e) {} }
  function chave(n) { return String(n || "").trim().replace(/^https?:\/\/github\.com\//i, "").replace(/\.git$/, "").replace(/\/+$/, "").split(/[?#]/)[0]; }
  var SEL = window.SEL = {
    todos: function () { return ler(); },
    tem: function (n) { var s = ler(), k = chave(n).toLowerCase(); return Object.keys(s).some(function (x) { return x.toLowerCase() === k; }); },
    add: function (n, extra) {
      var s = ler(), k = chave(n); if (!/^[\w.-]+\/[\w.-]+$/.test(k)) return false;
      if (SEL.tem(k)) return false;
      var o = extra || {}; o.n = k; o.u = "https://github.com/" + k; o.t = Date.now();
      s[k] = o; gravar(s); SEL.pintar(); return true;
    },
    del: function (n) {
      var s = ler(), k = chave(n).toLowerCase();
      Object.keys(s).forEach(function (x) { if (x.toLowerCase() === k) delete s[x]; });
      gravar(s); SEL.pintar();
    },
    conta: function () { return Object.keys(ler()).length; },
    // marca os botões ☆/★ e atualiza o contador flutuante
    pintar: function (raiz) {
      var s = ler(), set = {};
      Object.keys(s).forEach(function (x) { set[x.toLowerCase()] = 1; });
      (raiz || document).querySelectorAll("[data-sel]").forEach(function (b) {
        var on = !!set[b.getAttribute("data-sel").toLowerCase()];
        b.setAttribute("aria-pressed", on); b.textContent = on ? "★ Na seleção" : "☆ Selecionar";
      });
      var f = document.getElementById("sel-flut");
      if (f) { var n = Object.keys(s).length; f.querySelector("b").textContent = n; f.hidden = !n && !/minha\.html/.test(location.pathname); }
    }
  };
  // ---- estilo ----
  var css = document.createElement("style");
  css.textContent = [
    ".sel{margin-left:auto;font:inherit;font-size:12px;font-weight:600;border:1px solid var(--line);background:var(--surface);color:var(--muted);border-radius:999px;padding:2px 10px;cursor:pointer;white-space:nowrap}",
    ".sel[aria-pressed=\"true\"]{border-color:var(--star);background:var(--star-bg);color:var(--star)}",
    "#sel-flut{position:fixed;right:14px;bottom:calc(14px + env(safe-area-inset-bottom));z-index:30;display:flex;align-items:center;gap:6px;background:var(--accent);color:var(--accent-ink);font-weight:700;border-radius:999px;padding:11px 16px;box-shadow:0 6px 18px rgba(0,0,0,.28);text-decoration:none}",
    "#sel-flut[hidden]{display:none}",
    "#sel-flut b{background:var(--accent-ink);color:var(--accent);border-radius:999px;padding:0 8px;font-size:13px}",
    "html.t-aberto #sel-flut{display:none}"
  ].join("\n");
  document.head.appendChild(css);
  // ---- botão nos cards do guia (os da lista já vêm com o botão) ----
  function porNosCards() {
    document.querySelectorAll(".card[data-repo]").forEach(function (c) {
      if (c.querySelector("[data-sel]")) return;
      var bs = c.querySelector(".bs"); if (!bs) return;
      var b = document.createElement("button"); b.className = "sel"; b.type = "button";
      b.setAttribute("data-sel", c.getAttribute("data-repo")); bs.appendChild(b);
    });
  }
  function flutuante() {
    if (/minha\.html/.test(location.pathname)) return;
    var a = document.createElement("a"); a.id = "sel-flut"; a.href = "minha.html";
    a.innerHTML = "⭐ Minha seleção <b>0</b>"; document.body.appendChild(a);
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-sel]"); if (!b) return;
    e.preventDefault();
    var n = b.getAttribute("data-sel");
    if (SEL.tem(n)) SEL.del(n);
    else {
      var c = b.closest(".card"), d = c && c.querySelector(".faz"), g = c && c.getAttribute("data-g");
      SEL.add(n, { d: d ? d.textContent.trim() : "", g: g || "" });
    }
  });
  window.addEventListener("storage", function (e) { if (e.key === K) SEL.pintar(); });
  function iniciar() { porNosCards(); flutuante(); SEL.pintar(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", iniciar); else iniciar();
})();
