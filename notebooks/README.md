# Notebooks

This directory contains Jupyter notebooks for data analysis and visualization.

## Analysis Notebooks

### Metrics and Tables
- `table.ipynb` - Calculates binary classification metrics (accuracy, precision, recall, F1) comparing model predictions to human ratings
- `table_mse.ipynb` - Calculates regression metrics (MSE, RMSE, L1 distance) for model vs human rating comparisons

### Visualizations
- `gerrig_visualizations.ipynb` - Visualizations for Gerrig experiment results
- `brewer_visualizations.ipynb` - Visualizations for Brewer experiment results
- `lehne_delatorre_visualizations.ipynb` - Combined visualizations for Lehne and Delatorre experiments

### Data Processing
- `parse_adversarial.ipynb` - Parsing and analysis of adversarial experiment results

## Usage

These notebooks expect the following directory structure:
- Output data in `../outputs/[experiment_name]_experiment/`
- Research data accessible from project root

To run the notebooks:
```bash
jupyter notebook notebooks/[notebook_name].ipynb
```