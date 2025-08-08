# Configuration Files

This directory contains all experiment configuration files in YAML format.

## Experiment Configs

### Main Experiments
- `gerrig.yaml` - Gerrig 1994 experiment configuration
- `brewer.yaml` - Brewer 1986 experiment configuration  
- `delatorre.yaml` - Delatorre 2018 experiment configuration
- `lehne.yaml` - Lehne 2015 experiment configuration
- `bentz.yaml` - Bentz 2024 experiment configuration

### Environment
- `env.yaml` - Environment configuration

## Usage

Run an experiment with a specific config:
```bash
python src/thriller/Thriller.py -c configs/gerrig.yaml
```

Or with overrides:
```bash
python src/thriller/Thriller.py -c configs/brewer.yaml -o "model.temperature=0.7"
```

## Configuration Structure

Each experiment config typically contains:
- `experiment`: Experiment series, output directory, settings
- `model`: API type, model names, generation parameters
- `parse_model`: Model for parsing responses
- `augmentation`: Text augmentation settings (if applicable)