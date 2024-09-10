#!/usr/bin/env python3

"""
Main entrypoint for running the Thriller experiments
Use Example:
> python ./src/thriller/Thriller.py -c config.yaml
"""

import argparse
import os
import sys
from pathlib import Path
from tqdm import tqdm
import logging

from dotenv import load_dotenv


# Add the project root directory to Python path
project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.thriller.misc import run_experiment
from src.thriller.utils import (
    load_config,
    process_and_save_results,
    generate_experiment_id,
)

import src.thriller.gerrig as gerrig
import src.thriller.lehne as lehne
import src.thriller.brewer as brewer
import src.thriller.delatorre as delatorre
import src.thriller.bentz as bentz


def main(args):
    logging.basicConfig(level=logging.WARNING)

    # Load configuration if provided
    config = load_config(args.config) if args.config else {}

    # Load model and experiment configurations from the configuration file
    model_config = config.get("model", None)
    experiment_config = config.get("experiment", None)
    parse_model_config = config.get("parse_model", None)
    if model_config is None:
        raise ValueError("Model configuration not found in the configuration file")
    if parse_model_config is None:
        raise ValueError(
            "Parse model configuration not found in the configuration file"
        )
    if experiment_config is None:
        raise ValueError("Experiment configuration not found in the configuration file")

    # Load API key from secret .env file for model
    model_api_key = ""
    model_api_type = model_config.get("api_type")
    if not model_api_type:
        raise ValueError("API type not specified in the configuration")
    if model_api_type == "together":
        model_api_key = os.getenv("TOGETHER_API_KEY")
        if not model_api_key:
            raise ValueError("API key for TogetherAI must be provided in the .env file")
    elif model_api_type == "openai":
        model_api_key = os.getenv("OPENAI_API_KEY")
        if not model_api_key:
            raise ValueError("API key for OpenAI must be provided in the .env file")
    elif model_api_type == "anthropic":
        model_api_key = os.getenv("ANTHROPIC_API_KEY")
        if not model_api_key:
            raise ValueError("API key for Anthropic must be provided in the .env file")
    else:
        raise ValueError("API type must be provided in the configuration file")
    model_config["api_key"] = model_api_key

    # Load API key from secret .env file for parse model
    parse_model_api_key = ""
    parse_model_api_type = parse_model_config.get("api_type")
    if parse_model_api_type == "together":
        parse_model_api_key = os.getenv("TOGETHER_API_KEY")
        if not parse_model_api_key:
            raise ValueError("API key for TogetherAI must be provided in the .env file")
    elif parse_model_api_type == "openai":
        parse_model_api_key = os.getenv("OPENAI_API_KEY")
        if not parse_model_api_key:
            raise ValueError("API key for OpenAI must be provided in the .env file")
    elif parse_model_api_type == "anthropic":
        parse_model_api_key = os.getenv("ANTHROPIC_API_KEY")
        if not parse_model_api_key:
            raise ValueError("API key for Anthropic must be provided in the .env file")
    else:
        raise ValueError("API type must be provided in the configuration file")
    parse_model_config["api_key"] = parse_model_api_key

    # Ensure output directory exists
    output_path = Path(experiment_config["output_dir"])
    output_path.mkdir(parents=True, exist_ok=True)

    # Determine experiment series
    experiment = None
    experiment_series = experiment_config.get("experiment_series")
    if experiment_series == "gerrig":
        experiment = gerrig
    elif experiment_series == "lehne":
        experiment = lehne
    elif experiment_series == "brewer":
        experiment = brewer
    elif experiment_series == "delatorre":
        experiment = delatorre
    elif experiment_series == "bentz":
        experiment = bentz
    if not experiment:
        raise ValueError(
            "Valid experiment series not found (must be gerrig, lehne, or delatorre)"
        )

    # Generate experiment texts
    prompts, version_prompts = experiment.generate_experiment_texts(experiment_config)

    # Run the experiment
    model_names = model_config.get("name")
    total_models = len(model_names)

    with tqdm(total=total_models, desc="Overall Progress") as pbar:
        for model_name in model_names:
            cur_model_config = model_config.copy()
            cur_model_config["name"] = model_name
            # Generate a unique experiment ID for each model run
            experiment_id = generate_experiment_id()

            # Create a subfolder structure: model_name/experiment_id
            cur_output_path = output_path / model_name.replace("/", "_") / experiment_id
            cur_output_path.mkdir(parents=True, exist_ok=True)

            tqdm.write(f"\nProcessing model: {model_name}")
            results = run_experiment(
                output_path=cur_output_path,
                model_config=cur_model_config,
                parse_model_config=parse_model_config,
                prompts=prompts,
                version_prompts=version_prompts,
            )

            # Process and save results
            process_and_save_results(results, cur_output_path)

            pbar.update(1)

    tqdm.write("\nExperiment completed successfully!")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the given experiment")

    parser.add_argument(
        "-c", "--config", type=str, help="Path to the configuration file"
    )

    return parser.parse_args()


if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    args = parse_arguments()
    main(args)
