/* lista.js — lista completa. Item: [nome, estrelas, arquivado, grupo, o que faz, faz bem, atualizado, release, tag, capa] */
(function(){
  var lst=document.getElementById('lst'),mais=document.getElementById('mais'),q=document.getElementById('q'),nada=document.getElementById('nada');
  var dados=[],filtrado=[],mostrados=0,cat='Todos',ordem='s',PASSO=40,verOcu=false,lg='';
  var LGN={zh:'🇨🇳 Chinês',ja:'🇯🇵 Japonês',ko:'🇰🇷 Coreano'};
  function origem(r){return r[21]?'<span class="b lg-b">'+LGN[r[21]]+'</span>':''}
  function norm(t){return (t||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'')}
  function esc(t){return (t||'').replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function card(r){
    if(r[10])return cardOcu(r);
    var qd=window.quandoTxt(r[6],r[2]);
    return '<div class="card"><div class="ct"><a href="https://github.com/'+esc(r[0])+'" target="_blank" rel="noopener">'+esc(r[0])+'</a></div>'+
      '<div class="bs"><span class="b st">★ '+r[1]+'</span><span class="b gr">'+esc(r[3])+'</span>'+origem(r)+(r[2]?'<span class="b arq">ARQ</span>':'')+'<button class="sel" type="button" data-sel="'+esc(r[0])+'"></button></div>'+
      (r[4]?'<p class="faz">'+esc(r[4])+'</p>':'')+
      (r[5]?'<p class="forte"><b>👍 Faz bem:</b> '+esc(r[5])+'</p>':'')+
      (r[19]?'<div class="bs">'+selo(r)+'</div>'+como(r):'')+
      (r[13]?'<p class="risco"><b>⚠️ Atenção ('+esc(r[14])+'):</b> '+esc(r[13])+'</p>':'')+
      '<div class="meta">'+(qd?'<span class="quando '+qd.c+'">'+qd.t+'</span>':'')+
      (r[7]?'<a class="baixar" href="'+esc(r[7])+'" target="_blank" rel="noopener">⬇ Baixar '+esc(r[8])+'</a>':'')+'</div></div>';
  }
  var TN={pir:'🏴‍☠️ Pirataria',gol:'🎣 Golpe',mal:'🦠 Vírus (malware)'};
  function selo(r){return r[19]?'<span class="b tp-'+r[19]+'">'+TN[r[19]]+'</span>':''}
  function como(r){return r[20]?'<p class="como tp-'+r[19]+'"><b>⚙️ Como funciona:</b> '+esc(r[20])+'</p>':''}
  function cardOcu(r){
    var nome=r[15]?'<span class="semlink" title="Sem link de propósito">'+esc(r[0])+'</span>':'<a href="https://github.com/'+esc(r[0])+'" target="_blank" rel="noopener">'+esc(r[0])+'</a>';
    return '<div class="card ocu-card'+(r[15]?' perigo':'')+'"><div class="ct">'+nome+'</div>'+
      '<div class="bs">'+selo(r)+(r[17]?'<span class="b susp-b">❓ Suspeito</span>':'<span class="b ocu-b">🚫 Oculto</span>')+(r[12]?'<span class="b gr">'+esc(r[12])+'</span>':'')+(r[1]?'<span class="b st">★ '+r[1]+'</span>':'')+'</div>'+
      (r[4]?'<p class="faz"><b>O que faz:</b> '+esc(r[4])+'</p>':'')+
      (r[11]?'<p class="ocu-m"><b>Por que está oculto:</b> '+esc(r[11])+'</p>':'')+como(r)+
      (r[13]?'<p class="risco"><b>⚠️ Riscos'+(r[14]?' ('+esc(r[14])+')':'')+':</b> '+esc(r[13])+'</p>':'')+
      (r[15]?'<p class="nota">Sem link de propósito: é pirataria ou golpe. Veja <a href="riscos.html">⚖️ Riscos e lei</a>.</p>':'')+'</div>';
  }
  function desenha(reset){
    if(reset){lst.innerHTML='';mostrados=0}
    var h='';for(var i=mostrados;i<Math.min(mostrados+PASSO,filtrado.length);i++)h+=card(filtrado[i]);
    lst.insertAdjacentHTML('beforeend',h);if(window.SEL)SEL.pintar(lst);if(window.GLOS)GLOS.marcar(lst);mostrados=Math.min(mostrados+PASSO,filtrado.length);
    mais.hidden=mostrados>=filtrado.length;
    mais.textContent='Mostrar mais ('+(filtrado.length-mostrados)+' restantes)';
    nada.hidden=filtrado.length>0;
  }
  // caixa do assunto + contagem, acima da lista
  var temaBox=document.createElement('div');temaBox.id='tema';temaBox.hidden=true;
  var conta=document.createElement('p');conta.id='contagem';conta.hidden=true;
  lst.parentNode.insertBefore(temaBox,lst);lst.parentNode.insertBefore(conta,lst);
  function campos(r){
    var N=window.INTELI?INTELI.norm:norm;
    return r._c||(r._c=[{t:N(r[0]),p:3},{t:N(r[4]),p:2},{t:N(r[5]+' '+(r[20]||'')),p:1},
      {t:N((r[11]||'')+' '+(r[12]||'')+' '+(r[13]||'')+' '+(r[14]||'')+' '+(r[16]||'')+' '+r[3]),p:1.5}]);
  }
  function filtra(){
    var an=window.INTELI?INTELI.analisar(q.value):{q:norm(q.value.trim()),toks:norm(q.value.trim()).split(/\s+/).filter(Boolean),extras:[],temas:[],pir:0};
    var busca=!!an.q;
    temaBox.innerHTML=window.INTELI?INTELI.cartao(an):'';temaBox.hidden=!temaBox.innerHTML;
    filtrado=[];
    dados.forEach(function(r){
      // ocultos: aparecem com o botão, no filtro "Ocultos" ou quando a busca é sobre pirataria/golpe/vírus/catálogo/instalação
      if(r[10]&&!verOcu&&cat!=='Ocultos'&&!(busca&&an.pir&&r[15]))return;
      if(cat==='Ocultos'){if(!r[10])return}else if(cat!=='Todos'&&r[3]!==cat&&!(busca&&r[10]))return;
      if(ordem==='b'&&!r[7])return;
      if(lg&&r[21]!==lg)return;
      if(busca){
        var sc=window.INTELI?INTELI.pontuar(campos(r),an):1;
        if(sc<(an.temas.length?2:1))return;
        r._sc=sc+(r[15]&&an.pir?3:0)+Math.log(1+r[1])/10;
      }
      filtrado.push(r);
    });
    if(busca)filtrado.sort(function(a,b){return b._sc-a._sc});
    else if(ordem==='p')filtrado.sort(function(a,b){return (b[6]||'').localeCompare(a[6]||'')});
    conta.hidden=!busca;
    if(busca){
      var np=filtrado.filter(function(r){return r[15]}).length;
      conta.innerHTML='🔎 <b>'+filtrado.length+'</b> resultado(s) para “'+esc(q.value.trim())+'”'+
        (an.temas.length?' — assunto: '+an.temas.map(function(t){return t.tit}).join(' + '):'')+
        (np?' · <b>'+np+'</b> de pirataria/golpe/vírus (sem link)':'')+' · ordenado por relevância';
    }
    desenha(true);
    if(window.GLOS)GLOS.marcar(temaBox);
  }
  function grupoBotoes(sel,attr,cb){
    document.querySelectorAll(sel).forEach(function(b){
      b.addEventListener('click',function(){
        document.querySelectorAll(sel).forEach(function(x){x.setAttribute('aria-pressed','false')});
        b.setAttribute('aria-pressed','true');cb(b.getAttribute(attr));filtra();
      });
    });
  }
  grupoBotoes('.filtros button[data-c]','data-c',function(v){cat=v});
  grupoBotoes('.filtros button[data-o]','data-o',function(v){ordem=v});
  grupoBotoes('.filtros button[data-lg]','data-lg',function(v){lg=v});
  var bo=document.querySelector('[data-ocu]');
  function ocu(on){verOcu=on;if(bo)bo.setAttribute('aria-pressed',on);filtra();}
  if(bo)bo.addEventListener('click',function(){ocu(!verOcu)});
  function soOcultos(){
    cat='Ocultos';
    document.querySelectorAll('.filtros button[data-c]').forEach(function(x){x.setAttribute('aria-pressed',x.getAttribute('data-c')==='Ocultos')});
    ocu(true);
  }
  var faixa=document.createElement('div');faixa.id='faixa-ocu';faixa.hidden=true;
  faixa.innerHTML='<b>🚫 Você está vendo os ocultos</b> — cada um diz o que faz, por que ficou de fora e os riscos. '+
    '<a href="riscos.html">⚖️ Pirataria, golpe e vírus</a> · <button type="button" id="faixa-volta">Voltar para os visíveis</button>';
  lst.parentNode.insertBefore(faixa,lst);
  document.getElementById('faixa-volta').addEventListener('click',function(){
    cat='Todos';document.querySelectorAll('.filtros button[data-c]').forEach(function(x){x.setAttribute('aria-pressed',x.getAttribute('data-c')==='Todos')});
    if(location.hash)history.replaceState(null,'',location.pathname);ocu(false);
  });
  var filtraAnt=filtra;filtra=function(){faixa.hidden=!(cat==='Ocultos');filtraAnt();};
  if(/ocultos/.test(location.hash))setTimeout(soOcultos,0);
  window.addEventListener('hashchange',function(){if(/ocultos/.test(location.hash))soOcultos();});
  var t;q.addEventListener('input',function(){clearTimeout(t);t=setTimeout(filtra,150)});
  mais.addEventListener('click',function(){desenha(false)});
  try{var qp=new URLSearchParams(location.search).get('q');if(qp)q.value=qp;}catch(e){}
  if(window.LISTA){dados=window.LISTA;filtra();return}
  fetch('lista.json').then(function(r){return r.json()}).then(function(d){dados=d;filtra()})
    .catch(function(){lst.innerHTML='<p class="nota">Não consegui carregar a lista.</p>'});
})();
