/* Worker del juez: compila C++ (clang 8 en WebAssembly) y ejecuta el resultado con una entrada.
   Todo ocurre en el navegador del alumno: su código no sale de su equipo. */
self.importScripts('vendor/wasm-clang-shared.js');

let api = null, sink = null, modulo = null;
const ANSI = /\x1b\[[0-9;]*m/g;
// WebAssembly (sin soporte de excepciones): se acepta `throw` al compilar, pero lanzar una excepción
// termina el programa con error de ejecución. Estas funciones se añaden al final del código del alumno.
const STUB_EXC = `
#include <cstdlib>
#include <cstdio>
extern "C" {
void* __cxa_allocate_exception(unsigned long n) { return malloc(n ? n : 1); }
[[noreturn]] void __cxa_throw(void*, void*, void (*)(void*)) { fputs("excepcion lanzada (throw) y no capturada\\n", stderr); abort(); }
void* __cxa_begin_catch(void* p) { return p; }
void __cxa_end_catch() {}
}
// comparaciones de long double (128 bits) que libc++ necesita para std::sort/min/max y no vienen en esta libc
typedef unsigned __int128 u128_;
static inline int q_nan_(u128_ u) { return ((u >> 112) & 0x7fff) == 0x7fff && (u & ((((u128_)1) << 112) - 1)); }
static inline __int128 q_ord_(u128_ u) { u128_ m = u & ~(((u128_)1) << 127); return (u >> 127) ? -(__int128)m : (__int128)m; }
static inline int q_cmp_(long double a, long double b) {
  u128_ x, y; __builtin_memcpy(&x, &a, 16); __builtin_memcpy(&y, &b, 16);
  if (q_nan_(x) || q_nan_(y)) return 2;
  __int128 p = q_ord_(x), q = q_ord_(y);
  return p < q ? -1 : (p > q ? 1 : 0);
}
extern "C" {
int __lttf2(long double a, long double b) { int c = q_cmp_(a, b); return c == 2 ? 1 : c; }
int __letf2(long double a, long double b) { int c = q_cmp_(a, b); return c == 2 ? 1 : c; }
int __eqtf2(long double a, long double b) { int c = q_cmp_(a, b); return c == 2 ? 1 : c; }
int __netf2(long double a, long double b) { int c = q_cmp_(a, b); return c == 2 ? 1 : c; }
int __gttf2(long double a, long double b) { int c = q_cmp_(a, b); return c == 2 ? -1 : c; }
int __getf2(long double a, long double b) { int c = q_cmp_(a, b); return c == 2 ? -1 : c; }
}
`;
const limpia = partes => partes.join('').replace(ANSI, '').replace(/\r/g, '');

async function iniciar({ wasmBase }) {
  const pide = async f => {
    const r = await fetch(wasmBase + f);
    if (!r.ok) throw new Error('No se pudo descargar ' + f + ' (' + r.status + ')');
    return r.arrayBuffer();
  };
  api = new API({
    readBuffer: pide,
    compileStreaming: async f => WebAssembly.compile(await pide(f)),
    hostWrite: s => { if (sink) sink.push(s); },
  });
  await api.ready;
  api.hostLog = () => {};     // sin trazas de la herramienta: solo salida del compilador / del programa
  api.hostWrite = () => {};
}

async function compilar({ codigo, ficheros }) {
  sink = [];
  modulo = null;
  for (const [nombre, texto] of Object.entries(ficheros || {})) api.memfs.addFile(nombre, texto);
  api.memfs.addFile('test.cc', codigo + STUB_EXC);
  try {
    const clang = await api.getModule('clang');
    await api.run(clang, 'clang', '-cc1', '-emit-obj', ...api.clangCommonArgs,
      '-std=c++17', '-DDOMJUDGE', ...(self.EXTRA_FLAGS || ['-fcxx-exceptions', '-fexceptions']), '-O2', '-o', 'test.o', '-x', 'c++', 'test.cc');
    await api.link('test.o', 'test.wasm');
    modulo = await WebAssembly.compile(api.memfs.getFileContents('test.wasm'));
  } catch (e) {
    const log = limpia(sink) || String(e && e.message || e);
    return { ok: false, log };
  }
  return { ok: true, log: limpia(sink) };
}

async function ejecutar({ entrada }) {
  sink = [];
  api.memfs.setStdinStr(entrada);
  const t0 = performance.now();
  let estado = 'ok', detalle = '';
  try {
    await api.run(modulo, 'test.wasm');
  } catch (e) {
    estado = 'rte';
    detalle = String(e && e.message || e);
  }
  const ms = Math.round(performance.now() - t0);
  let salida = limpia(sink);
  if (estado === 'rte') { detalle += ' ' + salida.replace(/Error:[\s\S]*$/, '').trim().slice(0, 300); salida = ''; }
  let recortada = false;
  if (salida.length > 2e6) { salida = salida.slice(0, 2e6); recortada = true; }
  return { estado, detalle, salida, ms, recortada };
}

self.onmessage = async ev => {
  const { id, tipo } = ev.data;
  try {
    let r;
    if (tipo === 'iniciar') r = await iniciar(ev.data);
    else if (tipo === 'compilar') r = await compilar(ev.data);
    else if (tipo === 'ejecutar') r = await ejecutar(ev.data);
    self.postMessage({ id, ok: true, r });
  } catch (e) {
    self.postMessage({ id, ok: false, error: String(e && e.message || e) });
  }
};
