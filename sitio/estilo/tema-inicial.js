/* Aplica el tema guardado antes de pintar, para que no parpadee. Va en el <head>. */
try{var t=localStorage.getItem("tema");if(t)document.documentElement.dataset.theme=t}catch(e){}
