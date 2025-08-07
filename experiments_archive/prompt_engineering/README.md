# Prompt Engineering Experiment Archive

**Status**: Archived | **Last Active**: March 2025 | **Author**: Zini Chakraborty

## Overview

This experiment tested variations in prompt formulations for the DeLaTorre experiment to explore how different prompt structures affect model responses.

## Experiment Details

### Purpose
Testing modified prompts to potentially improve model performance on suspense/thriller narrative analysis tasks.

### Models Tested
- Qwen_Qwen2-72B-Instruct
- deepseek-ai_DeepSeek-V3
- google_gemma-2-27b-it
- google_gemma-2-9b-it
- meta-llama variants
- microsoft_WizardLM-2-8x22B
- mistralai variants

### Code Changes
The experiment involved minimal code modifications:
- `delatorre.yaml`: Modified prompt configuration (1 line)
- `src/thriller/delatorre.py`: 4 line changes for prompt handling
- `src/thriller/lehne.py`: 2 line changes
- `requirements.txt`: 6 dependency updates

See `code_changes.patch` for the exact modifications.

### Results
- **Output Files**: 90+ experimental outputs across multiple models
- **Conditions Tested**: 
  - Journalistic vs Novel narrative styles
  - Good vs Bad outcomes
  - Revealed vs Not Revealed information

### Key Findings
The experiment generated extensive outputs but appears to have been exploratory without definitive conclusions documented.

## Archive Contents

```
prompt_engineering/
├── README.md              # This file
├── code_changes.patch     # Git diff of code modifications
├── commit_history.txt     # Full commit history
└── output_files_sample.txt # Sample list of output files
```

## Git History

Original branch: `origin/prompt-engineering`
Merged with: `--strategy=ours` to preserve history without affecting main codebase
Commit: 8b048e23fd23850b09ce7d3280dfa82f1eb2e594

## Notes

- This was primarily an output-generating experiment rather than a code development branch
- The actual experimental outputs were not archived due to volume (90+ files)
- The code changes were minimal and exploratory in nature
- No significant algorithmic or architectural changes were made

## How to Reproduce

1. Apply the patch file to see code changes:
   ```bash
   git apply experiments_archive/prompt_engineering/code_changes.patch
   ```

2. The modified prompts focused on adjusting the framing and instructions given to models

3. Results suggested some variation in model outputs but no breakthrough improvements

## Decision to Archive

This branch was archived rather than merged because:
- The changes were experimental and incomplete
- No clear performance improvements were documented
- The primary value was in learning what prompt variations don't significantly help
- The volume of outputs didn't justify preservation