# Gera o site (index.html + lista.html + lista.json) a partir do GITHUB-NINTENDO.md
# e dos JSON de busca. Uso: python -I gerar.py <pasta_dos_json_de_busca>
import re, json, glob, os, sys, html

AQUI = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(os.path.dirname(AQUI), 'GITHUB-NINTENDO.md')
GH = sys.argv[1] if len(sys.argv) > 1 else None

# ---------- recomendados (selo verde) ----------
REC = set('''Atmosphere-NX/Atmosphere CTCaer/hekate SciresM/hactool jakcron/nstool julesontheroad/NSC_BUILDER
nicoboss/nsz KillzXGaming/Switch-Toolbox FanTranslatorsInternational/Kuriimu2 zeldamods/oead J-D-K/JKSV
NaGaa95/sphaira HamletDuFromage/aio-switch-updater ndeadly/MissionControl exelix11/SysDVR mtheall/ftpd
retronx-team/sys-clk ppkantorski/Ultrahand-Overlay Huntereb/Awoo-Installer LumaTeam/Luma3DS d0k3/GodMode9
Universal-Team/Universal-Updater azahar-emu/azahar dnasdw/3dstool cemu-project/Cemu wiiu-env/Aroma
dolphin-emu/dolphin melonDS-emu/melonDS DS-Homebrew/TWiLightMenu mgba-emu/mgba LIJI32/SameBoy Rosalie241/RMG
Zelda64Recomp/Zelda64Recomp HarbourMasters/Shipwright snesrev/zelda3 snes9xgit/snes9x SourMesen/Mesen2
kwsch/PKHeX kwsch/pkNX libretro/RetroArch GerbilSoft/rom-properties Davidobot/BetterJoy HiddenRamblings/TagMo
PretendoNetwork/.github devinacker/bsnes-plus pleonex/tinke 2ship2harkinian/2ship2harkinian'''.split())

FORTE = {}
for _l in open(os.path.join(AQUI, 'forte.txt'), encoding='utf-8'):
    if '|' in _l and not _l.startswith('#'):
        _k, _v = _l.split('|', 1); FORTE[_k.strip()] = _v.strip()

REPOS = {}
_rp = os.path.join(AQUI, 'dados', 'repos.json')
if os.path.exists(_rp):
    REPOS = {k.lower(): v for k, v in json.load(open(_rp, encoding='utf-8')).items()}

def meta_html(nome):
    r = REPOS.get(nome.lower())
    if not r: return '', ''
    rel = r.get('rel') or ''
    bx = (f'<a class="baixar" href="{html.escape(rel, quote=True)}" target="_blank" rel="noopener">⬇ Baixar {html.escape(r.get("relt") or "")}</a>'
          if rel else '')
    quando = f'<span class="quando" data-p="{r.get("p", "")}" data-a="{1 if r.get("arq") else 0}"></span>' if r.get('p') else ''
    attrs = f' data-p="{r.get("p", "")}" data-rel="{html.escape(rel, quote=True)}" data-capa="{html.escape(r.get("capa") or "", quote=True)}"'
    return (f'<div class="meta">{quando}{bx}</div>' if (quando or bx) else ''), attrs

# ---------- blocos extras por seção: recomendação + exemplos ----------
def ex(titulo, codigo):
    return f'<div class="ex"><div class="ex-t">{titulo}</div><pre><code>{html.escape(codigo)}</code></pre></div>'

def rec(txt):
    return f'<div class="rec"><b>Recomendação:</b> {txt}</div>'

def passo(itens):
    return '<ol class="passos">' + ''.join(f'<li>{i}</li>' for i in itens) + '</ol>'

EXTRA = {
'0': '<p class="nota">Esses projetos foram removidos por pressão da Nintendo. O que continua no GitHub (Atmosphère, hekate, Dolphin, Cemu, Azahar...) segue firme há anos. Sempre baixe da página oficial do projeto (aba <b>Releases</b>), nunca de sites de terceiros com "versão modificada".</p>',
'1': rec('para começar no Switch o kit mínimo é <b>hekate + Atmosphère</b> (boot e CFW), <b>sphaira</b> (menu e instalador), <b>JKSV</b> (backup de saves) e <b>aio-switch-updater</b> (manter tudo atualizado). Use sempre <b>emuMMC</b> (sistema separado no SD) para não arriscar o sistema original.') +
     ex('Estrutura básica do cartão SD', 'SD:/\n├─ atmosphere/        ← Atmosphère (CFW)\n│  └─ contents/       ← mods e traduções (LayeredFS)\n├─ bootloader/        ← hekate (config em hekate_ipl.ini)\n├─ switch/            ← apps homebrew (.nro)\n├─ config/            ← configurações dos apps\n└─ payload.bin / hbmenu.nro'),
'1.1': passo(['Console em modo RCM (jig no trilho direito + Volume+ + Power) ou modchip.',
              'No PC, abra o <b>TegraRcmGUI</b> (ou <b>Rekado</b> no Android) e envie o <code>hekate_ctcaer_x.x.x.bin</code>.',
              'No hekate: <b>Tools → Backup eMMC</b> (guarde esse backup!), depois <b>emuMMC → Create</b>.',
              'Volte e escolha <b>Launch → Atmosphère (emuMMC)</b>.']),
'1.2': ex('Abrir um NSP e extrair o RomFS (onde ficam textos, fontes e imagens)',
          '# 1) separar o NSP em NCAs\nhactool -t pfs0 --outdir=nsp_ext jogo.nsp\n\n# 2) achar a NCA de programa (a maior) e extrair RomFS/ExeFS\nhactool -k prod.keys --titlekey=<chave_do_ticket> \\\n  --romfsdir=romfs --exefsdir=exefs nsp_ext/xxxx.nca\n\n# o mesmo com nstool (mostra mais informações)\nnstool -v nsp_ext/xxxx.nca') +
         ex('Comprimir e descomprimir', 'nsz -C jogo.nsp        # NSP → NSZ (menor)\nnsz -D jogo.nsz        # NSZ → NSP\nnsz --verify -D jogo.nsz') +
         rec('as chaves (<code>prod.keys</code>/<code>title.keys</code>) se tiram do <b>seu próprio console</b>; ninguém pode distribuí-las. Guarde-as numa pasta fixa (ex.: <code>~/.switch</code>), que é onde hactool, nstool e NSC_BUILDER procuram por padrão.'),
'1.3': ex('Testar tradução/mod sem reempacotar o jogo (LayeredFS)',
          'SD:/atmosphere/contents/0100ABCD12345000/   ← Title ID do jogo\n   ├─ romfs/   ← só os arquivos alterados, mesma estrutura do RomFS original\n   └─ exefs/   ← main, main.npdm (se mexeu no código)') +
         ex('Automatizar com Python (oead)', 'import oead\n\ndados = open("Msg_USen.product.sarc.zs","rb").read()  # .zs = zstd; .szs = yaz0\nsarc = oead.Sarc(oead.yaz0.decompress(open("Layout.szs","rb").read()))\nfor f in sarc.get_files():\n    print(f.name, len(f.data))\n\nbyml = oead.byml.from_binary(open("Dados.byml","rb").read())\nprint(oead.byml.to_text(byml))   # vira YAML legível') +
         rec('<b>Switch-Toolbox</b> para texturas (BNTX), fontes (BFFNT) e layouts (BFLYT); <b>Kuriimu2</b> quando o jogo não é da Nintendo; <b>oead</b> quando são centenas de arquivos e vale a pena um script.'),
'1.4': rec('o combo mais útil: <b>sphaira</b> (menu + instalador + loja), <b>JKSV</b> (saves), <b>Ultrahand</b> + <b>sys-clk</b> (overlay e overclock), <b>ftpd</b> (copiar arquivos pela rede), <b>SysDVR</b> (gravar a tela no PC).') +
           ex('Copiar para o SD pela rede com o ftpd', 'No Switch: abra o ftpd → ele mostra IP:porta (ex. 192.168.0.15:5000)\nNo PC: WinSCP ou FileZilla → protocolo FTP, sem senha → arraste os arquivos'),
'1.6': '<p class="nota">Os "ports nativos" (recompilação estática) exigem que você tenha o jogo e faça o dump do seu cartucho; eles não vêm com o jogo.</p>',
'2': rec('siga o <b>3ds.hacks.guide</b> (repositório Guide_3DS) do começo ao fim: ele instala <b>boot9strap + Luma3DS + GodMode9</b>. Depois use <b>Universal-Updater</b> para baixar o resto. No PC, o emulador atual é o <b>Azahar</b>.') +
     ex('Atalhos úteis no 3DS', 'Segurar SELECT ao ligar  → configurações do Luma3DS\nSegurar START ao ligar   → GodMode9\nL + ↓ + SELECT           → menu Rosalina (cheats, prints, FTP)'),
'3': rec('o caminho atual é <b>Aroma</b> (homebrew + plugins). Para jogar no PC, faça dump dos seus jogos com <b>dumpling</b> e use o <b>Cemu</b> com os <b>graphic packs</b>. Para ter online de novo, instale o <b>Pretendo</b> (plugin Inkay).'),
'4': rec('<b>Dolphin</b> no PC/Android para jogar; no Wii real, <b>Homebrew Channel + Priiloader</b> (instale o Priiloader logo no começo, ele evita brick).') +
     ex('Dolphin: jogo bonito em 3 passos', 'Gráficos → Melhorias → Resolução interna 3x (1080p) ou 6x (4K)\nGráficos → Geral → Proporção: Forçar 16:9 (+ código widescreen do jogo)\nJogo (botão direito) → Propriedades → Códigos Gecko'),
'5': rec('<b>melonDS</b> no PC e Android; no DSi/3DS real, <b>TWiLight Menu++</b>. Para traduzir jogos de DS, <b>Tinke</b> abre a maioria dos formatos (NARC, NCGR, NFTR).'),
'6': rec('<b>mGBA</b> serve para GB, GBC e GBA e tem visualizador de memória, tiles e scripts — ótimo para achar onde fica o texto. Para GB/GBC super precisos, <b>SameBoy</b>.') +
     ex('Achar texto na ROM (mGBA)', 'Ferramentas → Visualizador de memória → procure pelos bytes do texto\nFerramentas → Visualizador de tiles → veja a fonte e a tabela de caracteres\nMonte uma "tabela" (.tbl): 80=A, 81=B ... e use num editor hexa'),
'7': rec('para jogar: <b>RMG</b> ou <b>ares</b>. Se o jogo tem recompilação (<b>Zelda64Recomp</b>, <b>Ship of Harkinian</b>, <b>Starship</b>), prefira ela: roda nativo, com widescreen e 60 fps.') +
     ex('Ship of Harkinian (Ocarina of Time no PC/Switch)', '1. Baixe a release do Shipwright\n2. Coloque a SUA ROM de Ocarina (.z64) na mesma pasta\n3. Abra o programa: ele gera o arquivo oot.o2r a partir da ROM\n4. Pronto — tem até versão para Switch com Atmosphère'),
'8': rec('<b>Snes9x</b> para jogar leve; <b>Mesen2</b> ou <b>bsnes-plus</b> para romhack/tradução (depurador, visualizador de VRAM e de tabela de texto). NES: <b>Mesen2</b> ou <b>FCEUX</b>.'),
'9': '<p class="nota">Decompilação ≠ jogo pirata: o repositório tem só o código reconstruído; para compilar você precisa da sua ROM, de onde são extraídos gráficos e sons.</p>' +
     ex('Compilar a decompilação do Pokémon Emerald', 'git clone https://github.com/pret/pokeemerald\ncd pokeemerald\n# siga o INSTALL.md (precisa do devkitARM ou do agbcc)\nmake            # gera pokeemerald.gba idêntico ao original\n# os textos ficam em data/text/*.inc e src/data/text/ → dá para traduzir direto'),
'10': rec('<b>PKHeX</b> é o essencial (saves de todas as gerações). <b>pkNX</b> para mexer nos dados das ROMs de Switch. Para romhack de GBA, comece pelo <b>pokeemerald-expansion</b> + <b>porymap</b>.') +
      ex('Consultar dados na PokeAPI (navegador ou script)', 'https://pokeapi.co/api/v2/pokemon/pikachu\nhttps://pokeapi.co/api/v2/move/thunderbolt\nhttps://pokeapi.co/api/v2/item/master-ball\n# cada resposta traz "names" em vários idiomas'),
'11': rec('no Android, <b>TagMo</b> grava amiibo em etiquetas NTAG215 baratas. No Switch com Atmosphère nem precisa: a emulação de amiibo é nativa.'),
'12': rec('<b>RetroArch</b> se você quer tudo num lugar só (inclusive no celular); <b>rom-properties</b> no Windows para ver nome, ícone e Title ID das ROMs direto no Explorador.'),
}

