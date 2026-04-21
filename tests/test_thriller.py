from unittest.mock import patch


from src.thriller.Thriller import main as main_func
from src.thriller.Thriller import parse_arguments
from src.thriller.Thriller import run_config
from src.thriller.utils import save_test_output


@patch("src.thriller.Thriller.run_experiment", return_value=[])
@patch("src.thriller.Thriller.process_and_save_results")
@patch("src.thriller.Thriller.write_prompt_snapshots")
@patch("src.thriller.Thriller.load_config")
@patch("src.thriller.Thriller.os.getenv")
def test_thriller(
    mock_getenv,
    mock_load_config,
    mock_write_prompt_snapshots,
    mock_process_and_save_results,
    mock_run_experiment,
):
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
        "parse_model": {
            "api_type": "together",
            "name": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            "prompt": "Parse the response.",
            "max_tokens": 50,
            "temperature": 0.0,
            "top_p": 0.9,
            "repetition_penalty": 1.0,
        },
        "experiment": {
            "experiment_series": "gerrig",
            "use_alternative": False,
            "output_dir": "./outputs/",
        },
        "augmentation": {"augmentation_order": []},
    }
    mock_load_config.return_value = mock_config

    test_args = [
        "--config",
        "config.yaml",
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
    mock_write_prompt_snapshots.assert_called_once()


@patch("src.thriller.Thriller.run_experiment")
@patch("src.thriller.Thriller.write_prompt_snapshots")
@patch("src.thriller.Thriller.os.getenv")
def test_run_config_dry_run_skips_writes_and_execution(
    mock_getenv,
    mock_write_prompt_snapshots,
    mock_run_experiment,
):
    mock_getenv.return_value = "TOGETHER_API_KEY"
    config = {
        "model": {
            "api_type": "together",
            "name": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            "max_tokens": 50,
            "temperature": 0.7,
            "top_k": 50,
            "top_p": 0.9,
            "repetition_penalty": 1.0,
        },
        "parse_model": {
            "api_type": "together",
            "name": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            "prompt": "Parse the response.",
            "max_tokens": 50,
            "temperature": 0.0,
            "top_p": 0.9,
            "repetition_penalty": 1.0,
        },
        "experiment": {
            "experiment_series": "gerrig",
            "use_alternative": False,
            "output_dir": "./outputs/",
        },
        "augmentation": {"augmentation_order": []},
    }

    output_paths = run_config(config, write_prompts=False, dry_run=True)

    assert output_paths == []
    mock_write_prompt_snapshots.assert_not_called()
    mock_run_experiment.assert_not_called()



def test_parse_arguments():
    save_test_output(
        "test_parse_arguments_input",
        {
            "test_args": [
                "--config",
                "configs/gerrig.yaml",
                "--overrides",
                "model.temperature=0.7",
            ]
        },
    )
    test_args = [
        "--config",
        "configs/gerrig.yaml",
        "--overrides",
        "model.temperature=0.7",
    ]

    with patch("sys.argv", ["pytest"] + test_args):
        args = parse_arguments()

    assert args.config == "configs/gerrig.yaml"
    assert args.overrides == ["model.temperature=0.7"]
