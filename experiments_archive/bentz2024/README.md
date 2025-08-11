# Bentz 2024 - Real-Time Suspense Measurement

This experiment explores real-time suspense measurement using the German story "Die Brasilianische Katze" (The Brazilian Cat).

## Contents

### Research Paper
- `Bentz 2024 Measuring Suspense in Real Time - A New Experimental Methodology.pdf`

### Data Files
- `Katze_suspense_data.csv.gz` - Compressed word-level suspense ratings
- `Katze_aligned.txt` - Aligned text passages
- `Katze_text_lines.txt` - Individual text lines
- `Katze_text_lines_suspense.txt` - Suspense ratings per line
- `Katze_suspense_data_export.txt` - Exported paragraph text
- `line_file_cats.csv` - Line categorization data
- `katze_results.zip` - Additional results archive
- `data_explanation.txt` - Documentation of data format

### Processing Scripts
- `encoding_fixer.py` - Fixes Unicode encoding issues in German text
- `extract_text.py` - Extracts paragraphs from CSV data
- `get_sentence_suspense.py` - Calculates sentence-level suspense from word-level data

## Note
This experiment was not fully implemented in the main codebase but provides valuable data on real-time suspense measurement methodology.