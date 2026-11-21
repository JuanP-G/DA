// Comprobador de 11-2 «Aibofobia» (versión navegador de 11-2.py; deben decir lo mismo).
// Es una expresión: la web la evalúa y obtiene comprobar(entrada, esperada, obtenida).
(function () {
  function lineas(t) {
    const l = t.replace(/\r/g, '').split('\n').map(x => x.replace(/\s+$/, ''));
    while (l.length && l[l.length - 1] === '') l.pop();
    return l;
  }
  function subsecuencia(a, b) {
    let k = 0;
    for (const c of b) if (k < a.length && a[k] === c) k++;
    return k === a.length;
  }
  function revisa(s, kEsp, linea) {
    const t = linea.split(/\s+/).filter(Boolean);
    if (t.length !== 2) return 'cada línea debe tener el número de letras añadidas y el palíndromo, separados por un espacio';
    if (!/^-?[0-9]+$/.test(t[0])) return 'la línea debe empezar por el número de letras añadidas';
    const k = parseInt(t[0], 10), p = t[1];
    if (k !== kEsp) return `el mínimo de letras que hay que añadir es ${kEsp} y escribes ${k}`;
    if (!/^[a-z]+$/.test(p)) return 'el palíndromo debe estar formado solo por letras minúsculas';
    if (p !== p.split('').reverse().join('')) return `«${p}» no es un palíndromo`;
    if (p.length !== s.length + k) return `el palíndromo debería tener ${s.length} + ${k} = ${s.length + k} letras y tiene ${p.length}`;
    if (!subsecuencia(s, p)) return `«${p}» no se obtiene añadiendo letras a «${s}» (no contiene sus letras en orden)`;
    return null;
  }
  function comprobarLineas(entrada, esperada, obtenida) {
    const e = lineas(esperada), o = lineas(obtenida);
    const t = entrada.split(/\s+/).filter(Boolean);
    const pal = t.slice(1, 1 + parseInt(t[0], 10));
    for (let i = 0; i < pal.length; i++) {
      const x = e[i], y = i < o.length ? o[i] : null;
      const d = { linea: i + 1, esperada: x, obtenida: y, total: e.length, lineas_tuyas: o.length };
      if (y === null) { d.motivo = 'tu salida acaba antes'; return d; }
      if (y === x) continue;
      const motivo = revisa(pal[i], parseInt(x.split(/\s+/)[0], 10), y);
      if (motivo) { d.motivo = motivo; return d; }
      if (y !== y.split(/\s+/).filter(Boolean).join(' ')) {
        d.motivo = 'la respuesta es válida, pero el número y el palíndromo deben ir separados por un solo espacio'; d.pe = true; return d;
      }
    }
    if (o.length > e.length) return { linea: e.length + 1, esperada: null, obtenida: o[e.length], total: e.length, lineas_tuyas: o.length, motivo: 'escribes líneas de más' };
    return null;
  }
  return function comprobar(entrada, esperada, obtenida) {
    const d = comprobarLineas(entrada, esperada, obtenida);
    if (d === null || d.pe) return d;
    const pal = obtenida.split(/\s+/).filter(Boolean);
    if (pal.length === 2 * lineas(esperada).length) {
      const nuevas = [];
      for (let k = 0; k < pal.length; k += 2) nuevas.push(pal.slice(k, k + 2).join(' '));
      if (comprobarLineas(entrada, esperada, nuevas.join('\n') + '\n') === null) {
        return Object.assign({}, d, { pe: true, motivo: 'tus respuestas son correctas, pero no están repartidas en líneas como pide el enunciado' });
      }
    }
    return d;
  };
})()
