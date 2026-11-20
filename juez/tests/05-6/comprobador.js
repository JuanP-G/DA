// Comprobador de 05-6 «Sistema de inecuaciones» (versión navegador de 05-6.py; deben decir lo mismo).
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
      const n = sig(), m = sig(), ineq = [];
      for (let k = 0; k < m; k++) ineq.push([sig(), sig()]);
      r.push([n, ineq]);
    }
    return r;
  }
  function revisa(n, ineq, linea) {
    const t = linea.split(/\s+/).filter(Boolean);
    if (t.length === 1 && t[0] === 'NO') return 'escribes NO, pero el sistema sí tiene solución';
    if (!t.length || t[0] !== 'SI') return 'la línea debe empezar por SI (o ser NO)';
    const vs = t.slice(1);
    if (!vs.every(x => /^-?\d+$/.test(x))) return 'después de SI solo puede haber números enteros';
    const vals = vs.map(x => BigInt(x));
    if (vals.length !== n) return `hay ${n} variables y escribes ${vals.length} valores`;
    for (const [i, j] of ineq) {
      if (!(vals[i - 1] < vals[j - 1])) return `no se cumple x${i} < x${j}: le das ${vals[i - 1]} a x${i} y ${vals[j - 1]} a x${j}`;
    }
    return null;
  }
  function comprobarLineas(entrada, esperada, obtenida) {
    const e = lineas(esperada), o = lineas(obtenida);
    const cs = casos(entrada);
    for (let i = 0; i < cs.length; i++) {
      const [n, ineq] = cs[i];
      const x = e[i], y = i < o.length ? o[i] : null;
      const d = { linea: i + 1, esperada: x, obtenida: y, total: e.length, lineas_tuyas: o.length };
      if (y === null) { d.motivo = 'tu salida acaba antes'; return d; }
      if (y === x) continue;
      if (x === 'NO') { d.motivo = 'hay un ciclo de inecuaciones: la respuesta es NO'; return d; }
      const motivo = revisa(n, ineq, y);
      if (motivo) { d.motivo = motivo; return d; }
      if (y !== y.split(/\s+/).filter(Boolean).join(' ')) {
        d.motivo = 'la asignación es válida, pero los valores deben ir separados por un solo espacio'; d.pe = true; return d;
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
