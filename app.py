"""Entrada real de las seis vistas; ningún experimento se inicia al abrir."""
import io
import json
import random
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from audrithm.algorithms import kadane, brute_force, kadane_trace
from audrithm.experiment import run_experiment, source_hash
from audrithm.qa import run_qa
from audrithm.visualization import chart, summary
from audrithm.reporting import SECTIONS, report_markdown

st.set_page_config(page_title="AudRithm · Laboratorio", page_icon="◈", layout="wide")
st.html("""<style>
.aud-hero{background:linear-gradient(115deg,#103d30,#087f5b);padding:2rem;border-radius:20px;color:white;margin-bottom:1.5rem}
.aud-hero h1{color:white;margin:0}.aud-kicker{letter-spacing:.2em;font-size:.75rem;color:#a7f3d0}
.aud-cell{display:inline-block;padding:.6rem;margin:.2rem;border-radius:8px;background:#e2e8e5;color:#163c32}
.aud-opt{background:#059669;color:white}.aud-flow{padding:1.2rem;border:1px solid #c9dfd5;border-radius:14px;line-height:2}
</style>""")
st.sidebar.title("▰ AudRithm")
st.sidebar.caption("LABORATORIO DE ALGORITMOS")
view = st.sidebar.radio("Navegación", ["Inicio", "Algoritmos", "Pruebas QA", "Experimentos", "Resultados", "Reporte"], key="navigation")
st.sidebar.divider()
st.sidebar.link_button("Repositorio del equipo ↗", "https://github.com/yrenecorralesg-ux/AudRithm")
st.sidebar.caption("Equipo 5 · Bitácora 1\n\nReferencia asistida por IA. Nombres y contribuciones reales pendientes de validación.")


def load_json(name):
    path = ROOT / "results" / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def results_frame():
    if "experiment_rows" in st.session_state:
        return pd.DataFrame(st.session_state.experiment_rows)
    path = ROOT / "results" / "experiment_results.csv"
    return pd.read_csv(path) if path.exists() else None


def show_theory():
    tabs = st.tabs(["Análisis teórico", "Complejidad", "Invariante"])
    for tab, name in zip(tabs, ["specification.md", "complexity.md", "correctness.md"]):
        with tab:
            st.markdown((ROOT / "docs" / name).read_text(encoding="utf-8"))


def navigate(destination):
    st.session_state.navigation = destination


if view == "Inicio":
    st.html('''<style>
    .st-key-aud_welcome{background:#003b32;border:1px solid #16614f;border-radius:22px;overflow:hidden;margin-bottom:24px;box-shadow:0 16px 45px #003b321a}
    .st-key-aud_welcome_actions{padding:0 24px 24px}
    .aud-section-label{font-size:11px;letter-spacing:2px;font-weight:700;color:#059669;margin:10px 0}
    @media(max-width:600px){.st-key-aud_welcome_actions{padding:0 14px 14px}}
    </style>''')
    with st.container(key="aud_welcome"):
        st.image(str(ROOT / "assets" / "audrithm-auditoria-empresarial.png"), width="stretch")
        with st.container(key="aud_welcome_actions"):
            begin, repository, _ = st.columns([1,1.25,1.7])
            begin.button("Comenzar →", type="primary", on_click=navigate, args=("Algoritmos",), width="stretch")
            repository.link_button("Ver repositorio ↗", "https://github.com/yrenecorralesg-ux/AudRithm", width="stretch")
    st.html('<div class="aud-section-label">EVIDENCIA DEL LABORATORIO</div>')
    qa = st.session_state.get("qa", load_json("qa_results.json"))
    frame = results_frame()
    cols = st.columns(3)
    cols[0].metric("Algoritmos implementados", 2)
    cols[1].metric("Pruebas aprobadas", f'{qa["passed"]}/{qa["tests"]}' if qa else "Pendiente")
    cols[2].metric("Mediciones disponibles", len(frame) if frame is not None else "Sin datos")
    st.html('<div class="aud-flow"><span>01 · Entrada</span><b>→</b><span>02 · Algoritmos</span><b>→</b><span>03 · Validación</span><b>→</b><span>04 · Experimentos</span><b>→</b><span>05 · Análisis</span><b>→</b><span>06 · Reporte</span></div>')
    st.subheader("Tu laboratorio, de principio a fin")
    st.write("Bitácora 1 · Subarreglo de suma máxima. Explora Kadane y fuerza bruta, valida sus resultados y contrasta su crecimiento con evidencia reproducible.")
    for row in [[("Algoritmos", "Explora la solución", "Ejecuta ambos motores y sigue la traza real de Kadane."),
                 ("Pruebas QA", "Comprueba los resultados", "Casos límite, oráculo independiente y pruebas diferenciales."),
                 ("Experimentos", "Mide el rendimiento", "Entradas pareadas, semilla fija y cinco repeticiones.")],
                [("Resultados", "Interpreta la evidencia", "Medianas, razones de crecimiento y gráficas descargables."),
                 ("Reporte", "Prepara tu bitácora", "Ocho requisitos, matriz de cumplimiento y PDF de trabajo.")]]:
        for column, (destination, title, description) in zip(st.columns(len(row)), row):
            with column, st.container(border=True):
                st.caption(destination.upper())
                st.markdown(f"**{title}**")
                st.write(description)
                st.button(f"Abrir {destination} →", key=f"open_{destination}", on_click=navigate, args=(destination,))
    st.caption("Equipo 5 · Implementación de referencia asistida por IA. El informe requiere revisión, comprensión y aprobación académica del equipo.")

