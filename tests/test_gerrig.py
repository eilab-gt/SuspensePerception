from pathlib import Path
from unittest.mock import patch

import pytest

from src.thriller.gerrig import (
    alternative_substitutions,
    apply_substitutions,
    default_substitutions,
    generate_experiment_texts,
)
from src.thriller.misc import run_experiment


def test_apply_substitutions():
    template = "This is a {test}."
    substitutions = {"test": "success"}
    result = apply_substitutions(template, substitutions)
    assert result == "This is a success."


def test_generate_default_experiment_texts():
    prompts, version_prompts = generate_experiment_texts(default_substitutions)
    assert "{hero_lastname}" not in prompts["Experiment A"]
    assert "{villain}" not in prompts["Experiment A"]
    assert "{author_firstname}" not in prompts["Experiment A"]
    assert "Bond" in prompts["Experiment A"]
    assert "Le Chiffre" in prompts["Experiment A"]
    assert "Casino Royale" in prompts["Experiment A"]


def test_generate_alternative_experiment_texts():
    prompts, version_prompts = generate_experiment_texts(alternative_substitutions)
    assert "{hero_lastname}" not in prompts["Experiment A"]
    assert "{villain}" not in prompts["Experiment A"]
    assert "{author_firstname}" not in prompts["Experiment A"]
    assert "Mers" in prompts["Experiment A"]
    assert "Chifrex" in prompts["Experiment A"]
    assert "Meeting at Midnight" in prompts["Experiment A"]


def test_version_prompts_default():
    prompts, version_prompts = generate_experiment_texts(default_substitutions)

    for versions in version_prompts.values():
        for version_name, version_text in versions:
            assert "{hero_lastname}" not in version_text
            assert "{villain}" not in version_text
            assert "Bond" in version_text or "James" in version_text
            assert "Le Chiffre" in version_text or "Blofeld" in version_text

def test_version_prompts_alternative():
    prompts, version_prompts = generate_experiment_texts(alternative_substitutions)

    for versions in version_prompts.values():
        for version_name, version_text in versions:
            assert "{hero_lastname}" not in version_text
            assert "{villain}" not in version_text
            assert "Mers" in version_text or "Charles" in version_text
            assert "Chifrex" in version_text or "Kalweitz" in version_text


# Mock data for the `gerrig` experiment
prompts = {
    "Experiment A": "Experiment A prompt",
    "Experiment B": "Experiment B prompt",
    "Experiment C": "Experiment C prompt",
}

# Update mock data
version_prompts = {
    "Experiment A": [
        ("Pen Not Mentioned", "Experiment A version 1"),
        ("Pen Mentioned Removed", "Experiment A version 2"),
        ("Pen Mentioned Not Removed", "Experiment A version 3"),
    ],
    "Experiment B": [
        ("Unused Comb", "Experiment B version 1"),
        ("Used Comb", "Experiment B version 2"),
    ],
    "Experiment C": [
        ("Prior Solution Not Mentioned", "Experiment C version 1"),
        ("Prior Solution Mentioned and Removed", "Experiment C version 2"),
        ("Prior Solution Mentioned Not Removed", "Experiment C version 3"),
    ],
}

# Mock responses for each prompt and version
mock_responses = {
    ("Experiment A", "Pen Not Mentioned"): "Response for Experiment A version 1",
    ("Experiment A", "Pen Mentioned Removed"): "Response for Experiment A version 2",
    ("Experiment A", "Pen Mentioned Not Removed"): "Response for Experiment A version 3",
    ("Experiment B", "Unused Comb"): "Response for Experiment B version 1",
    ("Experiment B", "Used Comb"): "Response for Experiment B version 2",
    ("Experiment C", "Prior Solution Not Mentioned"): "Response for Experiment C version 1",
    ("Experiment C", "Prior Solution Mentioned and Removed"): "Response for Experiment C version 2",
    ("Experiment C", "Prior Solution Mentioned Not Removed"): "Response for Experiment C version 3",
}

def mock_generate_response(messages, model_config):
    exp_name = messages[0]["content"].split(" prompt")[0].strip()
    version_text = messages[1]["content"]
    for version_name, v_text in version_prompts[exp_name]:
        if v_text == version_text:
            response = mock_responses.get((exp_name, version_name), "")
            return f"Response: {response}"  # Add a key that can be parsed
    return ""

@patch("src.thriller.misc.generate_response", side_effect=mock_generate_response)
@patch("src.thriller.misc.save_raw_api_output")
def test_run_experiment(mock_save_raw_api_output, mock_generate_response):
    model_config = {
        "name": "gpt-3",
        "max_tokens": 50,
        "temperature": 0.7,
        "top_k": 50,
        "top_p": 0.9,
        "repetition_penalty": 1.0,
    }
    output_path = Path("/fake/path")

    results = run_experiment(output_path, model_config, prompts, version_prompts)

    expected_results = [
        {
            "experiment_name": "Experiment A",
            "version": "Pen Not Mentioned",
            "raw_response": "Response: Response for Experiment A version 1",
            "parsed_response": {"Response": "Response for Experiment A version 1"},
        },
        {
            "experiment_name": "Experiment A",
            "version": "Pen Mentioned Removed",
            "raw_response": "Response: Response for Experiment A version 2",
            "parsed_response": {"Response": "Response for Experiment A version 2"},
        },
        {
            "experiment_name": "Experiment A",
            "version": "Pen Mentioned Not Removed",
            "raw_response": "Response: Response for Experiment A version 3",
            "parsed_response": {"Response": "Response for Experiment A version 3"},
        },
        {
            "experiment_name": "Experiment B",
            "version": "Unused Comb",
            "raw_response": "Response: Response for Experiment B version 1",
            "parsed_response": {"Response": "Response for Experiment B version 1"},
        },
        {
            "experiment_name": "Experiment B",
            "version": "Used Comb",
            "raw_response": "Response: Response for Experiment B version 2",
            "parsed_response": {"Response": "Response for Experiment B version 2"},
        },
        {
            "experiment_name": "Experiment C",
            "version": "Prior Solution Not Mentioned",
            "raw_response": "Response: Response for Experiment C version 1",
            "parsed_response": {"Response": "Response for Experiment C version 1"},
        },
        {
            "experiment_name": "Experiment C",
            "version": "Prior Solution Mentioned and Removed",
            "raw_response": "Response: Response for Experiment C version 2",
            "parsed_response": {"Response": "Response for Experiment C version 2"},
        },
        {
            "experiment_name": "Experiment C",
            "version": "Prior Solution Mentioned Not Removed",
            "raw_response": "Response: Response for Experiment C version 3",
            "parsed_response": {"Response": "Response for Experiment C version 3"},
        },
    ]

    assert results == expected_results
    assert mock_generate_response.call_count == 8
    assert mock_save_raw_api_output.call_count == 8
    
if __name__ == "__main__":
    pytest.main([__file__])
