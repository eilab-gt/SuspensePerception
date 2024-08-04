import json
from pathlib import Path

import pandas as pd
import yaml


def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def save_raw_api_output(output, filename, output_dir):
    raw_output_dir = Path(output_dir) / "raw_outputs"
    raw_output_dir.mkdir(parents=True, exist_ok=True)

    with open(raw_output_dir / filename, "w") as f:
        json.dump(output, f, indent=2)


def process_and_save_results(results, output_dir):
    output_path = Path(output_dir)
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
