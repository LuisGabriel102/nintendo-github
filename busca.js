/* busca.js — busca das páginas de guia/números/riscos/glossário, com a busca inteligente (inteli.js). */
(function(){
  var q=document.getElementById('q'),nada=document.getElementById('nada');
  if(!q)return;
  var secs=[].slice.call(document.querySelectorAll('details.sec'));
  var estado=secs.map(function(s){return s.open});
  var N=window.INTELI?INTELI.norm:function(t){return String(t||'').toLowerCase()};
  var cards=[].slice.call(document.querySelectorAll('.card')).map(function(c){
    return [c,[{t:N(c.getAttribute('data-s')||c.textContent),p:1},{t:N((c.querySelector('.ct')||{}).textContent||''),p:2}]];
  });
  // caixa de assunto + link para a lista completa, logo abaixo da barra de busca
  var box=document.createElement('div');box.id='busca-topo';box.hidden=true;
  var pular=document.querySelector('.pular');(pular&&pular.parentNode?pular.parentNode:document.body).insertBefore(box,pular?pular.nextSibling:null);
  var t;
  q.addEventListener('input',function(){clearTimeout(t);t=setTimeout(filtra,150)});
  q.addEventListener('keydown',function(e){if(e.key==='Enter'&&q.value.trim()){location.href='lista.html?q='+encodeURIComponent(q.value.trim());}});
  function filtra(){
    var v=q.value.trim(),achou=0;
    if(!v){
      cards.forEach(function(c){c[0].classList.remove('oculto')});
      secs.forEach(function(s,i){s.classList.remove('oculto');s.open=estado[i]});
      if(nada)nada.hidden=true;box.hidden=true;return;
    }
    var an=window.INTELI?INTELI.analisar(v):{q:v.toLowerCase(),toks:v.toLowerCase().split(/\s+/),extras:[],temas:[]};
    cards.forEach(function(c){
      var sc=window.INTELI?INTELI.pontuar(c[1],an):(c[1][0].t.indexOf(an.q)>=0?1:0);
      var ok=sc>=(an.temas.length?2:1);
      c[0].classList.toggle('oculto',!ok);if(ok)achou++;
    });
    secs.forEach(function(s){
      var n=s.querySelectorAll('.card:not(.oculto)').length;
      s.classList.toggle('oculto',n===0);
      if(n)s.open=true;
    });
    box.innerHTML=(window.INTELI?INTELI.cartao(an):'')+
      '<p class="busca-link">🔎 '+achou+' nesta página · <a href="lista.html?q='+encodeURIComponent(v)+'"><b>Ver todos os resultados na lista completa (inclusive ocultos de pirataria) →</b></a></p>';
    box.hidden=false;
    if(window.GLOS)GLOS.marcar(box);
    if(nada)nada.hidden=true;
  }
  document.querySelectorAll('nav a[href^="#"],.pular-trilho a[href^="#"]').forEach(function(a){
    a.addEventListener('click',function(){var d=document.querySelector(a.getAttribute('href'));if(d&&d.tagName==='DETAILS')d.open=true});
  });
  if(location.hash&&location.hash.length>1){try{var d=document.querySelector(location.hash);if(d&&d.tagName==='DETAILS')d.open=true}catch(e){}}
})();
