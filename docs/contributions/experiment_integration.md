# Integración del experimento · 2026-11-06

La versión ac656a8 sustituyó el módulo importado por la aplicación por un script
independiente. Se perdieron ROOT, commit_id, source_hash, run_experiment y
save_results, requeridos por app.py, qa.py, reporting.py y las pruebas.
El síntoma es un ImportError durante el arranque, antes de mostrar las vistas.

Se preservó íntegramente esa versión en experiment_ac656a8.py.txt y en el
historial Git. La corrección recupera la API compartida y los motores puros de
algorithms.py, e integra una entrada ejecutar_experimento que presenta tabla
y exportación sin ejecutar trabajo al importar el módulo.

La tabla usa mediana, según la pauta académica, en lugar del promedio de la
versión independiente. Se mantienen perf_counter_ns, semilla 20261105, orden
alternado, metadatos y límites de 3200 elementos y 90 segundos. La configuración
original de 16000 elementos sin presupuesto no se activa en el hosting.

Ejecución opcional desde la raíz en PowerShell:

    $env:PYTHONPATH = "src"
    python -m audrithm.experiment

El pipeline oficial sigue siendo python run_pipeline.py, que exige QA antes de
medir. Nuevas pruebas protegen los imports del aplicativo y la exportación de
la entrada en español sin ejecutar experimentos pesados durante esas pruebas.
