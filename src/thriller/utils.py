import json
from pathlib import Path

import pandas as pd
import yaml


def save_test_output(test_name, output):
    output_dir = Path("Thriller/tests/outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / f"{test_name}.json", "w") as f:
        json.dump(output, f, indent=2)


def load_config(config_path):
    try:
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(
            f"Config file {config_path} not found. Using default empty configuration."
        )
        return {}


def save_raw_api_output(output, filename, output_path: Path):
    raw_output_dir = Path(output_path) / "raw_outputs"
    raw_output_dir.mkdir(parents=True, exist_ok=True)

    with open(raw_output_dir / filename, "w") as f:
        json.dump(output, f, indent=2)


def process_and_save_results(results, output_path: Path):
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

    data = []
    for result in results:
        parsed_response = result["parsed_response"]
        data.append(
            {
                "experiment_name": result["experiment_name"],
                "version": result["version"],
                "response": parsed_response,
            }
        )

    df = pd.DataFrame(data)
    df.to_csv(output_path / "results.csv", index=False)
    df.to_parquet(output_path / "results.parquet", index=False)

    return df
