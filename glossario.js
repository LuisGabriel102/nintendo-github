/* glossario.js — termos técnicos viram "botões": tocou, aparece a explicação simples embaixo da tela. */
(function () {
  "use strict";
  // [termo exibido, expressão (regex), explicação simples]
  var G = [
    ["amiibo", "amiibos?", "Bonequinhos e cartões da Nintendo com um chip (NFC). Ao encostar no console, liberam bônus nos jogos, como roupas, personagens ou itens."],
    ["NFC", "NFC", "Comunicação por aproximação, a mesma do pagamento por aproximação do celular. É assim que o amiibo conversa com o console."],
    ["Flipper Zero", "Flipper Zero", "Aparelhinho de bolso, vendido livremente, que lê e imita sinais como NFC, controle remoto e cartões. Dá para usá-lo para 'fingir' ser um amiibo."],
    ["dump", "dumps?|despej\\w*", "Cópia exata de algo tirada de um aparelho ou mídia: de um cartucho, da memória do console, de um amiibo. Fazer dump do que é seu é cópia de segurança; espalhar dumps é distribuir o conteúdo."],
    ["JSON", "JSON", "Formato de arquivo de texto organizado (listas e campos), fácil para programas lerem. Muito usado para guardar dados."],
    ["NSP", "NSP", "Formato de arquivo de jogo/atualização do Switch como vem da eShop. É o 'instalador' de um jogo."],
    ["XCI", "XCI", "Cópia (dump) de um cartucho de Switch inteiro em um arquivo."],
    ["NSZ / XCZ", "NSZ|XCZ", "Versões comprimidas (menores) de NSP e XCI."],
    ["ROM", "ROMs?", "Arquivo com o conteúdo de um jogo (geralmente de cartucho) para rodar em emulador. Ter a ROM do seu próprio cartucho é cópia de segurança; baixar ROMs de jogos que você não tem é pirataria."],
    ["ISO", "ISOs?", "Cópia de um disco inteiro em um arquivo (ex.: jogos de GameCube e Wii)."],
    ["emulador", "emulador(?:es)?|emulação|emula", "Programa que imita um videogame no PC ou celular, para rodar os jogos dele. Emulador em si é legal; o problema é de onde vêm os jogos."],
    ["firmware", "firmwares?", "O 'sistema operacional' do console (como o Android do celular). A Nintendo atualiza de tempos em tempos."],
    ["CFW", "CFW|custom firmware|firmware customizado|firmware modificado", "Firmware customizado: uma versão modificada do sistema do console que libera coisas que a Nintendo bloqueia (homebrew, mods, traduções — e também pirataria)."],
    ["Atmosphère", "Atmosph[eè]re", "O CFW mais usado no Switch. Roda por cima do sistema original e libera homebrew, mods e traduções."],
    ["hekate", "hekate", "Programa que liga primeiro no Switch desbloqueado e escolhe o que iniciar (o sistema original ou o Atmosphère). Também faz backups."],
    ["homebrew", "homebrews?", "Programa feito por fãs (não pela Nintendo) para rodar no console: gerenciadores de save, players de vídeo, jogos independentes."],
    ["Tinfoil", "Tinfoil", "Programa para Switch desbloqueado que instala jogos. Ficou famoso porque aceita 'lojas' — listas na internet de jogos para baixar sem pagar."],
    ["loja (Tinfoil)", "lojas?(?= do Tinfoil| Tinfoil| estilo Tinfoil)|shops?", "Endereço na internet que o Tinfoil lê como um 'cardápio' de jogos para baixar e instalar. Quase sempre com jogos piratas."],
    ["Google Drive", "Google Drive", "Serviço de guardar arquivos do Google. Muito usado para hospedar jogos piratas, porque é rápido e gratuito."],
    ["chaves (prod.keys / title.keys)", "prod\\.?keys|title\\.?keys|chaves de criptografia|chaves do Switch|chaves", "Códigos secretos que o Switch usa para trancar os jogos. Cada console tem as suas; sem elas, nenhum programa consegue abrir os arquivos de jogo. Espalhar essas chaves é distribuir material protegido."],
    ["ticket", "tickets?", "O 'recibo' digital que prova que você comprou um jogo na eShop. Sem ele o jogo não abre."],
    ["eShop", "eShop", "A loja digital oficial da Nintendo."],
    ["LayeredFS", "LayeredFS", "Recurso do Atmosphère que troca arquivos do jogo na hora em que ele roda, sem mexer no original. É assim que funcionam mods e traduções de fã."],
    ["RomFS", "RomFS", "A 'pasta' de dentro do jogo onde ficam textos, imagens, sons e fontes. É o que se edita numa tradução."],
    ["payload", "payloads?", "Pequeno programa enviado ao Switch por cabo, num modo especial, para iniciar o desbloqueio."],
    ["RCM", "RCM", "Modo de recuperação escondido dos primeiros Switch, usado para enviar o payload e desbloquear o console."],
    ["emuMMC", "emuMMC|emuNAND", "Uma cópia do sistema do Switch dentro do cartão SD. O desbloqueio roda nela, sem mexer no sistema original."],
    ["NAND", "NAND", "A memória interna do console, onde fica o sistema."],
    ["sysmodule", "sysmodules?|módulo de sistema", "Programa que fica rodando em segundo plano no Switch desbloqueado (ex.: overclock, controles de outros consoles)."],
    ["overlay", "overlays?", "Menu que aparece por cima do jogo, chamado por uma combinação de botões."],
    ["overclock", "overclock|underclock", "Fazer o processador trabalhar mais rápido (ou mais devagar) que o normal. Melhora o desempenho, mas esquenta e gasta mais bateria."],
    ["cheat", "cheats?|trapaças?|trainer", "Códigos que mudam o jogo (vida infinita, dinheiro, etc.)."],
    ["save", "saves?", "O arquivo com o seu progresso no jogo."],
    ["decompilação", "decompila\\w*", "Reconstruir, a partir do jogo pronto, um código que o programador consegue ler e modificar. Exige o jogo original para funcionar."],
    ["recompilação / port", "recompila\\w*|ports? nativos?|port\\b", "Transformar um jogo de console em programa que roda direto no PC/celular, sem emulador. Normalmente exige que você tenha o jogo."],
    ["romhack", "romhacks?", "Versão modificada de um jogo feita por fãs (fases novas, histórias novas, traduções)."],
    ["patch", "patch(?:es)?", "Arquivo que aplica mudanças num jogo que você já tem (correções, traduções, mods). Não contém o jogo."],
    ["mod", "mods?", "Modificação feita por fãs num jogo: visual, personagens, fases, regras."],
    ["tradução de fã", "tradução de fã|fan translation|汉化", "Tradução feita por fãs, sem ligação com a empresa, normalmente distribuída como patch."],
    ["BIOS", "BIOS", "Programa interno do console que alguns emuladores precisam para funcionar. É material da fabricante; o certo é extrair do seu aparelho."],
    ["CIA", "CIA", "Formato de instalador de jogos e apps do 3DS."],
    ["NUS / CDN", "NUS|CDN", "Os servidores de onde os consoles baixam jogos e atualizações oficiais. Programas que baixam direto deles sem compra facilitam a pirataria."],
    ["flashcart", "flashcarts?|flash ?cart", "Cartucho especial onde se grava ROMs num cartão de memória para rodar no console original."],
    ["modchip", "modchips?", "Chip soldado dentro do console para desbloqueá-lo."],
    ["repositório", "repositórios?", "A 'pasta' de um projeto no GitHub, com o código, as instruções e as versões para baixar."],
    ["estrelas (★)", "estrelas", "Os 'curtir' do GitHub. Quanto mais estrelas, mais gente acompanha o projeto."],
    ["Releases", "Releases?", "Aba do GitHub com as versões prontas para baixar — o programa já montado, sem precisar mexer em código."],
    ["fork", "forks?", "Cópia de um projeto que alguém fez para mudar por conta própria."],
    ["código aberto", "código aberto|open source", "Projeto que mostra todo o seu código para qualquer pessoa ver, conferir e melhorar."],
    ["bot", "bots?", "Programa que age sozinho: joga, responde mensagens, faz trocas automaticamente."],
    ["Discord", "Discord", "Aplicativo de chat por servidores, muito usado por comunidades de jogos."],
    ["Pokémon GO", "Pokémon GO", "Jogo de celular da Niantic (não da Nintendo) em que se captura Pokémon andando pela rua."],
    ["frontend", "frontends?", "Programa 'vitrine' que organiza jogos e emuladores num menu bonito."],
    ["libretro / núcleo", "libretro|núcleos?", "O libretro é o sistema por trás do RetroArch; cada 'núcleo' é um emulador de um console diferente."],
    ["FPGA", "FPGA", "Chip que pode ser 'reconfigurado' para virar o circuito de um console antigo — recria o hardware em vez de imitar por software."],
    ["linha de comando", "linha de comando|terminal|CLI", "Programa usado digitando comandos em texto, sem botões e janelas."],
    ["raspa (scraper)", "raspa|scraper|raspador", "Programa que entra num site automaticamente e copia as informações dele."],
    ["Zona cinzenta", "Zona cinzenta", "Não é crime por si só, mas contorna proteções do console: pode dar banimento online e, no Brasil, responsabilidade civil (Lei 9.610/98, art. 107)."],
    ["banimento", "banimento|banir|banido", "Quando a Nintendo detecta pirataria ou modificação e bloqueia o console ou a conta de usar o online e a eShop — geralmente para sempre."],
    ["malware", "malware|vírus", "Programa malicioso escondido: rouba senhas, minera criptomoeda ou dá acesso ao seu aparelho para outra pessoa."],
    ["isca", "isca", "Repositório montado para parecer útil (emulador, crack, jogo grátis) e levar a pessoa a baixar um arquivo perigoso."],
    ["crack / keygen", "cracks?|crackead\\w*|keygen", "Programas que burlam a licença de um software pago. Muitas vezes vêm com vírus."],
    ["DMCA", "DMCA", "Lei americana usada para pedir a retirada de conteúdo que viola direitos autorais. No GitHub, só o dono dos direitos pode pedir."]
  ];
  var MAPA = {}, partes = [];
  G.forEach(function (g, i) { MAPA[i] = g; partes.push("(" + g[1] + ")"); });
  var RE = new RegExp("(^|[^\\wÀ-ÿ])(" + partes.join("|") + ")(?=$|[^\\wÀ-ÿ])", "gi");
  function qual(m) {
    for (var i = 0; i < G.length; i++) if (new RegExp("^(?:" + G[i][1] + ")$", "i").test(m)) return i;
    return -1;
  }
  var ALVOS = ".faz,.forte,.como,.risco,.ocu-m,.t-desc,.dif p,.lei p,.tab td,.card p,.rec,.nota,.passos li";
  function marcar(raiz) {
    (raiz || document).querySelectorAll(ALVOS).forEach(function (el) {
      if (el.getAttribute("data-g")) return; el.setAttribute("data-g", "1");
      var vistos = {}, w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT, null), nos = [], n;
      while ((n = w.nextNode())) { if (!n.parentNode.closest("a,button,code,.termo")) nos.push(n); }
      nos.forEach(function (t) {
        var s = t.nodeValue; RE.lastIndex = 0; if (!RE.test(s)) return; RE.lastIndex = 0;
        var frag = document.createDocumentFragment(), ult = 0, m;
        while ((m = RE.exec(s))) {
          var palavra = m[2], i = qual(palavra), ini = m.index + m[1].length;
          if (i < 0 || vistos[i]) continue;
          vistos[i] = 1;
          frag.appendChild(document.createTextNode(s.slice(ult, ini)));
          var b = document.createElement("button"); b.type = "button"; b.className = "termo"; b.setAttribute("data-i", i); b.textContent = palavra;
          frag.appendChild(b); ult = ini + palavra.length;
        }
        if (!ult) return;
        frag.appendChild(document.createTextNode(s.slice(ult)));
        t.parentNode.replaceChild(frag, t);
      });
    });
  }
  // folha de explicação
  var css = document.createElement("style");
  css.textContent = [
    ".termo{font:inherit;color:inherit;background:none;border:0;padding:0;margin:0;cursor:help;text-decoration:underline dotted;text-decoration-color:var(--blue);text-underline-offset:3px;text-decoration-thickness:2px}",
    ".termo:hover,.termo:focus{color:var(--blue);outline:none}",
    "#gl-folha{position:fixed;left:10px;right:10px;bottom:calc(10px + env(safe-area-inset-bottom));z-index:70;max-width:560px;margin:0 auto;background:var(--surface);color:var(--ink);border:1px solid var(--line);border-top:4px solid var(--blue);border-radius:14px;padding:14px 16px;box-shadow:0 10px 30px rgba(0,0,0,.3);display:grid;gap:6px}",
    "#gl-folha[hidden]{display:none}",
    "#gl-folha h4{margin:0;font-family:var(--font-display);font-size:17px;padding-right:36px}",
    "#gl-folha p{margin:0;font-size:15px;line-height:1.5}",
    "#gl-folha .x{position:absolute;top:8px;right:8px;width:34px;height:34px;border-radius:50%;border:1px solid var(--line);background:var(--surface);color:var(--ink);font-size:16px;cursor:pointer}",
    "#gl-folha a{font-size:13px}",
    ".gl-lista{display:grid;gap:8px;grid-template-columns:repeat(auto-fill,minmax(260px,1fr))}",
    ".gl-lista div{border:1px solid var(--line);border-radius:10px;padding:10px 12px;background:var(--surface)}",
    ".gl-lista b{display:block;font-family:var(--font-display);margin-bottom:2px}"
  ].join("\n");
  document.head.appendChild(css);
  var folha = document.createElement("div"); folha.id = "gl-folha"; folha.hidden = true;
  folha.innerHTML = '<button class="x" type="button" aria-label="Fechar">✕</button><h4></h4><p></p><a href="glossario.html">📖 Ver o glossário completo</a>';
  document.body.appendChild(folha);
  document.addEventListener("click", function (e) {
    var b = e.target.closest(".termo");
    if (b) {
      e.preventDefault(); e.stopPropagation();
      var g = MAPA[b.getAttribute("data-i")];
      folha.querySelector("h4").textContent = "📖 " + g[0];
      folha.querySelector("p").textContent = g[2];
      folha.hidden = false; return;
    }
    if (e.target.closest("#gl-folha .x") || (!e.target.closest("#gl-folha") && !folha.hidden)) folha.hidden = true;
  }, true);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") folha.hidden = true; });
  // página do glossário
  function listaCompleta() {
    var alvo = document.getElementById("gl-todos"); if (!alvo) return;
    alvo.innerHTML = G.slice().sort(function (a, b) { return a[0].localeCompare(b[0], "pt"); })
      .map(function (g) { return '<div data-s="' + (g[0] + " " + g[2]).toLowerCase().replace(/"/g, "") + '" class="card"><b>' + g[0] + "</b>" + g[2] + "</div>"; }).join("");
  }
  window.GLOS = { marcar: marcar };
  function iniciar() { listaCompleta(); marcar(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", iniciar); else iniciar();
})();
