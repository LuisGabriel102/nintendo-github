/* tempo.js — "atualizado há X" calculado na hora em que a página abre */
window.quandoTxt = function (p, arq) {
  if (!p) return null;
  var d = new Date(p + "T12:00:00"), dias = Math.floor((Date.now() - d.getTime()) / 864e5), t, c;
  if (dias < 1) t = "hoje"; else if (dias < 2) t = "ontem";
  else if (dias < 31) t = "há " + dias + " dias";
  else if (dias < 365) { var m = Math.round(dias / 30.4); t = "há " + m + (m > 1 ? " meses" : " mês"); }
  else { var a = Math.floor(dias / 365); t = "há " + a + (a > 1 ? " anos" : " ano"); }
  c = arq ? "q-arq" : dias <= 60 ? "q-viva" : dias <= 365 ? "q-ok" : dias <= 730 ? "q-lenta" : "q-parada";
  var ic = { "q-viva": "🟢", "q-ok": "🟢", "q-lenta": "🟡", "q-parada": "⚪", "q-arq": "⚪" }[c];
  return { t: ic + " " + (arq ? "arquivado · última mudança " : "atualizado ") + t, c: c };
};
window.preencherQuando = function (raiz) {
  (raiz || document).querySelectorAll(".quando[data-p]:not([data-ok])").forEach(function (el) {
    var q = window.quandoTxt(el.getAttribute("data-p"), el.getAttribute("data-a") === "1");
    if (q) { el.textContent = q.t; el.className = "quando " + q.c; el.setAttribute("data-ok", "1"); }
  });
};
document.addEventListener("DOMContentLoaded", function () { window.preencherQuando(); });
