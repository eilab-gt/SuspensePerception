import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.thriller.misc import parse_response, run_experiment

# sys.path.append(str(Path(__file__).resolve().parent.parent) + "/src")


def test_parse_response():
    response = """
    Character: James Bond
    Emotion: Determined
    Intensity: High
    Explanation: Bond is focused on escaping.
    """
    parsed = parse_response(response)
    assert parsed == {
        "Character": "James Bond",
        "Emotion": "Determined",
        "Intensity": "High",
        "Explanation": "Bond is focused on escaping.",
    }


@patch(
    "src.thriller.misc.generate_response",
    return_value="Character: James Bond\nEmotion: Determined\nIntensity: High\nExplanation: Bond is focused on escaping.",
)
@patch("src.thriller.misc.save_raw_api_output")
def test_run_experiment(mock_save_raw_api_output, mock_generate_response):
    experiment_series = "gerrig"
    model_config = {
        "name": "gpt-3",
        "max_tokens": 50,
        "temperature": 0.7,
        "top_k": 50,
        "top_p": 0.9,
        "repetition_penalty": 1.0,
    }
    prompts = {"Experiment A": "Prompt A"}
    version_prompts = {"Experiment A": ["Version A1", "Version A2"]}

    results = run_experiment(experiment_series, model_config, prompts, version_prompts)

    assert len(results) == 2
    assert results[0]["experiment_name"] == "Experiment A"
    assert results[0]["version"] == 0
    assert results[0]["parsed_response"] == {
        "Character": "James Bond",
        "Emotion": "Determined",
        "Intensity": "High",
        "Explanation": "Bond is focused on escaping.",
    }

    mock_save_raw_api_output.assert_called()
