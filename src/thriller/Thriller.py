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

from dotenv import load_dotenv

# Add the project root directory to Python path
project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import src.thriller.gerrig as gerrig
import src.thriller.lehne as lehne
from src.thriller.misc import run_experiment
from src.thriller.utils import load_config, process_and_save_results


def main(args):
    # Load configuration if provided
    config = load_config(args.config) if args.config else {}

    # Load model and experiment configurations from the configuration file
    model_config = config.get("model", {})
    experiment_config = config.get("experiment", {})
    settings_config = config.get("settings", {})
    if model_config is None:
        raise ValueError("Model configuration not found in the configuration file")
    if experiment_config is None:
        raise ValueError("Experiment configuration not found in the configuration file")

    # Load API type and key from the configuration
    api_type = model_config.get("api_type")
    if not api_type:
        raise ValueError("API type not specified in the configuration")

    # Load API key from secret .env file
    if api_type == "together":
        api_key = os.getenv("TOGETHER_API_KEY")
        if not api_key:
            raise ValueError("API key for TogetherAI must be provided in the .env file")
    elif api_type == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API key for OpenAI must be provided in the .env file")
    elif api_type == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("API key for Anthropic must be provided in the .env file")
    else:
        raise ValueError("API type must be provided in the configuration file")

    # Override config with command-line arguments if they are provided
    model_config.update(
        {
            "api_type": model_config.get("api_type"),
            "api_key": api_key,
            "name": model_config.get("name"),
            "max_tokens": model_config.get("max_tokens"),
            "temperature": model_config.get("temperature"),
            "top_k": model_config.get("top_k"),
            "top_p": model_config.get("top_p"),
            "repetition_penalty": model_config.get("repetition_penalty"),
        }
    )
    experiment_config.update(
        {
            "experiment_series": experiment_config.get("experiment_series"),
            "output_dir": experiment_config.get("output_dir"),
            # "use_alternative": experiment_config.get("use_alternative"),
        }
    )

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
    if not experiment:
        raise ValueError("Valid experiment series not found (must be gerrig, )")

    # Generate experiment texts
    prompts, version_prompts = experiment.generate_experiment_texts(settings_config)

    # Run the experiment
    results = run_experiment(
        output_path=output_path,
        model_config=model_config,
        prompts=prompts,
        version_prompts=version_prompts,
    )

    # Process and save results
    process_and_save_results(results, experiment_config["output_dir"])


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the Gerrig experiments")

    parser.add_argument(
        "-c", "--config", type=str, help="Path to the configuration file"
    )

    return parser.parse_args()


if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    args = parse_arguments()
    main(args)
