/* lista.js — lista completa. Item: [nome, estrelas, arquivado, grupo, o que faz, faz bem, atualizado, release, tag, capa] */
(function(){
  var lst=document.getElementById('lst'),mais=document.getElementById('mais'),q=document.getElementById('q'),nada=document.getElementById('nada');
  var dados=[],filtrado=[],mostrados=0,cat='Todos',ordem='s',PASSO=40,verOcu=false;
  function norm(t){return (t||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'')}
  function esc(t){return (t||'').replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function card(r){
    if(r[10])return cardOcu(r);
    var qd=window.quandoTxt(r[6],r[2]);
    return '<div class="card"><div class="ct"><a href="https://github.com/'+esc(r[0])+'" target="_blank" rel="noopener">'+esc(r[0])+'</a></div>'+
      '<div class="bs"><span class="b st">★ '+r[1]+'</span><span class="b gr">'+esc(r[3])+'</span>'+(r[2]?'<span class="b arq">ARQ</span>':'')+'<button class="sel" type="button" data-sel="'+esc(r[0])+'"></button></div>'+
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
    return '<div class="card oculto'+(r[15]?' perigo':'')+'"><div class="ct">'+nome+'</div>'+
      '<div class="bs">'+selo(r)+(r[17]?'<span class="b susp-b">❓ Suspeito</span>':'<span class="b ocu-b">🚫 Oculto</span>')+(r[12]?'<span class="b gr">'+esc(r[12])+'</span>':'')+(r[1]?'<span class="b st">★ '+r[1]+'</span>':'')+'</div>'+
      (r[4]?'<p class="faz"><b>O que faz:</b> '+esc(r[4])+'</p>':'')+
      (r[11]?'<p class="ocu-m"><b>Por que está oculto:</b> '+esc(r[11])+'</p>':'')+como(r)+
      (r[13]?'<p class="risco"><b>⚠️ Riscos'+(r[14]?' ('+esc(r[14])+')':'')+':</b> '+esc(r[13])+'</p>':'')+
      (r[15]?'<p class="nota">Sem link de propósito: é pirataria ou golpe. Veja <a href="riscos.html">⚖️ Riscos e lei</a>.</p>':'')+'</div>';
  }
  function desenha(reset){
    if(reset){lst.innerHTML='';mostrados=0}
    var h='';for(var i=mostrados;i<Math.min(mostrados+PASSO,filtrado.length);i++)h+=card(filtrado[i]);
    lst.insertAdjacentHTML('beforeend',h);if(window.SEL)SEL.pintar(lst);mostrados=Math.min(mostrados+PASSO,filtrado.length);
    mais.hidden=mostrados>=filtrado.length;
    mais.textContent='Mostrar mais ('+(filtrado.length-mostrados)+' restantes)';
    nada.hidden=filtrado.length>0;
  }
  function filtra(){
    var termos=norm(q.value.trim()).split(/\s+/).filter(Boolean);
    filtrado=dados.filter(function(r){
      if(r[10]&&!verOcu&&cat!=='Ocultos')return false;
      if(cat==='Ocultos'){if(!r[10])return false}else if(cat!=='Todos'&&r[3]!==cat)return false;
      if(ordem==='b'&&!r[7])return false;
      var s=r._s||(r._s=norm(r[0]+' '+r[3]+' '+r[4]+' '+r[5]+' '+(r[11]||'')+' '+(r[12]||'')+' '+(r[13]||'')+' '+(r[14]||'')));
      return termos.every(function(x){return s.indexOf(x)>=0});
    });
    if(ordem==='p')filtrado.sort(function(a,b){return (b[6]||'').localeCompare(a[6]||'')});
    desenha(true);
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
  var bo=document.querySelector('[data-ocu]');
  function ocu(on){verOcu=on;if(bo)bo.setAttribute('aria-pressed',on);filtra();}
  if(bo)bo.addEventListener('click',function(){ocu(!verOcu)});
  if(/ocultos/.test(location.hash))setTimeout(function(){ocu(true)},0);
  var t;q.addEventListener('input',function(){clearTimeout(t);t=setTimeout(filtra,150)});
  mais.addEventListener('click',function(){desenha(false)});
  if(window.LISTA){dados=window.LISTA;filtra();return}
  fetch('lista.json').then(function(r){return r.json()}).then(function(d){dados=d;filtra()})
    .catch(function(){lst.innerHTML='<p class="nota">Não consegui carregar a lista.</p>'});
})();
