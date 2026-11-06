"""Suite fija; no se aceptan comandos ni rutas provenientes de la interfaz."""
import json
import os
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from .experiment import ROOT, commit_id, source_hash


def _read_junit(xml):
    root = ET.parse(xml).getroot()
    suites = list(root.iter("testsuite"))
    if not suites:
        raise ValueError("El XML JUnit no contiene una suite.")
    counts = {
        key: sum(int(suite.get(key, 0)) for suite in suites)
        for key in ("tests", "failures", "errors", "skipped")
    }
    counts["passed"] = counts["tests"] - counts["failures"] - counts["errors"] - counts["skipped"]
    cases = []
    for case in root.iter("testcase"):
        status, message = "passed", None
        for tag, outcome in (("error", "error"), ("failure", "failed"), ("skipped", "skipped")):
            detail = case.find(tag)
            if detail is not None:
                status = outcome
                message = detail.get("message") or (detail.text or "").strip() or None
                break
        cases.append(dict(
            name="::".join(part for part in (case.get("classname"), case.attrib["name"]) if part),
            status=status,
            duration_s=float(case.get("time", "0")),
            message=message,
        ))
    return counts, cases


def run_qa():
    started = time.perf_counter()
    counts = dict(tests=0, passed=0, failures=0, errors=0, skipped=0)
    cases = []
    with tempfile.TemporaryDirectory() as temp:
        xml = Path(temp) / "qa.xml"
        env = os.environ.copy()
        env["PYTHONPATH"] = os.pathsep.join([str(ROOT / "src"), *[p for p in sys.path if p]])
        env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
        try:
            proc = subprocess.run([sys.executable, "-m", "pytest", "tests", "-q", f"--junitxml={xml}"], cwd=ROOT,
                                  env=env, capture_output=True, text=True, timeout=45)
            exit_code = proc.returncode
            output = proc.stdout + proc.stderr
            try:
                counts, cases = _read_junit(xml)
            except (OSError, ET.ParseError, ValueError, KeyError) as exc:
                exit_code = exit_code or 1
                output += f"\nEvidencia JUnit no disponible: {exc}"
        except subprocess.TimeoutExpired:
            exit_code, output = 124, "Timeout de la suite fija (45 s)."
        except OSError as exc:
            exit_code, output = 1, f"No se pudo ejecutar la suite fija: {exc}"
    if exit_code and not (counts["failures"] or counts["errors"]):
        counts["errors"] = 1
    return dict(**counts, cases=cases, exit_code=exit_code, output=output[-24000:],
                duration_s=time.perf_counter()-started, date=datetime.now(timezone.utc).isoformat(),
                commit=commit_id(), source_sha256=source_hash())
