// Comprobador de 11-L «La fiesta de graduación» (versión navegador de 11-l.py; deben decir lo mismo).
// Es una expresión: la web la evalúa y obtiene comprobar(entrada, esperada, obtenida).
(function () {
  function casos(entrada) {
    const l = entrada.replace(/\r/g, '').split('\n');
    const n = parseInt(l[0].trim().split(/\s+/)[0], 10);
    const pal = s => (s === undefined ? [] : s.split(/\s+/).filter(Boolean));
    const r = [];
    for (let c = 0; c < n; c++) r.push([pal(l[1 + 2 * c]), pal(l[2 + 2 * c])]);
    return r;
  }
  function subsecuencia(x, a) {
    let i = 0;
    for (const c of x) {
      while (i < a.length && a[i] !== c) i++;
      if (i >= a.length) return false;
      i++;
    }
    return true;
  }
  return function comprobar(entrada, esperada, obtenida) {
    const cs = casos(entrada);
    const e = esperada.replace(/\r/g, '').split('\n');
    const o = obtenida.replace(/\r/g, '').split('\n').map(x => x.replace(/\s+$/, ''));
    while (o.length && o[o.length - 1] === '') o.pop();
    const n = cs.length, mias = o.length;
    let formato = null;
    if (o.length > n) {
      return { linea: n + 1, esperada: null, obtenida: o[n], total: n, lineas_tuyas: mias,
        motivo: 'escribes líneas de más: una por caso' };
    }
    while (o.length < n) o.push('');
    for (let c = 0; c < n; c++) {
      const [a, b] = cs[c];
      const mejor = e[c].split(/\s+/).filter(Boolean).length;
      const fallo = motivo => ({ linea: c + 1, esperada: e[c], obtenida: o[c], total: n, lineas_tuyas: mias, motivo });
      const x = o[c].split(/\s+/).filter(Boolean);
      if (!subsecuencia(x, a)) return fallo('esa lista no es subsecuencia de la lista de la mañana (orden, repeticiones o canciones que no están)');
      if (!subsecuencia(x, b)) return fallo('esa lista no es subsecuencia de la lista de la tarde (orden, repeticiones o canciones que no están)');
      if (x.length !== mejor) return fallo(`la lista común más larga tiene ${mejor} canciones y escribes ${x.length}`);
      if (o[c] !== x.join(' ') && formato === null) formato = fallo('la lista es correcta, pero las canciones deben ir separadas por un solo espacio');
    }
    if (formato !== null) formato.pe = true;
    return formato;
  };
})()
