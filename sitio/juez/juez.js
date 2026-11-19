/* Juez de la web de DA: componente independiente.
   Uso:  DAJuez.mount(elemento, { manifest: '04-3/manifest.json', wasmBase: 'https://…/' })
   Encaja donde se quiera (pestaña «Probar» o página propia): solo necesita un <div>. */
(function () {
  const AQUI = (document.currentScript && document.currentScript.src) || location.href;
  const RUTA_WORKER = new URL('juez-worker.js', AQUI).href;
  const WASM_BASE = 'https://binji.github.io/wasm-clang/';

  // Veredictos (las siglas son las de los jueces de programación, DOMjudge incluido)
  const NOMBRES = {
    ac: 'Correcto', wa: 'Respuesta incorrecta', pe: 'Error de presentación', ce: 'Error de compilación',
    tle: 'Tiempo excedido', mle: 'Memoria excedida', rte: 'Error de ejecución', ole: 'Salida excesiva',
    skip: 'No ejecutada',
  };
  const SIGLAS = { ac: 'AC', wa: 'WA', pe: 'PE', ce: 'CE', tle: 'TLE', mle: 'MLE', rte: 'RTE', ole: 'OLE', skip: '—' };
  const QUE_ES = {
    wa: 'Tu programa termina, pero escribe algo distinto de lo esperado.',
    pe: 'Los datos son correctos, pero el formato no: espacios, saltos de línea o el orden en que los escribes.',
    tle: 'Tu programa tarda más del límite: o no termina (bucle infinito) o el algoritmo es demasiado lento.',
    mle: 'Tu programa usa más memoria de la permitida.',
    rte: 'Tu programa se rompe mientras se ejecuta (acceso fuera de rango, división entre cero, excepción...).',
    ole: 'Tu programa escribe muchísimo más de lo esperado (casi siempre, un bucle que no para).',
    ce: 'El código no compila: el compilador te dice en qué línea está el error.',
  };
  // Orden en que se busca la prueba que mejor explica el fallo: las pensadas para un error concreto primero.
  const PRIORIDAD = { trampa: 0, borde: 1, enunciado: 2, aleatorio: 3, rendimiento: 4 };

  // ---- comparación: ignora espacios al final de línea y líneas vacías finales ----
  function lineas(t) {
    const l = t.replace(/\r/g, '').split('\n').map(x => x.replace(/\s+$/, ''));
    while (l.length && l[l.length - 1] === '') l.pop();
    return l;
  }
  function compara(esperada, obtenida) {
    const a = lineas(esperada), b = lineas(obtenida);
    const n = Math.max(a.length, b.length);
    for (let i = 0; i < n; i++) {
      if (a[i] !== b[i]) {
        const pe = esperada.trim().split(/\s+/).join(' ') === obtenida.trim().split(/\s+/).join(' ');
        return { igual: false, linea: i + 1, esperada: a[i], obtenida: b[i], total: a.length, lineas_tuyas: b.length, pe };
      }
    }
    return { igual: true };
  }

  function explica(d) {
    if (/unreachable|abort/.test(d)) return 'El programa se detuvo de golpe: acceso fuera de rango (por ejemplo v.at(i) o un puntero), excepción sin capturar, assert o abort().';
    if (/out of bounds|memory/.test(d)) return 'Acceso a memoria fuera de rango o memoria agotada. ' + d;
    if (/call stack|Maximum/.test(d)) return 'Recursión demasiado profunda (desbordamiento de pila). ' + d;
    if (/exited with code/.test(d)) return 'El programa terminó con código de error: ' + d;
    return d;
  }
  function h(tag, attrs, ...hijos) {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
      if (k === 'class') e.className = v; else if (k.startsWith('on')) e[k] = v; else e.setAttribute(k, v);
    }
    for (const c of hijos.flat()) if (c != null) e.append(c.nodeType ? c : document.createTextNode(c));
    return e;
  }
  const corta = (s, n = 160) => (s == null ? '(nada: la salida acaba antes)' : s.length > n ? s.slice(0, n) + '…' : s);

  class Juez {
    constructor(raiz, cfg) {
      this.raiz = raiz;
      this.cfg = cfg;
      this.wasmBase = cfg.wasmBase || WASM_BASE;
      this.worker = null;
      this.msgs = new Map();
      this.sigId = 1;
      this.cacheTexto = new Map();
      this.ocupado = false;
      this.compilado = null;   // { codigo } si el worker tiene el programa listo
    }

    async arrancar() {
      this.manifestUrl = new URL(this.cfg.manifest, location.href).href;
      this.m = await (await fetch(this.manifestUrl)).json();
      this.clave = 'da-juez-' + this.m.id;
      this.dibujar();
    }

    url(rel) { return new URL(rel, this.manifestUrl).href; }

    async texto(rel) {
      const u = this.url(rel);
      if (!this.cacheTexto.has(u)) {
        const r = await fetch(u);
        if (!r.ok) throw new Error('No se pudo leer ' + rel);
        this.cacheTexto.set(u, await r.text());
      }
      return this.cacheTexto.get(u);
    }

    // ---------- interfaz ----------
    dibujar() {
      let guardado = '';
      try { guardado = localStorage.getItem(this.clave) || ''; } catch (e) {}
      this.ta = h('textarea', { class: 'dj-code', spellcheck: 'false', 'aria-label': 'Tu código C++', rows: 22 });
      this.ta.value = guardado || this.m.plantilla;
      this.ta.addEventListener('input', () => { try { localStorage.setItem(this.clave, this.ta.value); } catch (e) {} });
      this.ta.addEventListener('keydown', ev => {
        if (ev.key === 'Tab') { ev.preventDefault(); document.execCommand('insertText', false, '    '); }
      });
      this.btn = h('button', { class: 'btn prim', type: 'button', onclick: () => this.comprobar() }, 'Comprobar');
      const botones = [
        this.btn,
        h('button', { class: 'btn', type: 'button', onclick: () => this.poner(this.m.plantilla) }, 'Plantilla vacía'),
      ];
      if (this.m.demo) {
        botones.push(h('button', { class: 'btn', type: 'button', onclick: async () => this.poner(await this.texto(this.m.demo.solucion)) }, 'Demo: solución correcta'));
        botones.push(h('button', { class: 'btn', type: 'button', onclick: async () => this.poner(await this.texto(this.m.demo.fallo)) }, 'Demo: con un fallo'));
      }
      this.estado = h('div', { class: 'dj-estado', role: 'status', 'aria-live': 'polite' });
      this.res = h('div', { class: 'dj-res' });
      this.raiz.replaceChildren(
        this.cfg.servidor
          ? h('p', { class: 'dj-nota' }, 'Al pulsar Comprobar, tu código se envía al servidor del juez (una Raspberry Pi), que lo compila con g++ (C++17) y lo ejecuta aislado con límites de tiempo y memoria. Si el servidor no responde, se usa el compilador del navegador (clang 8, ~60 MB la primera vez).')
          : h('p', { class: 'dj-nota' }, 'Tu código se compila y se ejecuta en tu navegador con ', h('b', {}, 'clang 8 (C++17)'),
          '; no se envía a ningún servidor. La primera vez descarga el compilador (~60 MB, queda en caché).'),
        this.ta,
        h('div', { class: 'dj-bar' }, botones),
        this.estado, this.res);
    }

    poner(codigo) { this.ta.value = codigo; this.ta.dispatchEvent(new Event('input')); this.res.replaceChildren(); this.estado.textContent = ''; }

    msg(t) { this.estado.textContent = t; }

    // ---------- worker ----------
    pide(tipo, datos) {
      return new Promise((ok, ko) => {
        const id = this.sigId++;
        this.msgs.set(id, { ok, ko });
        this.worker.postMessage(Object.assign({ id, tipo }, datos));
      });
    }

    async nuevoWorker() {
      if (this.worker) this.worker.terminate();
      this.worker = new Worker(RUTA_WORKER);
      this.compilado = null;
      this.worker.onmessage = ev => {
        const p = this.msgs.get(ev.data.id);
        if (!p) return;
        this.msgs.delete(ev.data.id);
        ev.data.ok ? p.ok(ev.data.r) : p.ko(new Error(ev.data.error));
      };
      this.worker.onerror = ev => {
        for (const p of this.msgs.values()) p.ko(new Error(ev.message || 'Fallo del worker'));
        this.msgs.clear();
      };
      await this.pide('iniciar', { wasmBase: this.wasmBase });
    }

    async ficheros() {
      const f = {};
      for (const c of this.m.cabeceras || []) f[c.nombre] = await this.texto(c.url);
      return f;
    }

    async asegurarCompilado(codigo) {
      if (this.worker && this.compilado === codigo) return { ok: true, log: '' };
      await this.nuevoWorker();
      this.msg('Compilando…');
      const r = await this.pide('compilar', { codigo, ficheros: await this.ficheros() });
      if (r.ok) this.compilado = codigo;
      return r;
    }

    // ---------- comprobar ----------
    // Si hay servidor (la Raspberry Pi), el código se juzga allí; si no responde, se usa el navegador.
    async comprobar() {
      if (this.ocupado) return;
      if (!this.cfg.servidor) return this.comprobarWasm();
      this.ocupado = true;
      this.btn.disabled = true;
      this.res.replaceChildren();
      let r;
      // Si la Pi no contesta en un tiempo razonable (colgada, sin red, túnel caído), se usa el navegador.
      const corte = new AbortController();
      const reloj = setTimeout(() => corte.abort(), 150000);
      try {
        this.msg('Enviando al servidor del juez…');
        const resp = await fetch(this.cfg.servidor.replace(/\/$/, '') + '/juzgar', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ id: this.m.id, codigo: this.ta.value }),
          signal: corte.signal,
        });
        r = await resp.json();
        if (resp.status === 503) throw new Error('juez ocupado o en mantenimiento');
        if (!resp.ok) {              // límites (429/413): se informa, no se cae al navegador
          this.msg('');
          this.res.replaceChildren(h('div', { class: 'dj-err' }, r.error || ('Error ' + resp.status)));
          this.ocupado = false; this.btn.disabled = false;
          return;
        }
      } catch (e) {                  // servidor apagado, colgado, ocupado o sin conexión: respaldo en el navegador
        clearTimeout(reloj);
        this.ocupado = false; this.btn.disabled = false;
        this.msg('El servidor del juez no responde; se usa el compilador del navegador…');
        return this.comprobarWasm();
      }
      clearTimeout(reloj);
      this.msg('');
      try {
        if (r.error) this.res.replaceChildren(h('div', { class: 'dj-err' }, r.error));
        else if (r.veredicto === 'ce' && !r.tests) this.pintarCE(r.log || '');
        else {
          const filas = r.tests.map(f => ({ t: this.m.tests.find(x => x.n === f.n) || { nombre: '' }, v: f.v, ms: f.ms, dif: f.dif, detalle: f.detalle }));
          this.pintar(filas, true);
        }
      } finally {
        this.ocupado = false;
        this.btn.disabled = false;
      }
    }

    async comprobarWasm() {
      if (this.ocupado) return;
      this.ocupado = true;
      this.btn.disabled = true;
      this.res.replaceChildren();
      const codigo = this.ta.value;
      const limite = this.m.limite_ms || 3000;
      const filas = [];
      try {
        this.msg(this.worker ? 'Compilando…' : 'Cargando el compilador (la primera vez tarda)…');
        const c = await this.asegurarCompilado(codigo);
        if (!c.ok) {
          this.msg('');
          this.pintarCE(c.log);
          return;
        }
        for (let i = 0; i < this.m.tests.length; i++) {
          const t = this.m.tests[i];
          this.msg(`Probando ${i + 1} de ${this.m.tests.length}…`);
          const fila = await this.probar(codigo, t, limite);
          filas.push(fila);
          this.pintar(filas);
          if (fila.v === 'tle') {      // no se espera el límite en cada prueba restante
            for (const r of this.m.tests.slice(i + 1)) filas.push({ t: r, v: 'skip', ms: 0 });
            break;
          }
        }
        this.msg('');
        this.pintar(filas, true);
      } catch (e) {
        this.msg('');
        this.res.replaceChildren(h('div', { class: 'dj-err' }, 'No se pudo comprobar: ' + e.message));
      } finally {
        this.ocupado = false;
        this.btn.disabled = false;
      }
    }

    async probar(codigo, t, limite) {
      const entrada = await this.texto(t.in), esperada = await this.texto(t.out);
      await this.asegurarCompilado(codigo);
      let temporizador;
      const tope = new Promise(ok => { temporizador = setTimeout(() => ok('tiempo'), limite + 1500); });
      const r = await Promise.race([this.pide('ejecutar', { entrada }), tope]);
      clearTimeout(temporizador);
      if (r === 'tiempo') {                       // el programa no acaba: se descarta el worker
        this.worker.terminate(); this.worker = null; this.compilado = null; this.msgs.clear();
        return { t, v: 'tle', ms: limite };
      }
      if (r.estado === 'rte') return { t, v: 'rte', ms: r.ms, detalle: explica(r.detalle) };
      if (r.ms > limite) return { t, v: 'tle', ms: r.ms };
      const d = compara(esperada, r.salida);
      return d.igual ? { t, v: 'ac', ms: r.ms } : { t, v: d.pe ? 'pe' : 'wa', ms: r.ms, dif: d };
    }

    veredicto(v, texto) { return h('div', { class: 'dj-ver dj-' + v }, texto); }

    pintar(filas, final) {
      const total = this.m.tests.length;
      const ok = filas.filter(f => f.v === 'ac').length;
      const hechas = filas.filter(f => f.v !== 'skip').length;
      const mal = filas.find(f => f.v !== 'ac' && f.v !== 'skip');
      let cab;
      if (final && !mal) cab = this.veredicto('ac', `${SIGLAS.ac} · Correcto · ${ok}/${total} pruebas`);
      else if (mal && final) cab = this.veredicto(mal.v, `${SIGLAS[mal.v]} · ${NOMBRES[mal.v]} · ${ok}/${total} pruebas`);
      else cab = this.veredicto('run', `En curso · ${ok}/${hechas} bien`);
      const lista = h('ul', { class: 'dj-tests' }, filas.map((f, i) => {
        const li = h('li', { class: 'dj-' + f.v },
          h('span', { class: 'dj-pill', title: NOMBRES[f.v] }, SIGLAS[f.v]),
          h('b', {}, `Prueba ${f.t.n || i + 1}`), f.t.nombre ? ' · ' + f.t.nombre : '',
          f.t.tipo ? h('span', { class: 'dj-tipo' }, f.t.tipo) : null,
          h('span', { class: 'dj-ms' }, f.v === 'skip' ? '' : f.ms + ' ms'));
        if (f.v === 'wa' || f.v === 'pe') {
          li.append(h('div', { class: 'dj-dif' },
            `Primera diferencia en la línea ${f.dif.linea} de ${f.dif.total}` + ((f.t.casos || 0) > 1 && f.dif.linea > 1 ? ` (las ${f.dif.linea - 1} primeras están bien)` : '') + ':',
            h('div', {}, h('span', {}, 'esperado '), h('code', {}, corta(f.dif.esperada))),
            h('div', {}, h('span', {}, 'tu salida '), h('code', {}, corta(f.dif.obtenida)))));
        } else if (f.v === 'rte' || f.v === 'mle' || f.v === 'ole') {
          li.append(h('div', { class: 'dj-dif' }, f.detalle || QUE_ES[f.v]));
        } else if (f.v === 'tle') {
          li.append(h('div', { class: 'dj-dif' }, `Pasó del límite de ${this.m.limite_ms || 3000} ms.`));
        }
        if (f.t.comprueba && f.v !== 'ac' && f.v !== 'skip') li.append(h('div', { class: 'dj-que' }, 'Qué comprueba: ' + f.t.comprueba));
        return li;
      }));
      const partes = [cab];
      if (final && mal) partes.push(this.guia(filas));
      partes.push(lista);
      this.res.replaceChildren(...partes);
    }

    // ---------- guía: de dónde viene el fallo ----------
    diagnostico(filas) {
      const malas = filas.filter(f => f.v !== 'ac' && f.v !== 'skip');
      const ok = filas.filter(f => f.v === 'ac');
      const notas = [];
      let clave = null;
      const veredictos = new Set(malas.map(f => f.v));
      // 1) Todo PE: los datos están bien
      if (malas.length && malas.every(f => f.v === 'pe')) {
        clave = malas[0];
        notas.push('Tus resultados son correctos: solo falla el formato. Compara carácter a carácter tu salida con la esperada (espacios entre números, un salto de línea por caso, nada de texto extra como «Resultado:»).');
        return { clave, notas };
      }
      // 2) Estado que se arrastra entre casos: aciertan las pruebas de un caso y en las de varios
      //    los primeros casos salen bien pero luego no.
      const multi = malas.filter(f => (f.v === 'wa') && (f.t.casos || 0) > 1 && f.dif && f.dif.linea > 1);
      const unCasoMal = malas.some(f => (f.t.casos || 0) === 1 && f.t.tipo !== 'rendimiento');
      if (multi.length >= 2 && !unCasoMal) {
        clave = filas.find(f => /varios casos/i.test(f.t.nombre || '') && f.v !== 'ac') || multi[0];
        notas.push(`En ${multi.length} pruebas con varios casos aciertas los primeros y fallas los siguientes, y las pruebas de un solo caso salen bien. Casi seguro hay algo que no se reinicia entre casos (un vector, un contador o un máximo declarado fuera de la función de cada caso).`);
        return { clave, notas };
      }
      // 3) La prueba que mejor explica el fallo
      // Puntuación: tipo de prueba; si falla en un caso posterior al primero, su «trampa» puede no ser la
      // causa (+2); si la prueba no tiene explicación para ese veredicto, explica menos (+3).
      const puntos = f => (PRIORIDAD[f.t.tipo] ?? 3) + (f.dif && f.dif.linea > 1 ? 2 : 0) + ((f.t.si && f.t.si[f.v]) ? 0 : 3);
      const ord = malas.slice().sort((a, b) => puntos(a) - puntos(b) || (a.t.n - b.t.n));
      clave = ord[0];
      const especifica = !!(clave && clave.t.si && clave.t.si[clave.v]);
      const enun = filas.filter(f => f.t.tipo === 'enunciado');
      const rend = filas.filter(f => f.t.tipo === 'rendimiento');
      const soloRend = rend.length && malas.length && malas.every(f => f.t.tipo === 'rendimiento');
      if (enun.length && enun.every(f => f.v === 'ac') && malas.length && !soloRend) notas.push('Los ejemplos del enunciado salen bien: la idea es buena y falla en casos especiales.');
      if (soloRend) {
        notas.push('Todas las pruebas pequeñas salen bien y solo fallan las grandes: el algoritmo es correcto pero no es eficiente (o gasta demasiada memoria). Fíjate en el coste: ¿repites trabajo?, ¿copias estructuras grandes al llamar a funciones?');
        clave = ord[0];
      }
      if (clave && clave.dif && !especifica) {
        if (clave.dif.obtenida == null) notas.push(`Tu salida tiene menos líneas de las esperadas (${clave.dif.lineas_tuyas ?? '?'} de ${clave.dif.total}): ¿te saltas casos o el programa termina antes de tiempo?`);
        else if (clave.dif.esperada == null) notas.push('Escribes líneas de más: quita mensajes de depuración o texto que no pide el enunciado.');
        else {
          const ne = (clave.dif.esperada.match(/-?\d+/g) || []).map(Number), no = (clave.dif.obtenida.match(/-?\d+/g) || []).map(Number);
          if (ne.length === no.length && ne.length > 1 && ne.slice().sort().join() === no.slice().sort().join()) notas.push('Escribes los números correctos pero en otro orden.');
          else if (ne.length === no.length && ne.length && ne.every((x, i) => Math.abs(x - no[i]) <= 1) && ne.some((x, i) => x !== no[i])) notas.push('Te diferencias en una unidad: revisa los límites de los bucles (< o ≤) y por dónde empiezas a contar.');
        }
      }
      if (veredictos.has('rte') && !notas.length) notas.push('Un error de ejecución en C++ suele ser un índice fuera del vector, un puntero sin memoria o una pila de llamadas infinita.');
      return { clave, notas };
    }

    guia(filas) {
      const { clave, notas } = this.diagnostico(filas);
      const caja = h('div', { class: 'dj-guia' });
      caja.append(h('b', { class: 'dj-guia-t' }, 'Dónde falla'));
      if (clave) {
        caja.append(h('p', {}, h('b', {}, `${SIGLAS[clave.v]} en la prueba ${clave.t.n} · ${clave.t.nombre || ''}. `), QUE_ES[clave.v] || ''));
        if (clave.t.comprueba) caja.append(h('p', {}, 'Esta prueba comprueba: ' + clave.t.comprueba));
        const si = clave.t.si && (clave.t.si[clave.v] || clave.t.si.wa);
        if (si && clave.v !== 'pe') caja.append(h('p', { class: 'dj-guia-si' }, si));
      }
      for (const n of notas) caja.append(h('p', {}, n));
      // Pistas: de menos a más; al final, la entrada de la prueba si es pequeña.
      const pistas = ((clave && clave.t.pistas) || []).slice();
      const verEntrada = clave && clave.t.bytes != null && clave.t.bytes <= 3000;
      if (pistas.length || verEntrada) {
        const zona = h('div', { class: 'dj-pistas' });
        let dadas = 0;
        const btn = h('button', { class: 'btn', type: 'button' }, 'Dame una pista');
        btn.onclick = async () => {
          if (dadas < pistas.length) {
            zona.append(h('p', { class: 'dj-pista' }, h('b', {}, `Pista ${dadas + 1}: `), pistas[dadas]));
            dadas++;
          } else if (verEntrada) {
            const [ent, sal] = await Promise.all([this.texto(clave.t.in), this.texto(clave.t.out)]);
            zona.append(h('div', { class: 'dj-pista' }, h('b', {}, 'Entrada de la prueba:'), h('pre', { class: 'dj-log' }, ent),
                                                    h('b', {}, 'Salida esperada:'), h('pre', { class: 'dj-log' }, sal)));
            dadas++;
          }
          const quedan = pistas.length - dadas + (verEntrada && dadas <= pistas.length ? 1 : 0);
          if (quedan <= 0) btn.remove();
          else btn.textContent = dadas < pistas.length ? 'Otra pista' : 'Ver la entrada de esta prueba';
        };
        caja.append(zona, h('div', { class: 'dj-bar' }, btn));
      }
      return caja;
    }

    pintarCE(log) {
      const notas = [];
      const reglas = [
        [/was not declared in this scope/, 'Usas algo que no está declarado: una variable con otro nombre, una función que no existe o te falta un #include (por ejemplo <vector>, <string> o <algorithm>).'],
        [/expected [^\n]*['‘];['’]/, 'Falta un punto y coma (;) en la línea que indica o en la anterior.'],
        [/expected ['‘]?\}['’]? at end of input|expected declaration/, 'Hay una llave { sin cerrar: cuenta las llaves de tus funciones.'],
        [/no matching function for call/, 'Llamas a una función con argumentos de tipo o número distinto al que espera.'],
        [/undefined reference to [`'‘]main/, 'Falta la función main: usa la plantilla del ejercicio completa.'],
        [/No such file or directory/, 'Un #include que no existe en el juez: usa solo cabeceras estándar y las del ejercicio.'],
        [/Rechazado antes de compilar/, 'El juez no permite esa llamada o cabecera (crear procesos, ficheros del sistema, red...). Ningún ejercicio la necesita.'],
        [/conversion from .* to non-scalar|cannot convert/, 'Mezclas tipos que no son compatibles (por ejemplo, asignar un vector a un int).'],
      ];
      for (const [rx, t] of reglas) if (rx.test(log)) notas.push(t);
      const lin = (log.match(/main\.cpp:(\d+):/) || [])[1];
      const caja = h('div', { class: 'dj-guia' }, h('b', { class: 'dj-guia-t' }, 'Dónde falla'),
        h('p', {}, QUE_ES.ce + (lin ? ` El primer error está en la línea ${lin}.` : '')), ...notas.map(n => h('p', {}, n)));
      this.res.replaceChildren(this.veredicto('ce', 'CE · No compila'), caja, h('pre', { class: 'dj-log' }, log));
    }
  }

  window.DAJuez = {
    mount(el, cfg) { const j = new Juez(el, cfg); j.arrancar().catch(e => { el.textContent = 'No se pudo cargar el juez: ' + e.message; }); return j; },
    compara,
  };
})();
