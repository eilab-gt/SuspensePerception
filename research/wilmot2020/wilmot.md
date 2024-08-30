# Wilmot Dataset Summary

## Overview

This document summarizes the WritingPrompts dataset used for suspense annotation, including details about the data files, annotation process, and key information for working with the data.

## Dataset Information

### Source

- Dataset: WritingPrompts corpus from /r/WritingPrompts subreddit
- Corpus size: Approximately 300,000 short stories
- Split: 90% train, 5% development, 5% test

### Annotated Subset

- 100 stories from development set
- 100 stories from test set
- Story length: 25-75 sentences each
- Estimated total annotated sentences: ~10,000 (assuming average of 50 sentences per story)

## Annotation Process

### Annotators

- 5 master workers from Amazon Mechanical Turk per story

### Annotation Method

- Sentence-by-sentence reading
- Relative suspense judgment for each sentence
- Framed as "dramatic tension" rather than "suspense"
- Character's perspective encouraged

### Suspense Rating Scale

1. Big Decrease (1% of cases)
2. Decrease (11% of cases)
3. Same (50% of cases)
4. Increase (31% of cases)
5. Big Increase (7% of cases)

### Additional Tasks

- Short summary written after completing each story

### Quality Control

- Annotators screened for low agreement (mean α < 0.35)
- Removed if suspiciously low reading times (mean RT < 600 ms per sentence)
- Checked quality of story summaries

### Inter-annotator Agreement

- Development set: α = 0.52
- Test set: α = 0.57

## Data Files

### mturk_sentence_sample.csv

#### Key Columns

- sentence_id: Unique identifier for each sentence
- story_id: Unique identifier for each story
- suspense: Aggregated suspense rating (0-4 scale)
- duration_milliseconds: Time spent judging this sentence
- sentence_len: Length of the sentence
- sentence_num: The number of the sentence within the story
- thought_question: Annotator's thoughts on the story
- summary_question: A brief summary of the story
- rating_question: Overall rating of how interesting the story is (0-4 scale)

### mturk_story_sample.csv

#### Key Columns

- story_id: Unique identifier for each story
- rating_question: Overall rating of how interesting the story is (0-4 scale)
- thought_question: Annotator's thoughts on the entire story
- summary_question: A brief summary of the entire story
- suspense_* columns: Various statistical measures of suspense across all sentences in the story
- duration_milliseconds_* columns: Statistical measures of time spent on judgments
- sentence_len_* columns: Statistical measures of sentence lengths

## Working with the Data

### Accessing Sentence-Level Data

1. Use mturk_sentence_sample.csv
2. Focus on 'story_id', 'sentence_num', and 'suspense' columns
3. The 'suspense' column likely represents the aggregated score from all annotators

### Linking Annotations to Story Text

- Use 'story_id' and 'sentence_num' from mturk_sentence_sample.csv
- Join with story text from evaluation_dataset JSONL files (not provided in samples)

### Analyzing Overall Story Metrics

- Use mturk_story_sample.csv for aggregate statistics and overall ratings

## Additional Notes and Advice

1. The suspense ratings are relative changes, not absolute levels.
2. If an aggregated 'suspense' score is not provided, consider using the median of the five annotators' ratings.
3. Remember that annotators read and rated stories in order, sentence by sentence.
4. The original paper doesn't explicitly mention creating a "gold label" for each sentence's suspense change.
5. The reported percentages of suspense changes are likely based on aggregated labels.
6. Consider reaching out to the paper's authors for clarification on how they aggregated individual annotations into a single label per sentence.
7. When recreating the experiment, ensure to follow the original annotation process closely, including annotator training and quality control measures.

## References

- Fan, A., Lewis, M., & Dauphin, Y. (2018). Hierarchical Neural Story Generation. arXiv preprint arXiv:1805.04833.
- Wilmot, D., & Keller, F. (2020). A Psycholinguistic Model of Suspense. arXiv preprint arXiv:2010.12794.

# Wilmot Dataset Summary - Addendum

This addendum provides additional information about the dataset structure and contents based on the email from the dataset provider.

## Dataset Structure

The dataset is provided as a ZIP file containing several main parts:

### 1. full_dataset

- Contains training, validation, and test splits as JSONL files
- Includes story IDs and sentences
- Some stories don't start at sentence 0 due to initial header removal and quality filtering

### 2. evaluation_dataset

- Contains two subsets:
  a. devset (development set)
  b. withheldset (test set used for final results in the paper)
- Includes story_ids with corresponding sentence_nums that align with the evaluations

### 3. annotations

- Located at `\annotations\witheldset\sentence_annotations_stats` (and a similar path for the devset)
- Contains two main files:
  a. mturk_story.csv
  b. mturk_sentence.csv

#### mturk_story.csv

- Contains aggregate statistics and answers for each story as a whole
- Includes the general question about how interesting the story is (0 = Bad, 4 = Excellent)

#### mturk_sentence.csv

- Contains per-sentence annotations
- Use story_id and sentence_num to join with story text from evaluation_dataset JSONL files
- Suspense judgments scale:
  0 = Major decrease
  2 = Same
  4 = Major increase
- Includes additional data:
  - Sentence time per judgment
  - MTurk metadata (e.g., whether the evaluation was accepted or rejected)
  - Overall judgments about the story used for testing understanding

### 4. Additional Annotation Data

- Not strictly necessary but may be of interest
- Contains various inter-annotator agreement measures
- Includes plots of the annotations as seen in the paper

## Working with the Dataset

1. To access full story text:

   - Use the JSONL files in the full_dataset directory
   - Join with annotation data using story_id and sentence_num
2. For evaluation data:

   - Use the files in the evaluation_dataset directory
   - The withheldset was used for the final results in the paper
3. To analyze annotations:

   - Use mturk_story.csv for story-level data
   - Use mturk_sentence.csv for sentence-level data
   - Join these with the story text using story_id and sentence_num
4. For additional insights:

   - Explore the other directories in the annotations folder for inter-annotator agreement measures and annotation plots

## Notes

- The training data for WritingPrompts is formatted in the same way as the evaluation data
- The dataset includes both the development set (devset) and the final test set (withheldset)
- When working with story text, remember that some stories may not start at sentence 0 due to preprocessing

This addendum provides a more detailed overview of the dataset structure and contents as described in the email. Use this information in conjunction with the main Wilmot Dataset Summary for a comprehensive understanding of the dataset.
