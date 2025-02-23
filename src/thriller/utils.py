"""
Functions related to file I/O such as loading configuration files and saving output files
"""

from argparse import Namespace
import io
import json
from pathlib import Path
import pandas as pd
import yaml
from datetime import datetime
import uuid
import ast
import os

# This class is 100% autocomplete generated
class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    @staticmethod
    def from_nested_dict(data):
        """Construct nested dotdict from nested dictionary"""
        if not isinstance(data, dict):
            return data
        else:
            return dotdict({key: dotdict.from_nested_dict(data[key]) for key in data})

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


def load_config(args: Namespace) -> io.TextIOWrapper:
    """
    Open and return the configuration file
    Args:
        config_path: path to the configuration yaml file
    Return:
        Opened configuration file
    """

    argdict = {}

    if args.config:
        config_path = os.path.join("config", "experiment", args.config)
        if not config_path.endswith(".yaml"):
            config_path += ".yaml"
        with open(config_path, "r") as f:
            argdict = yaml.safe_load(f)
    else:
        raise ValueError("Configuration file not provided")
    if args.augmentation:
        aug_config_path = os.path.join("config", "augmentation", args.augmentation)
        if not aug_config_path.endswith(".yaml"):
            aug_config_path += ".yaml"
        with open(aug_config_path, "r") as f:
            aug_dict = yaml.safe_load(f)
            argdict["augmentation"] = aug_dict

    if args.overrides:
        for override in args.overrides:
            try:
                key, value = override.split("=")
                key_hierarchy = key.split(".")
                temp_dict = argdict
                for k in key_hierarchy[:-1]:
                    temp_dict = temp_dict[k]
                temp_dict[key_hierarchy[-1]] = ast.literal_eval(value)
            except KeyError:
                raise ValueError(f"Key {key_hierarchy} not found in configuration file")
            
    if "model" not in argdict:
        raise ValueError("Model configuration not found in the configuration file")
    if "parse_model" not in argdict:
        raise ValueError("Parse model configuration not found in the configuration file")
    if "experiment" not in argdict:
        raise ValueError("Experiment configuration not found in the configuration file")
    if "augmentation" not in argdict:
        raise ValueError("Augmentation configuration not found in the configuration file")
    
    return argdict

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
