(function(){
  var lst=document.getElementById('lst'),mais=document.getElementById('mais'),q=document.getElementById('q'),nada=document.getElementById('nada');
  var dados=[],filtrado=[],mostrados=0,cat='Todos',PASSO=60;
  function norm(t){return (t||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'')}
  function esc(t){return (t||'').replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function card(r){
    return '<div class="card"><div class="ct"><a href="https://github.com/'+esc(r[0])+'" target="_blank" rel="noopener">'+esc(r[0])+'</a></div>'+
      '<div class="bs"><span class="b st">★ '+r[1]+'</span>'+(r[2]?'<span class="b arq">ARQ</span>':'')+'<span class="b arq">'+esc(r[3])+'</span></div>'+
      (r[4]?'<p>'+esc(r[4])+'</p>':'')+'</div>';
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
      var s=r._s||(r._s=norm(r[0]+' '+r[4]+' '+r[3]));
      return termos.every(function(x){return s.indexOf(x)>=0});
    });
    desenha(true);
  }
  document.querySelectorAll('.filtros button').forEach(function(b){
    b.addEventListener('click',function(){
      document.querySelectorAll('.filtros button').forEach(function(x){x.setAttribute('aria-pressed','false')});
      b.setAttribute('aria-pressed','true');cat=b.getAttribute('data-c');filtra();
    });
  });
  var t;q.addEventListener('input',function(){clearTimeout(t);t=setTimeout(filtra,150)});
  mais.addEventListener('click',function(){desenha(false)});
  fetch('lista.json').then(function(r){return r.json()}).then(function(d){dados=d;filtra()})
    .catch(function(){lst.innerHTML='<p class="nota">Não consegui carregar a lista.</p>'});
})();
