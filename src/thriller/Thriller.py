#!/usr/bin/env python3

"""
Main entrypoint for running the Thriller experiments
Use Example:
> python ./src/thriller/Thriller.py -c config.yaml
"""

import argparse
import copy
from dataclasses import dataclass
import os
import sys
from pathlib import Path
from tqdm import tqdm
import logging
import json
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
from src.thriller.adversarial import (
    process_and_augment_stories,
    get_default_augmentation_config
)

import src.thriller.gerrig as gerrig
import src.thriller.lehne as lehne
import src.thriller.brewer as brewer
import src.thriller.delatorre as delatorre
import src.thriller.bentz as bentz


EXPERIMENT_MODULES = {
    "gerrig": gerrig,
    "lehne": lehne,
    "brewer": brewer,
    "delatorre": delatorre,
    "bentz": bentz,
}

API_KEY_ENV_VARS = {
    "together": "TOGETHER_API_KEY",
    "openai": "OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
}


@dataclass
class PreparedExperiment:
    model_config: dict
    parse_model_config: dict
    experiment_config: dict
    augmentation_config: dict
    experiment_series: str
    prompts: dict
    version_prompts: dict


def attach_api_key(model_config: dict, label: str) -> None:
    api_type = model_config.get("api_type")
    if not api_type:
        raise ValueError(f"API type not specified in the {label} configuration")

    env_var = API_KEY_ENV_VARS.get(api_type)
    if not env_var:
        raise ValueError(
            f"Unsupported API type in the {label} configuration: {api_type}"
        )

    api_key = os.getenv(env_var)
    if not api_key:
        raise ValueError(f"API key for {api_type} must be provided via {env_var}")

    model_config["api_key"] = api_key


def attach_api_keys(model_config: dict, parse_model_config: dict) -> None:
    attach_api_key(model_config, "model")
    attach_api_key(parse_model_config, "parse_model")


def get_experiment_module(experiment_series: str):
    experiment = EXPERIMENT_MODULES.get(experiment_series)
    if not experiment:
        valid = ", ".join(sorted(EXPERIMENT_MODULES))
        raise ValueError(f"Valid experiment series not found (must be one of: {valid})")
    return experiment


def prepare_experiment_config(config: dict) -> PreparedExperiment:
    config = copy.deepcopy(config)
    model_config = config.get("model", None)
    experiment_config = config.get("experiment", None)
    parse_model_config = config.get("parse_model", None)
    augmentation_config = config.get("augmentation", None)

    if model_config is None:
        raise ValueError("Model configuration not found in the configuration file")
    if parse_model_config is None:
        raise ValueError("Parse model configuration not found in the configuration file")
    if experiment_config is None:
        raise ValueError("Experiment configuration not found in the configuration file")
    if augmentation_config is None:
        raise ValueError("Augmentation configuration not found in the configuration file")

    attach_api_keys(model_config, parse_model_config)

    experiment_series = experiment_config.get("experiment_series")
    experiment_module = get_experiment_module(experiment_series)
    prompts, version_prompts = experiment_module.generate_experiment_texts(
        experiment_config
    )

    augmentation_config = get_default_augmentation_config() | augmentation_config
    augmentation_order = augmentation_config.get("augmentation_order", [])

    for exp_name in version_prompts:
        version_prompts[exp_name] = [
            (key, process_and_augment_stories(story, augmentation_config))
            for key, story in version_prompts[exp_name]
        ]
        if "caesar_cipher" in augmentation_order:
            prompts[exp_name] = (
                prompts[exp_name]
                + "\nThis text has been encrypted using a Caesar cipher with a step of 3."
            )

    return PreparedExperiment(
        model_config=model_config,
        parse_model_config=parse_model_config,
        experiment_config=experiment_config,
        augmentation_config=augmentation_config,
        experiment_series=experiment_series,
        prompts=prompts,
        version_prompts=version_prompts,
    )


def write_prompt_snapshots(
    experiment_series: str,
    prompts: dict,
    version_prompts: dict,
    augmentation_config: dict,
    prompt_root: Path = Path("prompts"),
) -> None:
    augmentation_order = augmentation_config.get("augmentation_order", [])
    augmentation = augmentation_order[0] if augmentation_order else "control"
    augmentation = "control" if augmentation == "" else augmentation

    for exp_name in version_prompts:
        filename = prompt_root / experiment_series / augmentation / f"{exp_name}.json"
        filename.parent.mkdir(parents=True, exist_ok=True)
        snapshot = {
            "prompts": prompts[exp_name],
            "version_prompts": version_prompts[exp_name],
        }
        with open(filename, "w") as f:
            json.dump(snapshot, f)


def get_model_names(model_config: dict) -> list[str]:
    model_names = model_config.get("name")
    if isinstance(model_names, str):
        return [model_names]
    return list(model_names)


def run_config(
    config: dict,
    write_prompts: bool = True,
    dry_run: bool = False,
) -> list[Path]:
    prepared = prepare_experiment_config(config)

    if write_prompts:
        write_prompt_snapshots(
            experiment_series=prepared.experiment_series,
            prompts=prepared.prompts,
            version_prompts=prepared.version_prompts,
            augmentation_config=prepared.augmentation_config,
        )

    if dry_run:
        print("Dry run enabled. Skipping experiment execution.")
        if write_prompts:
            print("Prompts saved to file. Exiting.")
        else:
            print("Prompt snapshots disabled. Exiting.")
        return []

    output_path = Path(prepared.experiment_config["output_dir"])
    output_path.mkdir(parents=True, exist_ok=True)

    model_names = get_model_names(prepared.model_config)
    output_paths = []
    with tqdm(total=len(model_names), desc="Overall Progress") as pbar:
        for model_name in model_names:
            cur_model_config = prepared.model_config.copy()
            cur_model_config["name"] = model_name
            experiment_id = generate_experiment_id()
            cur_output_path = output_path / model_name.replace("/", "_") / experiment_id
            cur_output_path.mkdir(parents=True, exist_ok=True)

            tqdm.write(f"\nProcessing model: {model_name}")
            results = run_experiment(
                output_path=cur_output_path,
                model_config=cur_model_config,
                parse_model_config=prepared.parse_model_config,
                prompts=prepared.prompts,
                version_prompts=prepared.version_prompts,
            )

            process_and_save_results(results, cur_output_path)
            output_paths.append(cur_output_path)

            pbar.update(1)

    tqdm.write("\nExperiment completed successfully!")
    return output_paths


def main(args):
    logging.basicConfig(level=logging.WARNING)
    config = load_config(args) if args.config else {}
    dry_run = os.getenv("DRY_RUN") == "1"
    run_config(config, write_prompts=not dry_run, dry_run=dry_run)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the given experiment")

    parser.add_argument(
        "-c", "--config", type=str, help="Path to the configuration file"
    )
    parser.add_argument(
        "-o", "--overrides", nargs="*", help="Overrides for the configuration file"
    )

    return parser.parse_args()


if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    args = parse_arguments()
    main(args)
