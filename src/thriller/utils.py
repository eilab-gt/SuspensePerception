"""
Functions related to file I/O such as loading configuration files and saving output files
"""

import io
import json
from pathlib import Path

import pandas as pd
import yaml
from datetime import datetime
import uuid


def save_test_output(test_name: str, output: str) -> None:
    """
    Save output from tests
    Args:
        test_name: name of the test and file to save to
        output: test output
    """
    output_dir = Path("Thriller/tests/outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / f"{test_name}.json", "w") as f:
        json.dump(output, f, indent=2)


def load_config(config_path: str) -> io.TextIOWrapper:
    """
    Open and return the configuration file
    Args:
        config_path: path to the configuration yaml file
    Return:
        Opened configuration file
    """
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def process_and_save_results(results, output_path, experiment_series):
    df = pd.DataFrame(results)

    if experiment_series.lower() == "lee":
        # For Lee experiment, keep the parsed_response as is
        df["response"] = df["raw_response"]
        df["parsed_response"] = df["parsed_response"]
    else:
        # For other experiments, process as before
        df["response"] = df["raw_response"]
        df["Q1"] = df["parsed_response"].apply(lambda x: x.get("Q1", None))
        df["Q2"] = df["parsed_response"].apply(lambda x: x.get("Q2", None))

    output_file = output_path / "results.csv"
    df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")


def generate_experiment_id() -> str:
    """
    Generate a unique experiment ID for each model run.

    Returns:
        str: A unique experiment ID combining timestamp and UUID.
    """
    return f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