elif view == "Algoritmos":
    st.title("Laboratorio de algoritmos")
    st.caption("Subarreglo de suma máxima · índices inclusivos desde cero")
    with st.expander("Generar una entrada reproducible"):
        n = st.slider("Tamaño", 1, 1000, 20)
        bounds = st.slider("Rango de valores", -100, 100, (-20,20))
        seeded = st.checkbox("Usar semilla fija", True)
        seed = st.number_input("Semilla", value=20261105, step=1)
        if st.button("Generar arreglo aleatorio"):
            rng = random.Random(int(seed) if seeded else None)
            st.session_state["array_text"] = str([rng.randint(*bounds) for _ in range(n)])
    text = st.text_area("Arreglo de enteros (separados por comas)", value="[-2, 1, -3, 4, -1, 2, 1, -5, 4]", key="array_text", max_chars=18000)
    selected = st.selectbox("Algoritmos", ["Ambos algoritmos", "Kadane O(n)", "Fuerza bruta O(n²)"])
    if st.button("Ejecutar análisis", type="primary"):
        try:
            cleaned = text.strip()
            if cleaned.startswith("[") and cleaned.endswith("]"):
                cleaned = cleaned[1:-1]
            tokens = cleaned.split(",")
            if not 1 <= len(tokens) <= 1000 or any(not re.fullmatch(r"\s*[+-]?\d{1,10}\s*", t) for t in tokens):
                raise ValueError("Ingresa entre 1 y 1000 enteros de hasta diez dígitos, separados por comas.")
            arr = [int(t) for t in tokens]
            answers = []
            for name, fn in [("Kadane O(n)", kadane), ("Fuerza bruta O(n²)", brute_force)]:
                if selected == "Ambos algoritmos" or selected == name:
                    before = time.perf_counter_ns()
                    result = fn(arr)
                    elapsed = time.perf_counter_ns()-before
                    answers.append(result)
                    st.subheader(name)
                    a,b,c = st.columns(3)
                    a.metric("Suma máxima", result.total)
                    b.metric("Intervalo [inicio, fin]", f"[{result.start}, {result.end}]")
                    c.metric("Observación individual", f"{elapsed / 1000:.2f} μs")
                    st.write("Subarreglo:", list(result.subarray))
            if len(answers)==2:
                if answers[0] != answers[1]:
                    st.error("Discrepancia detectada")
                else:
                    st.success("Equivalencia confirmada: suma, índices y subarreglo coinciden.")
            result = answers[0]
            st.html("".join(f'<span class="aud-cell {"aud-opt" if result.start <= i <= result.end else ""}">{v}</span>' for i,v in enumerate(arr[:100])))
            if len(arr)>100:
                st.caption("Vista limitada a los primeros 100 elementos; el resultado utiliza la entrada completa.")
            st.caption("Una observación individual contiene ruido; usa Experimentos para comparar medianas.")
            with st.expander("Ejecución paso a paso de Kadane"):
                st.dataframe(pd.DataFrame(kadane_trace(arr)), hide_index=True)
        except (ValueError, TypeError) as exc:
            st.error(str(exc))
    show_theory()

elif view == "Pruebas QA":
    st.title("Validación y pruebas QA")
    st.write("Suite fija de Pytest, capturada en un subproceso con límite de 45 segundos. Incluye casos límite, comparación diferencial y un oráculo exhaustivo independiente.")
    if st.button("Ejecutar suite controlada", type="primary"):
        with st.spinner("Validando algoritmos y contratos…"):
            st.session_state.qa = run_qa()
    qa = st.session_state.get("qa", load_json("qa_results.json"))
    if qa:
        for col, key, label in zip(st.columns(4), ["tests","passed","failures","duration_s"], ["Ejecutadas","Aprobadas","Fallidas","Duración (s)"]):
            col.metric(label, round(qa[key],3) if key=="duration_s" else qa[key])
        st.caption(f'Evidencia: {qa["date"]} · commit: {qa.get("commit") or "no disponible"} · errores: {qa["errors"]} · omitidas: {qa["skipped"]}')
        if qa.get("source_sha256") != source_hash():
            st.warning("El código cambió desde esta evidencia. Ejecuta nuevamente la suite.")
        (st.success if qa["exit_code"]==0 else st.error)("Suite aprobada" if qa["exit_code"]==0 else "La suite requiere atención")
        st.code(qa["output"], language="text")
        st.download_button("Descargar evidencia QA", json.dumps(qa,ensure_ascii=False,indent=2), "qa_results.json", "application/json")
    else:
        st.info("Pendiente de ejecución. No hay resultados de pruebas registrados.")
    st.caption("No se mide ni se afirma un porcentaje de cobertura.")

