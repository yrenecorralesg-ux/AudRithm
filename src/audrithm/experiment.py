import random
import time
import csv
import json
import statistics

# Parametros de reproducibilidad del experimento
SEMILLA = 42
TAMANOS = [500, 1000, 2000, 4000, 8000, 16000]  # 6 tamaños duplicandose (n -> 2n)
REPETICIONES = 5
RANGO_MIN = -100
RANGO_MAX = 100

# Implementacion de referencia de las dos versiones a contrastar
# (Si el equipo las tiene en otro modulo, basta con importarlas arriba)
def subarreglo_fuerza_bruta(arr):
    """Versión cuadratica O(n^2): evalua todas las sumas posibles de subarreglos."""
    n = len(arr)
    mejor_global = arr[0]
    for i in range(n):
        suma_actual = 0
        for j in range(i, n):
            suma_actual += arr[j]
            if suma_actual > mejor_global:
                mejor_global = suma_actual
    return mejor_global


def subarreglo_lineal(arr):
    """Version lineal O(n) (Kadane): mantiene el mejor local y el mejor global."""
    mejor_actual = arr[0]
    mejor_global = arr[0]
    for i in range(1, len(arr)):
        # Invariante: mejor subarreglo que termina exactamente en la posición i
        if mejor_actual + arr[i] > arr[i]:
            mejor_actual = mejor_actual + arr[i]
        else:
            mejor_actual = arr[i]

        # Invariante: mejor subarreglo visto hasta ahora en todo el recorrido
        if mejor_actual > mejor_global:
            mejor_global = mejor_actual
    return mejor_global


def generar_arreglo(tamano):
    """Genera un arreglo aleatorio con valores negativos y positivos."""
    return [random.randint(RANGO_MIN, RANGO_MAX) for _ in range(tamano)]


def ejecutar_experimento():
    # Fijamos la semilla al inicio para garantizar reproducibilidad exacta
    random.seed(SEMILLA)

    registros_crudos = []
    resumen_por_tamano = []

    promedios_lineal = []
    promedios_bruta = []

    print(f"Iniciando experimento con SEMILLA = {SEMILLA}")
    print("-" * 75)
    print(f"{'n':>7} | {'T. Lineal (ms)':>15} | {'Razón Lin.':>10} | {'T. Bruta (ms)':>15} | {'Razón Bruta':>11}")
    print("-" * 75)

    for idx, n in enumerate(TAMANOS):
        tiempos_lineal = []
        tiempos_bruta = []

        for rep in range(1, REPETICIONES + 1):
            # Se usa el mismo arreglo de entrada para medir ambos algoritmos en igualdad de condiciones
            datos = generar_arreglo(n)

            # 1. Medicion version lineal O(n)
            inicio_lin = time.perf_counter()
            res_lin = subarreglo_lineal(datos)
            fin_lin = time.perf_counter()
            t_lin_ms = (fin_lin - inicio_lin) * 1000.0
            tiempos_lineal.append(t_lin_ms)

            # 2. Medicion version fuerza bruta O(n^2)
            inicio_bru = time.perf_counter()
            res_bru = subarreglo_fuerza_bruta(datos)
            fin_bru = time.perf_counter()
            t_bru_ms = (fin_bru - inicio_bru) * 1000.0
            tiempos_bruta.append(t_bru_ms)

            # Verificacion de sanidad: ambos algoritmos deben dar exactamente la misma suma maxima
            assert res_lin == res_bru, f"Discrepancia detectada en n={n}, rep={rep}"

            registros_crudos.append({
                "n": n,
                "repeticion": rep,
                "tiempo_lineal_ms": round(t_lin_ms, 6),
                "tiempo_fuerza_bruta_ms": round(t_bru_ms, 6),
                "suma_maxima_obtenida": res_lin
            })

        # Calculo de promedios de las 5 repeticiones
        prom_lin = statistics.mean(tiempos_lineal)
        prom_bru = statistics.mean(tiempos_bruta)
        promedios_lineal.append(prom_lin)
        promedios_bruta.append(prom_bru)

        # Calculo de la razón empirica T(2n) / T(n) exigida en la guia
        if idx == 0:
            razon_lin_str = "-"
            razon_bru_str = "-"
            razon_lin_val = None
            razon_bru_val = None
        else:
            razon_lin_val = round(prom_lin / promedios_lineal[idx - 1], 2)
            razon_bru_val = round(prom_bru / promedios_bruta[idx - 1], 2)
            razon_lin_str = f"{razon_lin_val:.2f}"
            razon_bru_str = f"{razon_bru_val:.2f}"

        resumen_por_tamano.append({
            "n": n,
            "promedio_lineal_ms": round(prom_lin, 6),
            "razon_T2n_Tn_lineal": razon_lin_val,
            "promedio_fuerza_bruta_ms": round(prom_bru, 6),
            "razon_T2n_Tn_fuerza_bruta": razon_bru_val
        })

        print(f"{n:>7} | {prom_lin:>15.4f} | {razon_lin_str:>10} | {prom_bru:>15.4f} | {razon_bru_str:>11}")

    # Exportar todas las corridas individuales (30 mediciones) a CSV
    with open("resultados_experimento.csv", mode="w", newline="", encoding="utf-8") as archivo_csv:
        columnas = ["n", "repeticion", "tiempo_lineal_ms", "tiempo_fuerza_bruta_ms", "suma_maxima_obtenida"]
        escritor = csv.DictWriter(archivo_csv, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(registros_crudos)

    # Exportar tabla resumen con promedios y razon T(2n)/T(n) lista para el informe y graficas
    with open("resumen_tiempos.csv", mode="w", newline="", encoding="utf-8") as archivo_resumen:
        columnas_res = ["n", "promedio_lineal_ms", "razon_T2n_Tn_lineal", "promedio_fuerza_bruta_ms", "razon_T2n_Tn_fuerza_bruta"]
        escritor_res = csv.DictWriter(archivo_resumen, fieldnames=columnas_res)
        escritor_res.writeheader()
        escritor_res.writerows(resumen_por_tamano)

    # Exportar tambien en JSON por respaldo
    salida_json = {
        "semilla": SEMILLA,
        "repeticiones_por_tamano": REPETICIONES,
        "rango_valores": [RANGO_MIN, RANGO_MAX],
        "resumen": resumen_por_tamano,
        "mediciones_detalladas": registros_crudos
    }
    with open("resultados_experimento.json", mode="w", encoding="utf-8") as archivo_json:
        json.dump(salida_json, archivo_json, indent=2)

    print("-" * 75)
    print("Archivos generados: resultados_experimento.csv, resumen_tiempos.csv y resultados_experimento.json")


if __name__ == "__main__":
    ejecutar_experimento()
