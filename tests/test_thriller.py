import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from together.error import AuthenticationError

from src.thriller.Thriller import main as main_func
from src.thriller.Thriller import parse_arguments


@patch("src.thriller.misc.run_experiment")
@patch("src.thriller.utils.process_and_save_results")
@patch("src.thriller.utils.load_config", return_value={})
@patch("os.getenv", return_value="dummy_api_key")
def test_thriller(
    mock_getenv,
    mock_load_config,
    mock_process_and_save_results,
    mock_run_experiment,
):
    mock_config = {
        "api_type": "together",
        "api_key": "dummy_api_key",
        "model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "max_tokens": 50,
        "temperature": 0.7,
        "top_k": 50,
        "top_p": 0.9,
        "repetition_penalty": 1.0,
    }
    mock_load_config.return_value = mock_config

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
        "./output",
    ]

    with patch("sys.argv", ["pytest"] + test_args):
        args = parse_arguments()

        # Use pytest.raises to catch the AuthenticationError
        with pytest.raises(AuthenticationError):
            main_func(args)

    # The following assertions are not be relevant while an API key error is to be expected.
    # Uncomment to check these even when an error is raised, or once I figure out how to auth to API w/o incurring cost
    # # Assert that the configuration was loaded
    # mock_load_config.assert_called_once()
    # # Assert that run_experiment was called
    # mock_run_experiment.assert_called_once()
    # call_args = mock_run_experiment.call_args[1]
    # assert 'model_config' in call_args
    # assert call_args['model_config']['api_key'] == "dummy_api_key"
    # assert call_args['model_config']['api_type'] == "together"
    # mock_process_and_save_results.assert_called_once()


def test_parse_arguments():
    test_args = [
        "--model",
        "gpt-3",
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
        "./output",
    ]

    with patch("sys.argv", ["pytest"] + test_args):
        args = parse_arguments()

    assert args.model == "gpt-3"
    assert args.max_tokens == 50
    assert args.temperature == 0.7
    assert args.top_k == 50
    assert args.top_p == 0.9
    assert args.repetition_penalty == 1.0
    assert args.experiment_series == "gerrig"
    assert args.output_dir == "./output"
