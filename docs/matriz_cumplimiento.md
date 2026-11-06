# Matriz de cumplimiento · Bitácora 1 · Equipo 5

Referencia de aceptación disponible: PDF académico «Asignación de proyectos por equipo y Bitácora 1», Profa. Msc. Sosa, Cohorte X, 2026-III, suministrado por el usuario. No se recibió una imagen adicional distinta del PDF. La solicitud de desarrollo está archivada en user_request.txt y no reemplaza los criterios académicos. Esta matriz puede evaluarse sin abrir la web.

Estados: **completo** = artefacto técnico y evidencia verificable disponibles; **parcial** = existe material verificable pero falta validación académica o declaración humana; **pendiente** = falta el entregable o su aprobación. La presencia de una pantalla no cuenta como evidencia. Todos los archivos indicados son relativos a la raíz del repositorio.

## 1. Problema y especificación

- Archivo: docs/specification.md; src/audrithm/algorithms.py.
- Respaldo: Result, _validate, kadane y brute_force; precondición n>=1, postcondición de máximo contiguo no vacío, índices inclusivos, desempate, ValueError para vacío, TypeError para otros tipos y no mutación.
- Evidencia: tests/test_algorithms.py::test_cases, test_empty, test_invalid y test_sum_and_trace; salida y conteos reales en results/qa_results.json.
- Estado: **completo** técnicamente.
- Validación humana: comprobar que el contrato y el desempate corresponden a la interpretación acordada por el equipo.

## 2. Demostración de corrección

- Archivo: docs/correctness.md; sección 2 del PDF y de docs/bitacora1.md.
- Respaldo: invariante formal con E(i), G(i), cuantificadores, sumatorias e índices; inicialización, mantenimiento, terminación, variante decreciente y argumento para fuerza bruta.
- Evidencia: argumento escrito enlazado con variables reales de kadane; tests/test_differential.py::test_exhaustive_independent_oracle contrasta 1092 arreglos pequeños con un oráculo independiente. Las pruebas finitas **no sustituyen** la demostración.
- Estado: **parcial**: propuesta asistida por IA, no demostración validada por estudiantes.
- Validación humana: reconstruir y verificar cada paso, empates y caso n=1; registrar revisor y fecha. La referencia académica prohíbe delegar la demostración.

## 3. Análisis de costo

- Archivo: docs/complexity.md; docstrings y bucles de src/audrithm/algorithms.py.
- Respaldo: operaciones dominantes K(n)=n-1 y B(n)=Σ(n-l)=n(n+1)/2. Cota K: n/2 <= K(n) <= n para n>=2 (c=1 para O(n), n0=2); cota B: n²/2 <= B(n) <= n² para n>=1 (c=1 para O(n²), n0=1). Las constantes se aplican al conteo definido, no al tiempo de pared completo.
- Evidencia: código con una pasada o dos bucles acumulativos; columna operations en results/experiment_results.csv; mejor, peor y esperanza bajo modelo RAM y valores acotados explícitos. Se documenta memoria auxiliar y salida.
- Estado: **completo** técnicamente; revisión formal pendiente.
- Validación humana: revisar el modelo de costo, el alcance de las constantes, sumatorias y supuesto sobre enteros y caso promedio.

## 4. Implementación y pruebas

- Archivo: src/audrithm/algorithms.py; tests/test_algorithms.py; tests/test_differential.py; tests/test_experiment.py; src/audrithm/qa.py.
- Respaldo: casos parametrizados, comparación diferencial de 500 arreglos con semilla fija, oráculo exhaustivo, no mutación, traza, validación de límites, exportación, medianas y razones.
- Evidencia: results/qa_results.json contiene conteos, salida real, duración, fecha UTC, commit disponible y hash fuente; .github/workflows/tests.yml automatiza QA. El número final debe leerse del JSON regenerado, no inferirse de esta matriz. La ejecución remota de Actions requiere confirmación en GitHub.
- Estado: **completo** localmente; CI remota se verifica por separado.
- Validación humana: reproducir pytest, examinar fallos si aparecen y registrar revisión del integrante 2. No se afirma cobertura.

## 5. Experimento reproducible

