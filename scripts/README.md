# Scripts

This directory contains utility scripts for running experiments and managing the project.

## Benchmark runner

`run_benchmark.py` plans and runs paper-style benchmark suites with explicit
model overrides, repeat-aware output directories, manifest files, and safety
checks for partial outputs.

Preview the Qwen final-main plan without writing outputs:

```bash
uv run python scripts/run_benchmark.py --suite final-main --dry-run
```

Run with API preflight and resume support:

```bash
uv run python scripts/run_benchmark.py --suite final-main --preflight-api --resume
```

## Directories

### slurm/
High-performance computing (HPC) job submission scripts for SLURM workload manager.

- `autoslurm.sh` - Batch submission script for running multiple experiments with different augmentations
- `entrypoint.sh` - SLURM job configuration and Python execution wrapper

These scripts are designed for running experiments on HPC clusters with SLURM scheduling.

### data_processing/
Data preprocessing and analysis scripts from various experiments.

#### Bentz2024 Scripts
- `bentz2024_encoding_fixer.py` - Fixes Unicode encoding issues in German text files
- `bentz2024_extract_text.py` - Extracts and combines paragraphs from CSV data
- `bentz2024_get_sentence_suspense.py` - Calculates sentence-level suspense from word-level ratings

Note: These scripts were originally part of the Bentz2024 experiment for processing German suspense data.
