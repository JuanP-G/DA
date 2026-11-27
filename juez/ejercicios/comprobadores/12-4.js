// Comprobador de 12-4 «Mejor no llevar muchas monedas» (versión navegador de 12-4.py; deben decir lo mismo).
// Es una expresión: la web la evalúa y obtiene comprobar(entrada, esperada, obtenida).
(function () {
  function casos(entrada) {
    const d = entrada.split(/\s+/).filter(Boolean).map(Number);
    let p = 0;
    const r = [];
    const t = d[p++];
    for (let c = 0; c < t; c++) {
      const n = d[p++];
      const v = d.slice(p, p + n); p += n;
      const q = d.slice(p, p + n); p += n;
      r.push([v, q, d[p++]]);
    }
    return r;
  }
  const palabras = s => s.split(/\s+/).filter(Boolean);
  return function comprobar(entrada, esperada, obtenida) {
    const cs = casos(entrada);
    const e = esperada.replace(/\r/g, '').split('\n');
    const o = obtenida.replace(/\r/g, '').split('\n').map(x => x.replace(/\s+$/, ''));
    while (o.length && o[o.length - 1] === '') o.pop();
    const n = cs.length, mias = o.length;
    let formato = null;
    if (mias > n) {
      return { linea: n + 1, esperada: null, obtenida: o[n], total: n, lineas_tuyas: mias,
        motivo: 'escribes líneas de más: una por caso' };
    }
    while (o.length < n) o.push('');
    for (let k = 0; k < n; k++) {
      const [v, c, P] = cs[k];
      const fallo = motivo => ({ linea: k + 1, esperada: e[k], obtenida: o[k], total: n, lineas_tuyas: mias, motivo });
      const x = palabras(o[k]), bien = palabras(e[k]);
      if (bien[0] === 'NO') {
        if (!(x.length === 1 && x[0] === 'NO')) return fallo('el precio no se puede pagar de forma exacta: hay que escribir NO');
      } else {
        if (x[0] !== 'SI') return fallo('el precio sí se puede pagar: la línea debe empezar por SI');
        if (x.length !== v.length + 1 || !x.slice(1).every(s => /^[0-9]{1,7}$/.test(s))) return fallo(`después de SI van ${v.length} números, uno por tipo de moneda`);
        const u = x.slice(1).map(Number);
        if (u.some((a, i) => a > c[i])) return fallo('usas más monedas de un tipo de las que hay');
        if (u.reduce((s, a, i) => s + a * v[i], 0) !== P) return fallo(`esas monedas no suman ${P}`);
        const minimo = bien.slice(1).reduce((s, a) => s + Number(a), 0);
        const mias_m = u.reduce((s, a) => s + a, 0);
        if (mias_m !== minimo) return fallo(`se puede pagar con ${minimo} monedas y usas ${mias_m}`);
      }
      if (o[k] !== x.join(' ') && formato === null) formato = fallo('la respuesta es correcta, pero separa con un solo espacio');
    }
    if (formato !== null) formato.pe = true;
    return formato;
  };
})()
