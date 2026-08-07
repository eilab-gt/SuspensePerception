#!/usr/bin/env python3
"""Plan and run paper-style Thriller benchmark suites."""

from __future__ import annotations

import argparse
import ast
import copy
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import pandas as pd
import yaml
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.thriller import bentz, brewer, delatorre, gerrig, lehne
from src.thriller.Thriller import attach_api_keys, run_config
from src.thriller.api import generate_response


DEFAULT_MODEL = "Qwen/Qwen3.5-9B"
DEFAULT_EXPERIMENTS = ("gerrig", "delatorre", "lehne", "brewer", "bentz")
EXPERIMENT_MODULES = {
    "gerrig": gerrig,
    "delatorre": delatorre,
    "lehne": lehne,
    "brewer": brewer,
    "bentz": bentz,
}


@dataclass(frozen=True)
class RunSpec:
    suite: str
    experiment: str
    repeat: int
    config_path: Path
    output_dir: Path
    model: str
    parse_model: str
    augmentation_order: tuple[str, ...]
    source_augmentation_order: tuple[str, ...]
    expected_rows: int
    expected_segments: int
    expected_calls: int


@dataclass(frozen=True)
class BenchmarkPlan:
    suite: str
    specs: tuple[RunSpec, ...]

    @property
    def total_calls(self) -> int:
        return sum(spec.expected_calls for spec in self.specs)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def safe_model_dir(model: str) -> str:
    return model.replace("/", "_")


def model_output_dir(spec: RunSpec) -> Path:
    return spec.output_dir / safe_model_dir(spec.model)


def load_yaml(path: Path) -> dict[str, Any]:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def output_dir_for(experiment: str, repeat: int) -> Path:
    if experiment == "brewer":
        return PROJECT_ROOT / "outputs" / "brewer_experiment" / "final" / "paper" / f"exp{repeat}"
    return PROJECT_ROOT / "outputs" / f"{experiment}_experiment" / "final" / f"e{repeat}"


def normalize_experiments(experiments: str | Iterable[str]) -> tuple[str, ...]:
    if isinstance(experiments, str):
        requested = tuple(item.strip() for item in experiments.split(",") if item.strip())
    else:
        requested = tuple(experiments)

    unknown = sorted(set(requested) - set(DEFAULT_EXPERIMENTS))
    if unknown:
        raise ValueError(f"Unknown experiment(s): {', '.join(unknown)}")
    return requested


def count_expected(config: dict[str, Any]) -> tuple[int, int, int]:
    series = config["experiment"]["experiment_series"]
    prompts, version_prompts = EXPERIMENT_MODULES[series].generate_experiment_texts(
        config["experiment"]
    )
    rows = sum(len(versions) for versions in version_prompts.values())
    segments = sum(
        len(text) if isinstance(text, list) else 1
        for versions in version_prompts.values()
        for _, text in versions
    )
    calls = segments * 2
    if len(prompts) != len(version_prompts):
        raise ValueError(f"Prompt/version mismatch for {series}")
    return rows, segments, calls


def effective_config_for_spec(spec: RunSpec) -> dict[str, Any]:
    config = load_yaml(spec.config_path)
    config = copy.deepcopy(config)
    config["model"]["name"] = spec.model
    config["parse_model"]["name"] = spec.parse_model
    config["experiment"]["output_dir"] = str(spec.output_dir)
    config["augmentation"]["augmentation_order"] = list(spec.augmentation_order)
    return config


def build_run_spec(
    suite: str,
    experiment: str,
    repeat: int,
    model: str,
    parse_model: str,
) -> RunSpec:
    if suite != "final-main":
        raise ValueError("Only the final-main suite is currently supported")

    config_path = PROJECT_ROOT / "configs" / f"{experiment}.yaml"
    source_config = load_yaml(config_path)
    source_augmentation_order = tuple(
        source_config["augmentation"].get("augmentation_order", [])
    )

    effective_config = copy.deepcopy(source_config)
    effective_config["model"]["name"] = model
    effective_config["parse_model"]["name"] = parse_model
    effective_config["experiment"]["output_dir"] = str(output_dir_for(experiment, repeat))
    effective_config["augmentation"]["augmentation_order"] = []

    rows, segments, calls = count_expected(effective_config)
    return RunSpec(
        suite=suite,
        experiment=experiment,
        repeat=repeat,
        config_path=config_path,
        output_dir=output_dir_for(experiment, repeat),
        model=model,
        parse_model=parse_model,
        augmentation_order=(),
        source_augmentation_order=source_augmentation_order,
        expected_rows=rows,
        expected_segments=segments,
        expected_calls=calls,
    )


