"""
Code for collecting and visualizing data from experiments
Currently only works for Gerrig data
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import re
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import uuid
import numpy as np


def generate_uid():
    return f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"


# Set up logging
uid = generate_uid()
output_dir = Path("./collected_data") / uid
output_dir.mkdir(parents=True, exist_ok=True)
log_file = output_dir / f"{uid}_data_collector.log"

logger = logging.getLogger("data_collector")
logger.setLevel(logging.DEBUG)
handler = RotatingFileHandler(log_file, maxBytes=1e6, backupCount=5)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Add a console handler to print logs to the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def get_response_limits(paper_name: str, experiment_name: str) -> dict:
    """
    Get the valid response limits for a given paper and experiment.

    Args:
    paper_name (str): The name of the paper (e.g., 'gerrig').
    experiment_name (str): The name of the experiment.

    Returns:
    dict: A dictionary containing the valid ranges for Q1 and Q2.
    """
    limits = {
        "gerrig": {
            "default": {"Q1": (1, 7), "Q2": (1, 7)},
            # Add specific experiments here if they have different ranges
        },
        # Add other papers here
    }

    paper_limits = limits.get(paper_name, {})
    return paper_limits.get(
        experiment_name, paper_limits.get("default", {"Q1": (0, 100), "Q2": (0, 100)})
    )


def validate_response(value: int, valid_range: tuple) -> tuple[int, bool]:
    """
    Validate if a response is within the specified range.

    Args:
    value (int): The response value to validate.
    valid_range (tuple): The valid range for the response (min, max).

    Returns:
    tuple: (validated_value, followed_instructions)
    """
    if (
        value is None
        or np.isnan(value)
        or value < valid_range[0]
        or value > valid_range[1]
    ):
        return None, False
    return value, True


def parse_response(
    response: str, paper_name: str, experiment_name: str
) -> tuple[int, int, bool]:
    """
    Parse the response string and extract values based on the experiment.

    Args:
    response (str): The response string from the language model.
    paper_name (str): The name of the paper (e.g., 'gerrig').
    experiment_name (str): The name of the experiment.

    Returns:
    tuple: (Q1 value, Q2 value, followed instructions)
    """
    limits = get_response_limits(paper_name, experiment_name)
    followed_instructions = True

    if paper_name == "gerrig":
        try:
            response_dict = ast.literal_eval(response)
            if any(key not in ["Q1", "Q2"] for key in response_dict.keys()):
                followed_instructions = False
            q1 = int(float(response_dict.get("Q1", float("nan"))))
            q2 = int(float(response_dict.get("Q2", float("nan"))))
        except (ValueError, SyntaxError):
            numbers = re.findall(r"\d+", response)
            q1 = int(numbers[0]) if len(numbers) > 0 else None
            q2 = int(numbers[1]) if len(numbers) > 1 else None
            followed_instructions = False

        q1, followed_q1 = validate_response(q1, limits["Q1"])
        q2, followed_q2 = validate_response(q2, limits["Q2"])
        followed_instructions = followed_instructions and followed_q1 and followed_q2
    else:
        # Placeholder for other experiments
        q1, q2 = None, None
        followed_instructions = False

    return q1, q2, followed_instructions


def collect_csv_data(
    root_dir: str = "./outputs",
    output_dir: Path = output_dir,
    collection_uid: str = uid,
) -> pd.DataFrame:
    """
    Collect all CSV data from the experiment folders into a single DataFrame.

    Args:
    root_dir (str): The root directory containing the experiment data.
    output_dir (Path): The directory to save the collected data and visualizations.
    collection_uid (str): The unique identifier for this data collection run.

    Returns:
    pd.DataFrame: A DataFrame containing all collected data with additional columns for folder structure information.
    """
    all_data = []
    root_path = Path(root_dir)
    output_path = output_dir
    output_path.mkdir(parents=True, exist_ok=True)

    for path in root_path.rglob("*.csv"):
        relative_path = path.relative_to(root_path)
        parts = relative_path.parts

        paper_name = parts[0].split("_")[0]  # Extract paper name (e.g., 'gerrig')
        experiment_type = parts[1]  # standard or alternative
        decoding_strategy = parts[2]  # creative, deterministic, or general
        model_name = parts[3]
        run_uid = parts[4]

        df = pd.read_csv(path)

        # Rename 'version' to 'experiment_version' if it exists
        if "version" in df.columns:
            df = df.rename(columns={"version": "experiment_version"})

        logger.info(f"Columns in {path}: {df.columns.tolist()}")

        if "response" not in df.columns:
            logger.warning(f"'response' column not found in {path}")
            df["response"] = "No response"
        df["Q1"], df["Q2"], df["FOLLOWED_INSTRUCTIONS"] = zip(
            *df.apply(
                lambda row: parse_response(
                    row["response"], paper_name, row["experiment_name"]
                ),
                axis=1,
            )
        )

        # Only add columns that don't already exist
        if "paper_name" not in df.columns:
            df["paper_name"] = paper_name
        if "experiment_type" not in df.columns:
            df["experiment_type"] = experiment_type
        if "decoding_strategy" not in df.columns:
            df["decoding_strategy"] = decoding_strategy
        if "model_name" not in df.columns:
            df["model_name"] = model_name
        if "run_uid" not in df.columns:
            df["run_uid"] = run_uid
        if "collection_uid" not in df.columns:
            df["collection_uid"] = collection_uid

        all_data.append(df)

        logger.debug(f"Processing file: {path}")
        logger.debug(f"Model name: {model_name}")
        logger.debug(f"Columns after processing: {df.columns.tolist()}")
        logger.debug(f"Sample data:\n{df.head().to_string()}")

    if not all_data:
        logger.error(f"No CSV files found in {root_dir}")
        raise ValueError(f"No CSV files found in {root_dir}")

    combined_df = pd.concat(all_data, ignore_index=True)

    # Remove any unnamed columns
    combined_df = combined_df.loc[:, ~combined_df.columns.str.contains("^Unnamed")]

    # Ensure only 'run_uid' is present, remove 'uid' if it exists
    if "uid" in combined_df.columns:
        combined_df = combined_df.drop(columns=["uid"])

    # Handle null values
    for col in ["Q1", "Q2"]:
        null_counts = (
            combined_df[combined_df[col].isnull()]
            .groupby(["model_name", "run_uid"])
            .size()
        )
        for (model, uid), count in null_counts.items():
            logger.warning(
                f"Found {count} null values in column {col} for model {model} (UID: {uid}). These will be excluded from visualizations."
            )

    combined_df.to_csv(output_dir / "combined_data.csv", index=False)
    logger.info(f"Combined data saved to {output_dir / 'combined_data.csv'}")

    return combined_df


def validate_data(df: pd.DataFrame) -> None:
    expected_columns = [
        "paper_name",
        "experiment_name",
        "experiment_version",
        "experiment_type",
        "decoding_strategy",
        "model_name",
        "run_uid",
        "collection_uid",
        "response",
        "Q1",
        "Q2",
        "FOLLOWED_INSTRUCTIONS",
    ]

    missing_cols = set(expected_columns) - set(df.columns)
    if missing_cols:
        logger.error(f"Missing expected columns: {missing_cols}")
        logger.info(f"Available columns: {df.columns.tolist()}")
        raise ValueError(f"Missing expected columns: {missing_cols}")

    if df.isnull().any().any():
        null_counts = df.isnull().sum()
        logger.warning(
            f"Found null values in the following columns: {null_counts[null_counts > 0].to_dict()}"
        )


def visualize_data(
    df: pd.DataFrame, output_dir: Path = output_dir / "visualizations"
) -> None:
    output_path = output_dir
    output_path.mkdir(parents=True, exist_ok=True)

    sns.set_style("whitegrid")
    sns.set_palette("deep")

    visualizations_created = False

    for experiment_type in df["experiment_type"].unique():
        exp_type_df = df[df["experiment_type"] == experiment_type]
        exp_type_output_dir = output_path / experiment_type
        exp_type_output_dir.mkdir(parents=True, exist_ok=True)

        for experiment_name in exp_type_df["experiment_name"].unique():
            exp_df = exp_type_df[exp_type_df["experiment_name"] == experiment_name]
            exp_output_dir = exp_type_output_dir / experiment_name
            exp_output_dir.mkdir(parents=True, exist_ok=True)

            for question in ["Q1", "Q2"]:
                valid_data = exp_df[exp_df[question].notnull()]
                if valid_data.empty:
                    logger.warning(
                        f"No valid data for {experiment_type} - {experiment_name} - {question}"
                    )
                    continue

                try:
                    plt.figure(figsize=(20, 10))
                    sns.boxplot(x="model_name", y=question, data=valid_data)
                    plt.title(
                        f"{experiment_type.capitalize()} - {experiment_name} - {question} Distribution by Model",
                        fontsize=16,
                    )
                    plt.xlabel("Model", fontsize=12)
                    plt.ylabel(question, fontsize=12)
                    plt.xticks(rotation=90, ha="right", fontsize=8)
                    plt.yticks(fontsize=10)
                    plt.tight_layout()
                    plt.savefig(
                        exp_output_dir / f"{question}_distribution_by_model.png",
                        dpi=300,
                        bbox_inches="tight",
                    )
                    plt.close()
                    visualizations_created = True
                    logger.info(
                        f"Created boxplot for {experiment_type} - {experiment_name} - {question}"
                    )
                except Exception as e:
                    logger.error(
                        f"Error creating boxplot for {experiment_type} - {experiment_name} - {question}: {str(e)}"
                    )

                try:
                    plt.figure(figsize=(20, 12))
                    response_counts = (
                        valid_data.groupby(["model_name", question])
                        .size()
                        .unstack(fill_value=0)
                    )
                    if not response_counts.empty:
                        sns.heatmap(
                            response_counts,
                            annot=True,
                            fmt="d",
                            cmap="YlGnBu",
                            cbar_kws={"label": "Count"},
                        )
                        plt.title(
                            f"{experiment_type.capitalize()} - {experiment_name} - {question} Response Distribution",
                            fontsize=16,
                        )
                        plt.xlabel("Response Value", fontsize=12)
                        plt.ylabel("Model", fontsize=12)
                        plt.xticks(fontsize=10)
                        plt.yticks(fontsize=8, rotation=0)
                        plt.tight_layout()
                        plt.savefig(
                            exp_output_dir / f"{question}_response_heatmap.png",
                            dpi=300,
                            bbox_inches="tight",
                        )
                        plt.close()
                        visualizations_created = True
                        logger.info(
                            f"Created heatmap for {experiment_type} - {experiment_name} - {question}"
                        )
                    else:
                        logger.warning(
                            f"No data for heatmap: {experiment_type} - {experiment_name} - {question}"
                        )
                except Exception as e:
                    logger.error(
                        f"Error creating heatmap for {experiment_type} - {experiment_name} - {question}: {str(e)}"
                    )

    if not visualizations_created:
        logger.warning(
            "No visualization files were generated due to lack of valid data."
        )
    else:
        logger.info(f"All visualizations saved in the '{output_path}' directory.")


def compute_summary_statistics(
    df: pd.DataFrame, output_dir: Path = output_dir
) -> pd.DataFrame:
    """
    Compute summary statistics for the collected data and save to CSV.

    Args:
    df (pd.DataFrame): The DataFrame containing the collected data.
    output_dir (Path): The directory to save the summary statistics.

    Returns:
    pd.DataFrame: A DataFrame containing summary statistics.
    """
    summary = (
        df.groupby(
            [
                "experiment_name",
                "experiment_type",
                "decoding_strategy",
                "model_name",
                "experiment_version",
            ]
        )
        .agg(
            {
                "Q1": ["mean", "median", "std", "min", "max", "count"],
                "Q2": ["mean", "median", "std", "min", "max", "count"],
                "FOLLOWED_INSTRUCTIONS": ["mean", "count"],
            }
        )
        .reset_index()
    )

    summary.columns = ["_".join(col).strip() for col in summary.columns.values]

    output_path = output_dir
    output_path.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_path / "summary_statistics.csv", index=False)
    logger.info("Summary statistics computed and saved to 'summary_statistics.csv'")

    return summary


def main():
    print(f"Starting data collection with UID: {uid}")
    print(f"Output directory: {output_dir}")
    print(f"Log file: {log_file}")

    try:
        df = collect_csv_data(output_dir=output_dir, collection_uid=uid)
        logger.debug(f"Collected data shape: {df.shape}")
        logger.debug(f"Collected data columns: {df.columns.tolist()}")
        logger.debug(f"Sample of collected data:\n{df.head().to_string()}")

        validate_data(df)
        logger.info("Data validation passed.")

        vis_output_dir = output_dir / "visualizations"
        visualize_data(df, output_dir=vis_output_dir)
        logger.info(f"Visualizations saved in the '{vis_output_dir}' directory.")

        # Check if visualizations were created
        vis_files = list(Path(vis_output_dir).rglob("*.png"))
        if vis_files:
            logger.info(f"Generated {len(vis_files)} visualization files.")
        else:
            logger.warning("No visualization files were generated.")

        compute_summary_statistics(df, output_dir=output_dir)
        logger.info("Summary statistics computed and saved to 'summary_statistics.csv'")

        print("\nData collection completed successfully.")
        print(f"Results can be found in: {output_dir}")
        print(f"Log file: {log_file}")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
        print(
            f"\nAn error occurred during data collection. Please check the log file for details: {log_file}"
        )


if __name__ == "__main__":
    main()
