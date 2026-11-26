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
        return (f'<div class="card{" r" if r else ""}" data-s="{busca}" data-repo="{rp}"><div class="ct">{inline(repo)}</div>'
                f'<div class="bs">{est_h}{selo}</div><p class="faz">{inline(desc)}</p>{fh}</div>')
    busca = html.escape(' '.join(cols).lower(), quote=True)
    return (f'<div class="card morto" data-s="{busca}"><div class="ct">{inline(cols[0])}</div>'
            f'<p><b>O que era:</b> {inline(cols[1])}</p><p><b>Situação:</b> {inline(cols[2])}</p></div>')

linhas = open(MD, encoding='utf-8').read().split('\n')
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
JS = open(os.path.join(AQUI, 'busca.js'), encoding='utf-8').read()

TJS = open(os.path.join(AQUI, 'tinder.js'), encoding='utf-8').read()
DSC = {'Removidos': 'saíram do GitHub', 'Switch': 'CFW, homebrew, tradução', '3DS': 'Luma, GodMode9, Azahar',
       'Wii U': 'Cemu, Aroma, Pretendo', 'Wii/GC': 'Dolphin, Homebrew Channel', 'DS': 'melonDS, TWiLight',
       'Game Boy': 'mGBA, SameBoy, dev', 'N64': 'emuladores e recomp', 'SNES/NES': 'Snes9x, Mesen, FCEUX',
       'Decomp/ports': 'Zelda, Mario no PC', 'Pokémon': 'PKHeX, pret, PokeAPI', 'amiibo': 'TagMo, bancos',
       'Multi': 'RetroArch e cia.', 'Tradução': 'o que usar'}
def ncards(s): return ''.join(s[2]).count('<div class="card')
TOTAL = sum(ncards(s) for s in secoes)
nav = ('<a href="#tinder" id="t-abrir" class="lc">🃏 Modo Tinder</a><a href="#comece">Comece</a>' +
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
               h1='Nintendo no GitHub', sub=f'{TOTAL} projetos explicados em português, com exemplos e recomendações · mais de 2 mil na lista completa'))

# ---------- lista completa ----------
if GH:
    import importlib.util
    seen = {}
    for f in sorted(glob.glob(os.path.join(GH, '*.json'))):
        t = os.path.basename(f)[:-5]
        try: data = json.load(open(f, encoding='utf-8'))
        except Exception: continue
        for r in data:
            seen.setdefault(r['fullName'], dict(r, topics=[]))['topics'].append(t)
    kw = re.compile(r'nintendo|switch|wii|gamecube|gcn|n64|nes\b|snes|famicom|game ?boy|gba|gbc|nds|\bds\b|3ds|mario|zelda|pok[eé]mon|metroid|kirby|pikmin|smash|splatoon|xenoblade|fire emblem|donkey kong|star ?fox|f-zero|amiibo|joy-?con|banjo|goldeneye|paper mario|animal crossing', re.I)
    grupos = [('Switch', ['nintendo-switch', 'switch-homebrew', 'homebrew-switch', 'atmosphere', 'joycon']),
              ('3DS', ['nintendo-3ds', '3ds', '3ds-homebrew']), ('Wii U', ['wiiu', 'wii-u']), ('Wii/GC', ['wii', 'gamecube']),
              ('DS', ['nintendo-ds', 'nds']), ('Game Boy', ['gba', 'gameboy-advance', 'gameboy', 'gameboy-color']),
              ('N64', ['n64', 'nintendo-64']), ('SNES', ['snes']), ('NES', ['nes', 'famicom']), ('Virtual Boy', ['virtual-boy']),
              ('Decomp', ['decompilation']), ('Pokémon', ['pokemon']), ('Zelda', ['zelda']), ('Mario', ['mario']),
              ('amiibo', ['amiibo']), ('Geral', ['nintendo'])]
    usado = set(); itens = []
    for nome, tops in grupos:
        rows = [r for k, r in seen.items() if k not in usado and any(t in r['topics'] for t in tops)]
        if nome == 'Decomp' or 'atmosphere' in tops:
            rows = [r for r in rows if kw.search((r['description'] or '') + ' ' + r['fullName']) or set(r['topics']) - {'decompilation', 'atmosphere'}]
        for r in rows:
            usado.add(r['fullName'])
            itens.append([r['fullName'], r['stargazersCount'], 1 if r['isArchived'] else 0, nome, (r['description'] or '')[:200]])
    itens.sort(key=lambda x: -x[1])
    json.dump(itens, open(os.path.join(AQUI, 'lista.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    cats = ['Todos'] + [g[0] for g in grupos]
    filtros = ''.join(f'<button data-c="{c}" aria-pressed="{"true" if c == "Todos" else "false"}">{c}</button>' for c in cats)
    corpo2 = (f'<section class="panel lista"><p>{len(itens)} repositórios encontrados pelos tópicos do GitHub, do mais estrelado ao menos. '
              'As descrições são as originais dos autores (quase todas em inglês). As explicações em português ficam no <a href="index.html">guia</a>.</p>'
              f'<div class="filtros">{filtros}</div><div id="lst" class="cards"></div>'
              '<button id="mais" class="mais">Mostrar mais</button></section>')
    open(os.path.join(AQUI, 'lista.html'), 'w', encoding='utf-8').write(
        PAG.format(tit='Lista completa — Nintendo no GitHub', css=CSS,
                   nav='<a href="index.html" class="lc">← Guia explicado</a><a href="index.html#tinder">🃏 Modo Tinder</a>', corpo=corpo2, tjs='', h1='Lista completa', sub=f'{len(itens)} repositórios ligados à Nintendo, do mais estrelado ao menos',
                   js=open(os.path.join(AQUI, 'lista.js'), encoding='utf-8').read(), ph=f'{len(itens)} repositórios'))
    print('lista:', len(itens))
print('secoes:', len(secoes))
