// Comprobador de 11-1 «El cazatesoros» (versión navegador de 11-1.py; deben decir lo mismo).
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
      const T = sig(), n = sig(), cofres = [];
      for (let k = 0; k < n; k++) cofres.push([sig(), sig()]);
      r.push([T, cofres]);
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
    for (const [T, cofres] of casos(entrada)) {
      const oro = parseInt(e[ie], 10), kEsp = parseInt(e[ie + 1], 10), sep = ie + kEsp + 2;
      // 1. oro máximo
      if (io >= o.length) return fallo('tu salida acaba antes', e[ie]);
      let x = numeros(o[io], 1);
      if (x === null) return fallo('en esta línea va el oro máximo (un solo número)', e[ie]);
      if (x[0] !== oro) return fallo(`el oro máximo es ${oro} y escribes ${x[0]}`, e[ie]);
      if (o[io] !== String(x[0]) && formato === null) formato = fallo('el oro es correcto, pero la línea debe tener solo el número', e[ie]);
      io++;
      // 2. número de cofres
      if (io >= o.length) return fallo('tu salida acaba antes: falta la línea con el número de cofres', e[ie + 1]);
      x = numeros(o[io], 1);
      if (x === null) return fallo('en esta línea va el número de cofres que hay que recoger (un solo número)', e[ie + 1]);
      const k = x[0];
      if (k < 0 || k > cofres.length) return fallo(`escribes ${k} cofres y en la entrada hay ${cofres.length}`, e[ie + 1]);
      io++;
      // 3. los cofres
      const quedan = new Map();
      for (const [p, g] of cofres) quedan.set(p + ' ' + g, (quedan.get(p + ' ' + g) || 0) + 1);
      let tiempo = 0, suma = 0;
      for (let c = 0; c < k; c++) {
        const esp = kEsp ? e[ie + 2] : e[sep];
        if (io >= o.length) return fallo(`tu salida acaba antes: dices que hay ${k} cofres y faltan líneas de cofres`, esp);
        x = numeros(o[io], 2);
        if (x === null) return fallo(`dices que hay ${k} cofres, así que aquí va un cofre como «profundidad oro»`, esp);
        const clave = x[0] + ' ' + x[1];
        if (!quedan.has(clave)) return fallo(`no hay ningún cofre «${x[0]} ${x[1]}» en la entrada (primero va la profundidad y luego el oro)`, esp);
        if (quedan.get(clave) === 0) return fallo(`el cofre «${x[0]} ${x[1]}» aparece más veces de las que está en la entrada (cada cofre se sube una sola vez)`, esp);
        if (o[io] !== clave && formato === null) formato = fallo('el cofre es correcto, pero la profundidad y el oro deben ir separados por un solo espacio', esp);
        quedan.set(clave, quedan.get(clave) - 1);
        tiempo += 3 * x[0];
        suma += x[1];
        io++;
      }
      if (tiempo > T) { io -= k ? 1 : 0; return fallo(`los cofres que escribes necesitan ${tiempo} segundos (3·p cada uno) y la botella da ${T}`, e[sep - 1]); }
      if (suma !== oro) { io -= k ? 1 : 0; return fallo(`los cofres que escribes suman ${suma} monedas y no ${oro}`, e[sep - 1]); }
      // 4. separador
      if (io >= o.length) return fallo('tu salida acaba antes: falta la línea «---» del final del caso', '---');
      if (o[io] !== '---') {
        if (o[io].trim() === '---' && formato === null) formato = fallo('la línea debe ser exactamente «---»', '---');
        else if (o[io].trim() !== '---') return fallo('después de los cofres de cada caso va una línea con «---»', '---');
      }
      io++;
      ie = sep + 1;
    }
    if (io < o.length) return fallo('escribes líneas de más', null);
    if (formato !== null) formato.pe = true;
    return formato;
  }
  return function comprobar(entrada, esperada, obtenida) {
    const d = comprobarLineas(entrada, esperada, obtenida);
    if (d === null || d.pe) return d;
    const a = obtenida.split(/\s+/).filter(Boolean), b = esperada.split(/\s+/).filter(Boolean);
    if (a.length === b.length && a.every((x, i) => x === b[i])) {
      return Object.assign({}, d, { pe: true, motivo: 'tus respuestas son correctas, pero no están repartidas en líneas como pide el enunciado' });
    }
    return d;
  };
})()
