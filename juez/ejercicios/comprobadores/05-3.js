// Comprobador de 05-3 «Ordenando tareas» (versión navegador de 05-3.py; deben decir lo mismo).
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
      const n = sig(), m = sig(), deps = [];
      for (let k = 0; k < m; k++) deps.push([sig(), sig()]);
      r.push([n, deps]);
    }
    return r;
  }
  function revisa(n, deps, linea) {
    const t = linea.split(/\s+/).filter(Boolean);
    if (t.length === 1 && t[0] === 'Imposible') return 'escribes Imposible, pero sí se pueden ordenar las tareas';
    if (!t.every(x => /^-?\d+$/.test(x))) return 'la línea debería tener solo números de tarea (o Imposible)';
    const nums = t.map(Number);
    if (nums.length !== n) return `hay ${n} tareas y escribes ${nums.length} números`;
    const pos = new Map();
    for (let i = 0; i < nums.length; i++) {
      const x = nums[i];
      if (!(x >= 1 && x <= n)) return `la tarea ${x} no existe (van de 1 a ${n})`;
      if (pos.has(x)) return `la tarea ${x} aparece dos veces`;
      pos.set(x, i);
    }
    for (const [a, b] of deps) if (pos.get(a) > pos.get(b)) return `la tarea ${a} debe ir antes que la ${b}, y en tu orden va después`;
    return null;
  }
  function comprobarLineas(entrada, esperada, obtenida) {
    const e = lineas(esperada), o = lineas(obtenida);
    const cs = casos(entrada);
    for (let i = 0; i < cs.length; i++) {
      const [n, deps] = cs[i];
      const x = e[i], y = i < o.length ? o[i] : null;
      const d = { linea: i + 1, esperada: x, obtenida: y, total: e.length, lineas_tuyas: o.length };
      if (y === null) { d.motivo = 'tu salida acaba antes'; return d; }
      if (y === x) continue;
      if (x === 'Imposible') { d.motivo = 'hay un ciclo de dependencias: la respuesta es Imposible'; return d; }
      const motivo = revisa(n, deps, y);
      if (motivo) { d.motivo = motivo; return d; }
      if (y !== y.split(/\s+/).filter(Boolean).join(' ')) {
        d.motivo = 'el orden es válido, pero los números deben ir separados por un solo espacio'; d.pe = true; return d;
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
