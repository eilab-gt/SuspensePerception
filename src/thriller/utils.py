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


def process_and_save_results(
    results: list[dict[str, str]], output_path: Path
) -> pd.DataFrame:
    """
    Save data to a dataframe and save as .csv
    Args:
        results: data to save
        output_path: path to the output directory
    Return:
        The data as a dataframe
    """
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
    # df.to_parquet(output_path / "results.parquet", index=False)

    return df


def generate_experiment_id() -> str:
    """
    Generate a unique experiment ID for each model run.

    Returns:
        str: A unique experiment ID combining timestamp and UUID.
    """
    return f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
