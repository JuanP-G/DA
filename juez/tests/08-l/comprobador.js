// Comprobador de 08-l «Planificación de conferencias» (versión navegador de 08-l.py; deben decir lo mismo).
// Es una expresión: la web la evalúa y obtiene comprobar(entrada, esperada, obtenida).
(function () {
  const NUM = /^-?\d+$/;
  function lineas(t) {
    const l = t.replace(/\r/g, '').split('\n').map(x => x.replace(/\s+$/, ''));
    while (l.length && l[l.length - 1] === '') l.pop();
    return l;
  }
  function palabras(t) { return t.split(/\s+/).filter(Boolean); }
  function casos(entrada) {
    const v = palabras(entrada).map(Number);
    let p = 0;
    const sig = () => v[p++];
    const r = [];
    for (let c = sig(); c > 0; c--) {
      const n = sig(), confs = [];
      for (let k = 0; k < n; k++) confs.push([sig(), sig()]);
      r.push(confs);
    }
    return r;
  }
  function revisaSalas(confs, R, linea) {
    const w = palabras(linea);
    if (!w.every(x => NUM.test(x))) return 'la línea debería tener solo números de sala';
    const n = confs.length;
    if (w.length !== n) return `hay ${n} conferencias y escribes ${w.length} números de sala`;
    const t = w.map(Number);
    for (let i = 0; i < n; i++) {
      if (!(t[i] >= 1 && t[i] <= R)) return `la conferencia ${i + 1} va a la sala ${t[i]}, que no existe (con ${R} salas van de 1 a ${R})`;
    }
    const orden = [...Array(n).keys()].sort((a, b) =>
      (t[a] - t[b]) || (confs[a][0] - confs[b][0]) || (confs[a][1] - confs[b][1]) || (a - b));
    for (let k = 0; k + 1 < n; k++) {
      const a = orden[k], b = orden[k + 1];
      if (t[a] === t[b] && confs[b][0] < confs[a][1]) {
        const x = Math.min(a, b), y = Math.max(a, b);
        return `las conferencias ${x + 1} (${confs[x][0]}-${confs[x][1]}) y ${y + 1} (${confs[y][0]}-${confs[y][1]}) se solapan y las pones las dos en la sala ${t[a]}`;
      }
    }
    return null;
  }
  function comprobarLineas(entrada, esperada, obtenida) {
    const e = lineas(esperada), o = lineas(obtenida);
    const cs = casos(entrada);
    for (let k = 0; k < cs.length; k++) {
      for (const j of [2 * k, 2 * k + 1]) {
        const x = e[j], y = j < o.length ? o[j] : null;
        const d = { linea: j + 1, esperada: x, obtenida: y, total: e.length, lineas_tuyas: o.length };
        if (y === null) { d.motivo = 'tu salida acaba antes'; return d; }
        if (y === x) continue;
        if (j === 2 * k) {
          const t = palabras(y);
          if (t.length === 1 && t[0] === x) { d.motivo = 'el número de salas es correcto, pero sobran espacios en la línea'; d.pe = true; }
          else if (t.length !== 1 || !NUM.test(t[0])) d.motivo = 'esta línea debería tener solo el número mínimo de salas';
          else if (Number(t[0]) > Number(x)) d.motivo = `usas ${Number(t[0])} salas y basta con ${x}`;
          else d.motivo = `con ${Number(t[0])} salas no caben: hay un momento con ${x} conferencias a la vez`;
          return d;
        }
        const motivo = revisaSalas(cs[k], Number(e[2 * k]), y);
        if (motivo) { d.motivo = motivo; return d; }
        if (y !== palabras(y).join(' ')) {
          d.motivo = 'la asignación es válida, pero los números deben ir separados por un solo espacio'; d.pe = true; return d;
        }
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
    const cuentas = lineas(esperada).map(l => palabras(l).length);
    const pal = palabras(obtenida);
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
