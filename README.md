---

## Reproducibilidad del Experimento (Integrante 3)

* **Lenguaje y versión:** Python 3.10+ (librerías estándar: `random`, `time`, `csv`, `json`, `statistics`).
* **Semilla fija utilizada:** `SEMILLA = 42`
* **Diseño experimental:** 6 tamaños de entrada duplicados (`500, 1000, 2000, 4000, 8000, 16000`), 5 repeticiones por tamaño, valores en el rango `[-100, 100]`.
* **Comando exacto para ejecutar el experimento:**
  ```bash
  python src/audrithm/experiment.py
