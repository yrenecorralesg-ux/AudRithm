# AudRithm · Laboratorio de Análisis de Algoritmos

Aplicación académica real en español para la Bitácora 1 del equipo 5: subarreglo de suma máxima, Kadane Θ(n) frente a fuerza bruta Θ(n²). Implementación de referencia asistida por IA, pendiente de aportes, revisión y aprobación del equipo. La web complementa el informe obligatorio.

## Requisitos e instalación

Python 3.11 o 3.13. Entorno de medición inicial: Python 3.13.3 en Windows; versiones efectivas y plataforma en results/experiment_metadata.json. Git para publicar. Dependencias directas fijadas en requirements.txt; no se requieren cuentas para usar el laboratorio.

PowerShell, desde la carpeta raíz de este repositorio:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe run_pipeline.py
.\.venv\Scripts\python.exe scripts/build_report.py
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Linux/macOS (también se admite Python 3.11):

```bash
python3.13 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest tests -q
.venv/bin/python run_pipeline.py
.venv/bin/python scripts/build_report.py
.venv/bin/python -m streamlit run app.py
```

No hace falta activar el entorno ni cambiar la política de ejecución de PowerShell. `python run_pipeline.py --qa-only` genera únicamente evidencia QA. El pipeline completo detiene la ejecución al fallar QA, mide, exporta y genera gráficas. No inicia Streamlit ni ejecuta experimentos al abrir la web.

requirements-lock.txt registra el entorno Windows/Python 3.13 observado, incluidas herramientas de inspección. Para despliegue o Python 3.11 usar requirements.txt: el resolvedor elegirá dependencias transitivas compatibles (por ejemplo, una versión de NumPy compatible con Python 3.11).

La comprobación funcional adicional se ejecuta con `python scripts/check_app.py` (seis vistas y ejemplo real). En entornos de desarrollo empaquetados que activen `global.developmentMode`, añadir `--global.developmentMode false` al comando de Streamlit si se configura un puerto explícito.

## Arquitectura y estructura

- app.py: seis vistas mediante navegación lateral, sin pantalla adicional.
- src/audrithm/algorithms.py: funciones puras, contrato, desempate y traza.
- experiment.py: mediciones pareadas, límite de tamaño y presupuesto temporal.
- qa.py: suite fija de Pytest con timeout y evidencia JSON.
- visualization.py: Pandas, medianas, razones y Matplotlib.
- reporting.py y docs/: ocho secciones académicas, transparencia y responsabilidades.
- tests/: casos, oráculo independiente exhaustivo y comparación diferencial.
- run_pipeline.py: orquestación CLI sin interfaz.
- scripts/build_report.py: PDF borrador con evidencia real.
- results/: CSV, metadatos JSON, evidencia QA, tabla y PNG de ambas escalas.
- output/pdf/: Equipo_5_Bitacora1.pdf (borrador para revisión).
- .github/workflows/tests.yml: QA en push y pull request sobre Python 3.11/3.13.

## Contrato y validación

Entrada no vacía de int de Python (sin bool); vacío produce ValueError. Índices inclusivos desde cero; desempate por menor inicio y después menor fin. Ambos motores mantienen la entrada intacta y devuelven suma, índices y tupla del subarreglo. Incluye función max_sum. El límite web es 1000 elementos de hasta diez dígitos y no se utiliza eval. La fuerza bruta usa exactamente dos bucles y suma acumulada.

## Experimentos e interpretación

Semilla 20261105; seis tamaños duplicados de 100 a 3200; cinco repeticiones por algoritmo, 60 observaciones. Entradas generadas antes de medir, compartidas en cada par, orden alternado y calentamiento previo. perf_counter_ns mide únicamente la llamada del motor. CSV incluye algoritmo, tamaño, repetición, semilla, tiempo en ns, orden y conteo dominante. Exportación y gráficos quedan fuera del cronometraje.

summary.csv contiene medianas en ns y razones únicamente entre tamaños duplicados. Las gráficas muestran ms. Las razones ideales 2 y 4 son orientativas; ruido, reloj, calentamiento, costo de contrato/salida y entorno influyen. Los conteos n-1 y n(n+1)/2 complementan tiempos cortos. Los experimentos no prueban una cota asintótica. Ver docs/complexity.md para modelo RAM, sumatorias, casos y constantes formales.

Límites: máximo 3200 y cinco repeticiones; presupuesto de 90 s comprobado entre llamadas. No es interrupción dura de una llamada en curso. Los experimentos web son por sesión y no sustituyen el CSV archivado; descargar sus artefactos. Los archivos QA incluyen fecha, commit y hash fuente. No se afirma cobertura ni se inventa estado de validación. El entorno público puede producir otros tiempos.

## Publicación

Repositorio destino: https://github.com/yrenecorralesg-ux/AudRithm

Con el código en la raíz, iniciar sesión como propietario en https://share.streamlit.io/, autorizar GitHub y elegir el repositorio, la rama publicada y app.py. En opciones avanzadas elegir Python 3.13 (o 3.11 y validar CI). Solicitar el subdominio audrithm; si no está disponible, probar audrithm-equipo5. requirements.txt y .streamlit/config.toml están incluidos. No hay secretos ni archivos locales obligatorios fuera del repositorio. Las seis vistas y descargas funcionan con rutas ancladas al proyecto.

Después de publicar: comprobar URL desde una sesión pública, las seis vistas, ejemplo suma 6, QA y descargas. No se declara URL pública hasta verificarla. La autenticación es del propietario; no introducir credenciales en archivos ni commits. Documentación oficial: https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy y https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies (consultadas 2026-11-05).

## Equipo, IA y entrega

docs/team_contributions.md conserva las cinco responsabilidades propuestas, sin atribuir aportes ficticios. El responsable propuesto de algorithms.py es el integrante 1. Los nombres están pendientes. docs/ai_usage.md y docs/user_request.txt registran herramienta, solicitud, verificaciones y descartes. El nivel propuesto de uso tecnológico es Ámbar, sujeto a declaración del equipo. No se implementa agente IA, login ni base de datos.

El PDF de asignación distingue Bitácora 1 (subarreglo) del proyecto integrador del equipo 5 (árbol de expansión mínima). La entrega requiere PDF de 4 a 8 páginas, repositorio o comprimido, declaración tecnológica y presentación. La demostración y conclusión deben ser comprendidas, validadas y defendidas por estudiantes. El borrador no está aprobado ni es definitivo.

La trazabilidad de los ocho requisitos está en docs/matriz_cumplimiento.md y se consulta también desde Reporte. El estado externo verificado, los bloqueos de autenticación y los pasos de publicación están en docs/publication_status.md.