def build_plan(
    suite: str,
    experiments: str | Iterable[str],
    repeats: int,
    model: str,
    parse_model: str,
) -> BenchmarkPlan:
    requested_experiments = normalize_experiments(experiments)
    specs = []
    for repeat in range(1, repeats + 1):
        for experiment in requested_experiments:
            specs.append(
                build_run_spec(
                    suite=suite,
                    experiment=experiment,
                    repeat=repeat,
                    model=model,
                    parse_model=parse_model,
                )
            )
    return BenchmarkPlan(suite=suite, specs=tuple(specs))


def validate_run_spec(spec: RunSpec) -> None:
    if spec.suite == "final-main" and spec.augmentation_order:
        raise ValueError(
            f"Refusing final-main run with augmentation_order={spec.augmentation_order}"
        )


def manifest_payload(
    spec: RunSpec,
    run_dir: Path,
    status: str,
    started_at: str,
    finished_at: str | None,
    actual_rows: int | None = None,
) -> dict[str, Any]:
    payload = asdict(spec)
    payload["config_path"] = str(spec.config_path)
    payload["output_dir"] = str(spec.output_dir)
    payload["run_dir"] = str(run_dir)
    payload["augmentation_order"] = list(spec.augmentation_order)
    payload["source_augmentation_order"] = list(spec.source_augmentation_order)
    payload["status"] = status
    payload["started_at"] = started_at
    payload["finished_at"] = finished_at
    payload["actual_rows"] = actual_rows
    return payload


def manifest_matches_spec(manifest: dict[str, Any], spec: RunSpec) -> bool:
    return (
        manifest.get("suite") == spec.suite
        and manifest.get("experiment") == spec.experiment
        and manifest.get("repeat") == spec.repeat
        and manifest.get("model") == spec.model
        and manifest.get("parse_model") == spec.parse_model
        and manifest.get("augmentation_order") == list(spec.augmentation_order)
    )


def find_completed_run(spec: RunSpec) -> Path | None:
    model_dir = model_output_dir(spec)
    if not model_dir.exists():
        return None

    completed = []
    for manifest_path in sorted(model_dir.glob("*/benchmark_manifest.json")):
        try:
            with open(manifest_path, "r") as f:
                manifest = json.load(f)
        except json.JSONDecodeError:
            continue
        run_dir = manifest_path.parent
        if (
            manifest_matches_spec(manifest, spec)
            and manifest.get("status") == "completed"
            and (run_dir / "results.csv").exists()
        ):
            completed.append(run_dir)
    return completed[-1] if completed else None


def existing_run_dirs(spec: RunSpec) -> list[Path]:
    model_dir = model_output_dir(spec)
    if not model_dir.exists():
        return []
    return sorted(path for path in model_dir.iterdir() if path.is_dir())


def ensure_output_state(spec: RunSpec, resume: bool) -> tuple[str, Path | None]:
    completed = find_completed_run(spec)
    if completed and resume:
        return "skip", completed
    if completed and not resume:
        raise RuntimeError(
            f"Completed output already exists for {spec.experiment} repeat {spec.repeat}: "
            f"{completed}. Use --resume to skip it or quarantine it first."
        )

    existing = existing_run_dirs(spec)
    if existing:
        formatted = "\n".join(f"  - {path}" for path in existing)
        raise RuntimeError(
            f"Existing output dirs would make this run ambiguous for "
            f"{spec.experiment} repeat {spec.repeat}:\n{formatted}\n"
            "Quarantine or remove them before running."
        )

    return "run", None


