/* Juez de la web de DA: componente independiente.
   Uso:  DAJuez.mount(elemento, { manifest: '04-3/manifest.json', wasmBase: 'https://…/' })
   Encaja donde se quiera (pestaña «Probar» o página propia): solo necesita un <div>. */
(function () {
  const AQUI = (document.currentScript && document.currentScript.src) || location.href;
  const RUTA_WORKER = new URL('juez-worker.js', AQUI).href;
  const WASM_BASE = 'https://binji.github.io/wasm-clang/';

  const NOMBRES = {
    ac: 'Correcto', wa: 'Respuesta incorrecta', ce: 'Error de compilación',
    tle: 'Tiempo excedido', rte: 'Error de ejecución', skip: 'No ejecutada',
  };

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
      if (a[i] !== b[i]) return { igual: false, linea: i + 1, esperada: a[i], obtenida: b[i], total: a.length };
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
      try {
        this.msg('Enviando al servidor del juez…');
        const resp = await fetch(this.cfg.servidor.replace(/\/$/, '') + '/juzgar', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ id: this.m.id, codigo: this.ta.value }),
        });
        r = await resp.json();
        if (!resp.ok) {              // límites (429/503/413): se informa, no se cae al navegador
          this.msg('');
          this.res.replaceChildren(h('div', { class: 'dj-err' }, r.error || ('Error ' + resp.status)));
          this.ocupado = false; this.btn.disabled = false;
          return;
        }
      } catch (e) {                  // servidor apagado o sin conexión: respaldo en el navegador
        this.ocupado = false; this.btn.disabled = false;
        this.msg('El servidor del juez no responde; se usa el compilador del navegador…');
        return this.comprobarWasm();
      }
      this.msg('');
      try {
        if (r.error) this.res.replaceChildren(h('div', { class: 'dj-err' }, r.error));
        else if (r.veredicto === 'ce' && !r.tests) this.res.replaceChildren(this.veredicto('ce', 'No compila'), h('pre', { class: 'dj-log' }, r.log || ''));
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
          this.res.replaceChildren(this.veredicto('ce', 'No compila'), h('pre', { class: 'dj-log' }, c.log));
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
      return d.igual ? { t, v: 'ac', ms: r.ms } : { t, v: 'wa', ms: r.ms, dif: d };
    }

    veredicto(v, texto) { return h('div', { class: 'dj-ver dj-' + v }, texto); }

    pintar(filas, final) {
      const total = this.m.tests.length;
      const ok = filas.filter(f => f.v === 'ac').length;
      const hechas = filas.filter(f => f.v !== 'skip').length;
      const mal = filas.find(f => f.v !== 'ac' && f.v !== 'skip');
      let cab;
      if (final && !mal) cab = this.veredicto('ac', `Correcto · ${ok}/${total} pruebas`);
      else if (mal && final) cab = this.veredicto(mal.v, `${NOMBRES[mal.v]} · ${ok}/${total} pruebas`);
      else cab = this.veredicto('run', `En curso · ${ok}/${hechas} bien`);
      const lista = h('ul', { class: 'dj-tests' }, filas.map((f, i) => {
        const li = h('li', { class: 'dj-' + f.v },
          h('span', { class: 'dj-pill' }, NOMBRES[f.v]),
          h('b', {}, `Prueba ${i + 1}`), f.t.nombre ? ' · ' + f.t.nombre : '',
          h('span', { class: 'dj-ms' }, f.ms + ' ms'));
        if (f.v === 'wa') {
          li.append(h('div', { class: 'dj-dif' },
            `Primera diferencia en la línea ${f.dif.linea} de ${f.dif.total}:`,
            h('div', {}, h('span', {}, 'esperado '), h('code', {}, corta(f.dif.esperada))),
            h('div', {}, h('span', {}, 'tu salida '), h('code', {}, corta(f.dif.obtenida)))));
        } else if (f.v === 'rte') {
          li.append(h('div', { class: 'dj-dif' }, f.detalle));
        } else if (f.v === 'tle') {
          li.append(h('div', { class: 'dj-dif' }, `Pasó del límite de ${this.m.limite_ms || 3000} ms (en este navegador; el juez de la asignatura puede ir más rápido).`));
        }
        return li;
      }));
      this.res.replaceChildren(cab, lista);
    }
  }

  window.DAJuez = {
    mount(el, cfg) { const j = new Juez(el, cfg); j.arrancar().catch(e => { el.textContent = 'No se pudo cargar el juez: ' + e.message; }); return j; },
    compara,
  };
})();
