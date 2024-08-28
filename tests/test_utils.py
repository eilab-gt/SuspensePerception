import sys
from pathlib import Path
from unittest.mock import mock_open, patch

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent) + "/src")

from src.thriller.utils import load_config, process_and_save_results


def test_load_config():
    config_yaml = """
    model:
      name: gpt-3
      max_tokens: 50
      temperature: 0.0
      top_p: 0.9
      repetition_penalty: 1.0
    """
    with patch("builtins.open", mock_open(read_data=config_yaml)):
        config = load_config("config.yaml")
        assert config["model"]["name"] == "gpt-3"


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
    df = process_and_save_results(results=results, output_path="./outputs/")
    assert isinstance(df, pd.DataFrame)
    mock_to_csv.assert_called_once_with(Path("outputs/results.csv"), index=False)
    mock_to_parquet.assert_called_once_with(
        Path("outputs/results.parquet"), index=False
    )
