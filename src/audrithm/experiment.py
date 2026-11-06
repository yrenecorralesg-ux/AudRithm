"""Mediciones pareadas con orden alternado y presupuesto temporal."""
import csv
import hashlib
import importlib.metadata
import json
import platform
import random
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from .algorithms import kadane, brute_force

ROOT = Path(__file__).resolve().parents[2]
SIZES = (100, 200, 400, 800, 1600, 3200)
SEED = 20261105


def commit_id():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, stderr=subprocess.DEVNULL, text=True, timeout=5).strip()
    except (OSError, subprocess.SubprocessError):
        return None


def source_hash():
    digest = hashlib.sha256()
    for path in sorted((ROOT / "src").rglob("*.py")):
        digest.update(path.relative_to(ROOT).as_posix().encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def run_experiment(sizes=SIZES, repetitions=5, seed=SEED, timeout=90, progress=None):
    sizes = tuple(sizes)
    if not sizes or any(type(n) is not int or not 1 <= n <= 3200 for n in sizes):
        raise ValueError("Tamaños permitidos: 1 a 3200.")
    if not 1 <= repetitions <= 5 or not 0 < timeout <= 120:
        raise ValueError("Máximo cinco repeticiones y 120 segundos.")
    rng = random.Random(seed)
    # Toda generación precede a las mediciones.
    inputs = {(n, r): [rng.randint(-100, 100) for _ in range(n)] for n in sizes for r in range(1, repetitions + 1)}
    for fn in (kadane, brute_force):
        fn(inputs[sizes[0], 1])  # calentamiento excluido
    started = time.perf_counter()
    rows = []
    for k, ((n, r), arr) in enumerate(inputs.items()):
        functions = [("Kadane", kadane), ("Fuerza bruta", brute_force)]
        if k % 2:
            functions.reverse()
        answers = []
        for order, (name, fn) in enumerate(functions, 1):
            if time.perf_counter() - started > timeout:
                raise TimeoutError("Presupuesto agotado; no se publican resultados parciales.")
            before = time.perf_counter_ns()
            answer = fn(arr)
            elapsed = time.perf_counter_ns() - before
            answers.append(answer)
            rows.append(dict(algorithm=name, input_size=n, repetition=r, seed=seed, elapsed_ns=elapsed,
                             execution_order=order, operations=n-1 if name == "Kadane" else n*(n+1)//2))
        if answers[0] != answers[1]:
            raise AssertionError("Los algoritmos discrepan.")
        if progress:
            progress((k + 1) / len(inputs))
    versions = {}
    for name in ("streamlit", "pandas", "matplotlib", "pytest"):
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = "no instalado"
    metadata = dict(python=platform.python_version(), os=platform.platform(), processor=platform.processor() or "no disponible",
                    dependencies=versions, date=datetime.now(timezone.utc).isoformat(), seed=seed, commit=commit_id(),
                    source_sha256=source_hash(), clock_resolution_s=time.get_clock_info("perf_counter").resolution,
                    configuration=dict(sizes=sizes, repetitions=repetitions, range=[-100,100], timeout=timeout,
                                       warmup="una ejecución por algoritmo", order="alternado por par"),
                    limitations="Una máquina, una distribución uniforme; ruido de SO, reloj y calentamiento; tiempo incluye validación y salida.")
    return rows, metadata


def save_results(rows, metadata, directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "experiment_results.csv").open("w", newline="", encoding="utf-8") as out:
        writer = csv.DictWriter(out, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (directory / "experiment_metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")


def ejecutar_experimento(directory=None):
    """Entrada CLI en español: mide, exporta y presenta medianas y razones.

    Integra la presentación del experimento sin duplicar los algoritmos ni
    cambiar el contrato que utiliza la interfaz. No se ejecuta al importar.
    """
    import pandas as pd
    from .visualization import summary

    output = Path(directory) if directory is not None else ROOT / "results"
    rows, metadata = run_experiment()
    save_results(rows, metadata, output)
    table = summary(pd.DataFrame(rows))
    table.to_csv(output / "summary.csv")
    print("Medianas en nanosegundos y razones entre tamaños duplicados:")
    print(table.to_string())
    print(f"{len(rows)} observaciones guardadas en {output}")
    return rows, metadata


if __name__ == "__main__":
    ejecutar_experimento()
