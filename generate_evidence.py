import pandas as pd
from pathlib import Path
from src.audrithm.visualization import save_operations_analysis

def generar_archivos_pr():
    # Busca el CSV real en la carpeta results
    resultados_dir = Path("results")
    archivos_csv = list(resultados_dir.glob("*.csv"))
    
    if not archivos_csv:
        print(" No se encontró ningún CSV en la carpeta results/ para analizar.")
        return
        
    # Usa el primer CSV de resultados que encuentre
    csv_real = archivos_csv[0]
    print(f"Procesando evidencia desde: {csv_real}")
    
    df = pd.read_csv(csv_real)
    save_operations_analysis(df, resultados_dir)
    print(f" Evidencia generada en la carpeta {resultados_dir}: 'operations_growth.png' y 'operations_summary.csv'")

if __name__ == "__main__":
    generar_archivos_pr()