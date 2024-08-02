import yaml
from argparse import Namespace
from .together import setup_together_api
from .utils import load_config, save_raw_api_output, process_and_save_results
from .misc import run_experiment


def main(args: Namespace):
    # Load configuration
    if args.config:
        config = load_config(args.config)
    else:
        config = {
            "model": {
                "name": args.model,
                "max_tokens": args.max_tokens,
                "temperature": args.temperature,
                "top_k": args.top_k,
                "top_p": args.top_p,
                "repetition_penalty": args.repetition_penalty,
            },
            "api": {"key": args.api_key},
            "experiment": {
                "story_file": args.story_file,
                "output_dir": args.output_dir,
            },
        }

    # Setup Together API
    # TODO: Store and load the API key from the .secrets file not a YAML
    setup_together_api(config["api"]["key"])

    # Run the experiment
    results = run_experiment(config)

    # Process and save results
    process_and_save_results(results, config["experiment"]["output_dir"])


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the Thriller experiment")
    parser.add_argument(
        "-c", "--config", type=str, help="Path to the configuration file"
    )
    parser.add_argument("--model", type=str, help="Model name")
    parser.add_argument("--api_key", type=str, help="Together API key")
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
    parser.add_argument("--story_file", type=str, help="Path to the story file")
    parser.add_argument("--output_dir", type=str, help="Directory for output files")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
