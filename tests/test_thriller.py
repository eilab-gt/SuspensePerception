import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent) + "/src")

from thriller import main as main_func, parse_arguments


@patch("thriller.run_experiment")
@patch("thriller.process_and_save_results")
@patch("thriller.load_config", return_value={})
@patch("os.getenv", return_value="dummy_api_key")
@patch("thriller.Path.mkdir")
def test_thriller(
    mock_mkdir,
    mock_getenv,
    mock_load_config,
    mock_process_and_save_results,
    mock_run_experiment,
):
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
        main_func(args)

    mock_run_experiment.assert_called_once()
    mock_process_and_save_results.assert_called_once()


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