def write_manifest(spec: RunSpec, run_dir: Path, started_at: str) -> None:
    results_csv = run_dir / "results.csv"
    if not results_csv.exists():
        raise RuntimeError(f"Missing results.csv for completed run: {run_dir}")

    actual_rows = len(pd.read_csv(results_csv))
    quality_issues = find_result_quality_issues(results_csv)
    status = (
        "completed"
        if actual_rows == spec.expected_rows and not quality_issues
        else "failed"
    )
    manifest = manifest_payload(
        spec=spec,
        run_dir=run_dir,
        status=status,
        started_at=started_at,
        finished_at=utc_now(),
        actual_rows=actual_rows,
    )
    manifest["quality_issues"] = quality_issues

    with open(run_dir / "benchmark_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    if actual_rows != spec.expected_rows:
        raise RuntimeError(
            f"Unexpected row count for {run_dir}: expected {spec.expected_rows}, "
            f"got {actual_rows}"
        )

    if quality_issues:
        raise RuntimeError(
            f"Result quality check failed for {run_dir}: "
            f"{len(quality_issues)} issue(s)"
        )


def find_result_quality_issues(results_csv: Path) -> list[dict[str, Any]]:
    issues = []
    df = pd.read_csv(results_csv)
    for row_index, row in df.iterrows():
        try:
            parsed = ast.literal_eval(row["response"])
        except (SyntaxError, ValueError) as exc:
            issues.append(
                {
                    "row": int(row_index),
                    "experiment_name": row.get("experiment_name"),
                    "version": row.get("version"),
                    "error": f"unparseable response: {exc}",
                }
            )
            continue

        bad_values = {
            key: value
            for key, value in parsed.items()
            if value is None or pd.isna(value)
        }
        if bad_values:
            issues.append(
                {
                    "row": int(row_index),
                    "experiment_name": row.get("experiment_name"),
                    "version": row.get("version"),
                    "bad_values": bad_values,
                }
            )
    return issues


def print_plan(plan: BenchmarkPlan) -> None:
    print(f"Benchmark suite: {plan.suite}")
    print(f"Runs: {len(plan.specs)}")
    print(f"Estimated calls: {plan.total_calls}")
    for spec in plan.specs:
        source_note = ""
        if spec.source_augmentation_order != spec.augmentation_order:
            source_note = (
                f" source_aug={list(spec.source_augmentation_order)}"
                f" -> effective_aug={list(spec.augmentation_order)}"
            )
        print(
            f"- {spec.experiment} repeat={spec.repeat} rows={spec.expected_rows} "
            f"segments={spec.expected_segments} calls={spec.expected_calls} "
            f"model={spec.model} parse_model={spec.parse_model} "
            f"output={spec.output_dir}{source_note}"
        )


def preflight_api(plan: BenchmarkPlan) -> None:
    if not plan.specs:
        return

    first_config = effective_config_for_spec(plan.specs[0])
    attach_api_keys(first_config["model"], first_config["parse_model"])

    configs = [
        ("model", first_config["model"]),
        ("parse_model", first_config["parse_model"]),
    ]
    seen = set()
    for label, model_config in configs:
        model_id = (model_config["api_type"], model_config["name"])
        if model_id in seen:
            continue
        seen.add(model_id)
        response = generate_response(
            [
                {"role": "system", "content": "Return only the number 7."},
                {"role": "user", "content": "Return only the number 7."},
            ],
            model_config,
        )
        if not response or "7" not in response:
            raise RuntimeError(
                f"Preflight failed for {label} {model_config['name']}: {response!r}"
            )
        print(f"Preflight OK: {label} {model_config['name']}")


def execute_plan(
    plan: BenchmarkPlan,
    dry_run: bool,
    resume: bool,
    preflight: bool,
    write_prompts: bool,
) -> None:
    for spec in plan.specs:
        validate_run_spec(spec)

    print_plan(plan)
    if dry_run:
        return

    if preflight:
        preflight_api(plan)

    for index, spec in enumerate(plan.specs, start=1):
        action, completed = ensure_output_state(spec, resume=resume)
        if action == "skip":
            print(
                f"[{index}/{len(plan.specs)}] Skipping completed "
                f"{spec.experiment} repeat {spec.repeat}: {completed}"
            )
            continue

        print(
            f"[{index}/{len(plan.specs)}] Running {spec.experiment} "
            f"repeat {spec.repeat}"
        )
        config = effective_config_for_spec(spec)
        started_at = utc_now()
        output_paths = run_config(
            config=config,
            write_prompts=write_prompts,
            dry_run=False,
        )
        if len(output_paths) != 1:
            raise RuntimeError(
                f"Expected exactly one output path for {spec.experiment}, "
                f"got {len(output_paths)}"
            )
        write_manifest(spec, output_paths[0], started_at)


def parse_arguments(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Thriller benchmark suites")
    parser.add_argument("--suite", default="final-main", choices=["final-main"])
    parser.add_argument("--experiments", default=",".join(DEFAULT_EXPERIMENTS))
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--parse-model", default=DEFAULT_MODEL)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--preflight-api", action="store_true")
    parser.add_argument(
        "--write-prompts",
        action="store_true",
        help="Write prompt snapshots under prompts/ during execution.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    load_dotenv(PROJECT_ROOT / ".env")
    args = parse_arguments(argv)
    if args.repeats < 1:
        raise ValueError("--repeats must be >= 1")

    plan = build_plan(
        suite=args.suite,
        experiments=args.experiments,
        repeats=args.repeats,
        model=args.model,
        parse_model=args.parse_model,
    )
    execute_plan(
        plan=plan,
        dry_run=args.dry_run,
        resume=args.resume,
        preflight=args.preflight_api,
        write_prompts=args.write_prompts,
    )


if __name__ == "__main__":
    main()
