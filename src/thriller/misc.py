"""
Code that is explicitly related to the execution and parsing of API calls for experiments
"""
# TODO: move to api.py and utils.py then delete this file

import sys
import typing
from pathlib import Path
from src.thriller.api import generate_response, save_raw_api_output
import openai
from together import Together
import re
from tqdm import tqdm
import logging
from typing import Union, Dict, List


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
    # TODO: move to api.py
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

    content = ""

    if api_type == "openai":
        parsed_response = openai.ChatCompletion.create(
            model=model_config["name"],
            messages=messages,
            max_tokens=model_config["max_tokens"],
            temperature=model_config["temperature"],
            top_p=model_config.get("top_p", None),
            top_k=model_config.get("top_k", None),
            repetition_penalty=model_config["repetition_penalty"],
        )

        content = parsed_response["choices"][0]["message"]["content"]

    elif api_type == "together":
        client = Together(api_key=model_config["api_key"])
        parsed_response = client.chat.completions.create(
            model=model_config["name"],
            messages=messages,
            max_tokens=model_config["max_tokens"],
            temperature=model_config["temperature"],
            top_p=model_config.get("top_p", None),
            top_k=model_config.get("top_k", None),
            repetition_penalty=model_config["repetition_penalty"],
            stop=model_config["stop"],
            stream=model_config["stream"],
        )

        for chunk in parsed_response:
            content += chunk.choices[0].delta.content or ""

    else:
        raise ValueError(f"Unsupported API type: {api_type}")

    if not content:
        return {}

    values = re.findall(r"\w+: \d+", content)
    if values:
        return {key: int(value) for key, value in values}

    values = re.findall(r"\d+", content)
    if values:
        return {"value": int(value) for value in values}

    return {}


def apply_substitutions(template: str, substitutions: dict[str, str]) -> str:
    # TODO: move to utils.py
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
    parse_model_config: dict[str, typing.Any],
    prompts: dict[str, str],
    version_prompts: Dict[str, Union[str, List[str]]],
) -> list[dict[str, str]]:
    # TODO: move to utils.py
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

                            # Try get LLM response. If context window too large, retry with 1 less message
                            for _ in range(10):
                                try:
                                    raw_response = generate_response(
                                        messages, model_config
                                    )
                                    break
                                except Exception as e:
                                    # logging.error(f"Error occurred: {e}") # This is almost guaranteed to spam
                                    if len(messages) >= 4:
                                        messages.pop(1)
                                        messages.pop(1)
                                    else:
                                        break

                            raw_responses.append(raw_response)

                            if raw_response:
                                messages.append(
                                    {"role": "assistant", "content": raw_response}
                                )

                                parsed_response = parse_response(
                                    raw_response, parse_model_config
                                )
                                parsed_responses.extend(parsed_response.values())

                            else:
                                messages.append(
                                    {"role": "assistant", "content": "No response."}
                                )

                                print(
                                    f"Failed to get response for {exp_name} segment {i} version: {version_name}"
                                )
                                # Don't add anything to parsed_responses for failed responses

                            if TQDM_ACTIVE:
                                inner_pbar.update(1)

                        raw_responses = "\n".join(raw_responses)
                        parsed_responses_dict = {}
                        for i, response in enumerate(parsed_responses):
                            converted_value = safe_int_conversion(response)
                            parsed_responses_dict[str(i)] = converted_value
                            if converted_value is None:
                                logging.warning(
                                    f"Non-numeric response encountered at index {i}: '{response}'"
                                )

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

                elif isinstance(version_text, str):
                    messages = [
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": version_text},
                    ]

                    raw_response = generate_response(messages, model_config)

                    if raw_response:
                        parsed_response = parse_response(
                            raw_response, parse_model_config
                        )

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
                        print(
                            f"Failed to get response for {exp_name} version: {version_name}"
                        )

                pbar.update(1)

    return results
