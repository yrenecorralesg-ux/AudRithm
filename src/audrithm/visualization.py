import matplotlib 
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

def operations_summary(frame):
    """
    Resume la columna operations por algoritmo y tamaño.
    Como los datos reales tienen una fila por repetición, usamos aggfunc="median" 
    para extraer el costo determinista de una sola llamada sin sumar las repeticiones.
    """
    if 'operations' not in frame.columns:
        raise ValueError("La columna 'operations' es requerida para este análisis.")
        
    return frame.pivot_table(
        index="input_size", 
        columns="algorithm", 
        values="operations", 
        aggfunc="median"
    ).sort_index()
    
def operations_ratios(ops_table):
    """
    Calcula las razones del conteo de operaciones entre tamaños que se duplican.
    
    Nota metodológica: Son operaciones de distinta naturaleza (asignaciones simples en Kadane 
    vs acumulaciones en Fuerza bruta). No se presenta su cociente como comparación de velocidad.
    """
    ratios = ops_table.copy()
    for name in ("Kadane", "Fuerza bruta"):
        if name in ratios.columns:
            ratio = ratios[name] / ratios[name].shift(1)
            ratios[f"Razón {name}"] = ratio.where(ratios.index.to_series() == 2 * ratios.index.to_series().shift(1))
    return ratios

def operations_chart(ops_table):
    """
    Genera la gráfica determinista del conteo de operaciones frente a n.
    Complementa las mediciones cortas (aislando ruido), pero no sustituye el análisis asintótico.
    """
    with plt.rc_context({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False}):
        fig, ax = plt.subplots(figsize=(8, 4), layout="constrained")
        for name, color in (("Kadane", "#059669"), ("Fuerza bruta", "#536878")):
            if name in ops_table.columns:
                ax.plot(ops_table.index, ops_table[name], "o-", label=name, color=color, linewidth=2)
        
        ax.set(xlabel="Tamaño de entrada n", ylabel="Operaciones por llamada", title="Crecimiento de Operaciones (Determinista)")
        ax.grid(alpha=.2)
        ax.legend()
        return fig

def save_operations_analysis(frame, directory):
    """
    Exporta la tabla y figura del análisis de operaciones.
    """
    ops_table = operations_summary(frame)
    ratios_table = operations_ratios(ops_table)
    
    fig = operations_chart(ops_table)
    fig.savefig(directory / "operations_growth.png", dpi=180)
    plt.close(fig)
    
    ratios_table.to_csv(directory / "operations_summary.csv")