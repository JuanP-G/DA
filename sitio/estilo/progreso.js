/* Progreso personal: ejercicios marcados como hechos. Se guarda solo en este navegador (localStorage).
   Los botones llevan data-ok="<slug>"; las tarjetas y bloques llevan data-ids="slug1,slug2,…". */
(function(){
  var KEY='studia-da-hechos';
  function leer(){try{return JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){return{}}}
  function guardar(h){try{localStorage.setItem(KEY,JSON.stringify(h))}catch(e){}}
  function pct(a,b){return b?Math.round(a/b*100):0}
  function cuenta(ids,h){return ids.filter(function(i){return h[i]}).length}
  function ids(el){return el.dataset.ids?el.dataset.ids.split(','):[]}
  function pintar(){
    var h=leer();
    document.querySelectorAll('[data-ok]').forEach(function(b){
      var on=!!h[b.dataset.ok];b.classList.toggle('on',on);b.setAttribute('aria-pressed',on?'true':'false');
      var f=b.closest('.exr');if(f)f.classList.toggle('hecho',on);
      var l=b.querySelector('.lab');if(l)l.textContent=on?'Hecho':'Marcar como hecho';
    });
    document.querySelectorAll('.tcard[data-ids],.box[data-ids],.thead[data-ids]').forEach(function(c){
      var l=ids(c),n=cuenta(l,h),t=l.length;
      var bar=c.querySelector('[data-bar]');if(bar)bar.style.width=pct(n,t)+'%';
      var tx=c.querySelector('[data-txt]');if(tx)tx.textContent=n+'/'+t+' · '+pct(n,t)+'%';
      var big=c.querySelector('[data-pct]');if(big)big.textContent=pct(n,t)+'%';
      var sm=c.querySelector('[data-hechos]');if(sm)sm.textContent=n+' de '+t+' hechos';
      var es=c.querySelector('[data-est]');if(es){es.className='est '+(n===0?'':n===t?'hecho':'curso');es.textContent=n===0?'Sin empezar':n===t?'Completado':'En curso'}
    });
    document.querySelectorAll('.bh[data-ids]').forEach(function(c){
      var l=ids(c),n=cuenta(l,h),t=l.length;
      var bar=c.querySelector('[data-bar]');if(bar)bar.style.width=pct(n,t)+'%';
      var tx=c.querySelector('[data-txt]');if(tx)tx.textContent=n+'/'+t+' hechos · '+pct(n,t)+'%';
    });
    var res=document.querySelector('[data-resumen]');
    if(res){
      var tarj=[].slice.call(document.querySelectorAll('.tcard[data-ids]')),todos=[],comp=0,curso=0,sig=null;
      tarj.forEach(function(c){var l=ids(c),n=cuenta(l,h);todos=todos.concat(l);if(n===l.length&&l.length)comp++;else if(n>0)curso++;if(!sig&&n<l.length)sig=c});
      var H=cuenta(todos,h),T=todos.length;
      var q=function(s){return res.querySelector(s)};
      q('[data-r=pct]').textContent=pct(H,T)+'%';q('[data-r=bar]').style.width=pct(H,T)+'%';
      q('[data-r=txt]').innerHTML=H+' de '+T+' ejercicios hechos'+(sig?' <a class="btn mini" href="'+sig.getAttribute('href')+'">Seguir en el tema '+sig.dataset.tema+' →</a>':'');
      q('[data-r=comp]').textContent=comp;q('[data-r=curso]').textContent=curso+' en curso';
    }
  }
  document.addEventListener('click',function(e){
    var b=e.target.closest('[data-ok]');if(!b)return;
    e.preventDefault();e.stopPropagation();
    var h=leer(),k=b.dataset.ok;if(h[k])delete h[k];else h[k]=1;guardar(h);pintar();
  });
  window.addEventListener('storage',pintar);window.addEventListener('pageshow',pintar);
  window.pintarProgreso=pintar;
  pintar();
})();
