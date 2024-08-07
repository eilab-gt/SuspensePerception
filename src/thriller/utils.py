"""
File IO, loading configuration files and saving output files
"""

import json
from pathlib import Path
import pandas as pd
import yaml
import io


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


def save_raw_api_output(output: str, filename: str, output_path: Path) -> None:
    """
    Save text to a JSON file
    Args:
        output: data to save 
        filename: name of the output JSON file
        output_path: path to the output directory
    """
    raw_output_dir = Path(output_path) / "raw_outputs"
    raw_output_dir.mkdir(parents=True, exist_ok=True)

    with open(raw_output_dir / filename, "w") as f:
        json.dump(output, f, indent=2)


def process_and_save_results(results: list[dict[str, str]], output_path: Path) -> pd.DataFrame:
    """
    Save data to a dataframe and save as .csv and .parquet
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
    df.to_parquet(output_path / "results.parquet", index=False)

    return df
