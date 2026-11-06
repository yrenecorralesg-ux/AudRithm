import pandas as pd
import pytest
from audrithm.experiment import run_experiment, save_results
from audrithm.visualization import summary

def test_paired_measurement_and_exports(tmp_path):
    rows, meta = run_experiment(sizes=(4,8), repetitions=2, seed=7)
    save_results(rows,meta,tmp_path)
    frame = pd.read_csv(tmp_path / "experiment_results.csv")
    assert len(frame) == 8
    assert (frame.elapsed_ns > 0).all()
    for (n,r),group in frame.groupby(["input_size","repetition"]):
        assert set(group.algorithm)=={"Kadane","Fuerza bruta"}
        assert set(group.execution_order)=={1,2}
    assert meta["seed"] == 7
    assert meta["configuration"]["sizes"] == (4,8)

def test_medians_and_doubling_ratios():
    rows = [dict(algorithm=a,input_size=n,elapsed_ns=t) for a in ("Kadane","Fuerza bruta")
            for n,ts in [(2,[1,9,3]),(4,[6,2,10]),(10,[20,10,30])] for t in ts]
    table = summary(pd.DataFrame(rows))
    assert table.loc[2,"Kadane"] == 3
    assert table.loc[4,"Razón Kadane"] == 2
    assert pd.isna(table.loc[10,"Razón Kadane"])

@pytest.mark.parametrize("kwargs", [dict(sizes=(3201,)),dict(repetitions=6),dict(timeout=121)])
def test_experiment_limits(kwargs):
    with pytest.raises(ValueError):
        run_experiment(**kwargs)


def test_application_experiment_contract():
    # app.py y qa.py dependen de estos nombres, incluso antes de medir.
    from audrithm.experiment import ROOT, SEED, SIZES, commit_id, source_hash, ejecutar_experimento
    from audrithm.qa import run_qa
    assert (ROOT / "app.py").is_file()
    assert SIZES == (100, 200, 400, 800, 1600, 3200)
    assert SEED == 20261105
    assert len(source_hash()) == 64
    assert callable(commit_id) and callable(run_qa) and callable(ejecutar_experimento)


def test_spanish_entrypoint_uses_shared_engine(tmp_path, monkeypatch, capsys):
    import audrithm.experiment as experiment
    rows = [dict(algorithm=name, input_size=n, repetition=1, seed=7, elapsed_ns=t)
            for name in ("Kadane", "Fuerza bruta") for n,t in ((2,10),(4,20))]
    monkeypatch.setattr(experiment, "run_experiment", lambda: (rows, {"seed":7}))
    assert experiment.ejecutar_experimento(tmp_path) == (rows, {"seed":7})
    assert (tmp_path / "experiment_results.csv").exists()
    assert (tmp_path / "experiment_metadata.json").exists()
    assert (tmp_path / "summary.csv").exists()
    assert "Medianas" in capsys.readouterr().out
