/* Botón de tema claro/oscuro compartido. Busca un elemento con id="tema". */
(function(){
  var b=document.getElementById("tema");if(!b)return;
  b.addEventListener("click",function(){
    var r=document.documentElement,oscuro=matchMedia("(prefers-color-scheme:dark)").matches;
    var n=(r.dataset.theme||(oscuro?"dark":"light"))==="dark"?"light":"dark";
    r.dataset.theme=n;try{localStorage.setItem("tema",n)}catch(e){}
  });
})();
