import argparse
import os
from pathlib import Path

from dotenv import load_dotenv

from gerrig import (
    alternative_substitutions,
    default_substitutions,
    generate_experiment_texts,
)
from misc import run_experiment
from utils import load_config, process_and_save_results


def main(args):
    # Load configuration if provided
    config = load_config(args.config) if args.config else {}
    # Load model and experiment configurations from the configuration file
    model_config = config.get("model", {})
    experiment_config = config.get("experiment", {})
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
            "name": args.model or model_config.get("name"),
            "max_tokens": args.max_tokens or model_config.get("max_tokens"),
            "temperature": args.temperature or model_config.get("temperature"),
            "top_k": args.top_k or model_config.get("top_k"),
            "top_p": args.top_p or model_config.get("top_p"),
            "repetition_penalty": args.repetition_penalty
            or model_config.get("repetition_penalty"),
        }
    )
    experiment_config.update({
        "experiment_series": args.experiment_series or experiment_config.get("experiment_series"),
        "output_dir": args.output_dir or experiment_config.get("output_dir"),
    })

    # Ensure output directory exists
    output_path = Path(experiment_config["output_dir"])
    output_path.mkdir(parents=True, exist_ok=True)

    # Determine which substitutions to use
    substitutions = (
        alternative_substitutions if args.use_alternative else default_substitutions
    )

    # Generate experiment texts
    prompts, version_prompts = generate_experiment_texts(substitutions)

    # Run the experiment
    results = run_experiment(
        args.experiment_series, model_config, prompts, version_prompts
    )

    # Process and save results
    process_and_save_results(results, experiment_config["output_dir"])


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the Gerrig experiments")
    parser.add_argument(
        "-c", "--config", type=str, help="Path to the configuration file"
    )
    parser.add_argument("--api_type", type=str, help="API Type, engine to use e.g. together, openai, anthropic")
    parser.add_argument("--model", type=str, help="Model name")
    parser.add_argument(
        "--max_tokens", type=int, help="Maximum number of tokens for text generation"
    )
    parser.add_argument(
        "--temperature", type=float, help="Temperature for text generation"
    )
    parser.add_argument("--top_k", type=int, help="Top-k for text generation")
    parser.add_argument("--top_p", type=float, help="Top-p for text generation")
    parser.add_argument(
        "--repetition_penalty",
        type=float,
        help="Repetition penalty for text generation",
    )
    parser.add_argument(
        "--experiment_series",
        type=str,
        help="Name of the experiment series to run",
    )
    parser.add_argument("--output_dir", type=str, help="Directory for output files")
    parser.add_argument(
        "--use_alternative",
        action="store_true",
        help="Use alternative names and titles",
    )
    return parser.parse_args()


if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    args = parse_arguments()
    main(args)
