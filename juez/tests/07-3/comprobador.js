// Comprobador de 07-3 «RapidEats con ruta» (versión navegador de 07-3.py; deben decir lo mismo).
// Es una expresión: la web la evalúa y obtiene comprobar(entrada, esperada, obtenida).
(function () {
  const FORMA = /^(\d+): (\d+(?: -> \d+)*)$/;
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
      const n = sig(), nt = sig(), tramos = new Map();
      for (let k = 0; k < nt; k++) {
        const a = sig(), b = sig(), t = sig();
        for (const key of [a + ',' + b, b + ',' + a]) tramos.set(key, Math.min(t, tramos.has(key) ? tramos.get(key) : t));
      }
      const ped = [];
      for (let k = sig(); k > 0; k--) ped.push([sig(), sig()]);
      r.push([tramos, ped]);
    }
    return r;
  }
  function revisa(tramos, o, d, esperada, linea) {
    if (esperada === 'NO LLEGA') return 'no hay ningún camino de un punto al otro: hay que escribir NO LLEGA';
    if (linea === 'NO LLEGA') return `escribes NO LLEGA, pero sí hay camino de ${o} a ${d}`;
    const norm = linea.split(/\s+/).filter(Boolean).join(' ').replace(/\s*:\s*/, ': ').replace(/\s*->\s*/g, ' -> ');
    const m = norm.match(FORMA);
    if (!m) return 'el formato debe ser «tiempo: origen -> ... -> destino»';
    const tiempo = Number(m[1]);
    const camino = m[2].split(' -> ').map(Number);
    const minimo = Number(esperada.split(':')[0]);
    if (tiempo !== minimo) return `el tiempo mínimo es ${minimo} y escribes ${tiempo}`;
    if (camino[0] !== o) return `el camino debe empezar en el origen (${o}) y empieza en ${camino[0]}`;
    if (camino[camino.length - 1] !== d) return `el camino debe acabar en el destino (${d}) y acaba en ${camino[camino.length - 1]}`;
    let suma = 0;
    for (let k = 0; k + 1 < camino.length; k++) {
      const key = camino[k] + ',' + camino[k + 1];
      if (!tramos.has(key)) return `no hay ningún tramo entre ${camino[k]} y ${camino[k + 1]}`;
      suma += tramos.get(key);
    }
    if (suma !== minimo) return `tu camino tarda ${suma}, no ${minimo}: no es un camino mínimo`;
    if (norm !== linea) return ['PE', 'el camino es correcto, pero el formato no es exacto: «tiempo: a -> b -> c», con un espacio tras los dos puntos y alrededor de cada ->'];
    return null;
  }
  function comprobarLineas(entrada, esperada, obtenida) {
    const e = lineas(esperada), o = lineas(obtenida);
    let i = 0;
    for (const [tramos, pedidos] of casos(entrada)) {
      for (const p of pedidos.concat([null])) {          // null = la línea «---» tras el caso
        const x = e[i], y = i < o.length ? o[i] : null;
        const d = { linea: i + 1, esperada: x, obtenida: y, total: e.length, lineas_tuyas: o.length };
        i++;
        if (y === null) { d.motivo = 'tu salida acaba antes'; return d; }
        if (y === x) continue;
        if (p === null) { d.motivo = 'tras los pedidos de cada caso va una línea con ---'; return d; }
        const motivo = revisa(tramos, p[0], p[1], x, y);
        if (Array.isArray(motivo)) { d.motivo = motivo[1]; d.pe = true; return d; }
        if (motivo) { d.motivo = motivo; return d; }
      }
    }
    if (o.length > e.length) return { linea: e.length + 1, esperada: null, obtenida: o[e.length], total: e.length, lineas_tuyas: o.length, motivo: 'escribes líneas de más' };
    return null;
  }
  return function comprobar(entrada, esperada, obtenida) {
    const d = comprobarLineas(entrada, esperada, obtenida);
    if (d === null || d.pe) return d;
    // ¿Los mismos datos con otro reparto en líneas? Se reparten tus palabras como en la salida
    // esperada y, si así es correcta, es un error de presentación.
    const cuentas = lineas(esperada).map(l => l.split(/\s+/).filter(Boolean).length);
    const pal = obtenida.split(/\s+/).filter(Boolean);
    if (pal.length === cuentas.reduce((a, b) => a + b, 0)) {
      const nuevas = []; let k = 0;
      for (const c of cuentas) { nuevas.push(pal.slice(k, k + c).join(' ')); k += c; }
      if (comprobarLineas(entrada, esperada, nuevas.join('\n') + '\n') === null) {
        return Object.assign({}, d, { pe: true, motivo: 'tus respuestas son correctas, pero no están repartidas en líneas como pide el enunciado' });
      }
    }
    return d;
  };
})()
