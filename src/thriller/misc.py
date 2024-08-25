"""
Helper functions for running experiments
"""

import sys
import typing
from pathlib import Path

from src.thriller.api import generate_response, save_raw_api_output

# Add the project root directory to Python path
project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)


# def parse_response(response: str) -> dict[str, str]:
#     """
#     Process a LLM response into a key value pair
#     Args:
#         response: LLM model's response (see src.thriller.api.generate_response())
#     Return:
#         The response split as a dictionary between question-answer pairs
#     """
#     if not response:
#         return {}
#     lines = response.split("\n")
#     parsed = {}
#     for line in lines:
#         if ":" in line:
#             key, value = line.split(":", 1)
#             parsed[key.strip()] = value.strip()
#     return parsed


# def format_system_message(message: str) -> dict[str, str]:
#     """
#     Args:
#         message: the system message
#     Return:
#         Format for system messages
#     """
#     return {"role": "system", "content": message}


# def format_user_message(message: str) -> dict[str, str]:
#     """
#     Args:
#         message: the user message
#     Return:
#         Format for user messages
#     """
#     return {"role": "user", "content": message}


def apply_substitutions(template: str, substitutions: dict[str, str]) -> str:
    """
    Apply substitutions to a given template
    Args:
        template: the template to replace
        substitutions: the substitutions to use
    Return:
        The template with substitutions
    """
    for key, value in substitutions.items():
        template = template.replace(f"{{{key}}}", value)
    return template


def run_experiment(
    output_path: Path,
    model_config: dict[str, typing.Any],
    prompts: dict[str, str],
    version_prompts: dict[str, str],
) -> list[dict[str, str]]:
    """
    Run the experiment with the given configuration and save the results
    Args:
        output_path: path to the output directory
        model_config: Dictionary of model parameters.
                      Mandatory parameters are `api_type`, `name`, `max_tokens`, `temperature`
        prompts: system LLM messages for message formatting
        version_prompts: experiment LLM messages
    Return:
        Experiment results. Each result is a dictionary with keys `experiment_name`, `version`, `raw_response`, `parsed_response`
    """
    results = []

    for exp_name, prompt in prompts.items():
        print(f"Running experiment: {exp_name}")
        for version_name, version_text in version_prompts[exp_name]:
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": version_text},
            ]

            raw_response = generate_response(messages, model_config)
            if raw_response:
                parsed_response = parse_response(raw_response)

                result = {
                    "experiment_name": exp_name,
                    "version": version_name,
                    "raw_response": raw_response,
                    "parsed_response": parsed_response,
                }

                results.append(result)

                save_raw_api_output(
                    output=raw_response,
                    filename=f"{exp_name}_{version_name.replace(' ', '_')}.json",
                    output_path=output_path,
                )
            else:
                print(f"Failed to get response for {exp_name} version: {version_name}")

    return results
