import pandas as pd
from src.audrithm.visualization import operations_summary

def test_operation_counts():
    """
    Valida que el agrupamiento no sume accidentalmente las repeticiones.
    Simula 5 filas (repeticiones) por cada algoritmo para n=4.
    """
    data = {
        'algorithm': ['Kadane']*5 + ['Fuerza bruta']*5,
        'input_size': [4]*10,
        'operations': [3, 3, 3, 3, 3, 10, 10, 10, 10, 10]
    }
    frame = pd.DataFrame(data)
    summary = operations_summary(frame)
    
    kadane_ops = summary.loc[4, 'Kadane']
    fb_ops = summary.loc[4, 'Fuerza bruta']
    
    assert kadane_ops == 3.0, f"Error en Kadane: esperado 3, obtenido {kadane_ops}"
    assert fb_ops == 10.0, f"Error en Fuerza bruta: esperado 10, obtenido {fb_ops}"
    
    print("Pruebas superadas: El conteo aísla el costo de una sola llamada (Kadane=3, FB=10 para n=4).")

if __name__ == "__main__":
    test_operation_counts()