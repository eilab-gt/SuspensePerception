from pathlib import Path
from unittest.mock import patch


# from src.thriller.misc import parse_response
from src.thriller.misc import run_experiment
from src.thriller.utils import save_test_output



# def test_parse_response(response):
#     parsed = parse_response(response)
#     assert parsed


@patch(
    "src.thriller.misc.generate_response",
    return_value="Response for Experiment A Version Pen Removed",
)
@patch("src.thriller.misc.parse_response", return_value={"Q1": "1"})
@patch("src.thriller.misc.save_raw_api_output")
def test_run_experiment(
    mock_save_raw_api_output,
    mock_parse_response,
    mock_generate_response,
):
    experiment_series = "gerrig"
    model_config = {
        "name": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "max_tokens": 50,
        "temperature": 0.7,
        # "top_k": 50,
        # "top_p": 0.9,
        # "repetition_penalty": 1.0,
    }
    parse_model_config = {
        "api_type": "together",
        "name": "parser",
        "max_tokens": 50,
        "temperature": 0.0,
    }
    prompts = {"Experiment A": "Prompt A"}
    version_prompts = {
        "Experiment A": [
            ("Version A1 Name", "Version A1 Text"),
            ("Version A2 Name", "Version A2 Text"),
            ("Version A2 Name", "Version A2 Text"),
        ]
    }

    results = run_experiment(
        Path(experiment_series),
        model_config,
        parse_model_config,
        prompts,
        version_prompts,
    )

    assert len(results) == 3
    for result in results:
        assert result["experiment_name"] == "Experiment A"
        assert result["version"] in ["Version A1 Name", "Version A2 Name"]
        assert result["raw_response"] == "Response for Experiment A Version Pen Removed"
        assert result["parsed_response"] == {"0": 1}

    assert mock_generate_response.call_count == 3
    assert mock_parse_response.call_count == 3
    assert mock_save_raw_api_output.call_count == 3

    save_test_output(
        "test_run_experiment",
        {
            "experiment_series": experiment_series,
            "model_config": model_config,
            "parse_model_config": parse_model_config,
            "prompts": prompts,
            "version_prompts": version_prompts,
            "results": results,
        },
    )
