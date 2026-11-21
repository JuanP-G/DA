// Comprobador de eval-1 «MasterHash» (versión navegador de eval-1.py; deben decir lo mismo).
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
      const n = sig(), a = sig(), s = sig(), pl = sig(), aris = [];
      for (let k = 0; k < a; k++) aris.push([sig(), sig()]);
      r.push([n, s, pl, aris]);
    }
    return r;
  }
  function revisa(esperada, linea, P, aris) {
    const t = linea.split(/\s+/).filter(Boolean);
    if (!t.length) return 'la línea está vacía: hay que escribir SI (y el orden) o NO';
    if (t[0] === 'NO' && t.length === 1) return 'escribes NO, pero el plato sí se puede hacer';
    if (t[0] !== 'SI') return 'la línea debe empezar por SI (en mayúsculas y sin tilde) o ser NO';
    if (!t.slice(1).every(x => /^-?[0-9]+$/.test(x))) return 'después de SI solo van números de elaboración';
    const nums = t.slice(1).map(x => parseInt(x, 10));
    const nec = new Set(esperada.split(/\s+/).filter(Boolean).slice(1).map(x => parseInt(x, 10)));
    const pos = new Map();
    for (let i = 0; i < nums.length; i++) {
      const x = nums[i];
      if (!nec.has(x)) return `la elaboración ${x} no hace falta para el plato ${P}`;
      if (pos.has(x)) return `la elaboración ${x} aparece dos veces`;
      pos.set(x, i);
    }
    if (nums.length < nec.size) {
      let falta = Infinity;
      for (const x of nec) if (!pos.has(x) && x < falta) falta = x;
      return `falta la elaboración ${falta}, que también hace falta para el plato ${P}`;
    }
    if (nums[nums.length - 1] !== P) return `el plato ${P} debe ser el último`;
    for (const [x, y] of aris) if (pos.has(x) && pos.has(y) && pos.get(x) > pos.get(y)) return `la elaboración ${x} hace falta para la ${y}, y en tu orden va después`;
    return null;
  }
  function comprobarLineas(entrada, esperada, obtenida) {
    const e = lineas(esperada), o = lineas(obtenida);
    const cs = casos(entrada);
    for (let i = 0; i < cs.length; i++) {
      const [, , P, aris] = cs[i];
      const x = e[i], y = i < o.length ? o[i] : null;
      const d = { linea: i + 1, esperada: x, obtenida: y, total: e.length, lineas_tuyas: o.length };
      if (y === null) { d.motivo = 'tu salida acaba antes'; return d; }
      if (y === x) continue;
      if (x === 'NO') { d.motivo = 'el plato no se puede hacer: la respuesta es NO'; return d; }
      const motivo = revisa(x, y, P, aris);
      if (motivo) { d.motivo = motivo; return d; }
      if (y !== y.split(/\s+/).filter(Boolean).join(' ')) {
        d.motivo = 'el orden es válido, pero SI y los números deben ir separados por un solo espacio'; d.pe = true; return d;
      }
    }
    if (o.length > e.length) return { linea: e.length + 1, esperada: null, obtenida: o[e.length], total: e.length, lineas_tuyas: o.length, motivo: 'escribes líneas de más' };
    return null;
  }
  return function comprobar(entrada, esperada, obtenida) {
    const d = comprobarLineas(entrada, esperada, obtenida);
    if (d === null || d.pe) return d;
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
