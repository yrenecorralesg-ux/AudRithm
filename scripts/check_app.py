"""Verificación funcional de las seis vistas y la persistencia del análisis."""
from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib
import subprocess
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


def assert_no_exception(app, context):
    assert not app.exception, (context, app.exception)


def current_commit():
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except (FileNotFoundError, OSError, subprocess.SubprocessError):
        return "git-no-disponible"


app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
assert_no_exception(app, "inicio")
next(b for b in app.button if b.label == "Comenzar →").click().run()
assert_no_exception(app, "navegación desde inicio")
assert app.sidebar.radio[0].value == "Algoritmos"

# Verificación de persistencia y limpieza del último análisis.
app.text_area[0].set_value("[-2, 1, -3, 4, -1, 2, 1, -5, 4]").run()
next(b for b in app.button if b.label == "Ejecutar análisis").click().run()
assert_no_exception(app, "ejecutar análisis")
assert any(m.value == "6" for m in app.metric), [m.value for m in app.metric]
assert any("Equivalencia confirmada" in s.value for s in app.success), [s.value for s in app.success]
assert any("Entrada utilizada" in c.value for c in app.caption), [c.value for c in app.caption]

# Al volver a la vista, el estado debe conservarse sin señal de entrada modificada.
app.sidebar.radio[0].set_value("Inicio").run()
app.sidebar.radio[0].set_value("Algoritmos").run()
assert_no_exception(app, "regreso a algoritmos")
assert app.text_area[0].value == "[-2, 1, -3, 4, -1, 2, 1, -5, 4]"
assert not any("Entrada modificada" in w.value for w in app.warning), [w.value for w in app.warning]

# Si la entrada cambia, la app debe exigir ejecutar de nuevo para actualizar el resultado.
app.text_area[0].set_value("[-2, 2, -3, 4, -1, 2, 1, -5, 4]").run()
assert_no_exception(app, "entrada modificada")
assert any("Entrada modificada" in w.value for w in app.warning), [w.value for w in app.warning]

# La limpieza del análisis guardado debe dejar el estado vacío.
next(b for b in app.button if b.label == "Limpiar análisis guardado").click().run()
assert_no_exception(app, "limpieza del análisis")
assert not any("Entrada utilizada" in c.value for c in app.caption), [c.value for c in app.caption]
assert not any("Entrada modificada" in w.value for w in app.warning), [w.value for w in app.warning]

# Revisión de las seis vistas y las descargas contenidas.
verified = []
for view in ["Inicio","Algoritmos","Pruebas QA","Experimentos","Resultados","Reporte"]:
    app.sidebar.radio[0].set_value(view).run()
    assert_no_exception(app, view)
    print(f"OK: {view}")
    verified.append(view)

# Ejemplo real de suma máxima y descargas de intención operativa.
app.sidebar.radio[0].set_value("Algoritmos").run()
app.text_area[0].set_value("[-2, 1, -3, 4, -1, 2, 1, -5, 4]").run()
next(b for b in app.button if b.label == "Ejecutar análisis").click().run()
assert_no_exception(app, "validación final del análisis")
assert any(m.value == "6" for m in app.metric)
assert not any("Entrada modificada" in w.value for w in app.warning)

before = current_commit()
evidence = {"date": datetime.now(timezone.utc).isoformat(), "views": verified, "example_sum": 6,
            "equivalence": True, "exceptions": 0,
            "start_button_navigation": True,
            "persistence": True,
            "clean_state": True,
            "input_warning": True,
            "app_sha256": hashlib.sha256((ROOT / "app.py").read_bytes()).hexdigest(),
            "commit": before}
(ROOT / "results" / "app_check.json").write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding="utf-8")
