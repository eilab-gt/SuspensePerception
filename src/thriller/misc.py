"""
Code that is explicitly related to the execution and parsing of API calls for experiments
"""
# Note: Consider refactoring - these functions could be reorganized into api.py and utils.py

import sys
import typing
from typing import Union
from pathlib import Path
from src.thriller.api import generate_response, save_raw_api_output
import re
from tqdm import tqdm
import logging

# Add the project root directory to Python path
project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)


# Use tqdm?
TQDM_ACTIVE = True


def safe_int_conversion(value):
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        return int(value) if value.isdigit() else None
    return None


def parse_response(
    response: str, model_config: dict[str, typing.Any]
) -> dict[str, str]:
    # Note: Consider moving to api.py in future refactoring
    """
    Process a LLM response into a key value pair
    Args:
        response: LLM model's response (see src.thriller.api.generate_response())
        model_config: Dictionary of model parameters.
                      Mandatory parameters are `api_type`, `name`, `max_tokens`, `temperature`
    Return:
        The response split as a dictionary between question-answer pairs
    """
    api_type = model_config.get("api_type", None)

    prompt = model_config.get("prompt")

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": response},
    ]

    if api_type not in {"openai", "together"}:
        raise ValueError(f"Unsupported API type: {api_type}")

    content = generate_response(messages, model_config)

    if not content:
        return {}

    values = re.findall(r"\w+: \d+", content)
    if values:
        values = [value.split(":") for value in values]
        return {key: int(value) for key, value in values}

    values = re.findall(r"\d+", content)
    if values:
        return {"value": int(value) for value in values}

    return {}


def apply_substitutions(template: str, substitutions: dict[str, str]) -> str:
    # Note: Consider moving to utils.py in future refactoring
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

def truncate_messages(messages, max_tokens=4096):
    """
    Ensures the total token count of messages does not exceed max_tokens.
    """
    total_tokens = sum(len(msg["content"].split()) for msg in messages)
    
    while total_tokens > max_tokens and len(messages) > 2:
        messages.pop(1)  # Remove the oldest user message
        total_tokens = sum(len(msg["content"].split()) for msg in messages)

    return messages

def run_experiment(
    output_path: Path,
    model_config: dict[str, typing.Any],
    parse_model_config: dict[str, typing.Any],
    prompts: dict[str, str],
    version_prompts:  dict[str, Union[str, list[str]]],
) -> list[dict[str, str]]:
    # Note: Consider moving to utils.py in future refactoring
    """
    Run the experiment with the given configuration and save the results
    Args:
        output_path: path to the output directory
        model_config: Dictionary of model parameters.
                      Mandatory parameters are `api_type`, `name`, `max_tokens`, `temperature`
        parse_model_config: Dictionary of parsing model parameters.
                            Mandatory parameters are `api_type`, `name`, `max_tokens`, `temperature`
        prompts: system LLM messages for message formatting
        version_prompts: experiment LLM messages
    Return:
        Experiment results. Each result is a dictionary with keys `experiment_name`, `version`, `raw_response`, `parsed_response`
    """
    results = []
    total_experiments = sum(len(versions) for versions in version_prompts.values())

    with tqdm(total=total_experiments, desc="Overall Progress") as pbar:
        for exp_name, prompt in prompts.items():
            print(f"\nRunning experiment {exp_name} with {model_config.get('name')}")

            for version_name, version_text in version_prompts[exp_name]:
                if isinstance(version_text, str):
                    version_text = [version_text]
                if isinstance(version_text, list):
                    with tqdm(
                        total=len(version_text), desc=f"{exp_name} - {version_name}"
                    ) as inner_pbar:
                        messages = [
                            {"role": "system", "content": prompt},
                        ]

                        raw_responses = []
                        parsed_responses = []

                        for i, paragraph in enumerate(version_text):
                            messages.append({"role": "user", "content": prompt + paragraph})

                            raw_response = ""
                            last_error = None

                            # Try get LLM response. If context window too large, retry with 1 less message
                            for _ in range(10):
                                try:
                                    messages = truncate_messages(messages, max_tokens=4096)
                                    raw_response = generate_response(
                                        messages, model_config
                                    )
                                    break
                                except Exception as exc:
                                    # logging.error(f"Error occurred: {e}") # This is almost guaranteed to spam
                                    last_error = exc
                                    if len(messages) >= 4:
                                        messages.pop(1)
                                        messages.pop(1)
                                    else:
                                        raise RuntimeError(
                                            f"Failed to get response for {exp_name} "
                                            f"segment {i} version: {version_name}"
                                        ) from exc

                            parsed_response = {"value": float("nan")}
                            if not raw_response or raw_response.isspace():
                                if last_error is not None:
                                    raise RuntimeError(
                                        f"Failed to get response for {exp_name} "
                                        f"segment {i} version: {version_name}"
                                    ) from last_error
                                raw_response = "Error - No Response: Empty Response"
                                print(f"Failed to get response for {exp_name} segment {i} version: {version_name}. Empty Response")
                            else:
                                parsed_response = parse_response(
                                    raw_response, parse_model_config
                                )

                            raw_responses.append(raw_response)
                            messages.append(
                                {"role": "assistant", "content": raw_response}
                            )
                            parsed_responses.extend(parsed_response.values())

                            if TQDM_ACTIVE:
                                inner_pbar.update(1)

                        raw_responses = "\n####################################################################################################\n".join(raw_responses)
                        parsed_responses_dict = {}
                        for i, response in enumerate(parsed_responses):
                            converted_value = safe_int_conversion(response)
                            parsed_responses_dict[str(i)] = converted_value
                            if converted_value is None:
                                logging.warning(f"Non-numeric response encountered at index {i}: '{response}'")

                        result = {
                            "experiment_name": exp_name,
                            "version": version_name,
                            "raw_response": raw_responses,
                            "parsed_response": parsed_responses_dict,
                        }

                        results.append(result)

                        save_raw_api_output(
                            output=raw_responses,
                            filename=f"{exp_name}_{version_name.replace(' ', '_')}.txt",
                            output_path=output_path,
                        )

                else:
                    raise ValueError("Experiment should be in list format.")

                pbar.update(1)

    return results
