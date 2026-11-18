/* Botón de tema claro/oscuro compartido. Busca un elemento con id="tema". */
(function(){
  var b=document.getElementById("tema");if(!b)return;
  b.addEventListener("click",function(){
    var r=document.documentElement;
    var oscuro=r.dataset.theme?r.dataset.theme==="dark":getComputedStyle(r).colorScheme.indexOf("dark")>=0;
    var n=oscuro?"light":"dark";
    r.dataset.theme=n;try{localStorage.setItem("tema",n)}catch(e){}
  });
})();