# ---------- mini-conversor de markdown ----------
def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r'\*\*ARQ\*\*', '<span class="b arq">ARQ</span>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return s

def card(cols, cab):
    # colunas: [repo, ★, descrição] ou [projeto, o que era, situação]
    if cab[1].strip() == '★':
        repo, est, desc = cols[0], cols[1], cols[2]
        nomes = re.findall(r'https://github\.com/([^)\s]+)', repo)
        r = any(n in REC for n in nomes)
        selo = '<span class="b rec-b">★ recomendado</span>' if r else ''
        est_h = f'<span class="b st">★ {html.escape(est)}</span>' if est.strip() not in ('', '—') else ''
        forte = next((FORTE[n] for n in nomes if n in FORTE), '')
        busca = html.escape((re.sub(r'<[^>]+>', '', repo + ' ' + desc + ' ' + forte)).lower(), quote=True)
        fh = f'<p class="forte"><b>👍 Faz bem:</b> {html.escape(forte)}</p>' if forte else ''
        rp = html.escape(nomes[0], quote=True) if nomes else ''
        mh, at = meta_html(nomes[0]) if nomes else ('', '')
        return (f'<div class="card{" r" if r else ""}" data-s="{busca}" data-repo="{rp}"{at}><div class="ct">{inline(repo)}</div>'
                f'<div class="bs">{est_h}{selo}</div><p class="faz">{inline(desc)}</p>{fh}{mh}</div>')
    busca = html.escape(' '.join(cols).lower(), quote=True)
    return (f'<div class="card morto" data-s="{busca}"><div class="ct">{inline(cols[0])}</div>'
            f'<p><b>O que era:</b> {inline(cols[1])}</p><p><b>Situação:</b> {inline(cols[2])}</p></div>')

_txt = open(MD, encoding='utf-8').read()
for _a, _b in [(' É onde as suas traduções entram.', ' É por ele que traduções e mods entram no jogo.'),
               (' (o que você usa para destrancar e trancar)', ' (abrir e reempacotar jogos)'),
               (' **Muito útil para organizar a sua pasta de traduções.**', ' **Muito útil para organizar pastas de jogos e traduções.**'),
               ('(para gravar/capturar prints de tradução)', '(para gravar e tirar prints)'),
               ('com as chaves de `~/.switch`', 'com as suas chaves')]:
    _txt = _txt.replace(_a, _b)
linhas = _txt.split('\n')
# pula o cabeçalho pessoal (até o primeiro ---)
i0 = linhas.index('---') + 1
linhas = linhas[i0:]

secoes = []   # (id, titulo, html)
atual = None
cab = None
buf = []
lista_aberta = False

def fecha_grade():
    global cab
    if cab is not None:
        atual[2].append('</div><!--c-->'); cab = None

def fecha_lista():
    global lista_aberta
    if lista_aberta:
        atual[2].append('</ol>'); lista_aberta = False

