# Experiments Archive

This directory contains archived experimental branches that were developed but not merged into the main codebase. Each experiment represents research work that may be valuable for future reference.

## Archived Experiments

### 1. Haider2020 Poetry Emotion (PO-EMO)
**Status**: Most Complete | **Last Active**: Dec 2024

Poetry emotion analysis experiment based on Haider et al. 2020 work.

- **Implementation**: `haider2020_poetry/src/haider_en.py`
- **Config**: `haider2020_poetry/haider_en.yaml`
- **Visualization**: `haider2020_poetry/src/haider_visualization_all.ipynb`
- **Data**: Poetry emotion dataset with 100+ poems analyzed

**Key Features**:
- English poetry emotion classification
- Complete visualization notebook
- Extensive experimental outputs

---

### 2. Lee2023 Stock Emotions
**Status**: Partially Complete | **Last Active**: Aug 2024

Stock market sentiment analysis using tweet data.

- **Implementation**: `lee2023_stock_emotions/src/lee.py`
- **Config**: `lee2023_stock_emotions/lee.yaml`
- **Data**: StockEmo dataset (train/val/test splits)
- **Docs**: Annotation guide and research notes

**Known Issues**:
- CSV output formatting needs debugging
- Parser LLM integration incomplete

---

### 3. Wilmot2020 Story Suspense
**Status**: Early Draft | **Last Active**: Sep 2024

Suspense modeling in short stories using neural representations.

- **Implementation**: `wilmot2020_suspense/src/wilmot.py`
- **Config**: `wilmot2020_suspense/wilmot.yaml`
- **Data**: Limited test dataset
- **Paper**: Original research paper included

**Note**: Minimal testing completed, draft implementation only.

---

## Git History Preservation

These experiments were merged using `--strategy=ours` to preserve their git history without affecting the main codebase. The original branches remain available at:

- `origin/new_experiment/haider2020`
- `origin/new_experiment/lee2023`
- `origin/new_experiment/wilmot2020`

## Usage

To resurrect any experiment:

1. Copy the relevant files from this archive to your working directory
2. Install any missing dependencies from the experiment's requirements
3. Update import paths as needed for current project structure
4. Run using the provided YAML configuration files

## Contact

For questions about these experiments, refer to the original commit authors in git history.