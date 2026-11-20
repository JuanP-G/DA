// Comprobador de 10-2 «Construyendo dianas» (versión navegador de 10-2.py; deben decir lo mismo).
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
    const r = [];
    while (p + 1 < v.length) {
      const V = v[p], S = v[p + 1];
      r.push([V, v.slice(p + 2, p + 2 + S)]);
      p += 2 + S;
    }
    return r;
  }
  function revisa(V, sectores, k, linea) {
    if (linea.trim() === 'Imposible') return [`escribes Imposible, pero sí se puede conseguir ${V} (con ${k} dardos)`, false];
    const m = /^\s*(-?\d+)\s*:((?:\s*-?\d+)*)\s*$/.exec(linea);
    if (!m) return ['la línea debe ser «número de dardos: puntuaciones» (por ejemplo «2: 4 4») o Imposible', false];
    const n = Number(m[1]);
    const nums = m[2].split(/\s+/).filter(Boolean).map(Number);
    if (n !== k) return [`escribes ${n} dardos y el mínimo es ${k}`, false];
    if (nums.length !== n) return [`dices ${n} dardos pero escribes ${nums.length} puntuaciones`, false];
    const ss = new Set(sectores);
    for (const x of nums) if (!ss.has(x)) return [`la puntuación ${x} no es ningún sector de esta diana`, false];
    const suma = nums.reduce((a, b) => a + b, 0);
    if (suma !== V) return [`tus puntuaciones suman ${suma} y no ${V}`, false];
    if (linea !== `${n}: ` + nums.join(' ')) return ['la solución es correcta, pero el formato no: «dardos», dos puntos pegados, y cada puntuación precedida de un espacio', true];
    return null;
  }
  return function comprobar(entrada, esperada, obtenida) {
    const e = lineas(esperada), o = lineas(obtenida);
    const cs = casos(entrada);
    for (let i = 0; i < cs.length; i++) {
      const [V, sectores] = cs[i];
      const x = e[i], y = i < o.length ? o[i] : null;
      const d = { linea: i + 1, esperada: x, obtenida: y, total: e.length, lineas_tuyas: o.length };
      if (y === null) { d.motivo = 'tu salida acaba antes'; return d; }
      if (y === x) continue;
      if (x === 'Imposible') { d.motivo = `no se puede conseguir ${V} con estas puntuaciones: la respuesta es Imposible`; return d; }
      const r = revisa(V, sectores, Number(x.split(':')[0]), y);
      if (r) { d.motivo = r[0]; if (r[1]) d.pe = true; return d; }
    }
    if (o.length > e.length) return { linea: e.length + 1, esperada: null, obtenida: o[e.length], total: e.length, lineas_tuyas: o.length, motivo: 'escribes líneas de más' };
    return null;
  };
})()
