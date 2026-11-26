/* lista.js — lista completa. Item: [nome, estrelas, arquivado, grupo, o que faz, faz bem, atualizado, release, tag, capa] */
(function(){
  var lst=document.getElementById('lst'),mais=document.getElementById('mais'),q=document.getElementById('q'),nada=document.getElementById('nada');
  var dados=[],filtrado=[],mostrados=0,cat='Todos',ordem='s',PASSO=40;
  function norm(t){return (t||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'')}
  function esc(t){return (t||'').replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function card(r){
    var qd=window.quandoTxt(r[6],r[2]);
    return '<div class="card"><div class="ct"><a href="https://github.com/'+esc(r[0])+'" target="_blank" rel="noopener">'+esc(r[0])+'</a></div>'+
      '<div class="bs"><span class="b st">★ '+r[1]+'</span><span class="b gr">'+esc(r[3])+'</span>'+(r[2]?'<span class="b arq">ARQ</span>':'')+'</div>'+
      (r[4]?'<p class="faz">'+esc(r[4])+'</p>':'')+
      (r[5]?'<p class="forte"><b>👍 Faz bem:</b> '+esc(r[5])+'</p>':'')+
      '<div class="meta">'+(qd?'<span class="quando '+qd.c+'">'+qd.t+'</span>':'')+
      (r[7]?'<a class="baixar" href="'+esc(r[7])+'" target="_blank" rel="noopener">⬇ Baixar '+esc(r[8])+'</a>':'')+'</div></div>';
  }
  function desenha(reset){
    if(reset){lst.innerHTML='';mostrados=0}
    var h='';for(var i=mostrados;i<Math.min(mostrados+PASSO,filtrado.length);i++)h+=card(filtrado[i]);
    lst.insertAdjacentHTML('beforeend',h);mostrados=Math.min(mostrados+PASSO,filtrado.length);
    mais.hidden=mostrados>=filtrado.length;
    mais.textContent='Mostrar mais ('+(filtrado.length-mostrados)+' restantes)';
    nada.hidden=filtrado.length>0;
  }
  function filtra(){
    var termos=norm(q.value.trim()).split(/\s+/).filter(Boolean);
    filtrado=dados.filter(function(r){
      if(cat!=='Todos'&&r[3]!==cat)return false;
      if(ordem==='b'&&!r[7])return false;
      var s=r._s||(r._s=norm(r[0]+' '+r[3]+' '+r[4]+' '+r[5]));
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
  var t;q.addEventListener('input',function(){clearTimeout(t);t=setTimeout(filtra,150)});
  mais.addEventListener('click',function(){desenha(false)});
  if(window.LISTA){dados=window.LISTA;filtra();return}
  fetch('lista.json').then(function(r){return r.json()}).then(function(d){dados=d;filtra()})
    .catch(function(){lst.innerHTML='<p class="nota">Não consegui carregar a lista.</p>'});
})();
