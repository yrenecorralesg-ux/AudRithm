from types import SimpleNamespace

import pytest

from audrithm import qa


def test_read_junit_cases(tmp_path):
    xml = tmp_path / "qa.xml"
    xml.write_text(
        """
        <testsuites>
          <testsuite tests="4" failures="1" errors="1" skipped="1">
            <testcase classname="test_sample" name="test_ok[1]" time="0.125" />
            <testcase classname="test_sample" name="test_fail" time="0.25">
              <failure message="assert 1 == 2">traceback</failure>
            </testcase>
            <testcase name="test_skip" time="0.0">
              <skipped message="sin datos" />
            </testcase>
            <testcase name="test_error" time="0.5"><error>setup roto</error></testcase>
          </testsuite>
        </testsuites>
        """,
        encoding="utf-8",
    )

    counts, cases = qa._read_junit(xml)

    assert counts == dict(tests=4, passed=1, failures=1, errors=1, skipped=1)
    assert cases == [
        dict(name="test_sample::test_ok[1]", status="passed", duration_s=0.125, message=None),
        dict(name="test_sample::test_fail", status="failed", duration_s=0.25, message="assert 1 == 2"),
        dict(name="test_skip", status="skipped", duration_s=0.0, message="sin datos"),
        dict(name="test_error", status="error", duration_s=0.5, message="setup roto"),
    ]


@pytest.mark.parametrize(
    ("xml_content", "returncode", "expected_exit"),
    [
        (None, 4, 4),
        ("<testsuites>", 0, 1),
        ('<testsuite tests="0"/>', 5, 5),
    ],
)
def test_run_qa_reports_execution_errors(monkeypatch, xml_content, returncode, expected_exit):
    def run(command, **kwargs):
        if xml_content is not None:
            xml = qa.Path(command[-1].split("=", 1)[1])
            xml.write_text(xml_content, encoding="utf-8")
        return SimpleNamespace(returncode=returncode, stdout="salida", stderr="diagnóstico")

    monkeypatch.setattr(qa.subprocess, "run", run)
    monkeypatch.setattr(qa, "commit_id", lambda: None)

    result = qa.run_qa()

    assert result["exit_code"] == expected_exit
    assert result["errors"] == 1
    assert result["passed"] == 0
    assert result["cases"] == []
    assert "salidadiagnóstico" in result["output"]
