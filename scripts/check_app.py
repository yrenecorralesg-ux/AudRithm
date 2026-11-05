"""Verificación funcional de las seis vistas usando Streamlit AppTest."""
from pathlib import Path
from datetime import datetime, timezone
import json
import hashlib
import subprocess
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
assert not app.exception, app.exception
next(b for b in app.button if b.label == "Comenzar →").click().run()
assert not app.exception, app.exception
assert app.sidebar.radio[0].value == "Algoritmos"
verified = []
for view in ["Inicio","Algoritmos","Pruebas QA","Experimentos","Resultados","Reporte"]:
    app.sidebar.radio[0].set_value(view).run()
    assert not app.exception, (view, app.exception)
    if view == "Algoritmos":
        next(b for b in app.button if b.label == "Ejecutar análisis").click().run()
        assert not app.exception, app.exception
        assert any(m.value == "6" for m in app.metric)
        assert any("Equivalencia confirmada" in s.value for s in app.success)
    print(f"OK: {view}")
    verified.append(view)
evidence = {"date": datetime.now(timezone.utc).isoformat(), "views": verified, "example_sum": 6,
            "equivalence": True, "exceptions": 0,
            "start_button_navigation": True,
            "app_sha256": hashlib.sha256((ROOT / "app.py").read_bytes()).hexdigest(),
            "commit": subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()}
(ROOT / "results" / "app_check.json").write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding="utf-8")
