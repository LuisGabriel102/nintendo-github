/* tinder.js — "🃏 Modo Tinder": um projeto por vez em tela cheia.
   Direita (⭐ / →) = Guardar · Esquerda (✖ / ←) = Pular · Cima (⏭ / ↓) = Depois (vai pro fim)
   ↶ (ou Backspace) desfaz. Esc ou o voltar do celular saem. Tudo fica salvo neste aparelho (localStorage). */
(function () {
  "use strict";
  var K = "ngh-T-";
  function ler(k, p) { try { var v = JSON.parse(localStorage.getItem(K + k) || "null"); return v == null ? p : v; } catch (e) { return p; } }
  function gravar(k, v) { try { localStorage.setItem(K + k, JSON.stringify(v)); } catch (e) {} }
  var guardados = ler("sim", {});   // nome -> {n, u, d, g}
  var pulados = new Set(ler("nao", []));
  var CORES = ["gray", "accent", "blue", "pronta", "pt", "blue", "gray"];

  // ---------- estilo ----------
  var css = document.createElement("style");
  css.textContent = [
    "html.t-aberto{overflow:hidden}",
    ".t-tela{position:fixed;inset:0;z-index:60;background:var(--bg);color:var(--ink);padding:max(8px,env(safe-area-inset-top)) 12px calc(10px + env(safe-area-inset-bottom))}",
    ".t-tela[hidden],.t-lista[hidden]{display:none}",
    ".t-col{max-width:520px;height:100%;margin:0 auto;display:flex;flex-direction:column;gap:8px}",
    ".t-topo{display:flex;align-items:center;gap:10px}",
    ".t-topo h2{font-size:19px;line-height:1.2}",
    ".t-conta{flex:1;min-width:0;font-size:13px;color:var(--muted);line-height:1.3}",
    ".t-conta b{color:var(--ink);font-weight:600}",
    ".t-x{flex:none;width:44px;height:44px;border-radius:50%;border:1px solid var(--line);background:var(--surface);color:var(--ink);font:inherit;font-size:18px;cursor:pointer}",
    ".t-filtros{display:flex;flex-wrap:wrap;gap:8px}",
    ".t-filtros select,.t-filtros button{flex:none;min-height:40px;font:inherit;font-size:14px;border-radius:999px;border:1px solid var(--line);background:var(--surface);color:var(--ink);padding:0 12px}",
    ".t-filtros select{flex:1 1 150px;min-width:0}",
    ".t-filtros button[aria-pressed=\"true\"]{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}",
    ".t-palco{position:relative;flex:1;min-height:0}",
    ".t-card{position:absolute;inset:0;display:flex;flex-direction:column;background:var(--surface);color:var(--ink);border:1px solid var(--line);border-radius:20px;overflow:hidden;box-shadow:0 10px 28px rgba(0,0,0,.16);touch-action:none;user-select:none;-webkit-user-select:none;cursor:grab;transition:transform .32s cubic-bezier(.2,.8,.25,1),opacity .32s ease;will-change:transform;z-index:2}",
    ".t-card.t-baixo{transform:translateY(10px) scale(.95);opacity:.75;z-index:1;pointer-events:none}",
    ".t-card.t-arr{transition:none;cursor:grabbing}",
    ".t-card.t-voa{z-index:3;pointer-events:none}",
    ".t-capa{position:relative;flex:0 0 36%;min-height:130px;display:grid;place-items:center;overflow:hidden;background:var(--cbg);color:var(--c)}",
    ".t-capa .t-fundo{position:absolute;inset:-24px;width:calc(100% + 48px);height:calc(100% + 48px);object-fit:cover;filter:blur(18px) saturate(1.2);opacity:.55}",
    ".t-capa .t-img{position:relative;max-width:94%;max-height:88%;border-radius:12px;box-shadow:0 6px 20px rgba(0,0,0,.3);background:var(--surface)}",
    ".t-capa .t-sem{position:relative;text-align:center}",
    ".t-capa .t-img+.t-sem{display:none}",
    ".t-capa .t-ico{font-size:54px;line-height:1}",
    ".t-capa .t-gr2{position:absolute;left:12px;bottom:10px;font-family:var(--font-display);font-weight:700;font-size:13px;background:var(--surface);color:var(--c);border:1px solid var(--c);border-radius:999px;padding:1px 10px}",
    ".t-bloco{display:grid;gap:4px;padding:10px 12px;border-radius:12px;background:var(--bg);border:1px solid var(--line)}",
    ".t-bloco h4{margin:0;font-family:var(--font-display);font-size:13px;letter-spacing:.04em;text-transform:uppercase;color:var(--muted)}",
    ".t-bloco.t-bem{border-left:4px solid var(--pt);background:var(--pt-bg)}",
    ".t-capa .t-ico{font-size:54px;line-height:1}",
    ".t-capa .t-gr{font-family:var(--font-display);font-weight:700;font-size:15px;margin-top:6px}",
    ".t-capa .t-est{position:absolute;right:12px;top:12px;font-weight:700;font-size:13px;background:var(--surface);color:var(--star);border:1px solid var(--star);border-radius:999px;padding:2px 10px}",
    ".t-capa .t-rec{position:absolute;left:12px;top:12px;font-weight:700;font-size:12px;background:var(--pt);color:#fff;border-radius:999px;padding:2px 10px}",
    ".t-corpo{flex:1;min-height:0;overflow-y:auto;padding:14px 16px 16px;display:grid;gap:8px;align-content:start;touch-action:pan-y}",
    ".t-tit{font-family:var(--font-display);font-size:22px;font-weight:700;line-height:1.2;word-break:break-word}",
    ".t-tit a{color:var(--ink)}",
    ".t-desc{font-size:16px;line-height:1.55}",
    ".t-desc a{pointer-events:auto}",
    ".t-sec{font-size:13px;color:var(--muted)}",
    ".t-ver{justify-self:start;font-weight:600;border:1px solid var(--accent);color:var(--accent);background:var(--accent-soft);border-radius:9px;padding:7px 14px}",
    ".t-carimbo{position:absolute;top:24px;font-family:var(--font-display);font-size:28px;font-weight:800;border:4px solid;border-radius:12px;padding:2px 12px;opacity:0;z-index:4;pointer-events:none;background:var(--surface)}",
    ".t-c-sim{left:20px;color:var(--pt);transform:rotate(-14deg)}",
    ".t-c-nao{right:20px;color:var(--veto);transform:rotate(14deg)}",
    ".t-c-dep{left:50%;top:auto;bottom:40px;transform:translateX(-50%);color:var(--sua)}",
    ".t-bts{display:flex;justify-content:center;align-items:center;gap:14px;padding:4px 0}",
    ".t-bts button{width:58px;height:58px;border-radius:50%;border:2px solid var(--line);background:var(--surface);font-size:24px;cursor:pointer;display:grid;place-items:center;color:var(--ink)}",
    ".t-bts .t-b-nao{border-color:var(--veto);color:var(--veto)}",
    ".t-bts .t-b-sim{border-color:var(--pt);color:var(--pt);width:66px;height:66px;font-size:28px}",
    ".t-bts .t-b-dep{border-color:var(--sua);color:var(--sua);width:50px;height:50px;font-size:20px}",
    ".t-bts .t-desf{width:44px;height:44px;font-size:18px}",
    ".t-dica{text-align:center;font-size:12px;color:var(--muted)}",
    ".t-vazio{position:absolute;inset:0;display:grid;place-items:center;text-align:center;color:var(--muted);padding:20px;gap:10px;align-content:center}",
    ".t-lista{position:fixed;inset:0;z-index:61;background:var(--bg);overflow-y:auto;padding:max(10px,env(safe-area-inset-top)) 14px calc(20px + env(safe-area-inset-bottom))}",
    ".t-lista .t-col{height:auto;gap:10px}",
    ".t-li{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:4px 10px;align-items:center;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:10px 12px}",
    ".t-li b{font-family:var(--font-display);word-break:break-word}",
    ".t-li span{grid-column:1;font-size:13px;color:var(--muted)}",
    ".t-li button{grid-row:1/span 2;grid-column:2;border:1px solid var(--line);background:var(--surface);color:var(--veto);border-radius:9px;padding:6px 10px;font:inherit;font-size:13px}",
    ".t-acoes{display:flex;flex-wrap:wrap;gap:8px}",
    ".t-acoes button{font:inherit;font-size:14px;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:9px;padding:8px 12px}"
  ].join("\n");
  document.head.appendChild(css);

  var ICO = { "Removidos": "🪦", "Switch": "🔴", "3DS": "🟦", "Wii U": "🟦", "Wii/GC": "💿", "DS": "📱", "Game Boy": "🟩", "N64": "🎮", "SNES/NES": "🕹️", "SNES": "🕹️", "NES": "🕹️", "Decomp/ports": "🧩", "Decomp": "🧩", "Pokémon": "⚡", "amiibo": "🪆", "Multi": "🌐", "Zelda": "🗡️", "Mario": "🍄", "Geral": "🎮", "Virtual Boy": "🥽", "Tradução": "📝" };

  // ---------- fontes de dados ----------
  function doGuia() {
    var out = [];
    document.querySelectorAll("details.sec").forEach(function (sec, si) {
      var g = sec.getAttribute("data-g") || ""; if (!g || sec.id === "comece") return;
      sec.querySelectorAll(".card").forEach(function (c) {
        var a = c.querySelector(".ct a"); if (!a) return;
        var desc = c.querySelector(".faz"), fo = c.querySelector(".forte"), sub = c.closest(".in") ? prevH3(c) : "";
        var est = c.querySelector(".st");
        out.push({ repo: c.getAttribute("data-repo") || a.textContent.trim(), f: fo ? fo.innerHTML.replace(/^<b>[^<]*<\/b>\s*/, "") : "", n: a.textContent.trim(), u: a.href, h: c.querySelector(".ct").innerHTML, d: desc ? desc.innerHTML : "",
          g: g, sub: sub, e: est ? est.textContent.replace("★", "").trim() : "", r: c.classList.contains("r"), arq: !!c.querySelector(".arq"), cor: si });
      });
    });
    return out;
  }
  function prevH3(card) {
    var grade = card.parentNode, el = grade && grade.previousElementSibling;
    while (el && el.tagName !== "H3") el = el.previousElementSibling;
    return el ? el.textContent : "";
  }
  var cacheLista = null;
  function daLista(cb) {
    if (cacheLista) return cb(cacheLista);
    fetch("lista.json").then(function (r) { return r.json(); }).then(function (d) {
      var gs = []; cacheLista = d.map(function (r) {
        if (gs.indexOf(r[3]) < 0) gs.push(r[3]);
        return { repo: r[0], f: autoForte(r), n: r[0], u: "https://github.com/" + r[0], h: "", d: esc(r[4] || "(sem descrição)"), g: r[3], sub: "", e: String(r[1]), r: false, arq: !!r[2], cor: gs.indexOf(r[3]) };
      }); cb(cacheLista);
    }).catch(function () { cb([]); });
  }
  function autoForte(r) {
    var e = r[1], t = e >= 5000 ? "Um dos mais populares da comunidade (" + e + " estrelas)" : e >= 1000 ? "Muito usado e conhecido (" + e + " estrelas)" : e >= 300 ? "Projeto consolidado, com boa base de usuários" : "Projeto menor/nichado — vale olhar se o assunto interessa";
    return t + (r[2] ? ". Arquivado: funciona como está, mas não recebe mais atualização." : ".");
  }
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  // ---------- tela ----------
  var tela = document.createElement("div");
  tela.className = "t-tela"; tela.hidden = true;
  tela.innerHTML = '<div class="t-col">' +
    '<div class="t-topo"><h2>🃏 Modo Tinder</h2><div class="t-conta"></div><button class="t-x" data-a="lista" title="Guardados">⭐</button><button class="t-x" data-a="fechar" title="Fechar">✕</button></div>' +
    '<div class="t-filtros"><select data-f="fonte"><option value="guia">Guia explicado (PT)</option><option value="lista">Lista completa (2 mil+)</option></select>' +
    '<select data-f="grupo"><option value="">Todos os consoles</option></select>' +
    '<button data-f="rec" aria-pressed="false">Só recomendados</button><button data-f="vistos" aria-pressed="false">Rever pulados</button></div>' +
    '<div class="t-palco"></div>' +
    '<div class="t-bts"><button class="t-desf" data-a="desf" title="Desfazer">↶</button><button class="t-b-nao" data-a="nao" title="Pular">✖</button><button class="t-b-dep" data-a="dep" title="Depois">⏭</button><button class="t-b-sim" data-a="sim" title="Guardar">⭐</button></div>' +
    '<div class="t-dica">→ guardar · ← pular · ↑ depois · toque no nome para abrir no GitHub</div></div>';
  document.body.appendChild(tela);
  var lista = document.createElement("div");
  lista.className = "t-lista"; lista.hidden = true;
  document.body.appendChild(lista);

  var palco = tela.querySelector(".t-palco"), conta = tela.querySelector(".t-conta");
  var selFonte = tela.querySelector('[data-f="fonte"]'), selGrupo = tela.querySelector('[data-f="grupo"]');
  var btRec = tela.querySelector('[data-f="rec"]'), btVis = tela.querySelector('[data-f="vistos"]');
  var filtro = ler("filtro", { fonte: "guia", grupo: "", rec: false, vistos: false });
  var base = [], fila = [], hist = [], total = 0;

  function montarFila() {
    var pega = filtro.fonte === "lista" ? daLista : function (cb) { cb(doGuia()); };
    pega(function (d) {
      base = d;
      var gs = []; d.forEach(function (x) { if (gs.indexOf(x.g) < 0) gs.push(x.g); });
      selGrupo.innerHTML = '<option value="">Todos os consoles</option>' + gs.map(function (g) { return '<option' + (g === filtro.grupo ? " selected" : "") + ">" + esc(g) + "</option>"; }).join("");
      if (gs.indexOf(filtro.grupo) < 0) filtro.grupo = "";
      var vistos = {}; fila = d.filter(function (x) {
        if (vistos[x.n]) return false; vistos[x.n] = 1;
        if (filtro.grupo && x.g !== filtro.grupo) return false;
        if (filtro.rec && !x.r) return false;
        if (guardados[x.n]) return false;
        if (pulados.has(x.n)) return !!filtro.vistos;
        return !filtro.vistos;
      });
      total = fila.length; hist = [];
      desenhar();
    });
  }

  function capa(x) {
    var rp = String(x.repo || "").split(/[\/#?]/).slice(0, 2).join("/"), dono = rp.split("/")[0];
    if (!/^[\w.-]+\/[\w.-]+$/.test(rp)) return '<div class="t-sem"><div class="t-ico">' + (ICO[x.g] || "🎮") + "</div></div>";
    return '<img class="t-fundo" alt="" loading="lazy" src="https://github.com/' + dono + '.png?size=120" onerror="this.remove()">' +
      '<img class="t-img" alt="Capa de ' + esc(rp) + '" src="https://opengraph.githubassets.com/1/' + rp + '" onerror="this.remove()"><div class="t-sem"><div class="t-ico">' + (ICO[x.g] || "🎮") + '</div></div>';
  }
  function cardHTML(x) {
    var c = "var(--" + CORES[x.cor % CORES.length] + ")", cb = CORES[x.cor % CORES.length];
    var cbg = { accent: "var(--accent-soft)" }[cb] || "var(--" + cb + "-bg)";
    return '<div class="t-carimbo t-c-sim">GUARDAR</div><div class="t-carimbo t-c-nao">PULAR</div><div class="t-carimbo t-c-dep">DEPOIS</div>' +
      '<div class="t-capa" style="--c:' + c + ';--cbg:' + cbg + '">' +
      (x.r ? '<span class="t-rec">★ recomendado</span>' : "") + (x.e ? '<span class="t-est">★ ' + esc(x.e) + "</span>" : "") +
      capa(x) + '<span class="t-gr2">' + (ICO[x.g] || "🎮") + " " + esc(x.g) + "</span></div>" +
      '<div class="t-corpo"><div class="t-tit"><a href="' + x.u + '" target="_blank" rel="noopener">' + esc(x.n) + "</a></div>" +
      (x.sub || x.arq ? '<div class="t-sec">' + esc(x.sub) + (x.arq ? (x.sub ? " · " : "") + "arquivado (sem atualização)" : "") + "</div>" : "") +
      '<div class="t-bloco"><h4>O que faz</h4><div class="t-desc">' + x.d + "</div></div>" +
      (x.f ? '<div class="t-bloco t-bem"><h4>👍 O que faz bem</h4><div class="t-desc">' + x.f + "</div></div>" : "") +
      '<a class="t-ver" href="' + x.u + '" target="_blank" rel="noopener">Abrir no GitHub ↗</a></div>';
  }

  function desenhar() {
    palco.innerHTML = "";
    var feitos = total - fila.length;
    conta.innerHTML = "<b>" + feitos + "</b> de " + total + " · ⭐ " + Object.keys(guardados).length + " guardados";
    if (!fila.length) {
      palco.innerHTML = '<div class="t-vazio"><div style="font-size:44px">🎉</div><div>' + (total ? "Você viu todos deste filtro." : "Nada neste filtro.") +
        '</div><div class="t-acoes" style="justify-content:center"><button data-a="lista">Ver guardados</button><button data-a="rever">Rever pulados</button></div></div>';
      return;
    }
    for (var i = Math.min(1, fila.length - 1); i >= 0; i--) {
      var el = document.createElement("div");
      el.className = "t-card" + (i ? " t-baixo" : "");
      el.innerHTML = cardHTML(fila[i]);
      palco.appendChild(el);
      if (!i) arrastavel(el);
    }
  }

  function decidir(tipo) {
    if (!fila.length) return;
    var x = fila[0], el = palco.querySelector(".t-card:not(.t-baixo)");
    hist.push({ x: x, tipo: tipo });
    if (tipo === "sim") { guardados[x.n] = { n: x.n, u: x.u, d: x.d.replace(/<[^>]+>/g, ""), g: x.g }; gravar("sim", guardados); }
    if (tipo === "nao") { pulados.add(x.n); gravar("nao", Array.from(pulados)); }
    fila.shift(); if (tipo === "dep") fila.push(x);
    if (el) {
      el.classList.add("t-voa");
      el.style.transform = tipo === "sim" ? "translateX(130%) rotate(18deg)" : tipo === "nao" ? "translateX(-130%) rotate(-18deg)" : "translateY(-120%)";
      el.style.opacity = "0";
      setTimeout(desenhar, 230);
    } else desenhar();
  }
  function desfazer() {
    var h = hist.pop(); if (!h) return;
    if (h.tipo === "sim") { delete guardados[h.x.n]; gravar("sim", guardados); }
    if (h.tipo === "nao") { pulados.delete(h.x.n); gravar("nao", Array.from(pulados)); }
    if (h.tipo === "dep") fila.pop();
    fila.unshift(h.x); desenhar();
  }

  function arrastavel(el) {
    var x0 = 0, y0 = 0, dx = 0, dy = 0, ativo = false, id = null;
    var cs = el.querySelector(".t-c-sim"), cn = el.querySelector(".t-c-nao"), cd = el.querySelector(".t-c-dep");
    el.addEventListener("pointerdown", function (e) {
      if (e.target.closest("a")) return;
      ativo = true; id = e.pointerId; x0 = e.clientX; y0 = e.clientY; dx = dy = 0;
      el.classList.add("t-arr"); try { el.setPointerCapture(id); } catch (er) {}
    });
    el.addEventListener("pointermove", function (e) {
      if (!ativo || e.pointerId !== id) return;
      dx = e.clientX - x0; dy = e.clientY - y0;
      el.style.transform = "translate(" + dx + "px," + Math.min(dy, 40) + "px) rotate(" + dx / 18 + "deg)";
      cs.style.opacity = Math.max(0, Math.min(1, dx / 90));
      cn.style.opacity = Math.max(0, Math.min(1, -dx / 90));
      cd.style.opacity = Math.abs(dx) < 60 ? Math.max(0, Math.min(1, -dy / 90)) : 0;
    });
    function solta(e) {
      if (!ativo || (e && e.pointerId !== id)) return;
      ativo = false; el.classList.remove("t-arr");
      var w = palco.clientWidth;
      if (dx > w * 0.28) decidir("sim");
      else if (dx < -w * 0.28) decidir("nao");
      else if (dy < -110 && Math.abs(dx) < 80) decidir("dep");
      else { el.style.transform = ""; cs.style.opacity = cn.style.opacity = cd.style.opacity = 0; }
    }
    el.addEventListener("pointerup", solta);
    el.addEventListener("pointercancel", solta);
  }

  function mostrarLista() {
    var g = Object.keys(guardados).map(function (k) { return guardados[k]; });
    lista.innerHTML = '<div class="t-col"><div class="t-topo"><h2>⭐ Guardados (' + g.length + ')</h2><div class="t-conta"></div><button class="t-x" data-a="voltar">✕</button></div>' +
      '<div class="t-acoes"><button data-a="copiar">Copiar lista</button><button data-a="zerar-nao">Esquecer pulados (' + pulados.size + ')</button><button data-a="zerar-sim">Apagar guardados</button></div>' +
      (g.length ? g.map(function (x) {
        return '<div class="t-li"><b><a href="' + x.u + '" target="_blank" rel="noopener">' + esc(x.n) + '</a></b><span>' + esc(x.g) + " · " + esc((x.d || "").slice(0, 140)) + '</span><button data-del="' + esc(x.n) + '">tirar</button></div>';
      }).join("") : '<p class="t-dica" style="font-size:15px">Nada guardado ainda. Arraste para a direita os que interessam.</p>') + "</div>";
    lista.hidden = false;
  }

  function abrir() {
    tela.hidden = false; document.documentElement.classList.add("t-aberto");
    selFonte.value = filtro.fonte; btRec.setAttribute("aria-pressed", filtro.rec); btVis.setAttribute("aria-pressed", filtro.vistos);
    history.pushState({ t: 1 }, ""); montarFila();
  }
  function fechar(semHist) {
    if (tela.hidden) return;
    tela.hidden = true; lista.hidden = true; document.documentElement.classList.remove("t-aberto");
    if (!semHist && history.state && history.state.t) history.back();
  }
  window.addEventListener("popstate", function () { if (!lista.hidden) { lista.hidden = true; history.pushState({ t: 1 }, ""); return; } fechar(true); });

  function salvarFiltro() { gravar("filtro", filtro); montarFila(); }
  selFonte.addEventListener("change", function () { filtro.fonte = selFonte.value; filtro.grupo = ""; salvarFiltro(); });
  selGrupo.addEventListener("change", function () { filtro.grupo = selGrupo.value; salvarFiltro(); });
  btRec.addEventListener("click", function () { filtro.rec = !filtro.rec; btRec.setAttribute("aria-pressed", filtro.rec); salvarFiltro(); });
  btVis.addEventListener("click", function () { filtro.vistos = !filtro.vistos; btVis.setAttribute("aria-pressed", filtro.vistos); salvarFiltro(); });

  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-a],[data-del],#t-abrir"); if (!b) return;
    if (b.id === "t-abrir") { e.preventDefault(); abrir(); return; }
    if (b.hasAttribute("data-del")) { delete guardados[b.getAttribute("data-del")]; gravar("sim", guardados); mostrarLista(); return; }
    var a = b.getAttribute("data-a");
    if (a === "fechar") fechar();
    else if (a === "sim" || a === "nao" || a === "dep") decidir(a);
    else if (a === "desf") desfazer();
    else if (a === "lista") mostrarLista();
    else if (a === "voltar") { lista.hidden = true; montarFila(); }
    else if (a === "rever") { filtro.vistos = true; btVis.setAttribute("aria-pressed", true); salvarFiltro(); }
    else if (a === "zerar-nao") { if (confirm("Esquecer todos os pulados?")) { pulados.clear(); gravar("nao", []); mostrarLista(); } }
    else if (a === "zerar-sim") { if (confirm("Apagar todos os guardados?")) { guardados = {}; gravar("sim", guardados); mostrarLista(); } }
    else if (a === "copiar") {
      var txt = Object.keys(guardados).map(function (k) { return guardados[k].n + " — " + guardados[k].u; }).join("\n");
      (navigator.clipboard ? navigator.clipboard.writeText(txt) : Promise.reject()).then(function () { b.textContent = "Copiado ✓"; }, function () { prompt("Copie:", txt); });
    }
  });
  document.addEventListener("keydown", function (e) {
    if (tela.hidden || !lista.hidden || /INPUT|SELECT/.test(e.target.tagName)) return;
    if (e.key === "ArrowRight") decidir("sim");
    else if (e.key === "ArrowLeft") decidir("nao");
    else if (e.key === "ArrowDown" || e.key === "ArrowUp") decidir("dep");
    else if (e.key === "Backspace") { e.preventDefault(); desfazer(); }
    else if (e.key === "Escape") fechar();
  });
  if (location.hash === "#tinder") setTimeout(abrir, 50);
})();
