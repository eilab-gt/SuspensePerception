import json
import sys
from pathlib import Path
from unittest.mock import call, mock_open, patch

import pandas as pd
import pytest
import yaml

sys.path.append(str(Path(__file__).resolve().parent.parent) + "/src")

from src.thriller.utils import (
    load_config,
    process_and_save_results,
    save_raw_api_output,
)


def test_load_config():
    config_yaml = """
    model:
      name: gpt-3
      max_tokens: 50
      temperature: 0.7
      top_k: 50
      top_p: 0.9
      repetition_penalty: 1.0
    """
    with patch("builtins.open", mock_open(read_data=config_yaml)):
        config = load_config("config.yaml")
        assert config["model"]["name"] == "gpt-3"


@patch("builtins.open", new_callable=mock_open)
@patch("pathlib.Path.mkdir")
def test_save_raw_api_output(mock_mkdir, mock_file):
    output = {"response": "test"}
    save_raw_api_output(output=output, filename="test.json", output_path="./outputs/")

    # The write method is called multiple times; verify each call
    expected_calls = [
        call().write("{\n"),
        call().write('  "response": "test"\n'),
        call().write("}"),
    ]

    # Adjust the expected calls to match the actual behavior of json.dump
    actual_calls = [
        call().write("{"),
        call().write("\n  "),
        call().write('"response"'),
        call().write(": "),
        call().write('"test"'),
        call().write("\n"),
        call().write("}"),
    ]

    mock_file().write.assert_has_calls(actual_calls, any_order=True)


@patch("pandas.DataFrame.to_csv")
@patch("pandas.DataFrame.to_parquet")
def test_process_and_save_results(mock_to_parquet, mock_to_csv):
    results = [
        {
            "experiment_name": "Experiment A",
            "version": 0,
            "parsed_response": "Response A0",
        },
        {
            "experiment_name": "Experiment A",
            "version": 1,
            "parsed_response": "Response A1",
        },
    ]
    df = process_and_save_results(results=results, output_path="./outputs/gerrig_experiment")
    assert isinstance(df, pd.DataFrame)
    mock_to_csv.assert_called_once_with(Path("output/results.csv"), index=False)
    mock_to_parquet.assert_called_once_with(Path("output/results.parquet"), index=False)