- Archivo: src/audrithm/experiment.py::run_experiment y save_results; run_pipeline.py; docs/experiment.md.
- Respaldo: seis tamaños 100,200,400,800,1600,3200; cinco repeticiones; semilla 20261105; entradas pareadas; orden alternado; generación previa; perf_counter_ns; mediana y presupuesto temporal.
- Evidencia: results/experiment_results.csv (60 filas medidas), results/experiment_metadata.json (entorno, versiones, fecha, reloj, semilla, commit/hash), results/summary.csv, results/timing_normal.png y results/timing_loglog.png. Tabla y gráficas incluidas en el PDF generado. Conteos deterministas complementan tiempos cortos.
- Estado: **completo** con datos locales reales.
- Validación humana: repetir pipeline en el entorno del equipo, comprobar CSV/metadatos, revisar ruido y confirmar que el rango de tamaños es adecuado para la entrega. Los tiempos no tienen por qué repetirse exactamente.

## 6. Contraste y conclusión

- Archivo: docs/analysis.md; src/audrithm/visualization.py::summary y chart; sección 6 del PDF.
- Respaldo: medianas reales, razones T(2n)/T(n) solo entre tamaños duplicados, escalas normal y log-log, predicciones 2 y 4 con sus límites. Se distingue explícitamente observación empírica de demostración asintótica.
- Evidencia: results/summary.csv y ambas figuras derivadas del CSV; advertencias de ruido, reloj, calentamiento y costo de contrato/salida.
- Estado: **parcial**: evidencia disponible; conclusión crítica final pendiente del equipo.
- Validación humana: interpretar cifras y discrepancias reales, redactar una conclusión acotada al rango medido y justificar la expresión «consistente con» si corresponde. No aprobar una frase automática solo porque existe una gráfica.

## 7. Registro de uso de IA

- Archivo: docs/ai_usage.md; docs/user_request.txt; docs/team_contributions.md; declaraciones de borrador en el reporte.
- Respaldo: herramienta/modelo disponible, fecha, solicitud íntegra, salidas relevantes, verificaciones, descartes y limitaciones de identificación de versión. Afirmación concreta a contrastar: ejemplo suma 6 y equivalencia del desempate.
- Evidencia: pruebas del ejemplo, comparación diferencial y oráculo independiente; resultados QA fechados. Implementación etiquetada como referencia asistida por IA; no se atribuyen aportes a integrantes.
- Estado: **parcial**: registro técnico preparado; declaración tecnológica individual/colectiva y revisiones reales pendientes.
- Validación humana: confirmar/refutar independientemente las afirmaciones registradas y completar responsables, fechas y declaración Ámbar según la pauta; demostrar comprensión propia del argumento y redactar juicio crítico.

## 8. Reproducibilidad

- Archivo: README.md; requirements.txt; run_pipeline.py; scripts/build_report.py; docs/reproducibility.md; .github/workflows/tests.yml.
- Respaldo: comandos exactos PowerShell/Linux, dependencias directas fijadas, semillas, pipeline que se detiene ante QA fallida y exporta evidencia; seis vistas integradas con módulos puros.
- Evidencia local verificada: `python scripts/check_app.py` ejecutado con éxito en 2026-11-06 y `python -m pytest tests -q` con 44 pruebas pasando. Ambos resultados son evidencia local real del repositorio. `results/app_check.json` refleja la ejecución local y no la publicación pública.
- Estado: **parcial** para despliegue real; **completo** para validación local de la app y de la regresión del laboratorio. La publicación web complementaria no reemplaza la entrega ni se declara verificada sin URL pública operativa.
- Validación humana: instalar desde cero, ejecutar comandos, comprobar artefactos y commit final; completar integrantes, aprobar informe, declaración y presentación de 15 minutos. Autenticación de Streamlit Community Cloud requiere al propietario y la publicación real sigue pendiente de verificación directa.

## 9. Mejora de sesión y comprobación local

- Archivo: app.py; scripts/check_app.py.
- Respaldo: el último análisis se conserva en `session_state`, la entrada y los algoritmos quedan visibles al volver a la vista Algoritmos, la entrada utilizada queda identificada en el resultado, la app advierte si cambia el arreglo y existe una opción para limpiar el análisis almacenado.
- Evidencia local verificada: ejecución real de `python scripts/check_app.py` (seis vistas, persistencia, advertencia y limpieza) con salida `OK: Inicio`, `OK: Algoritmos`, `OK: Pruebas QA`, `OK: Experimentos`, `OK: Resultados`, `OK: Reporte`.
- Estado: **completo** localmente; **pendiente** para la publicación real en entorno público.
- Validación humana: comprobar la experiencia en navegador real y distinguir siempre la validación local de la publicación operativa.

## Condición de cierre académico

No está aprobada la entrega definitiva mientras los requisitos 2, 6, 7 y 8 permanezcan parciales. La matriz documenta lo realizado y lo pendiente sin sustituir la evaluación de la profesora. El reporte y la matriz deben regenerarse o revisarse cuando cambien el código, los resultados o la aprobación humana.
