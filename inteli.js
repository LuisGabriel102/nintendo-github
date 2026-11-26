/* inteli.js — busca inteligente: entende assuntos e sinônimos em português e mostra um cartão explicando o tema. */
(function () {
  "use strict";
  function norm(t) { return String(t || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); }
  var PARE = ("a o as os de da do das dos e em um uma uns umas para pra por com sem no na nos nas que como qual quais sobre " +
              "the of and for to in on with is ser sao eh tem ter").split(" ");
  function raiz(w) {  // "stemming" simples: plural e terminações comuns
    if (w.length > 4) w = w.replace(/(oes|aes|ais|eis|ois)$/, "o").replace(/(ns)$/, "m").replace(/(es|s)$/, "");
    return w;
  }
  // temas: gatilhos (regex em texto normalizado), termos extras para procurar, explicação, se mostra ocultos de pirataria
  var TEMAS = [
    { id: "catalogo", tit: "📚 Catálogos e lojas de jogos",
      gat: /catalog|loja|shop|store|indice|vitrine|cardapio|lista de jogo|banco de dados|titledb|database/,
      extra: ["catalogo", "loja", "shop", "store", "indice", "lista de jogos", "titledb", "banco de dados", "eshop", "biblioteca", "tinfoil", "ownfoil", "nut", "database", "vitrine"],
      pir: 1,
      txt: "“Catálogo de jogos” pode ser três coisas bem diferentes: (1) a <b>loja oficial</b> (eShop) e bancos de dados com nomes e códigos dos jogos (titledb) — legítimo; " +
           "(2) programas que organizam <b>a sua própria biblioteca</b> e mandam os seus jogos para o seu console (ownfoil, nut) — legítimo; " +
           "(3) <b>“lojas” do Tinfoil</b> e índices com jogos de terceiros guardados em Google Drive ou servidores — <b>pirataria</b>." },
    { id: "pirataria", tit: "🏴‍☠️ Jogos piratas e pirataria",
      gat: /pirat|ilegal|sem licenca|warez|crack|baixar jogo|download de jogo|jogos? gratis|rom gratis|copia ilegal/,
      extra: ["pirataria", "pirata", "sem licenca", "baixa jogos", "download", "rom", "nsp", "xci", "tinfoil", "loja", "chaves", "prod.keys", "crack", "material protegido", "facilita pirataria", "direito autoral"],
      pir: 1,
      txt: "Pirataria é copiar, baixar ou distribuir jogos, firmware ou chaves <b>sem autorização</b> de quem tem os direitos. " +
           "Aqui aparecem as ferramentas e sites encontrados (sem link) e o que diz a lei: Código Penal art. 184 e Lei do Software 9.609/98. " +
           "<a href=\"riscos.html\">⚖️ Ver a página completa sobre pirataria, golpe e vírus</a>." },
    { id: "biblioteca", tit: "🗂️ Bibliotecas de jogos",
      gat: /bibliotec|library|colec|acervo|gerenciad|organiz|launcher|frontend/,
      extra: ["biblioteca", "library", "colecao", "gerenciador", "gerencia", "organiza", "launcher", "frontend", "catalogo", "backup", "ownfoil", "nut", "playnite", "retroarch"],
      pir: 1,
      txt: "Uma <b>biblioteca de jogos</b> legítima organiza os jogos que <b>você tem</b> (capas, nomes, versões) e abre no emulador ou manda para o seu console — ex.: frontends, ownfoil, nut. " +
           "Vira pirataria quando a “biblioteca” é de jogos <b>de outras pessoas</b>, compartilhada para qualquer um baixar." },
    { id: "instalacao", tit: "📡 Instalação de jogos pela internet ou pela rede",
      gat: /instal|install|online|pela rede|rede local|wifi|wi-fi|internet|remot|servidor|nuvem|google drive|usb/,
      extra: ["instalar", "instalador", "instala", "install", "installer", "rede", "network", "servidor", "server", "online", "internet", "google drive", "drive", "tinfoil", "dbi", "awoo", "goldleaf", "sphaira", "loja", "shop", "nsp", "nut", "ownfoil"],
      pir: 1,
      txt: "Instaladores para Switch desbloqueado (Awoo, Goldleaf, DBI, sphaira, Tinfoil) conseguem instalar jogos <b>pelo cabo, pela rede de casa ou pela internet</b>. " +
           "Isso é legítimo com os <b>seus</b> arquivos (cópia do seu cartucho ou da sua conta). A <b>“instalação online pirata”</b> acontece quando o instalador é apontado para uma " +
           "<b>“loja”</b> — um endereço com jogos de terceiros em Google Drive ou servidores — e o console baixa e instala sem pagar." },
    { id: "golpe", tit: "🎣 Golpes",
      gat: /golpe|fraude|scam|gift ?card|codigo.*gratis|gratis.*codigo|gerador|generator|cartao presente|ganhe/,
      extra: ["golpe", "fraude", "codigos gratis", "gift card", "gerador", "eshop", "roubo de conta", "login", "senha"],
      pir: 1,
      txt: "Golpe é <b>enganar</b> para tirar dinheiro, dados ou a conta: “códigos grátis da eShop”, “gerador de gift card”, console “desbloqueado com 100 jogos” que nunca chega. " +
           "A vítima não recebe nada. Pode configurar estelionato (Código Penal art. 171) e fraude eletrônica." },
    { id: "virus", tit: "🦠 Vírus e iscas",
      gat: /virus|malware|isca|trojan|perigos|seguranca|seguro|roubar senha|hack(?!ing)/,
      extra: ["malware", "virus", "isca", "padrao de isca", "roubo de conta", "suspeito"],
      pir: 1,
      txt: "Vírus (malware) vem <b>disfarçado</b> de emulador, crack ou jogo grátis e, ao abrir, rouba senhas, minera criptomoeda ou dá acesso ao aparelho. " +
           "Aqui os casos aparecem como <b>suspeitos</b> quando só o padrão de isca foi identificado." },
    { id: "emulador", tit: "🎮 Emuladores",
      gat: /emula/, extra: ["emulador", "emula", "emulator", "dolphin", "cemu", "azahar", "melonds", "mgba", "retroarch"],
      txt: "Emulador é um programa que imita um videogame no PC ou celular. <b>Emulador é legal</b>; o problema é de onde vêm os jogos (o certo é usar cópias dos seus)." },
    { id: "desbloqueio", tit: "🔓 Desbloqueio (CFW)",
      gat: /desbloque|destrav|cfw|custom firmware|atmosphere|hekate|jailbreak|modific|hackear/,
      extra: ["cfw", "atmosphere", "hekate", "desbloqueio", "desbloqueado", "custom firmware", "emummc", "payload", "rcm", "homebrew"],
      txt: "Desbloquear o console (CFW, como o Atmosphère) libera homebrew, mods e traduções. <b>Não é crime por si só</b>, mas contorna proteções: pode dar <b>banimento online</b> " +
           "e, no Brasil, responsabilidade civil (Lei 9.610/98, art. 107). Também é a porta de entrada para a pirataria." },
    { id: "traducao", tit: "🌐 Traduções de fã",
      gat: /tradu|portugues|legenda|localiza|patch.*pt|ptbr|pt-br|hanhua|汉化/,
      extra: ["traducao", "tradutor", "traduz", "translation", "localizacao", "patch", "texto", "fonte", "msbt", "kuriimu"],
      txt: "Traduções de fã são <b>patches</b> aplicados no jogo que você já tem — não contêm o jogo. Ferramentas como Switch-Toolbox e Kuriimu abrem textos, fontes e imagens." },
    { id: "amiibo", tit: "🪆 amiibo",
      gat: /amiibo|nfc|flipper|tagmo/, extra: ["amiibo", "nfc", "flipper", "tagmo", "bin", "dump"],
      txt: "amiibo são bonecos com chip NFC que liberam bônus. Gravar o <b>seu</b> amiibo é backup; espalhar arquivos de centenas de amiibos para quem não comprou é distribuir material protegido." }
  ];
  function analisar(q) {
    var nq = norm(q).trim(), toks = nq.split(/[^a-z0-9.+#-]+/).filter(function (w) { return w && PARE.indexOf(w) < 0; }).map(raiz);
    var temas = TEMAS.filter(function (t) { return t.gat.test(nq); });
    var extras = [];
    temas.forEach(function (t) { t.extra.forEach(function (e) { e = norm(e); if (extras.indexOf(e) < 0) extras.push(e); }); });
    if (temas.length) {  // com assunto, palavras genéricas não contam
      var GEN = ["jogo", "game", "nintendo", "console", "video", "videogame", "programa", "app", "online", "pirata", "pirataria"];
      toks = toks.filter(function (w) { return GEN.indexOf(w) < 0; });
    }
    return { q: nq, toks: toks, extras: extras, temas: temas, pir: temas.some(function (t) { return t.pir; }) };
  }
  // pontua um texto já normalizado; campos: [{t: texto, p: peso}]
  function pontuar(campos, an) {
    if (!an.q) return 1;
    var s = 0, achouTok = 0;
    campos.forEach(function (c) {
      if (!c.t) return;
      if (an.q.length > 3 && c.t.indexOf(an.q) >= 0) s += 6 * c.p;           // frase inteira
      an.toks.forEach(function (w) { if (w.length > 1 && c.t.indexOf(w) >= 0) { s += 2 * c.p; achouTok++; } });
      an.extras.forEach(function (e) { if (c.t.indexOf(e) >= 0) s += 1 * c.p; });
    });
    // com tema: precisa bater em algum termo do assunto (ou na frase inteira)
    if (an.temas.length) {
      var tudo2 = campos.map(function (c) { return c.t || ""; }).join(" ");
      var bate = an.extras.some(function (e) { return tudo2.indexOf(e) >= 0; }) || tudo2.indexOf(an.q) >= 0;
      if (!bate) return 0;
    }
    // sem tema: exige que todas as palavras apareçam em algum campo
    if (!an.temas.length) {
      var tudo = campos.map(function (c) { return c.t || ""; }).join(" ");
      if (!an.toks.every(function (w) { return tudo.indexOf(w) >= 0; })) return 0;
    }
    return s;
  }
  function cartao(an) {
    if (!an.temas.length) return "";
    return an.temas.slice(0, 2).map(function (t) {
      return '<div class="tema"><h3>' + t.tit + "</h3><p>" + t.txt + "</p></div>";
    }).join("");
  }
  window.INTELI = { norm: norm, analisar: analisar, pontuar: pontuar, cartao: cartao };
})();
