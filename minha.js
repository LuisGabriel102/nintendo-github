/* minha.js — página "Minha seleção": ver, adicionar (colar nomes/links/conversa), exportar. */
(function () {
  "use strict";
  var $ = function (s) { return document.querySelector(s); };
  var lst = $("#m-lista"), msg = $("#m-msg"), q = $("#q"), info = {}, carregou = false;
  function esc(t) { return String(t == null ? "" : t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function norm(t) { return String(t || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }

  // dados da lista completa (português) para enriquecer a seleção
  function usar(d) { d.forEach(function (r) { info[r[0].toLowerCase()] = r; }); carregou = true; desenhar(); }
  if (window.LISTA) usar(window.LISTA);
  else fetch("lista.json").then(function (r) { return r.json(); }).then(usar).catch(function () { carregou = true; desenhar(); });

  // ---------- extrair dono/repo de qualquer texto ----------
  function extrair(txt) {
    var achados = [], visto = {};
    function por(o, r) {
      r = r.replace(/[.,;:)\]]+$/, "").replace(/\.git$/, "");
      if (!/[a-z]/i.test(o) || !/[a-z]/i.test(r)) return;
      if (/^(www|http|https)$/i.test(o)) return;
      var k = o + "/" + r; if (visto[k.toLowerCase()]) return; visto[k.toLowerCase()] = 1; achados.push(k);
    }
    String(txt).replace(/github\.com\/([\w.-]+)\/([\w.-]+)/gi, function (m, o, r) { por(o, r); return " "; })
      .replace(/(^|[\s(\[:,;])([A-Za-z0-9][\w.-]*)\/([\w.-]+)((?:\s*\+\s*[A-Za-z][\w.-]*)*)/g, function (m, a, o, r, mais) {
        por(o, r);
        (mais || "").split("+").forEach(function (x) { x = x.trim(); if (x) por(o, x); });   // "Dono/A + B" = Dono/B
        return " ";
      });
    return achados;
  }

  function consultarGitHub(k) {
    return fetch("https://api.github.com/repos/" + k, { headers: { Accept: "application/vnd.github+json" } })
      .then(function (r) {
        if (r.status === 404) return { naoExiste: true };
        if (!r.ok) return { semResposta: true };
        return r.json().then(function (j) {
          return { n: j.full_name, d: j.description || "", s: j.stargazers_count, p: (j.pushed_at || "").slice(0, 10), arq: j.archived };
        });
      }).catch(function () { return { semResposta: true }; });
  }

  $("#m-add").addEventListener("click", function () {
    var nomes = extrair($("#m-txt").value);
    if (!nomes.length) { aviso("Não achei nenhum nome no formato dono/repositório (ex.: CTCaer/hekate) nem link do GitHub."); return; }
    var add = [], ja = [], nao = [], incertos = [];
    aviso("Conferindo " + nomes.length + " no GitHub…");
    var fila = nomes.slice();
    (function proximo() {
      var k = fila.shift();
      if (!k) {
        desenhar();
        aviso((add.length ? "✅ " + add.length + " adicionado(s). " : "") + (ja.length ? ja.length + " já estavam na seleção. " : "") +
          (nao.length ? "❌ Não existem no GitHub: " + nao.join(", ") + ". " : "") +
          (incertos.length ? "⚠️ Adicionados sem conferir (GitHub não respondeu): " + incertos.join(", ") + "." : ""));
        if (add.length) $("#m-txt").value = "";
        return;
      }
      if (SEL.tem(k)) { ja.push(k); return proximo(); }
      var loc = info[k.toLowerCase()];
      if (loc) { SEL.add(loc[0], {}); add.push(loc[0]); return proximo(); }
      consultarGitHub(k).then(function (r) {
        if (r.naoExiste) nao.push(k);
        else if (r.semResposta) { SEL.add(k, {}); incertos.push(k); }
        else if (SEL.tem(r.n)) ja.push(r.n);
        else { SEL.add(r.n, { d: r.d, s: r.s, p: r.p, arq: r.arq, fora: 1 }); add.push(r.n); }
        proximo();
      });
    })();
  });

  function aviso(t) { msg.textContent = t; msg.hidden = !t; }

  function itens() {
    var s = SEL.todos();
    return Object.keys(s).map(function (k) {
      var x = s[k], r = info[k.toLowerCase()];
      return r ? { n: r[0], s: r[1], arq: r[2], g: r[3], d: r[4], f: r[5], p: r[6], rel: r[7], relt: r[8], t: x.t || 0, pt: 1 }
               : { n: k, s: x.s, arq: x.arq, g: x.g || "Fora da lista", d: x.d || "", f: "", p: x.p || "", rel: "", relt: "", t: x.t || 0, pt: 0 };
    }).sort(function (a, b) { return b.t - a.t; });
  }

  function desenhar() {
    var xs = itens(), termos = norm(q.value.trim()).split(/\s+/).filter(Boolean);
    var vis = xs.filter(function (x) { var s = norm(x.n + " " + x.g + " " + x.d + " " + x.f); return termos.every(function (t) { return s.indexOf(t) >= 0; }); });
    $("#m-total").textContent = xs.length;
    if (!xs.length) { lst.innerHTML = '<p class="nota">Sua seleção está vazia. Toque em <b>☆ Selecionar</b> nos cards do guia ou da lista, arraste para a direita no Modo Tinder, ou cole nomes acima.</p>'; return; }
    lst.innerHTML = vis.map(function (x) {
      var qd = window.quandoTxt && window.quandoTxt(x.p, x.arq);
      return '<div class="card"><div class="ct"><a href="https://github.com/' + esc(x.n) + '" target="_blank" rel="noopener">' + esc(x.n) + "</a></div>" +
        '<div class="bs">' + (x.s != null ? '<span class="b st">★ ' + esc(x.s) + "</span>" : "") + '<span class="b gr">' + esc(x.g) + "</span>" +
        (x.arq ? '<span class="b arq">ARQ</span>' : "") + '<button class="sel" data-tirar="' + esc(x.n) + '">✕ Tirar</button></div>' +
        (x.d ? '<p class="faz">' + esc(x.d) + (x.pt ? "" : ' <i class="m-en">(descrição original)</i>') + "</p>" : "") +
        (x.f ? '<p class="forte"><b>👍 Faz bem:</b> ' + esc(x.f) + "</p>" : "") +
        '<div class="meta">' + (qd ? '<span class="quando ' + qd.c + '">' + qd.t + "</span>" : "") +
        '<a class="baixar" href="' + esc(x.rel || "https://github.com/" + x.n + "/releases") + '" target="_blank" rel="noopener">⬇ ' + (x.rel ? "Baixar " + esc(x.relt) : "Releases") + "</a></div></div>";
    }).join("") || '<p class="nota">Nada da seleção bate com a busca.</p>';
  }

  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-tirar]"); if (b) { SEL.del(b.getAttribute("data-tirar")); desenhar(); return; }
    var a = e.target.closest("[data-m]"); if (!a) return;
    var tipo = a.getAttribute("data-m"), xs = itens(), txt = xs.map(function (x) { return x.n; }).join("\n");
    if (tipo === "copiar") {
      (navigator.clipboard ? navigator.clipboard.writeText(txt) : Promise.reject()).then(function () { aviso("Lista copiada (" + xs.length + " nomes). Dá para colar de volta aqui em outro aparelho."); }, function () { prompt("Copie:", txt); });
    } else if (tipo === "zap") {
      window.open("https://wa.me/?text=" + encodeURIComponent("Minha seleção Nintendo no GitHub:\n" + xs.map(function (x) { return "• " + x.n + " — https://github.com/" + x.n; }).join("\n")), "_blank");
    } else if (tipo === "txt") {
      var blob = new Blob([xs.map(function (x) { return x.n + "\t" + (x.d || "") + "\thttps://github.com/" + x.n; }).join("\n")], { type: "text/plain;charset=utf-8" });
      var l = document.createElement("a"); l.href = URL.createObjectURL(blob); l.download = "minha-selecao-nintendo.txt"; l.click();
    } else if (tipo === "limpar") {
      if (confirm("Tirar todos os " + xs.length + " da seleção?")) { xs.forEach(function (x) { SEL.del(x.n); }); desenhar(); }
    }
  });
  var t; q.addEventListener("input", function () { clearTimeout(t); t = setTimeout(desenhar, 120); });
  window.addEventListener("storage", desenhar);
  desenhar();
})();
