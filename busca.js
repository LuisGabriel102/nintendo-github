(function(){
  var q=document.getElementById('q'),nada=document.getElementById('nada');
  var secs=[].slice.call(document.querySelectorAll('details.sec'));
  var estado=secs.map(function(s){return s.open});
  function norm(t){return t.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'')}
  var cards=[].slice.call(document.querySelectorAll('.card')).map(function(c){return [c,norm(c.getAttribute('data-s')||c.textContent)]});
  var t;
  q.addEventListener('input',function(){clearTimeout(t);t=setTimeout(filtra,120)});
  function filtra(){
    var v=norm(q.value.trim()),achou=0;
    if(!v){
      cards.forEach(function(c){c[0].classList.remove('oculto')});
      secs.forEach(function(s,i){s.classList.remove('oculto');s.open=estado[i]});
      nada.hidden=true;return;
    }
    var termos=v.split(/\s+/);
    cards.forEach(function(c){
      var ok=termos.every(function(x){return c[1].indexOf(x)>=0});
      c[0].classList.toggle('oculto',!ok);
    });
    secs.forEach(function(s){
      var n=s.querySelectorAll('.card:not(.oculto)').length;
      s.classList.toggle('oculto',n===0);
      if(n){s.open=true;achou+=n}
    });
    nada.hidden=achou>0;
  }
  // abrir a seção ao tocar no menu
  document.querySelectorAll('nav a[href^="#"]').forEach(function(a){
    a.addEventListener('click',function(){var d=document.querySelector(a.getAttribute('href'));if(d&&d.tagName==='DETAILS')d.open=true});
  });
  if(location.hash){var d=document.querySelector(location.hash);if(d&&d.tagName==='DETAILS')d.open=true}
})();
