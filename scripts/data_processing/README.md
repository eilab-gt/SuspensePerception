# Data Processing Scripts

Utility scripts for data processing and visualization for the Suspense Perception experiments.

## Available Scripts

### Core Processing Scripts

- `fix_encoding.py` - Fix text encoding issues in files
- `extract_text.py` - Extract text content from documents
- `parse_adversarial.py` - Parse and analyze adversarial experiment results from CSV files
- `brewer_visualizations.py` - Generate visualizations for Brewer experiment
- `gerrig_visualizations.py` - Generate visualizations for Gerrig experiment
- `lehne_delatorre_visualizations.py` - Generate visualizations for Lehne and Delatorre experiments
- `generate_metrics_table.py` - Generate performance metric tables for all experiments

## Detailed Script Documentation

### parse_adversarial.py

Processes adversarial attack experiment results, calculating mean scores and standard deviations.

**Usage:**
```bash
# Analyze both experiments
python scripts/data_processing/parse_adversarial.py

# Analyze specific experiment
python scripts/data_processing/parse_adversarial.py --target gerrig

# Generate comparison plot
python scripts/data_processing/parse_adversarial.py --plot --save-plot output.png

# Custom directories
python scripts/data_processing/parse_adversarial.py --log-dir ./outputs --output-dir ./results
```

**Features:**
- Automatically finds and parses all adversarial experiment CSV files
- Calculates mean scores and standard deviations for each attack type
- Generates comparison plots between Gerrig and Delatorre experiments
- Exports aggregated results to CSV files

### brewer_visualizations.py

Generates comprehensive visualizations for the Brewer experiment.

**Usage:**
```bash
# Generate all visualizations
python scripts/data_processing/brewer_visualizations.py --plot-type both

# Only evolution plots
python scripts/data_processing/brewer_visualizations.py --plot-type evolution

# Only agreement heatmaps
python scripts/data_processing/brewer_visualizations.py --plot-type agreement
```

**Features:**
- Line plots showing LLM and human ratings evolution across story passages
- Agreement heatmaps showing model-human alignment
- Support for multiple experimental runs with averaging

### gerrig_visualizations.py

Creates visualization analysis for the Gerrig experiment.

**Usage:**
```bash
# Generate all visualizations
python scripts/data_processing/gerrig_visualizations.py --plot-type both

# Model agreement only
python scripts/data_processing/gerrig_visualizations.py --plot-type model

# Attack analysis only
python scripts/data_processing/gerrig_visualizations.py --plot-type attack
```

**Features:**
- Model agreement heatmaps with human baselines
- Attack effect visualizations
- Support for adversarial experiment analysis

### lehne_delatorre_visualizations.py

Flexible visualization script for both Lehne and Delatorre experiments.

**Usage:**
```bash
# Lehne experiment visualizations
python scripts/data_processing/lehne_delatorre_visualizations.py --experiment lehne --plot-type all

# Delatorre experiment visualizations
python scripts/data_processing/lehne_delatorre_visualizations.py --experiment delatorre --plot-type all

# Specific plot types
python scripts/data_processing/lehne_delatorre_visualizations.py --experiment lehne --plot-type agreement
```

**Features:**
- Agreement heatmaps between models and human ratings
- Change direction analysis
- Attack agreement visualizations
- Inflection point analysis for Lehne experiment
- Configurable figure sizes and parameters per experiment

### generate_metrics_table.py

Generates comprehensive performance metric tables across all experiments.

**Usage:**
```bash
# Generate F1 score tables in CSV format
python scripts/data_processing/generate_metrics_table.py --metric-type binary --format csv

# Generate error metrics (L1 distance)
python scripts/data_processing/generate_metrics_table.py --metric-type error --error-metric l1

# Generate all metrics in both CSV and LaTeX formats
python scripts/data_processing/generate_metrics_table.py --metric-type both --format both

# Use different error metrics
python scripts/data_processing/generate_metrics_table.py --error-metric mse  # Mean Squared Error
python scripts/data_processing/generate_metrics_table.py --error-metric rmse # Root Mean Squared Error
```

**Features:**
- Binary classification metrics: accuracy, precision, recall, F1
- Error metrics: MSE, RMSE, L1 distance
- Support for all experiments (Brewer, Gerrig, Lehne, Delatorre)
- Output in CSV and LaTeX formats
- Automatic averaging and standard deviation calculations

## Dependencies

All scripts require the following Python packages:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

## Directory Structure

Scripts expect the following organization:
```
outputs/
├── [experiment]_experiment/
│   ├── final/
│   │   └── [run]/
│   │       └── [model]/
│   │           └── results.csv
│   └── adversarial/
│       └── [attack_type]/
│           └── [run]/
│               └── [model]/
│                   └── results.csv
```

Results are saved to:
```
analysis_results/
├── adversarial/
├── brewer/
├── gerrig/
├── lehne/
├── delatorre/
└── tables/
```

## Common Options

Most scripts support these common arguments:
- `--output-dir`: Base directory containing experiment outputs
- `--save-dir`: Directory to save generated files
- `--plot-type` or `--metric-type`: Type of output to generate

## Running Scripts with uv

If using `uv` for Python environment management:
```bash
uv run python scripts/data_processing/[script_name].py [options]
```