import yaml
import json
from pathlib import Path
import pandas as pd


def load_config(config_path):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def save_raw_api_output(output, filename, output_dir):
    raw_output_dir = Path(output_dir) / "raw_outputs"
    raw_output_dir.mkdir(parents=True, exist_ok=True)

    with open(raw_output_dir / filename, "w") as f:
        json.dump(output, f, indent=2)


def process_and_save_results(results, output_dir):
    data = []
    for result in results:
        quantitative_info = extract_quantitative_info(result["parsed_response"])
        data.append(
            {
                "story_id": result["story_id"],
                "question_id": result["question_id"],
                "character": quantitative_info["character"],
                "emotion": quantitative_info["emotion"],
                "intensity": quantitative_info["intensity"],
                "explanation": result["parsed_response"].get("Explanation", ""),
            }
        )

    df = pd.DataFrame(data)

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path / "results.csv", index=False)
    df.to_parquet(output_path / "results.parquet", index=False)

    return df


def extract_quantitative_info(parsed_response):
    quantitative_info = {
        "character": parsed_response.get("Character", ""),
        "emotion": parsed_response.get("Emotion", ""),
        "intensity": parsed_response.get("Intensity", ""),
    }

    try:
        quantitative_info["intensity"] = float(quantitative_info["intensity"])
    except ValueError:
        pass

    return quantitative_info
