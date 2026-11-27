// Comprobador de 12-10 «Megaautopista de Oriente» (versión navegador de 12-10.py; deben decir lo mismo).
// Es una expresión: la web la evalúa y obtiene comprobar(entrada, esperada, obtenida).
(function () {
  function casos(entrada) {
    const d = entrada.split(/\s+/).filter(Boolean).map(Number);
    let p = 0;
    const r = [];
    while (p < d.length) {
      const n = d[p++], D = d[p++];
      const b = new Map();
      for (let i = 0; i < n; i++) b.set(d[p + i], d[p + n + i]);
      p += 2 * n;
      r.push([D, b]);
    }
    return r;
  }
  const palabras = s => s.split(/\s+/).filter(Boolean);
  return function comprobar(entrada, esperada, obtenida) {
    const cs = casos(entrada);
    const e = esperada.replace(/\r/g, '').split('\n');
    const o = obtenida.replace(/\r/g, '').split('\n').map(x => x.replace(/\s+$/, ''));
    while (o.length && o[o.length - 1] === '') o.pop();
    const total = 2 * cs.length, mias = o.length;
    let formato = null;
    if (mias > total) {
      return { linea: total + 1, esperada: null, obtenida: o[total], total, lineas_tuyas: mias,
        motivo: 'escribes líneas de más: dos por caso' };
    }
    while (o.length < total) o.push('');
    for (let c = 0; c < cs.length; c++) {
      const [D, b] = cs[c];
      const fallo = (k, motivo) => ({ linea: k + 1, esperada: e[k], obtenida: o[k], total, lineas_tuyas: mias, motivo });
      const i = 2 * c, j = 2 * c + 1;
      const v = palabras(o[i]), s = palabras(o[j]);
      if (!(v.length === 1 && v[0] === e[i].trim())) return fallo(i, 'el beneficio máximo no es ese');
      if (!s.length || !s.every(t => /^[0-9]{1,9}$/.test(t))) return fallo(j, 'la segunda línea son los puntos kilométricos de los restaurantes');
      const p = s.map(Number);
      if (p.some(q => !b.has(q))) return fallo(j, 'alguna de esas posiciones no es un área de descanso');
      if (p.some((q, k) => k > 0 && q - p[k - 1] < D)) return fallo(j, `las posiciones deben ir de menor a mayor y separadas al menos ${D} km`);
      if (p.reduce((a, q) => a + b.get(q), 0) !== Number(e[i])) return fallo(j, 'esas áreas no suman el beneficio máximo');
      for (const [k, t] of [[i, v], [j, s]]) {
        if (o[k] !== t.join(' ') && formato === null) formato = fallo(k, 'la respuesta es correcta, pero separa con un solo espacio');
      }
    }
    if (formato !== null) formato.pe = true;
    return formato;
  };
})()
