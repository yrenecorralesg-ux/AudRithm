Ejecutar `python -m pytest tests -q` o `python run_pipeline.py --qa-only`. La evidencia medida está en results/qa_results.json con fecha UTC, commit si existe, hash del código fuente y salida capturada; no se afirma cobertura.

La suite contempla positivos, negativos, mixtos, ceros, singleton positivo y negativo, vacíos, repetidos, óptimos al inicio/final/centro y empates. Verifica suma, índices, salida y ausencia de mutación. Se comparan 500 entradas aleatorias de semilla 20261105 y los 1092 arreglos de longitudes 1 a 6 sobre {-1,0,1}, estos últimos también contra un oráculo independiente basado en sumas directas. La traza se contrasta con prefijos y sufijos calculados directamente.

Pytest reporta cada función de prueba y cada instancia parametrizada como un caso. Las dos pruebas diferenciales reportan un caso cada una. En sus bucles internos verifican hasta 1092 arreglos exhaustivos y 500 entradas seudoaleatorias, respectivamente, si completan todas las iteraciones. Esos arreglos no tienen resultados individuales en JUnit y estas cifras no representan un porcentaje de cobertura.

## Contrato de evidencia QA para el integrante 5

`run_qa()` ejecuta la suite fija `tests` con un límite de 45 segundos. El JSON conserva `tests`, `passed`, `failures`, `errors`, `skipped`, `exit_code`, `output`, `duration_s`, `date`, `commit` y `source_sha256`. El campo nuevo `cases` es una lista en el orden del XML JUnit.

| Campo por caso | Tipo | Contenido |
| --- | --- | --- |
| `name` | cadena | `classname::name` de JUnit, o solo `name` si falta la clase. Incluye el identificador de parametrización cuando Pytest lo reporta. |
| `status` | cadena | `passed` (aprobado), `failed` (fallido), `skipped` (omitido) o `error`. |
| `duration_s` | número | Duración en segundos según JUnit. |
| `message` | cadena o `null` | Mensaje JUnit de fallo, error u omisión, con el texto del elemento como respaldo. |

La interfaz debe usar `exit_code == 0` para identificar una ejecución exitosa. Si falla la ejecución y JUnit no registra fallos ni errores, el resumen registra un error a nivel de suite. En ese escenario, `errors` puede incluir un error sin una fila correspondiente en `cases`. Si el XML falta o es ilegible, `cases` queda vacío y el diagnóstico aparece en `output`. Los archivos generados antes de este cambio pueden carecer de `cases`.
