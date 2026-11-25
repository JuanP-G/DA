// Comprobador de 11-3 «La colecta de primavera» (versión navegador de 11-3.py; deben decir lo mismo).
// Es una expresión: la web la evalúa y obtiene comprobar(entrada, esperada, obtenida).
(function () {
  function lineas(t) {
    const l = t.replace(/\r/g, '').split('\n').map(x => x.replace(/\s+$/, ''));
    while (l.length && l[l.length - 1] === '') l.pop();
    return l;
  }
  function casos(entrada) {
    const v = entrada.split(/\s+/).filter(Boolean).map(Number);
    let p = 0;
    const sig = () => v[p++];
    const r = [];
    for (let c = sig(); c > 0; c--) {
      const V = sig(), C = sig();
      const pago = [[], [], [], [], []];
      for (let k = 0; k < V; k++) pago[0].push(0);
      for (let k = 1; k <= 4; k++) for (let i = 0; i < V; i++) pago[k].push(sig());
      r.push([V, C, pago]);
    }
    return r;
  }
  function numeros(linea, cuantos) {
    const t = linea.split(/\s+/).filter(Boolean);
    if (t.length !== cuantos || !t.every(x => /^-?[0-9]+$/.test(x))) return null;
    return t.map(x => parseInt(x, 10));
  }
  function comprobarLineas(entrada, esperada, obtenida) {
    const e = lineas(esperada), o = lineas(obtenida);
    let ie = 0, io = 0, formato = null;
    const fallo = (motivo, esp) => ({ linea: io + 1, esperada: esp, obtenida: io < o.length ? o[io] : null,
      total: e.length, lineas_tuyas: o.length, motivo });
    for (const [V, C, pago] of casos(entrada)) {
      const mejor = parseInt(e[ie], 10);
      if (io >= o.length) return fallo('tu salida acaba antes', e[ie]);
      let x = numeros(o[io], 1);
      if (x === null) return fallo('en esta línea va el beneficio máximo (un solo número)', e[ie]);
      if (x[0] !== mejor) return fallo(`el beneficio máximo es ${mejor} y escribes ${x[0]}`, e[ie]);
      if (o[io] !== String(x[0]) && formato === null) formato = fallo('el beneficio es correcto, pero la línea debe tener solo el número', e[ie]);
      io++;
      if (io >= o.length) return fallo('tu salida acaba antes: falta la línea con las cajas de cada vecino', e[ie + 1]);
      x = numeros(o[io], V);
      if (x === null) return fallo(`en esta línea van ${V} enteros: las cajas que se venden a cada vecino`, e[ie + 1]);
      if (x.some(c => c < 0 || c > 4)) return fallo('a cada vecino se le venden entre 0 y 4 cajas', e[ie + 1]);
      const suma = x.reduce((a, b) => a + b, 0);
      if (suma > C) return fallo(`vendes ${suma} cajas y solo hay ${C}`, e[ie + 1]);
      let ganancia = 0;
      x.forEach((c, i) => { if (c) ganancia += pago[c][i]; });
      if (ganancia !== mejor) return fallo(`con ese reparto se recaudan ${ganancia} y el máximo es ${mejor}`, e[ie + 1]);
      if (o[io] !== x.join(' ') && formato === null) formato = fallo('el reparto es correcto, pero los números deben ir separados por un solo espacio', e[ie + 1]);
      io++;
      ie += 2;
    }
    if (io < o.length) return fallo('escribes líneas de más', null);
    if (formato !== null) formato.pe = true;
    return formato;
  }
  function reparte(entrada, obtenida) {
    const tok = obtenida.split(/\s+/).filter(Boolean);
    let k = 0;
    const out = [];
    for (const [V] of casos(entrada)) {
      if (k + 1 + V > tok.length) return null;
      out.push(tok[k]);
      out.push(tok.slice(k + 1, k + 1 + V).join(' '));
      k += 1 + V;
    }
    return k === tok.length ? out.join('\n') + '\n' : null;
  }
  return function comprobar(entrada, esperada, obtenida) {
    const d = comprobarLineas(entrada, esperada, obtenida);
    if (d === null || d.pe) return d;
    const r = reparte(entrada, obtenida);
    if (r !== null && comprobarLineas(entrada, esperada, r) === null) {
      return Object.assign({}, d, { pe: true, motivo: 'tus respuestas son correctas, pero no están repartidas en líneas como pide el enunciado' });
    }
    return d;
  };
})()