for ln in linhas:
    if ln.startswith('## '):
        if atual: fecha_grade()
        fecha_lista()
        t = ln[3:].strip()
        t = t.replace('O que é mais útil para o seu trabalho de tradução', 'Para quem traduz jogos: o que usar')
        num = t.split('.')[0]
        atual = [num, t, []]
        secoes.append(atual)
        if num in EXTRA: atual[2].append(EXTRA[num])
        cab = None
    elif ln.startswith('### '):
        fecha_grade(); fecha_lista()
        t = ln[4:].strip()
        sub = t.split(' ')[0]
        atual[2].append(f'<h3>{inline(t)}</h3>')
        if sub in EXTRA: atual[2].append(EXTRA[sub])
        cab = None
    elif ln.startswith('|'):
        cols = [c.strip() for c in ln.strip().strip('|').split('|')]
        if all(re.fullmatch(r':?-+:?', c) for c in cols): continue
        if cab is None:
            cab = cols; atual[2].append('<div class="cards">'); continue
        if len(cols) >= 3 and cols[0]:
            atual[2].append(card(cols, cab))
        elif cols and cols[0]:
            atual[2].append(f'<p class="nota">{inline(cols[0])}</p>')
    elif re.match(r'\d+\. ', ln):
        fecha_grade()
        if not lista_aberta:
            atual[2].append('<ol class="passos">'); lista_aberta = True
        atual[2].append('<li>' + inline(re.sub(r'^\d+\. ', '', ln)) + '</li>')
    elif ln.startswith('**') and ln.endswith('**') and atual:
        fecha_grade(); fecha_lista()
        atual[2].append(f'<h3>{inline(ln.strip("*"))}</h3>')
        cab = None
    elif ln.strip() == '' or ln.strip() == '---':
        fecha_grade()
        fecha_lista()
    else:
        if atual: fecha_grade(); fecha_lista(); atual[2].append(f'<p>{inline(ln)}</p>')
# fecha grades abertas
for s in secoes:
    abertas = s[2].count('<div class="cards">') - s[2].count('</div><!--c-->')
    s[2].extend(['</div><!--c-->'] * abertas)

# ---------- seção "Comece aqui" ----------
COMECE = '''
<p>Este guia junta os projetos ligados à Nintendo que existem no GitHub — do Switch ao NES — explicando <b>para que serve cada um</b>, com <b>exemplos</b> e <b>recomendações</b>. Os cards com borda verde são os recomendados.</p>
<div class="dicas">
 <div><b>★ estrelas</b><span>quanto mais, mais usado e confiável.</span></div>
 <div><b><span class="b arq">ARQ</span> arquivado</b><span>ainda funciona, mas não recebe atualização.</span></div>
 <div><b>Releases</b><span>no GitHub, o programa pronto fica na aba <i>Releases</i> (lado direito da página do projeto) — não precisa baixar o código.</span></div>
 <div><b>Busca</b><span>use a lupa lá em cima para filtrar por nome ou assunto (ex.: "save", "tradução", "amiibo").</span></div>
</div>
<h3>Quero... → use isto</h3>
<div class="quero">
 <div><b>Desbloquear o Switch</b><span>hekate + Atmosphère (seção 1.1)</span></div>
 <div><b>Backup de saves</b><span>JKSV (Switch) · Checkpoint/JKSM (3DS)</span></div>
 <div><b>Traduzir/editar jogo de Switch</b><span>hactool/nstool → Switch-Toolbox/Kuriimu2 → LayeredFS</span></div>
 <div><b>Jogar Switch na TV do PC</b><span>SysDVR</span></div>
 <div><b>Controle de PS5/Xbox no Switch</b><span>MissionControl</span></div>
 <div><b>Joy-Con no PC</b><span>BetterJoy</span></div>
 <div><b>Emular 3DS</b><span>Azahar</span></div>
 <div><b>Emular Wii U</b><span>Cemu</span></div>
 <div><b>Emular GameCube/Wii</b><span>Dolphin</span></div>
 <div><b>Emular DS</b><span>melonDS</span></div>
 <div><b>Emular GB/GBA</b><span>mGBA</span></div>
 <div><b>Emular N64</b><span>RMG ou ares (ou os ports nativos)</span></div>
 <div><b>Tudo num app só</b><span>RetroArch · Lemuroid (Android)</span></div>
 <div><b>Editar Pokémon</b><span>PKHeX</span></div>
 <div><b>Zelda/Mario nativo no PC</b><span>Ship of Harkinian, Zelda64Recomp, sm64ex</span></div>
 <div><b>Gravar amiibo</b><span>TagMo</span></div>
</div>
<p class="nota">Use as ferramentas com jogos e consoles que são seus. Nada aqui distribui jogos, chaves ou firmware da Nintendo — isso você extrai do seu próprio aparelho.</p>
'''

def curto(t):
    t = re.sub(r'^\d+\.\s*', '', t)
    return {'O que sumiu do GitHub (para não procurar à toa)': 'Removidos', 'Nintendo Switch': 'Switch',
            'Wii e GameCube': 'Wii/GC', 'DS / DSi': 'DS', 'Game Boy, Game Boy Color e Game Boy Advance': 'Game Boy',
            'Nintendo 64': 'N64', 'SNES e NES/Famicom': 'SNES/NES',
            'Decompilações e ports de PC (jogos da Nintendo transformados em código-fonte)': 'Decomp/ports',
            'Pokémon (a maior comunidade de todas)': 'Pokémon', 'Multi-sistema, celular, navegador, hardware': 'Multi',
            'Para quem traduz jogos: o que usar': 'Tradução'}.get(t, t)

CSS = open(os.path.join(AQUI, 'estilo.css'), encoding='utf-8').read()
TEMPO = open(os.path.join(AQUI, 'tempo.js'), encoding='utf-8').read()
SJS = open(os.path.join(AQUI, 'selecao.js'), encoding='utf-8').read() + open(os.path.join(AQUI, 'glossario.js'), encoding='utf-8').read()
JS = TEMPO + SJS + open(os.path.join(AQUI, 'busca.js'), encoding='utf-8').read()

TJS = open(os.path.join(AQUI, 'tinder.js'), encoding='utf-8').read()
DSC = {'Removidos': 'saíram do GitHub', 'Switch': 'CFW, homebrew, tradução', '3DS': 'Luma, GodMode9, Azahar',
       'Wii U': 'Cemu, Aroma, Pretendo', 'Wii/GC': 'Dolphin, Homebrew Channel', 'DS': 'melonDS, TWiLight',
       'Game Boy': 'mGBA, SameBoy, dev', 'N64': 'emuladores e recomp', 'SNES/NES': 'Snes9x, Mesen, FCEUX',
       'Decomp/ports': 'Zelda, Mario no PC', 'Pokémon': 'PKHeX, pret, PokeAPI', 'amiibo': 'TagMo, bancos',
       'Multi': 'RetroArch e cia.', 'Tradução': 'o que usar'}
def ncards(s): return ''.join(s[2]).count('<div class="card')
TOTAL = sum(ncards(s) for s in secoes)
nav = ('<a href="lista.html#ocultos" class="ocu-nav">🚫 Ocultos</a><a href="glossario.html" class="lc">📖 Glossário</a><a href="#tinder" id="t-abrir" class="lc">🃏 Modo Tinder</a><a href="minha.html" class="lc">⭐ Minha seleção</a><a href="numeros.html" class="lc">📊 Números</a><a href="riscos.html" class="lc">⚖️ Riscos e lei</a><a href="#comece">Comece</a>' +
       ''.join(f'<a href="#s{s[0]}">{html.escape(curto(s[1]))}</a>' for s in secoes) + '<a href="lista.html" class="lc">Lista completa →</a>')
tiles = '<div class="tiles">' + ''.join(
    f'<a class="tile c{i % 7}" href="#s{s[0]}"><span class="num">{ncards(s) or "✓"}</span><span class="lbl">{html.escape(curto(s[1]))}</span><span class="dsc">{DSC.get(curto(s[1]), "")}</span></a>'
    for i, s in enumerate(secoes)) + '</div>'
corpo = tiles + f'<details class="sec" id="comece" open data-g=""><summary><span class="dot" style="--c:var(--accent)"></span><h2>Comece aqui</h2></summary><div class="in">{COMECE}</div></details>'
for i, s in enumerate(secoes):
    abre = ' open' if s[0] == '1' else ''
    n = ncards(s)
    cnt = f'<span class="count">{n}</span>' if n else ''
    corpo += (f'<details class="sec c{i % 7}" id="s{s[0]}"{abre} data-g="{html.escape(curto(s[1]))}"><summary><span class="dot"></span>'
              f'<h2>{inline(s[1])}</h2>{cnt}</summary><div class="in">{"".join(s[2])}</div></details>')

