import importlib.util
import json
import sys
from dataclasses import replace
from pathlib import Path

import pytest


def load_runner_module():
    path = Path(__file__).resolve().parents[1] / "scripts" / "run_benchmark.py"
    spec = importlib.util.spec_from_file_location("run_benchmark", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_final_main_plan_counts_and_paths():
    runner = load_runner_module()

    plan = runner.build_plan(
        suite="final-main",
        experiments=runner.DEFAULT_EXPERIMENTS,
        repeats=3,
        model=runner.DEFAULT_MODEL,
        parse_model=runner.DEFAULT_MODEL,
    )

    assert len(plan.specs) == 15
    assert plan.total_calls == 3684

    by_experiment = {(spec.experiment, spec.repeat): spec for spec in plan.specs}
    assert by_experiment[("gerrig", 1)].expected_calls == 16
    assert by_experiment[("delatorre", 1)].expected_calls == 192
    assert by_experiment[("lehne", 1)].expected_calls == 130
    assert by_experiment[("brewer", 1)].expected_calls == 10
    assert by_experiment[("bentz", 1)].expected_calls == 880

    lehne = by_experiment[("lehne", 1)]
    assert lehne.source_augmentation_order == ("distraction_insertion",)
    assert lehne.augmentation_order == ()
    assert str(by_experiment[("brewer", 2)].output_dir).endswith(
        "outputs/brewer_experiment/final/paper/exp2"
    )


def test_final_main_refuses_effective_augmentation():
    runner = load_runner_module()
    plan = runner.build_plan(
        suite="final-main",
        experiments=("lehne",),
        repeats=1,
        model=runner.DEFAULT_MODEL,
        parse_model=runner.DEFAULT_MODEL,
    )
    unsafe_spec = replace(plan.specs[0], augmentation_order=("distraction_insertion",))

    with pytest.raises(ValueError, match="Refusing final-main"):
        runner.validate_run_spec(unsafe_spec)


def test_effective_config_forces_model_output_and_control_augmentation():
    runner = load_runner_module()
    plan = runner.build_plan(
        suite="final-main",
        experiments=("lehne",),
        repeats=2,
        model=runner.DEFAULT_MODEL,
        parse_model=runner.DEFAULT_MODEL,
    )

    config = runner.effective_config_for_spec(plan.specs[0])

    assert config["model"]["name"] == runner.DEFAULT_MODEL
    assert config["parse_model"]["name"] == runner.DEFAULT_MODEL
    assert config["augmentation"]["augmentation_order"] == []
    assert config["experiment"]["output_dir"].endswith("outputs/lehne_experiment/final/e1")


def test_output_state_blocks_partial_dirs_and_resumes_completed(tmp_path):
    runner = load_runner_module()
    plan = runner.build_plan(
        suite="final-main",
        experiments=("gerrig",),
        repeats=1,
        model=runner.DEFAULT_MODEL,
        parse_model=runner.DEFAULT_MODEL,
    )
    spec = replace(plan.specs[0], output_dir=tmp_path / "outputs" / "gerrig")

    action, completed = runner.ensure_output_state(spec, resume=False)
    assert action == "run"
    assert completed is None

    partial_dir = runner.model_output_dir(spec) / "20260420_partial"
    partial_dir.mkdir(parents=True)
    with pytest.raises(RuntimeError, match="Existing output dirs"):
        runner.ensure_output_state(spec, resume=True)

    completed_spec = replace(
        plan.specs[0], output_dir=tmp_path / "outputs" / "gerrig_completed"
    )
    run_dir = runner.model_output_dir(completed_spec) / "20260420_completed"
    run_dir.mkdir(parents=True)
    (run_dir / "results.csv").write_text("experiment_name,version,response\nA,B,{}\n")
    manifest = runner.manifest_payload(
        spec=completed_spec,
        run_dir=run_dir,
        status="completed",
        started_at="2026-04-20T00:00:00+00:00",
        finished_at="2026-04-20T00:00:01+00:00",
        actual_rows=completed_spec.expected_rows,
    )
    (run_dir / "benchmark_manifest.json").write_text(json.dumps(manifest))

    action, completed = runner.ensure_output_state(completed_spec, resume=True)
    assert action == "skip"
    assert completed == run_dir

    with pytest.raises(RuntimeError, match="Completed output already exists"):
        runner.ensure_output_state(completed_spec, resume=False)


def test_write_manifest_fails_on_null_parsed_values(tmp_path):
    runner = load_runner_module()
    plan = runner.build_plan(
        suite="final-main",
        experiments=("lehne",),
        repeats=1,
        model=runner.DEFAULT_MODEL,
        parse_model=runner.DEFAULT_MODEL,
    )
    spec = plan.specs[0]
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "results.csv").write_text(
        "experiment_name,version,response\n"
        "\"Experiment\",\"Normal\",\"{'0': 5, '1': None}\"\n"
    )

    with pytest.raises(RuntimeError, match="Result quality check failed"):
        runner.write_manifest(spec, run_dir, "2026-04-20T00:00:00+00:00")

    manifest = json.loads((run_dir / "benchmark_manifest.json").read_text())
    assert manifest["status"] == "failed"
    assert manifest["quality_issues"][0]["bad_values"] == {"1": None}