elif view == "Experimentos":
    st.title("Experimentos reproducibles")
    st.write("100, 200, 400, 800, 1600 y 3200 elementos · 5 repeticiones · misma entrada por par · orden alternado.")
    st.info("Máximo 60 observaciones por ejecución. El presupuesto de 90 s se comprueba entre llamadas; una llamada está acotada a 3200 elementos. No se generan datos, archivos ni gráficas dentro del intervalo medido.")
    seed = st.number_input("Semilla experimental", value=20261105, step=1)
    if st.button("Ejecutar experimento", type="primary"):
        bar = st.progress(0.0)
        try:
            with st.spinner("Midiendo…"):
                rows, meta = run_experiment(seed=int(seed), progress=bar.progress)
            st.session_state.experiment_rows = rows
            st.session_state.experiment_meta = meta
            st.success("Experimento completo. Consulta Resultados; las mediciones de esta sesión se conservan en memoria.")
        except (ValueError, TimeoutError, AssertionError) as exc:
            st.error(str(exc))
    frame = results_frame()
    if frame is not None:
        st.download_button("Descargar CSV", frame.to_csv(index=False), "experiment_results.csv", "text/csv")
        meta = st.session_state.get("experiment_meta", load_json("experiment_metadata.json"))
        st.download_button("Descargar metadatos", json.dumps(meta,ensure_ascii=False,indent=2), "experiment_metadata.json", "application/json")
        st.json(meta)

elif view == "Resultados":
    st.title("Teoría frente a evidencia")
    frame = results_frame()
    if frame is None:
        st.info("Sin datos. Ejecuta un experimento o el pipeline local.")
    else:
        st.caption("Medianas en nanosegundos; razones calculadas solo entre tamaños que se duplican.")
        st.dataframe(summary(frame), width="stretch")
        for log, name in [(False,"normal"),(True,"loglog")]:
            fig = chart(frame,log)
            st.pyplot(fig)
            buffer = io.BytesIO()
            fig.savefig(buffer,format="png",dpi=180)
            st.download_button(f"Descargar gráfica {name}", buffer.getvalue(), f"timing_{name}.png", "image/png")
            plt.close(fig)
        st.write("La teoría predice Θ(n) y Θ(n²). Al duplicar n, las razones ideales se aproximan a 2 y 4; las mediciones no tienen que coincidir exactamente. La evidencia experimental no demuestra una cota matemática.")
        st.warning("El ruido del sistema, la resolución del reloj y el calentamiento afectan la medición. El conteo de operaciones del CSV ofrece una referencia determinista: n−1 actualizaciones y n(n+1)/2 acumulaciones.")
        st.download_button("Descargar tabla de medianas",summary(frame).to_csv(),"summary.csv","text/csv")

elif view == "Reporte":
    st.title("Bitácora 1 · Equipo 5")
    st.warning("Borrador asistido por IA. El equipo debe revisar, comprender y validar la demostración, los datos y las conclusiones antes de entregar.")
    for i,(title,filename) in enumerate(SECTIONS,1):
        with st.expander(f"{i}. {title}",expanded=i==1):
            st.markdown((ROOT/"docs"/filename).read_text(encoding="utf-8"))
    with st.expander("Matriz de cumplimiento y evidencias"):
        matrix = ROOT / "docs" / "matriz_cumplimiento.md"
        if matrix.exists():
            st.markdown(matrix.read_text(encoding="utf-8"))
            st.download_button("Descargar matriz de cumplimiento", matrix.read_text(encoding="utf-8"), "matriz_cumplimiento.md", "text/markdown")
    st.download_button("Descargar contenido editable",report_markdown(),"bitacora1.md","text/markdown")
    pdf = ROOT/"output"/"pdf"/"Equipo_5_Bitacora1.pdf"
    if pdf.exists():
        st.download_button("Descargar PDF de referencia (borrador)",pdf.read_bytes(),pdf.name,"application/pdf")
        st.caption("El PDF contiene la ejecución local archivada; los experimentos de la sesión no regeneran el documento.")
