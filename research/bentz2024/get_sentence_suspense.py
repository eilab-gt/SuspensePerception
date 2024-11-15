#!/usr/bin/env python3

import pandas as pd

def get_average_suspense_of_word(df: pd.DataFrame, number: int):
    filtered_df = df[df['number'] == number]
    average_suspense = filtered_df['suspense'].mean()
    return average_suspense

def get_sentence_suspense(text_path: str, csv_path: str, out_path: str) -> None:
    """
    Get the average suspense of the given sentence
    Args:
        text_path: path to the text filing storing the sentences
        csv_path: path to the CSV storing the word-level sentence
        out_path: path to store the suspense output
    """
    with open(text_path, "r", encoding="utf-8") as f:
        passages = f.read().strip().split("\n\n")

    i = 0
    df = pd.read_csv(csv_path)
    df["suspense"] = pd.to_numeric(df["suspense"])

    avg_suspenses = []

    for passage in passages:
        
        suspenses = []

        words = passage.split(" ")
        for word in words:
            if word == df["text"][i]:
                suspense = get_average_suspense_of_word(df, df["number"][i])
                suspenses.append(suspense)
                i += 1
        
        avg_suspense = sum(suspenses) / len(suspenses) if len(suspenses) > 0 else 0
        avg_suspenses.append(avg_suspense)

    with open(out_path, "w", encoding="utf-8") as f:
        for avg_suspense in avg_suspenses:
            f.write(f"{avg_suspense}\n")

if __name__ == "__main__":
    get_sentence_suspense("Katze_aligned.txt", "Katze_suspense_data.csv", "Katze_text_lines_suspense.txt")
