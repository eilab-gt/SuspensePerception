from pathlib import Path
from .together import generate_response, format_system_message, format_user_message
from .utils import save_raw_api_output


def parse_response(response):
    if not response:
        return {}
    lines = response.split("\n")
    parsed = {}
    current_key = None
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key in ["Character", "Emotion", "Intensity", "Explanation"]:
                current_key = key
                parsed[current_key] = value
        elif current_key == "Explanation":
            parsed[current_key] += " " + line.strip()
    return parsed


def generate_questions(story):
    # This is a placeholder. In a real implementation, you might use NLP techniques
    # to generate questions about character emotions based on the story content.
    return [
        "How does James Bond feel after being captured by Le Chiffre?",
        "What is Vesper's emotional state during their captivity?",
        "How does Le Chiffre feel about his plan to extract information from Bond?",
    ]


def run_experiment(config):
    with open(config["experiment"]["story_file"], "r") as f:
        story = f.read()

    experiment_A_prompt = """The following is an excerpt from Fleming's first James Bond novel, "Casino Royale". In this book, Bond has been assigned to 'ruin' a criminal figure named Le Chiffre by, as it happens, causing Le Chiffre to lose a considerable amount of money gambling. Along the way, Bond has acquired a lady interest named Vesper. Although Bond has, in fact, brought about the gambling losses, Le Chiffre has laid a successful trap for Bond. Bond and Vesper are now the prisoners of Le Chiffre and his two gunmen.

{STORY}

Based on this excerpt, answer the following question about the characters' emotions:"""

    results = []
    for i, question in enumerate(generate_questions(story)):
        print(f"Processing question {i+1}")
        messages = [
            format_system_message(experiment_A_prompt.format(STORY=story)),
            format_user_message(question),
        ]

        raw_response = generate_response(messages, config["model"])
        if raw_response:
            parsed_response = parse_response(raw_response)

            result = {
                "story_id": "casino_royale",
                "question_id": i,
                "raw_response": raw_response,
                "parsed_response": parsed_response,
            }

            results.append(result)

            save_raw_api_output(
                raw_response, f"response_{i}.json", config["experiment"]["output_dir"]
            )
        else:
            print(f"Failed to get response for question {i+1}")

    return results
