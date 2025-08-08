#!/usr/bin/env python3

"""
Main entrypoint for running the src.thriller.experiments
Use Example:
> python ./src.thriller.src.thriller.py -c config.yaml
"""

import argparse
import os
import sys
from pathlib import Path
from tqdm import tqdm
import logging
import argparse
from omegaconf import OmegaConf, DictConfig
import hydra
from hydra import (
    compose,
    initialize
)
import warnings
import sys

from dotenv import load_dotenv


# Silence PyTorch UserWarnings
warnings.filterwarnings("ignore", category=UserWarning, module="torch")

# Add the project root directory to Python path
project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.thriller.misc import run_experiment
from src.thriller.utils import (
    load_config,
    process_and_save_results,
    generate_experiment_id,
    dotdict
)
from src.thriller.constants import SUPPORTED_API_TYPES, AVAILABLE_ATTACKS

from src.thriller.adversarial import (
    process_and_augment_stories,
    get_default_augmentation_config
)

import src.thriller.gerrig as gerrig
import src.thriller.lehne as lehne
import src.thriller.brewer as brewer
import src.thriller.delatorre as delatorre
import src.thriller.bentz as bentz

@hydra.main(config_path="../config", config_name="default", version_base=None)
def main(args):
    
    global_config = dotdict(args)

    assert_api_key(global_config)

    logging.basicConfig(level=logging.WARNING)

    # Ensure output directory exists
    output_dir = Path(global_config.experiment.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Determine experiment setup
    overrides = get_global_overrides()
    experiments_combinations = get_experiment_combinations(global_config)

    is_mpi = check_mpi_support()

    if is_mpi:
        from mpi4py import MPI
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()
        size = comm.Get_size()

        if rank == 0:
            print(f"MPI is enabled. Running {size} experiments in parallel.")
            data = list(experiments_combinations)
        else:
            data = None
        data = comm.bcast(data, root=0)

        for i in range(rank, len(data), size):
            text, aug = data[i]
            subdir = Path(os.path.join(output_dir, text, aug))
            subdir.mkdir(parents=True, exist_ok=True)
            hydra.core.global_hydra.GlobalHydra.instance().clear()
            with initialize(version_base=None, config_path='../config'):
                cfg = compose(config_name="default", overrides=[f"{k}={v}" for (k, v) in overrides] + [f"text={text}", f"+text.aug={aug}", f"experiment.output_dir={subdir}"])
                run_single_experiment(cfg)

    else:
        for text, aug in experiments_combinations:
            subdir = Path(os.path.join(output_dir, text, aug))
            subdir.mkdir(parents=True, exist_ok=True)

            hydra.core.global_hydra.GlobalHydra.instance().clear()
            with initialize(version_base=None, config_path='../config'):
                cfg = compose(config_name="default", overrides=[f"{k}={v}" for (k, v) in overrides] + [f"text={text}", f"+text.aug={aug}", f"experiment.output_dir={subdir}"])
                run_single_experiment(cfg)

def check_mpi_support():
    if "SLURM_NNODES" in os.environ and "SLURM_NTASKS" in os.environ and int(os.environ["SLURM_NTASKS"]) > 1:
        return True
    return False



def run_single_experiment(cfg : dotdict):
    
    experiment_series = cfg.text.experiment_series
    experiment = {
        "gerrig": gerrig,
        "lehne": lehne,
        "brewer": brewer,
        "delatorre": delatorre,
        "bentz": bentz
    }.get(experiment_series, None)

    if not experiment:
        raise ValueError("Valid experiment series not found (must be gerrig, lehne, brewer, delatorre, or bentz)")
        
    # # Generate experiment texts
    prompts, version_prompts = experiment.generate_experiment_texts(cfg.text)

    assert cfg.text.aug in AVAILABLE_ATTACKS, f"Invalid augmentation type: {cfg.text.aug}"

    cfg.aug.augmentation_order = [cfg.text.aug]

    augmentation_config = get_default_augmentation_config() | OmegaConf.to_object(cfg.aug)

    for experiment in version_prompts:
        version_prompts[experiment] = [(key, process_and_augment_stories(story, augmentation_config)) for key, story in version_prompts[experiment]]
        if 'caesar_cipher' in augmentation_config.get('augmentation_order', {}):
            prompts[experiment] = prompts[experiment] + "\nThis text has been encrypted using a Caesar cipher with a step of 3."

    model_names = cfg.model.name
    total_models = len(model_names)

    assert os.path.exists(cfg.experiment.output_dir)

    with tqdm(total=total_models, desc="Overall Progress", position=0, leave=False) as pbar:
        for model_name in model_names:
            model_config = cfg.model
            cfg.model.name = model_name
            # Generate a unique experiment ID for each model run
            experiment_id = generate_experiment_id()

            # Create a subfolder structure: model_name/experiment_id`
            
            cur_output_path = Path(os.path.join(cfg.experiment.output_dir, model_name.replace("/", "_"), experiment_id))
            cur_output_path.mkdir(parents=True, exist_ok=True)

            results = run_experiment(
                output_path=cur_output_path,
                model_config=cfg.model,
                parse_model_config=cfg.parse_model,
                prompts=prompts,
                version_prompts=version_prompts,
            )

            # Process and save results
            process_and_save_results(results, cur_output_path)

            pbar.update(1)

    tqdm.write("\nExperiment completed successfully!")


def assert_api_key(config: dotdict):
    
    model_api = config.model.api_type
    parse_model_api = config.parse_model.api_type
    
    load_dotenv()

    for api in set([model_api, parse_model_api]):
        assert api in ["together", "openai", "anthropic"], f"Invalid API type: {api}"
        if api == "openai" and "VLLM_HOSTNAME_URL" in os.environ:
            continue
        assert api.upper() + "_API_KEY" in os.environ, f"{api.upper()}_API_KEY not found in environment variables, or VLLM_HOSTNAME_URL not found in environment variables"

def get_global_overrides() -> list[tuple[str, str]]:
    
    overrides = sys.argv[1:]

    override_tuples = []

    for key, value in map(lambda x: x.split("="), overrides):
        assert key != "text", "text is a reserved key for individual experiment configs"
        assert key != "aug", "aug is a reserved key for augmentation configs"
        override_tuples.append((key, value))

    return override_tuples
    
def get_experiment_combinations(cfg : dotdict) -> list[tuple[str, str]]:

    texts = cfg.experiment.texts
    augs = cfg.experiment.augs

    return [(text, aug) for text in texts for aug in augs]

if __name__ == "__main__":
    main()
