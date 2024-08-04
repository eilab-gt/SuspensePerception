from api import generate_response
from gerrig import generate_experiment_texts
from utils import save_raw_api_output


def parse_response(response):
    if not response:
        return {}
    lines = response.split("\n")
    parsed = {}
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            parsed[key.strip()] = value.strip()
    return parsed


def format_system_message(message):
    return {"role": "system", "content": message}


def format_user_message(message):
    return {"role": "user", "content": message}


def run_experiment(experiment_series, model_config, prompts, version_prompts):
    results = []

    for exp_name, prompt in prompts.items():
        print(f"Running experiment: {exp_name}")
        for i, version in enumerate(version_prompts[exp_name]):
            messages = [format_system_message(prompt), format_user_message(version)]

            raw_response = generate_response(messages, model_config)
            if raw_response:
                parsed_response = parse_response(raw_response)

                result = {
                    "experiment_name": exp_name,
                    "version": i,
                    "raw_response": raw_response,
                    "parsed_response": parsed_response,
                }

                results.append(result)

                save_raw_api_output(
                    raw_response, f"{exp_name}_version_{i}.json", experiment_series
                )
            else:
                print(f"Failed to get response for {exp_name} version {i}")

    return results
