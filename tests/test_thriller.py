import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from together.error import AuthenticationError

from src.thriller.Thriller import main as main_func
from src.thriller.Thriller import parse_arguments
from src.thriller.utils import save_test_output


@patch("together.Together")
@patch("src.thriller.misc.run_experiment")
@patch("src.thriller.utils.process_and_save_results")
@patch("src.thriller.utils.load_config")
@patch("os.getenv")
def test_thriller(
    mock_together,
    mock_getenv,
    mock_load_config,
    mock_process_and_save_results,
    mock_run_experiment,
):
    # Mock the API key in the environment
    mock_together_instance = MagicMock()
    mock_together.return_value = mock_together_instance
    mock_together_instance.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="This is a mocked response."))]
    )
    mock_getenv.return_value = "TOGETHER_API_KEY"
    mock_config = {
        "model": {
            "api_type": "together",
            "name": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            "max_tokens": 50,
            "temperature": 0.7,
            "top_k": 50,
            "top_p": 0.9,
            "repetition_penalty": 1.0,
        },
        "experiment": {
            "experiment_series": "gerrig",
            "output_dir": "./outputs/",
        },
    }
    mock_load_config.return_value = mock_config

    test_args = [
        "--config",
        "config.yaml",
        "--api_type",
        "together",
        "--model",
        "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "--max_tokens",
        "50",
        "--temperature",
        "0.7",
        "--top_k",
        "50",
        "--top_p",
        "0.9",
        "--repetition_penalty",
        "1.0",
        "--experiment_series",
        "gerrig",
        "--output_dir",
        "./outputs/",
    ]

    with patch("sys.argv", ["pytest"] + test_args):
        args = parse_arguments()

        save_test_output(
            "test_thriller_input", {"args": vars(args), "mock_config": mock_config}
        )

        main_func(args)

    # Assert that the configuration was loaded
    mock_load_config.assert_called_once()
    # Assert that run_experiment was called
    mock_run_experiment.assert_called_once()
    call_args = mock_run_experiment.call_args[1]
    assert "model_config" in call_args
    assert call_args["model_config"]["api_key"] == "TOGETHER_API_KEY"
    assert call_args["model_config"]["api_type"] == "together"
    mock_process_and_save_results.assert_called_once()

    # The following assertions are not be relevant while an API key error is to be expected.
    # Uncomment to check these even when an error is raised, or once I figure out how to auth to API w/o incurring cost
    # # Assert that the configuration was loaded
    # mock_load_config.assert_called_once()
    # # Assert that run_experiment was called
    # mock_run_experiment.assert_called_once()
    # call_args = mock_run_experiment.call_args[1]
    # assert 'model_config' in call_args
    # assert call_args['model_config']['api_key'] == "TOGETHER_API_KEY"
    # assert call_args['model_config']['api_type'] == "together"
    # mock_process_and_save_results.assert_called_once()


def test_parse_arguments():
    save_test_output(
        "test_parse_arguments_input",
        {
            "test_args": [
                "--model",
                "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
                "--max_tokens",
                "50",
                "--temperature",
                "0.7",
                "--top_k",
                "50",
                "--top_p",
                "0.9",
                "--repetition_penalty",
                "1.0",
                "--experiment_series",
                "gerrig",
                "--output_dir",
                "./outputs/",
            ]
        },
    )
    test_args = [
        "--model",
        "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "--max_tokens",
        "50",
        "--temperature",
        "0.7",
        "--top_k",
        "50",
        "--top_p",
        "0.9",
        "--repetition_penalty",
        "1.0",
        "--experiment_series",
        "gerrig",
        "--output_dir",
        "./outputs/",
    ]

    with patch("sys.argv", ["pytest"] + test_args):
        args = parse_arguments()

    assert args.model == "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
    assert args.max_tokens == 50
    assert args.temperature == 0.7
    assert args.top_k == 50
    assert args.top_p == 0.9
    assert args.repetition_penalty == 1.0
    assert args.experiment_series == "gerrig"
    assert args.output_dir == "./outputs/"
