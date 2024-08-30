"""
Code that is explicitly related to the execution and parsing of API calls for experiments
"""
# TODO: move to api.py and utils.py then delete this file

import sys
import typing
from pathlib import Path
from src.thriller.api import generate_response, save_raw_api_output
from together import Together
import re
from tqdm import tqdm
import json
from openai import OpenAI


# Add the project root directory to Python path
project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)


def extract_emotion_class(content: str) -> str:
    """
    Extract the emotion class from the content.

    Args:
        content (str): The content to parse.

    Returns:
        str: The extracted emotion class or the stripped content if not found.
    """
    match = re.search(r"emotion_class:\s*(\w+)", content)
    return match.group(1) if match else content.strip()


def extract_key_value_pairs(content: str) -> dict[str, int]:
    """
    Extract key-value pairs from the content.

    Args:
        content (str): The content to parse.

    Returns:
        dict[str, int]: A dictionary of extracted key-value pairs.
    """
    values = re.findall(r"(\w+):\s*(\d+)", content)
    return {key: int(value) for key, value in values} if values else {}


def extract_single_value(content: str) -> dict[str, int]:
    """
    Extract a single numerical value from the content.

    Args:
        content (str): The content to parse.

    Returns:
        dict[str, int]: A dictionary with a single 'value' key and the extracted integer.
    """
    values = re.findall(r"(\d+)", content)
    return {"value": int(values[0])} if values else {}


def parse_response(
    response: str, model_config: dict[str, typing.Any]
) -> dict[str, str] | str:
    """
    Process a LLM response into a key value pair or string.

    Args:
        response: LLM model's response (see src.thriller.api.generate_response())
        model_config: Dictionary of model parameters.
                      Mandatory parameters are `api_type`, `name`, `max_tokens`, `temperature`

    Returns:
        The parsed response as a dictionary or string.
    """
    api_type = model_config.get("api_type", None)
    prompt = model_config.get("prompt")

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": response},
    ]

    content = ""

    if api_type == "openai":
        client = OpenAI()
        parsed_response = client.chat.completions.create(
            model=model_config["name"],
            messages=messages,
            max_tokens=model_config["max_tokens"],
            temperature=model_config["temperature"],
            top_p=model_config.get("top_p", None),
            frequency_penalty=model_config.get("frequency_penalty", 0),
            presence_penalty=model_config.get("presence_penalty", 0),
        )
        content = parsed_response.choices[0].message.content

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

    # Check if it's the Lee experiment
    if "emotion_class" in prompt.lower():
        return extract_emotion_class(content)

    # For other experiments
    parsed_content = extract_key_value_pairs(content)
    return parsed_content if parsed_content else extract_single_value(content)


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
    version_prompts: dict[str, str | list[str]],
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

                        for i, text_sequence in enumerate(version_text):
                            messages.append({"role": "user", "content": text_sequence})

                            raw_response = generate_response(messages, model_config)
                            raw_responses.append(raw_response)
                            messages.append(
                                {"role": "assistant", "content": raw_response}
                            )

                            if raw_response:
                                parsed_response = parse_response(
                                    raw_response, parse_model_config
                                )
                                parsed_responses.append(parsed_response)

                                # Save individual parsed response
                                save_raw_api_output(
                                    output=json.dumps(parsed_response, indent=2),
                                    filename=f"{exp_name}_{version_name}_segment_{i}_parsed.json",
                                    output_path=output_path / "parsed_outputs",
                                )
                            else:
                                print(
                                    f"Failed to get response for {exp_name} segment {i} version: {version_name}"
                                )
                                parsed_responses.append({})

                            inner_pbar.update(1)

                        raw_responses = "\n".join(raw_responses)
                        if exp_name.lower() == "lee":
                            parsed_responses = [
                                parse_response(response, parse_model_config)
                                for response in raw_responses
                            ]
                        else:
                            parsed_responses = {
                                str(i): int(s)
                                for i, s in enumerate(parsed_responses)
                                if isinstance(s, (int, float))
                            }

                        result = {
                            "experiment_name": exp_name,
                            "version": version_name,
                            "raw_response": raw_responses,
                            "parsed_response": parsed_responses,
                        }

                        results.append(result)

                        save_raw_api_output(
                            output=raw_responses,
                            filename=f"{exp_name}_{version_name.replace(' ', '_')}.json",
                            output_path=output_path / "raw_outputs",
                        )

                        # Save combined parsed responses
                        save_raw_api_output(
                            output=json.dumps(parsed_responses, indent=2),
                            filename=f"{exp_name}_{version_name.replace(' ', '_')}_parsed.json",
                            output_path=output_path / "parsed_outputs",
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
                            filename=f"{exp_name}_{version_name.replace(' ', '_')}.txt",
                            output_path=output_path / "raw_outputs",
                        )

                        # Save parsed response
                        save_raw_api_output(
                            output=json.dumps(parsed_response, indent=2),
                            filename=f"{exp_name}_{version_name.replace(' ', '_')}_parsed.json",
                            output_path=output_path / "parsed_outputs",
                        )

                    else:
                        print(
                            f"Failed to get response for {exp_name} version: {version_name}"
                        )

                pbar.update(1)

    return results
