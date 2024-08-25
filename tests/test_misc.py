import json
from pathlib import Path
from unittest.mock import patch


from src.thriller.misc import parse_response, run_experiment


def save_test_output(test_name, output):
    output_dir = Path("Thriller/tests/outputs")
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / f"{test_name}.json", "w") as f:
        json.dump(output, f, indent=2)


def test_parse_response(response):
    parsed = parse_response(response)
    assert parsed


@patch(
    "src.thriller.misc.generate_response",
    return_value="Response for Experiment A Version Pen Removed",
)
@patch("src.thriller.misc.save_raw_api_output")
def test_run_experiment(mock_save_raw_api_output, mock_generate_response):
    experiment_series = "gerrig"
    model_config = {
        "name": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "max_tokens": 50,
        "temperature": 0.7,
        # "top_k": 50,
        # "top_p": 0.9,
        # "repetition_penalty": 1.0,
    }
    prompts = {"Experiment A": "Prompt A"}
    version_prompts = {
        "Experiment A": [
            ("Version A1 Name", "Version A1 Text"),
            ("Version A2 Name", "Version A2 Text"),
        ]
    }

    results = run_experiment(
        Path(experiment_series), model_config, prompts, version_prompts
    )

    assert len(results) == 2
    for result in results:
        assert result["experiment_name"] == "Experiment A"
        assert result["version"] in ["Version A1 Name", "Version A2 Name"]
        assert result["raw_response"] == "Response for Experiment A Version Pen Removed"
        assert (
            result["parsed_response"] == "Response for Experiment A Version Pen Removed"
        )

    assert mock_generate_response.call_count == 2
    assert mock_save_raw_api_output.call_count == 2

    save_test_output(
        "test_run_experiment",
        {
            "experiment_series": experiment_series,
            "model_config": model_config,
            "prompts": prompts,
            "version_prompts": version_prompts,
            "results": results,
        },
    )
