/* Motor de diagnóstico del juez de DA: a partir de los resultados de cada prueba decide cuál explica
   mejor el fallo y qué patrones se ven. Lo usan la web (juez.js) y el verificador (juez/verificar.py,
   con node), así que lo que se comprueba es exactamente lo que verá el alumno.
   filas: [{ t: {n, nombre, tipo, casos, si, pistas, ...}, v: 'ac'|'wa'|..., dif?: {...} }]
   Devuelve { clave: fila | null, notas: [texto] }. */
(function (raiz) {
  // Orden en que se busca la prueba que mejor explica el fallo: las pensadas para un error concreto primero.
  const PRIORIDAD = { trampa: 0, borde: 1, enunciado: 2, aleatorio: 3, rendimiento: 4 };

  function diagnostico(filas) {
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
      //    No vale si alguna prueba ya falla en su primera línea: entonces el fallo no depende de lo anterior.
      const multi = malas.filter(f => f.v === 'wa' && f.t.tipo !== 'rendimiento' && (f.t.casos || 0) > 1 && f.dif && f.dif.linea > 1);
      const unCasoMal = malas.some(f => (f.t.casos || 0) === 1 && f.t.tipo !== 'rendimiento');
      const fallaAlPrincipio = malas.some(f => f.t.tipo !== 'rendimiento' && (f.v === 'wa' || f.v === 'pe') && f.dif && f.dif.linea === 1);
      if (multi.length >= 2 && !unCasoMal && !fallaAlPrincipio) {
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
      const soloRend = rend.length && malas.length && malas.every(f => f.t.tipo === 'rendimiento' && (f.v === 'tle' || f.v === 'mle'));
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
      if (malas.length > 1 && malas.every(f => f.v === 'ole')) notas.push('Todas las pruebas escriben demasiado: casi seguro hay un bucle que no termina y escribe en cada vuelta (o lees mal la entrada y el bucle de casos no para).');
      if (veredictos.has('rte') && !notas.length) notas.push('Un error de ejecución en C++ suele ser un índice fuera del vector, un puntero sin memoria o una pila de llamadas infinita.');
      return { clave, notas };
    }

  const api = { diagnostico, PRIORIDAD };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else raiz.DAJuezDiag = api;
})(typeof window !== 'undefined' ? window : globalThis);
