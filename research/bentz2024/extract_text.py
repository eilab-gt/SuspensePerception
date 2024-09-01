#!/usr/bin/env python3

import pandas as pd

def extract_text(in_file: str, out_file: str) -> None:
    """
    Extract text from CSV
    Args:
        in_file: filepath of the file to fix
        out_file: filepath of where to save the fixed file
    """
    df = pd.read_csv(in_file)[:7339]

    paragraphs_df = df.groupby('paragraph')['text'].apply(list).reset_index().sort_values('paragraph')

    print(paragraphs_df)

    paragraphs = ""

    for index, row in paragraphs_df.iterrows():
        paragraph = " ".join(row['text'])
        paragraphs += paragraph + "\n\n"

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(paragraphs)

if __name__ == "__main__":
    extract_text("Katze_suspense_data.csv", "Katze_suspense_data_export.txt")