PAG = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#13894f"><meta name="mobile-web-app-capable" content="yes">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<title>{tit}</title><style>{css}</style></head><body>
<div class="wrap">
<header><h1>🎮 {h1}</h1><p class="sub">{sub}</p></header>
<div class="pular"><input id="q" type="search" placeholder="Buscar ({ph})" autocomplete="off" aria-label="Buscar"><div class="pular-trilho">{nav}</div></div>
{corpo}<p id="nada" hidden>Nada encontrado.</p>
</div>
<footer>Levantamento de 26/11/2026 · estrelas do GitHub nessa data · <a href="#" onclick="scrollTo(0,0);return false">↑ topo</a></footer>
<script>{js}</script><script>{tjs}</script></body></html>"""

open(os.path.join(AQUI, 'index.html'), 'w', encoding='utf-8').write(
    PAG.format(tit='Nintendo no GitHub — guia explicado', css=CSS, nav=nav, corpo=corpo, js=JS, tjs=TJS, ph='nome ou assunto',
               h1='Nintendo no GitHub', sub=f'{TOTAL} projetos explicados em português, com exemplos e recomendações · mais de 4,6 mil na lista completa · inclui riscos, pirataria e golpes'))

# ---------- pirataria x golpe x vírus ----------
TIPO_NOME = {'pir': '🏴‍☠️ Pirataria', 'gol': '🎣 Golpe', 'mal': '🦠 Vírus (malware)'}
COMO = {
    'Loja/índice de jogos piratas (Tinfoil e similares)':
        'O Tinfoil (instalador para Switch desbloqueado) aceita "lojas": endereços que listam jogos guardados em Google Drive ou servidores. '
        'Quem cadastra o endereço no console baixa e instala jogos sem pagar. Estes repositórios divulgam ou mantêm esses endereços.',
    'Baixa jogos sem licença':
        'Programas ou páginas que procuram e baixam arquivos de jogos (NSP, XCI, ROM) de sites piratas. Muitos são só páginas de divulgação '
        'criadas em massa para levar cliques e anúncios a esses sites.',
    'Distribui chaves/firmware/títulos protegidos':
        'Publicam chaves de criptografia (prod.keys/title.keys), firmware ou arquivos do console que só deveriam ser extraídos do próprio aparelho. '
        'Com eles, jogos baixados ilegalmente passam a abrir em emuladores ou consoles desbloqueados.',
    'Outro (pirataria)':
        'Divulga ou facilita o acesso a jogos e arquivos protegidos sem autorização de quem tem os direitos.',
    'Golpe: códigos grátis da eShop / gift card':
        'Prometem códigos da eShop ou gift cards de graça. Para "liberar" o código pedem login da conta, dados pessoais, uma "taxa", pesquisas '
        'ou instalar um app. O código nunca chega: o golpista lucra com os dados, o dinheiro ou os cliques.',
    'Malware disfarçado':
        'Se passa por emulador, "crack" ou jogo grátis. O arquivo baixado instala um programa escondido que rouba senhas e sessões '
        '(Google, Discord, banco), minera criptomoeda ou dá acesso remoto ao aparelho. Costuma pedir para desligar o antivírus.',
}
COMO_TIPO = {
    'pir': 'Copia ou distribui jogos, firmware ou chaves sem autorização de quem tem os direitos. Quem usa sabe que não está pagando.',
    'gol': 'Engana a vítima com uma promessa (código grátis, jogo grátis, console barato) para tirar dinheiro, dados ou a conta.',
    'mal': 'Programa disfarçado que faz algo escondido no aparelho: rouba senhas, minera criptomoeda ou sequestra arquivos.',
}
def tipo_de(cat, tr):
    cat = cat or ''; tr = tr or ''
    if cat == 'Malware disfarçado' or tr == 'Malware': return 'mal'
    if cat.startswith('Golpe') or tr in ('Golpe / fraude', 'Roubo de conta / dados', 'Golpe / malware'): return 'gol'
    if cat in COMO or tr in ('Pirataria / direito autoral', 'Distribui material protegido', 'Facilita pirataria'): return 'pir'
    return ''
def como_de(cat, tr):
    t = tipo_de(cat, tr)
    return COMO.get(cat) or COMO_TIPO.get(t, '')

# ---------- página de números (para apresentar) ----------
def numeros(itens, fora):
    import datetime
    from collections import Counter
    hoje = datetime.date(2026, 11, 26)
    vis = [x for x in itens if not x[10]]
    ocu = [x for x in itens if x[10]]
    def dias(x): return (hoje - datetime.date.fromisoformat(x[6])).days if x[6] else 99999
    ativos = [x for x in vis if dias(x) <= 90]
    parados = [x for x in vis if 730 < dias(x) < 99999]
    estrelas = sum(x[1] for x in vis)
    com_dl = sum(1 for x in vis if x[7])
    por_g = Counter(x[3] for x in vis)
    est_g = Counter()
    for x in vis: est_g[x[3]] += x[1]
    cat = Counter(x[12] or 'Sem categoria' for x in ocu)
    def fmt(n): return f'{n:,}'.replace(',', '.')
    def tile(i, num, lbl, dsc, href=''):
        tag = f'a href="{href}"' if href else 'div'
        return f'<{tag} class="tile c{i}"><span class="num">{num}</span><span class="lbl">{lbl}</span><span class="dsc">{dsc}</span></{tag.split()[0]}>'
    def barras(pares, total_lbl):
        mx = max(v for _, v in pares) or 1
        linhas = ''.join(
            f'<div class="br" title="{html.escape(k)}: {fmt(v)} {total_lbl}"><span class="br-n">{html.escape(k)}</span>'
            f'<span class="br-t"><span class="br-b" style="width:{max(1.5, 100 * v / mx):.1f}%"></span></span><span class="br-v">{fmt(v)}</span></div>'
            for k, v in pares)
        return f'<div class="barras">{linhas}</div>'
    def tabela(cab, linhas):
        return ('<div class="tab"><table><thead><tr>' + ''.join(f'<th>{c}</th>' for c in cab) + '</tr></thead><tbody>' +
                ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in l) + '</tr>' for l in linhas) + '</tbody></table></div>')
    def lk(n): return f'<a href="https://github.com/{html.escape(n)}" target="_blank" rel="noopener">{html.escape(n)}</a>'
    top = vis[:15]
    top_at = sorted(ativos, key=lambda x: -x[1])[:10]
    corpo = (
        '<div class="tiles">' +
        tile(1, fmt(len(itens)), 'Repositórios analisados', 'tudo o que as buscas acharam') +
        tile(4, fmt(len(vis)), 'Ligados à Nintendo', 'aparecem no site') +
        tile(0, fmt(len(ocu)), 'Ocultos', 'toque para ver todos, com o motivo', 'lista.html#ocultos') +
        tile(2, fmt(estrelas), 'Estrelas somadas', 'dos projetos visíveis') +
        tile(3, fmt(len(ativos)), 'Ativos', 'atualizados nos últimos 90 dias') +
        tile(1, fmt(com_dl), 'Com download pronto', 'têm versão em Releases') +
        tile(6, fmt(len(parados)), 'Parados', 'sem atualização há 2+ anos') +
        tile(5, '309', 'Explicados no guia', 'com exemplos e recomendações') +
        '</div>' +
        '<section class="panel"><h2>Projetos por console / grupo</h2><p class="sub">Quantos projetos visíveis existem em cada grupo.</p>' +
        barras(por_g.most_common(), 'projetos') + '</section>' +
        '<section class="panel"><h2>Estrelas somadas por grupo</h2><p class="sub">Mede a popularidade: onde a comunidade mais se concentra.</p>' +
        barras(est_g.most_common(), 'estrelas') + '</section>' +
        '<section class="panel"><h2>Top 15 mais populares</h2>' +
        tabela(['#', 'Projeto', '★', 'Grupo', 'O que faz'], [[i, lk(x[0]), fmt(x[1]), html.escape(x[3]), html.escape(x[4])] for i, x in enumerate(top, 1)]) + '</section>' +
        '<section class="panel"><h2>Os 10 mais populares entre os ativos</h2><p class="sub">Atualizados nos últimos 90 dias.</p>' +
        tabela(['#', 'Projeto', '★', 'Atualizado', 'O que faz'], [[i, lk(x[0]), fmt(x[1]), x[6], html.escape(x[4])] for i, x in enumerate(top_at, 1)]) + '</section>' +
        '<section class="panel"><h2>Por que alguns ficaram ocultos</h2>'
        f'<p class="sub">{fmt(len(ocu))} repositórios usam o nome ou o visual da Nintendo, mas não são sobre ela. Todos aparecem na <a href="lista.html#ocultos">lista completa</a> com o motivo.</p>' +
        barras(cat.most_common(), 'ocultos') + '</section>' +
        '<section class="panel"><h2>Removidos do GitHub</h2><p>Não aparecem em nenhuma lista porque não existem mais lá: '
        '<b>yuzu</b> e <b>Citra</b> (mar/2024), <b>Ryujinx</b> (out/2024), <b>Lockpick_RCM</b>, <b>hacPack/4NXCI</b> e <b>LibHac</b>. '
        'O emulador de 3DS atual é o <b>Azahar</b>. <a href="index.html#s0">Detalhes</a>.</p></section>' +
        '<section class="panel"><h2>Baixar os dados</h2><p>Todos os repositórios — inclusive os ocultos, com o motivo — com estrelas, grupo, o que faz, '
        'o que faz bem, última atualização, release, linguagem, tópicos e descrição original.</p>'
        '<div class="m-acoes"><a class="baixar" href="dados/NINTENDO-GITHUB-DADOS.xlsx">⬇ Planilha (.xlsx)</a>'
        '<a class="btn" href="dados/NINTENDO-GITHUB-DADOS.csv">⬇ CSV</a></div>'
        '<p class="sub">Como foi feito: buscas por tópico e por palavra-chave na API do GitHub (26/11/2026), detalhes de cada repositório via GraphQL, '
        'e textos em português escritos por IA a partir da descrição e do README de cada projeto.</p></section>')
    return corpo

# ---------- página riscos e lei ----------
def pagina_riscos(itens):
    from collections import Counter
    def fmt(n): return f'{n:,}'.replace(',', '.')
    pir = [x for x in itens if x[15] and not x[17]]
    susp = [x for x in itens if x[15] and x[17]]
    ocu = [x for x in itens if x[10] and not x[15]]
    vis_r = [x for x in itens if not x[10] and x[14] and x[14] != 'Nenhum']
    lei = [
        ('Violação de direito autoral', 'Código Penal, art. 184 · Lei 9.610/98',
         'Copiar, distribuir ou disponibilizar jogos, músicas, imagens ou firmware sem autorização do dono.',
         'Detenção de 3 meses a 1 ano ou multa. Com intuito de lucro (vender, cobrar assinatura, anúncios): reclusão de 2 a 4 anos e multa.'),
        ('Pirataria de programa de computador', 'Lei do Software, Lei 9.609/98, art. 12',
         'Jogos e sistemas de console também são programas de computador.',
         'Detenção de 6 meses a 2 anos ou multa. Para fins de comércio: reclusão de 1 a 4 anos e multa. '
         'Exceção: o art. 6º permite UMA cópia de salvaguarda de um programa comprado legitimamente.'),
        ('Contornar proteção técnica', 'Lei 9.610/98, art. 107',
         'Desbloquear/remover a proteção de um aparelho ou obra.',
         'No Brasil é responsabilidade civil (indenização por perdas e danos), não crime por si só. Vira problema penal quando é usado para piratear.'),
        ('Golpe dos "códigos grátis" e "jogos grátis"', 'Código Penal, art. 171 (estelionato) e §2º-A (fraude eletrônica)',
         'Sites e programas que prometem códigos da eShop, gift cards ou jogos de graça em troca de login, dados, pagamento ou instalação.',
         'Estelionato: reclusão de 1 a 5 anos e multa. Por meio eletrônico (fraude eletrônica): reclusão de 4 a 8 anos e multa.'),
        ('Programa espião / invasão', 'Código Penal, art. 154-A (Lei 12.737/2012, alterada pela Lei 14.155/2021)',
         '"Geradores" e "cracks" que instalam vírus, roubam senhas ou controlam o aparelho.',
         'Invasão de dispositivo informático: reclusão de 1 a 4 anos e multa — vale também para quem produz e distribui o programa.'),
    ]
    casos = [
        ('Team Xecuter (SX OS)', 'Grupo que vendia o SX OS, firmware focado em rodar jogos piratas no Switch. Um dos líderes foi condenado nos EUA (2022) a 40 meses de prisão, além de indenizações milionárias à Nintendo.'),
        ('yuzu (emulador de Switch)', 'Em 2024 a equipe fechou acordo de US$ 2,4 milhões com a Nintendo e tirou o projeto do ar; o argumento central foi a facilitação de pirataria (jogos rodando antes do lançamento).'),
        ('RomUniverse', 'Site de ROMs condenado nos EUA (2021) a pagar cerca de US$ 2,1 milhões à Nintendo.'),
        ('Banimento online', 'A Nintendo bane do online consoles detectados com pirataria ou modificações — o console perde eShop, atualizações online e multiplayer de forma permanente.'),
    ]
    def unidades(xs):
        """Agrupa repositórios da mesma ferramenta/site (redes de spam) em uma unidade."""
        por = {}
        for x in xs:
            por.setdefault((x[16] or x[0]).strip().lower(), []).append(x)
        us = []
        for k, g in por.items():
            g.sort(key=lambda x: -x[1])
            us.append({'nome': g[0][16] or g[0][0].split('/')[-1], 'xs': g, 'est': sum(x[1] for x in g), 'cat': g[0][12] or 'Outro'})
        return sorted(us, key=lambda u: (-u['est'], -len(u['xs'])))
    def card_u(u, suspeito=False):
        x = u['xs'][0]; n = len(u['xs'])
        rede = f'<span class="b ocu-b">rede de {n} repositórios</span>' if n > 1 else ''
        ids = ''.join(f'<code>{html.escape(y[0])}</code> ' for y in u['xs'])
        lista_ids = (f'<details><summary>Ver os {n} identificadores</summary><p class="ids">{ids}</p></details>' if n > 1
                     else f'<p class="sub">Identificador no GitHub (para denúncia): <code>{html.escape(x[0])}</code></p>')
        return (f'<div class="card ocu-card perigo"><div class="ct"><span class="semlink">{html.escape(u["nome"])}</span></div>'
                f'<div class="bs">' + (f'<span class="b tp-{x[19]}">{TIPO_NOME[x[19]]}</span>' if x[19] else '') +
                ('<span class="b susp-b">❓ Suspeito</span>' if suspeito else '<span class="b ocu-b">🚫 Sem link</span>') +
                f'<span class="b gr">{html.escape(u["cat"])}</span>{rede}'
                + (f'<span class="b st">★ {fmt(u["est"])}</span>' if u['est'] else '') + '</div>'
                f'<p class="faz"><b>O que faz:</b> {html.escape(x[4])}</p>'
                + (f'<p class="como tp-{x[19]}"><b>⚙️ Como funciona:</b> {html.escape(x[20])}</p>' if x[20] else '')
                + (f'<p class="risco"><b>⚠️ Riscos e lei:</b> {html.escape(x[13])}</p>' if x[13] else '')
                + (f'<p class="ocu-m"><b>Por que é só suspeito:</b> {html.escape(x[18])}</p>' if suspeito and x[18] else '')
                + lista_ids + '</div>')
    UP = unidades(pir)
    grupos_pir = ''
    for t in ('pir', 'gol', 'mal'):
        ut = [u for u in UP if u['xs'][0][19] == t]
        if not ut: continue
        grupos_pir += (f'<h3 class="tp-h tp-{t}">{TIPO_NOME[t]} — {len(ut)} ferramenta(s)/site(s)</h3>'
                       f'<p class="como tp-{t}"><b>Como funciona:</b> {html.escape(COMO_TIPO[t])}</p>')
        porcat = Counter(u['cat'] for u in ut)
        for c, n in porcat.most_common():
            us = [u for u in ut if u['cat'] == c]
            grupos_pir += (f'<h3>{html.escape(c)} ({n})</h3>' + (f'<p class="sub">{html.escape(COMO.get(c, ""))}</p>' if COMO.get(c) else '') +
                           '<div class="cards">' + ''.join(card_u(u) for u in us) + '</div>')
    US = unidades(susp)
    grupos_susp = ('<div class="cards">' + ''.join(card_u(u, True) for u in US) + '</div>') if US else ''
    tv = Counter(x[14] for x in vis_r)
    tp = Counter(u['xs'][0][19] for u in UP)
    n_pir, n_gol, n_mal = tp.get('pir', 0), tp.get('gol', 0), tp.get('mal', 0)
    def col(cls, ic, tit, n, linhas):
        return (f'<div class="dif {cls}"><div class="dif-t"><span class="dif-i">{ic}</span><h3>{tit}</h3>'
                + (f'<span class="dif-n">{n} no GitHub</span>' if n is not None else '') + '</div>'
                + ''.join(f'<p><b>{k}:</b> {v}</p>' for k, v in linhas) + '</div>')
    diferencas = (
        '<section class="panel"><h2>🔍 Pirataria, golpe e vírus não são a mesma coisa</h2>'
        '<p class="sub">Muita gente mistura os três. A diferença está em <b>quem é prejudicado</b> e <b>qual lei se aplica</b>.</p><div class="difs">' +
        col('d-pir', '🏴‍☠️', 'Pirataria', n_pir, [
            ('O que é', 'copiar, baixar ou distribuir jogos, firmware, BIOS ou chaves sem autorização de quem tem os direitos.'),
            ('Como funciona', 'alguém extrai os jogos (ou as chaves) de um console ou da eShop e coloca em servidores/Google Drive; lojas do Tinfoil, sites de ROM e "downloaders" indicam onde baixar; o console desbloqueado ou o emulador instala e roda sem pagar.'),
            ('Exemplos', 'lojas do Tinfoil com jogos, sites de ROMs, pacotes de jogos de Switch, chaves prod.keys/title.keys distribuídas.'),
            ('Quem perde', 'a Nintendo e os estúdios (vendas). Quem usa arrisca banimento do console e da conta.'),
            ('Lei', 'direito autoral — CP art. 184, Lei 9.610/98 e Lei do Software 9.609/98.'),
            ('A pessoa sabe?', 'sim: quem usa sabe que está pegando algo sem pagar.')]) +
        col('d-gol', '🎣', 'Golpe', n_gol, [
            ('O que é', 'enganar alguém para tirar dinheiro, dados ou a conta. Não entrega o que promete.'),
            ('Como funciona', 'uma página promete o prêmio; para "liberar" pede login, dados, cartão, uma "taxa", pesquisas ou instalar um app; a vítima entrega e não recebe nada — o golpista vende os dados, usa a conta ou fica com o dinheiro.'),
            ('Exemplos', '"códigos grátis da eShop", "gerador de gift card", "Switch desbloqueado com 100 jogos" que nunca chega, sites que pedem login da conta Nintendo.'),
            ('Quem perde', 'a própria vítima (dinheiro, conta, cartão).'),
            ('Lei', 'estelionato — CP art. 171; por meio eletrônico, fraude eletrônica (§2º-A, 4 a 8 anos).'),
            ('A pessoa sabe?', 'não: ela acha que está recebendo algo de verdade.')]) +
        col('d-mal', '🦠', 'Vírus (malware)', n_mal, [
            ('O que é', 'programa que faz algo escondido no seu aparelho: rouba senhas, minera criptomoeda, sequestra arquivos.'),
            ('Como funciona', 'o arquivo vem com nome atraente (emulador, crack, jogo grátis); ao abrir, instala um programa escondido que copia senhas e sessões salvas no navegador, minera criptomoeda ou abre acesso remoto; muitas vezes pede para desligar o antivírus "porque dá falso positivo".'),
            ('Exemplos', '"crack", "keygen", "emulador de Switch para celular" falso, instalador de jogos que pede para desligar o antivírus.'),
            ('Quem perde', 'quem instala (PC, celular, contas, banco).'),
            ('Lei', 'invasão de dispositivo informático — CP art. 154-A; vale também para quem cria e distribui.'),
            ('A pessoa sabe?', 'não: o vírus vem disfarçado de outra coisa, muitas vezes junto com pirataria.')]) +
        col('d-ok', '🛠️', 'O que NÃO é nenhum dos três', None, [
            ('O que é', 'desbloquear o próprio console, rodar homebrew, fazer backup dos próprios jogos, emuladores, traduções e mods de fãs.'),
            ('Atenção', 'pode levar a banimento do online e, no Brasil, contornar proteção técnica pode gerar indenização (Lei 9.610/98 art. 107) — mas não é crime por si só.'),
            ('Lei', 'a Lei 9.609/98 art. 6º permite uma cópia de salvaguarda de um programa comprado legitimamente.')]) +
        '</div><p class="sub">Na prática eles andam juntos: sites de pirataria são a principal porta de entrada de golpes e vírus.</p></section>')
    vis_alvo = [{'nome': x[0].split('/')[-1], 'xs': [x], 'est': x[1], 'cat': x[14]} for x in vis_r
                if x[14] in ('Distribui material protegido', 'Facilita pirataria')]
    alvos = sorted(UP + vis_alvo, key=lambda u: -u['est'])[:25]
    ranking = ''
    if alvos:
        ranking = ('<section class="panel"><h2>🎯 Maiores alvos — por tamanho</h2>'
                   '<p class="sub">Ordenados por estrelas no GitHub (quanto mais estrelas, mais gente usa, copia e divulga; em redes de spam, '
                   'a soma de todos os repositórios). Junta as ferramentas/lojas ocultas e os projetos visíveis que distribuem material '
                   'protegido ou facilitam pirataria. Só entram os <b>confirmados</b> — os suspeitos ficam numa seção à parte.</p>'
                   '<div class="tab"><table><thead><tr><th>#</th><th>Ferramenta</th><th>★</th><th>Tipo</th><th>O que faz</th><th>Identificador</th></tr></thead><tbody>' +
                   ''.join(f'<tr><td>{i}</td><td><b>{html.escape(u["nome"])}</b>'
                           + (f'<br><small>rede de {len(u["xs"])} repositórios</small>' if len(u['xs']) > 1 else '') +
                           f'</td><td>{fmt(u["est"])}</td><td>' + (f'<span class="b tp-{u["xs"][0][19]}">{TIPO_NOME[u["xs"][0][19]]}</span><br>' if u["xs"][0][19] else '') + f'<small>{html.escape(u["cat"])}</small></td><td>{html.escape(u["xs"][0][4])}</td>'
                           f'<td><code>{html.escape(u["xs"][0][0])}</code>' + (' e outros' if len(u['xs']) > 1 else '') + '</td></tr>'
                           for i, u in enumerate(alvos, 1)) +
                   '</tbody></table></div>')
        redes = sorted([u for u in UP if len(u['xs']) >= 3], key=lambda u: -len(u['xs']))[:10]
        if redes:
            ranking += ('<h3>Maiores redes — por número de repositórios</h3>'
                        '<p class="sub">Têm poucas estrelas, mas são criadas em massa (muitas vezes por contas automáticas) para divulgar o mesmo site. '
                        'Denunciar a rede inteira de uma vez tem mais efeito do que um repositório isolado.</p>'
                        '<div class="tab"><table><thead><tr><th>#</th><th>Site/ferramenta divulgada</th><th>Repositórios</th><th>Tipo</th><th>O que fazem</th></tr></thead><tbody>' +
                        ''.join(f'<tr><td>{i}</td><td><b>{html.escape(u["nome"])}</b></td><td>{len(u["xs"])}</td>'
                                f'<td>{html.escape(u["cat"])}</td><td>{html.escape(u["xs"][0][4])}</td></tr>' for i, u in enumerate(redes, 1)) +
                        '</tbody></table></div>')
        ranking += '</section>'
    corpo = (
        '<section class="panel"><p class="nota"><b>Importante:</b> esta página informa sobre <b>ferramentas e serviços</b>, não acusa pessoas. '
        'Os textos foram escritos com ajuda de IA a partir das descrições públicas de cada projeto e <b>não são parecer jurídico</b> — '
        'confirme cada caso antes de denunciar. Projetos de pirataria e golpe aparecem <b>sem link</b> de propósito.</p></section>'
        '<div class="tiles">'
        f'<div class="tile c0"><span class="num">{fmt(len(UP))}</span><span class="lbl">Pirataria, golpe e vírus</span><span class="dsc">ferramentas/sites confirmados ({fmt(len(pir))} repositórios), sem link</span></div>'
        f'<div class="tile c4"><span class="num">{fmt(len(US))}</span><span class="lbl">Suspeitos</span><span class="dsc">não confirmados — à parte</span></div>'
        f'<div class="tile c6"><span class="num">{fmt(len(vis_r))}</span><span class="lbl">Visíveis com ⚠️</span><span class="dsc">exigem atenção legal ou de uso</span></div>'
        f'<div class="tile c2"><span class="num">{fmt(len(ocu))}</span><span class="lbl">Outros ocultos</span><span class="dsc">só usam o nome/visual</span></div>'
        '</div>'
        + diferencas +
        '<section class="panel"><h2>⚖️ O que diz a lei no Brasil</h2><div class="lei">' +
        ''.join(f'<div><h3>{html.escape(t)}</h3><p class="pena">{html.escape(b)}</p><p>{html.escape(d)}</p><p><b>Pena:</b> {html.escape(pn)}</p></div>' for t, b, d, pn in lei) +
        '</div></section>'
        '<section class="panel"><h2>📰 Casos reais</h2><div class="lei">' +
        ''.join(f'<div><h3>{html.escape(t)}</h3><p>{html.escape(d)}</p></div>' for t, d in casos) + '</div></section>'
        + ranking +
        '<section class="panel"><h2>🏴‍☠️ Ferramentas e lojas de pirataria e golpe encontradas no GitHub</h2>'
        '<p class="sub">Encontradas em buscas como "tinfoil shop", "free eshop codes", "nsp download". Estão ocultas no resto do site.</p>' +
        (grupos_pir or '<p class="nota">A análise ainda não terminou.</p>') + '</section>' +
        ('<section class="panel"><h2>❓ Suspeitos (não confirmados)</h2><p class="sub">Têm cara de pirataria, golpe ou isca de vírus, '
         'mas a descrição pública não basta para confirmar. Verifique antes de citar ou denunciar.</p>' + grupos_susp + '</section>' if grupos_susp else '') +
        '<section class="panel"><h2>⚠️ Projetos visíveis que pedem atenção</h2>'
        '<p>Continuam no site porque têm uso legítimo, mas cada card mostra o aviso. Por tipo:</p>' +
        ''.join(f'<p>• <b>{html.escape(k)}</b>: {v}</p>' for k, v in tv.most_common()) +
        '<p><a href="lista.html">Ver na lista completa</a> (procure por "atenção", "banimento" ou "protegido").</p></section>'
        '<section class="panel"><h2>📣 Como denunciar do jeito certo</h2><ol class="passos">'
        '<li><b>No GitHub:</b> na página do repositório, menu ⋯ → <b>Report repository</b> (golpe, malware, conteúdo abusivo). '
        'O pedido de retirada por direito autoral (<b>DMCA</b>) só pode ser feito pelo <b>dono dos direitos</b> — no caso, a Nintendo.</li>'
        '<li><b>À Nintendo:</b> pelo canal de propriedade intelectual/antipirataria no site oficial da Nintendo, informando o identificador do repositório.</li>'
        '<li><b>Golpes com vítima</b> (perdeu dinheiro, conta ou dados): boletim de ocorrência na delegacia de crimes cibernéticos ou na delegacia online do seu estado.</li>'
        '<li>Guarde prints com data e o endereço completo antes de denunciar — projetos costumam ser apagados e recriados.</li>'
        '</ol></section>')
    return corpo

# ---------- lista completa ----------
GRUPOS = ['Switch', '3DS', 'Wii U', 'Wii/GC', 'DS', 'Game Boy', 'N64', 'SNES', 'NES', 'Virtual Boy', 'Decomp',
          'Pokémon', 'Zelda', 'Mario', 'amiibo', 'Multi', 'Geral']
if REPOS:
    MOT = {}
    _mp = os.path.join(AQUI, '_trabalho', 'ocultos_motivos.json')
    if os.path.exists(_mp):
        MOT = {k.lower(): v for k, v in json.load(open(_mp, encoding='utf-8')).items()}
    RIS = {}
    _rv = os.path.join(AQUI, '_trabalho', 'riscos_visiveis.json')
    if os.path.exists(_rv):
        RIS = {k.lower(): v for k, v in json.load(open(_rv, encoding='utf-8')).items()}
    PIRC = {'Loja/índice de jogos piratas (Tinfoil e similares)', 'Baixa jogos sem licença', 'Distribui chaves/firmware/títulos protegidos',
            'Golpe: códigos grátis da eShop / gift card', 'Malware disfarçado', 'Outro (pirataria)'}
    itens, ja = [], set()
    for _arq, _susp in (('pirataria.json', 0), ('pirataria_suspeitos.json', 1)):
        _pp = os.path.join(AQUI, '_trabalho', _arq)
        if not os.path.exists(_pp): continue
        for x in json.load(open(_pp, encoding='utf-8')):
            if x['n'].lower() in ja: continue
            ja.add(x['n'].lower())
            itens.append([x['n'], x.get('s', 0), 0, 'Pirataria/golpe', x.get('faz', ''), '', x.get('p', ''), '', '', '',
                          1, x.get('m', ''), x.get('cat', ''), x.get('risco', ''), x.get('tipo_risco', ''), 1,
                          x.get('ferramenta') or x['n'].split('/')[-1], _susp, x.get('duvida', '')])
    for r in REPOS.values():
        if r['n'].lower() in ja: continue
        oc = 0 if r.get('k') else 1
        mo = (MOT.get(r['n'].lower()) if oc else RIS.get(r['n'].lower())) or r
        if not oc and (mo.get('tipo_risco') or '') in ('Golpe / malware', 'Malware'):
            # visível com sinal de isca de vírus: oculta por precaução, como suspeito
            mo = dict(mo, cat='Malware disfarçado', tipo_risco='Malware',
                      m='Tem sinais de isca de vírus; ocultado por precaução até ser verificado.')
            oc = 1
        cat = (mo.get('cat') or '') if oc else ''
        perigo = 1 if (oc and cat in PIRC) else 0
        tr = mo.get('tipo_risco') or ''
        itens.append([r['n'], r['s'], 1 if r.get('arq') else 0, r.get('g') or 'Geral', r.get('d') or '', r.get('f') or '',
                      r.get('p') or '', r.get('rel') or '', r.get('relt') or '', r.get('capa') or '',
                      oc, (mo.get('m') or '') if oc else '', cat,
                      (mo.get('risco') or '') if (oc or tr not in ('', 'Nenhum')) else '',
                      tr if (oc or tr not in ('', 'Nenhum')) else '', perigo,
                      r['n'].split('/')[-1] if perigo else '',
                      1 if (perigo and (cat == 'Malware disfarçado' or tr == 'Malware')) else 0,
                      'Marcado só pelo padrão de isca (título de propaganda, link externo, sem código). Não dá para confirmar que contém vírus sem analisar o arquivo.'
                      if (perigo and (cat == 'Malware disfarçado' or tr == 'Malware')) else ''])
    for x in itens:
        t = tipo_de(x[12], x[14])
        x[19:] = [t, como_de(x[12], x[14]) if t else '', (REPOS.get(x[0].lower()) or {}).get('lg', '')]
    itens.sort(key=lambda x: -x[1])
    fora = sum(1 for x in itens if x[10])
    json.dump(itens, open(os.path.join(AQUI, 'lista.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    cont = {g: sum(1 for x in itens if x[3] == g and not x[10]) for g in GRUPOS}
    NVIS = sum(1 for x in itens if not x[10])
    cont['Ocultos'] = fora
    cats = ['Todos', 'Ocultos'] + [g for g in GRUPOS if cont[g]]
    filtros = ''.join(f'<button data-c="{c}" aria-pressed="{"true" if c == "Todos" else "false"}">{c}'
                      f'{"" if c == "Todos" else f" <small>{cont[c]}</small>"}</button>' for c in cats)
    ordem = ('<div class="filtros ordem"><span>Ordenar:</span><button data-o="s" aria-pressed="true">★ Estrelas</button>'
             '<button data-o="p" aria-pressed="false">🕒 Atualizados</button><button data-o="b" aria-pressed="false">⬇ Com download</button>'
             f'<button data-ocu aria-pressed="false">🚫 Mostrar ocultos ({fora})</button></div>')
    _lg = {l: sum(1 for x in itens if x[21] == l and not x[10]) for l in ('zh', 'ja', 'ko')}
    ordem += ('<div class="filtros ordem"><span>Origem:</span><button data-lg="" aria-pressed="true">🌍 Todas</button>'
              f'<button data-lg="zh" aria-pressed="false">🇨🇳 Chinês <small>{_lg["zh"]}</small></button>'
              f'<button data-lg="ja" aria-pressed="false">🇯🇵 Japonês <small>{_lg["ja"]}</small></button>'
              f'<button data-lg="ko" aria-pressed="false">🇰🇷 Coreano <small>{_lg["ko"]}</small></button></div>')
    corpo2 = (f'<section class="panel lista"><p>{NVIS} projetos ligados à Nintendo, explicados em português. '
              f'Outros {fora} ficam ocultos porque só usam o nome ou o visual (temas, bots de Pokémon GO, decompiladores genéricos…) — '
              'toque em <b>🚫 Mostrar ocultos</b> para ver todos, com o motivo de cada um. '
              '<a href="dados/NINTENDO-GITHUB-DADOS.xlsx">⬇ Planilha completa (.xlsx)</a> · <a href="dados/NINTENDO-GITHUB-DADOS.csv">.csv</a>. '
              'Os mais importantes têm explicação maior e exemplos no <a href="index.html">guia</a>.</p>'
              f'<div class="filtros">{filtros}</div>{ordem}<div id="lst" class="cards"></div>'
              '<button id="mais" class="mais">Mostrar mais</button></section>')
    open(os.path.join(AQUI, 'lista.html'), 'w', encoding='utf-8').write(
        PAG.format(tit='Lista completa — Nintendo no GitHub', css=CSS,
                   nav='<a href="index.html" class="lc">← Guia explicado</a><a href="lista.html#ocultos" class="ocu-nav">🚫 Ocultos</a><a href="glossario.html" class="lc">📖 Glossário</a><a href="minha.html" class="lc">⭐ Minha seleção</a><a href="numeros.html" class="lc">📊 Números</a><a href="riscos.html" class="lc">⚖️ Riscos e lei</a><a href="index.html#tinder">🃏 Modo Tinder</a>', corpo=corpo2, tjs='',
                   h1='Lista completa', sub=f'{NVIS} projetos explicados em português (+{fora} ocultos) · o que faz, o que faz bem, quando foi atualizado e onde baixar',
                   js='window.LISTA=' + json.dumps(itens, ensure_ascii=False, separators=(',', ':')).replace('</', '<' + chr(92) + '/') + ';' + chr(10) + TEMPO + SJS +
                      open(os.path.join(AQUI, 'lista.js'), encoding='utf-8').read(), ph=f'{len(itens)} projetos'))
    NUM = numeros(itens, fora)
    RISC = pagina_riscos(itens)
    # markdown da lista completa (PC)
    md = ['# Lista completa — projetos Nintendo no GitHub', '',
          f'Atualizada em 26/11/2026. {len(itens)} projetos, explicados em português. ★ = estrelas. ARQ = arquivado.', '']
    for g in GRUPOS:
        xs = [x for x in itens if x[3] == g]
        if not xs: continue
        md += [f'## {g} ({len(xs)})', '', '| ★ | Projeto | O que faz | O que faz bem | Atualizado |', '|--:|---|---|---|---|']
        for x in xs:
            md.append(f"| {x[1]} | [{x[0]}](https://github.com/{x[0]}){' **ARQ**' if x[2] else ''} | {x[4].replace('|', '/')} | {x[5].replace('|', '/')} | {x[6]} |")
        md.append('')
    open(os.path.join(os.path.dirname(AQUI), 'GITHUB-NINTENDO-LISTA-COMPLETA.md'), 'w', encoding='utf-8').write(chr(10).join(md))
    print('lista:', len(itens), 'fora:', fora)
corpo3 = (
    '<section class="panel"><h2>⭐ Minha seleção (<span id="m-total">0</span>)</h2>'
    '<p>Fica salva <b>neste aparelho</b>. Para levar para outro celular ou PC, use <b>Copiar lista</b> e cole lá no campo abaixo.</p>'
    '<div class="m-acoes"><button class="btn" data-m="copiar">📋 Copiar lista</button><button class="btn" data-m="zap">💬 Mandar no WhatsApp</button>'
    '<button class="btn" data-m="txt">⬇ Baixar .txt</button><button class="btn m-perigo" data-m="limpar">🗑 Limpar</button></div></section>'
    '<section class="panel"><h2>➕ Adicionar repositórios</h2>'
    '<p>Cole <b>nomes</b> (ex.: <code>CTCaer/hekate</code>), <b>links do GitHub</b> ou até uma <b>conversa do WhatsApp</b> inteira — eu acho os nomes sozinho. '
    'Também entende <code>WerWolv/Tesla-Menu + nx-ovlloader</code>. Projetos que não estão no site são conferidos direto no GitHub.</p>'
    '<textarea id="m-txt" rows="6" placeholder="CTCaer/hekate&#10;https://github.com/nicoboss/nsz&#10;[11:13] Huntereb/Awoo-Installer"></textarea>'
    '<button id="m-add" class="mais">Adicionar à seleção</button><p id="m-msg" class="nota" hidden></p></section>'
    '<section class="panel"><div id="m-lista" class="cards"></div></section>')
if REPOS:
    open(os.path.join(AQUI, 'numeros.html'), 'w', encoding='utf-8').write(
        PAG.format(tit='Números — Nintendo no GitHub', css=CSS,
                   nav='<a href="index.html" class="lc">← Guia explicado</a><a href="lista.html#ocultos" class="ocu-nav">🚫 Ocultos</a><a href="glossario.html" class="lc">📖 Glossário</a><a href="lista.html" class="lc">Lista completa</a><a href="riscos.html" class="lc">⚖️ Riscos e lei</a><a href="minha.html">⭐ Minha seleção</a>',
                   corpo=NUM, tjs='', h1='Nintendo no GitHub em números', sub='Levantamento de 26/11/2026 · tudo o que foi encontrado, inclusive o que ficou oculto',
                   js=TEMPO + SJS + open(os.path.join(AQUI, 'busca.js'), encoding='utf-8').read(), ph='na página'))
if REPOS:
    open(os.path.join(AQUI, 'riscos.html'), 'w', encoding='utf-8').write(
        PAG.format(tit='Riscos e lei — Nintendo no GitHub', css=CSS,
                   nav='<a href="index.html" class="lc">← Guia explicado</a><a href="lista.html#ocultos" class="ocu-nav">🚫 Ocultos</a><a href="glossario.html" class="lc">📖 Glossário</a><a href="numeros.html" class="lc">📊 Números</a>',
                   corpo=RISC, tjs='', h1='⚖️ Pirataria, golpes e a lei', sub='O que é crime, o que é risco, e as ferramentas que ficaram de fora do site',
                   js=TEMPO + SJS + open(os.path.join(AQUI, 'busca.js'), encoding='utf-8').read(), ph='na página'))
open(os.path.join(AQUI, 'glossario.html'), 'w', encoding='utf-8').write(
    PAG.format(tit='Glossário — Nintendo no GitHub', css=CSS,
               nav='<a href="lista.html#ocultos" class="ocu-nav">🚫 Ocultos</a><a href="index.html" class="lc">← Guia explicado</a><a href="riscos.html" class="lc">⚖️ Riscos e lei</a><a href="numeros.html" class="lc">📊 Números</a>',
               corpo='<section class="panel"><p>As palavras técnicas que aparecem no site, explicadas para quem nunca mexeu com videogame. '
                     'Em qualquer página, as palavras com <span class="termo">sublinhado pontilhado</span> abrem essa explicação ao tocar.</p></section>'
                     '<section class="panel"><div id="gl-todos" class="gl-lista"></div></section>',
               tjs='', h1='📖 Glossário', sub='O que quer dizer cada termo — em português simples',
               js=TEMPO + SJS + open(os.path.join(AQUI, 'busca.js'), encoding='utf-8').read(), ph='um termo'))
open(os.path.join(AQUI, 'minha.html'), 'w', encoding='utf-8').write(
    PAG.format(tit='Minha seleção — Nintendo no GitHub', css=CSS,
               nav='<a href="index.html" class="lc">← Guia explicado</a><a href="lista.html#ocultos" class="ocu-nav">🚫 Ocultos</a><a href="glossario.html" class="lc">📖 Glossário</a><a href="lista.html" class="lc">Lista completa</a><a href="index.html#tinder">🃏 Modo Tinder</a>',
               corpo=corpo3, tjs='', h1='Minha seleção', sub='Os projetos que você marcou com ☆, guardou no Tinder ou adicionou aqui',
               js=TEMPO + SJS + open(os.path.join(AQUI, 'minha.js'), encoding='utf-8').read(), ph='na sua seleção'))
print('secoes:', len(secoes))
