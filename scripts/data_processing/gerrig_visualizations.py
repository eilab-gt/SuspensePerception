#!/usr/bin/env python3
"""
Gerrig visualization script - exact copy from notebook.
Generates all visualizations from the original notebook.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os
import ast
import json
import csv
from itertools import zip_longest
from collections import defaultdict
from pathlib import Path


def get_llm_ratings(llm_rating_sources: list[str]) -> dict[str, dict[str, list[float]]]:
    """Exact copy of get_llm_ratings from notebook."""
    llm_ratings = defaultdict(lambda: defaultdict(list))  

    for source in llm_rating_sources:
        # Adapt path construction for script location
        project_root = Path(__file__).parent.parent.parent
        source_path = str(project_root / "outputs" / source)
        
        for root, _, files in os.walk(source_path):
            model_name = os.path.basename(os.path.dirname(root))
            
            for file in files:
                if file.endswith(".csv"):
                    file_path = os.path.join(root, file)
                    df = pd.read_csv(file_path, header=None, names=['experiment_name', 'version', 'response'])

                    for _, row in df.iterrows():
                        experiment_name = row["experiment_name"]
                        version = row["version"]
                        response = row["response"]
                        
                        try:
                            response_dict = json.loads(response.replace("'", "\""))
                        except json.JSONDecodeError:
                            try:
                                response_dict = ast.literal_eval(response)
                            except (ValueError, SyntaxError):
                                continue  

                        value_at_key_1 = response_dict.get('1')

                        if value_at_key_1 is not None:
                            llm_ratings[model_name][experiment_name + ", " + version] = value_at_key_1

    return llm_ratings


def average_llm_ratings(llm_ratings_list: list[dict]) -> dict:
    """Exact copy of average_llm_ratings from notebook."""
    averaged_ratings = defaultdict(lambda: defaultdict(list))

    for llm_ratings in llm_ratings_list:
        for model_name, experiments in llm_ratings.items():
            for experiment_name, ratings in experiments.items():
                averaged_ratings[model_name][experiment_name].append(ratings)

    for model_name, experiments in averaged_ratings.items():
        for experiment_name, ratings in experiments.items():
            if ratings:
                averaged_ratings[model_name][experiment_name] = np.mean(ratings)

    return averaged_ratings


def process_experiment_data(source):
    """Exact copy of process_experiment_data from notebook."""
    project_root = Path(__file__).parent.parent.parent
    source_path = str(project_root / "data" / source)
    
    experiment_data = {}

    with open(source_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        
        for row in reader:
            if len(row) < 5:
                continue  
            if row[0] != "":
                experiment = row[0] + ", " + row[1]
                attack = row[2]     
                value = row[5] 

                if experiment not in experiment_data:
                    experiment_data[experiment] = {}
                
                experiment_data[experiment][attack] = value

    return experiment_data


def average_experiment_scores(llm_results):
    """Exact copy of average_experiment_scores from notebook."""
    experiment_totals = defaultdict(lambda: {"sum": 0, "count": 0})

    for llm, experiments in llm_results.items():
        for experiment, score in experiments.items():
            experiment_totals[experiment]["sum"] += score
            experiment_totals[experiment]["count"] += 1

    averaged_experiments = {
        experiment: data["sum"] / data["count"]
        for experiment, data in experiment_totals.items()
    }

    return averaged_experiments


def main():
    """Main function matching notebook execution."""
    
    # Create output directory
    output_dir = Path("scripts/analysis_results/gerrig")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Human ratings from notebook - Standard suspense / Q2 ratings
    human_ratings = {
        "Experiment A, Pen Not Mentioned": (3.78 + 3.43) / 2,
        "Experiment A, Pen Mentioned Removed": (4.38 + 4.06) / 2,
        "Experiment A, Pen Mentioned Not Removed": 3.47,
        "Experiment B, Unused Comb": 3.96,
        "Experiment B, Used Comb": 3.41,
        "Experiment C, Prior Solution Not Mentioned": (3.76 + 3.34) / 2,
        "Experiment C, Prior Solution Mentioned and Removed": (4.61 + 3.99) / 2,
        "Experiment C, Prior Solution Mentioned Not Removed": 4.14
    }
    
    # Get LLM ratings from three experiments
    llm_rating_sources1 = ["gerrig_experiment/final/e1"]
    llm_ratings1 = get_llm_ratings(llm_rating_sources1)
    llm_rating_sources2 = ["gerrig_experiment/final/e2"]
    llm_ratings2 = get_llm_ratings(llm_rating_sources2)
    llm_rating_sources3 = ["gerrig_experiment/final/e3"]
    llm_ratings3 = get_llm_ratings(llm_rating_sources3)
    
    # Average ratings across experiments
    averaged_ratings = average_llm_ratings([llm_ratings1, llm_ratings2, llm_ratings3])
    
    # Convert to normal dict
    normal_dict = {
        model: {
            experiment: (ratings.tolist() if isinstance(ratings, (list, np.ndarray)) else ratings)
            for experiment, ratings in experiments.items()
        }
        for model, experiments in averaged_ratings.items()
    }
    
    # Visualization 1: Main heatmap
    data = []
    models = list(normal_dict.keys())
    experiments = list(human_ratings.keys())
    shortened_model_names = ["DS-V3", "G-27B", "G-9B", 'L2-7B', 'L3-70B', 'L3-8B', 'W-22B', 'M-7B', 'Mx-7B', 'Q-72B']
    
    actual = []
    for model in models:
        for experiment in experiments:
            llm_rating = normal_dict[model].get(experiment, np.nan)
            human_rating = human_ratings.get(experiment, np.nan)
            
            if not np.isnan(llm_rating) and not np.isnan(human_rating):
                proximity = 1 - abs(llm_rating - human_rating) / max(1, abs(human_rating))
                data.append([model, experiment, llm_rating, human_rating, proximity])
    
    df = pd.DataFrame(data, columns=["Model", "Experiment", "LLM Rating", "Human Rating", "Proximity"])
    human_row = pd.DataFrame([["Human", experiment, np.nan, human_ratings[experiment], 1.0] for experiment in experiments], 
                             columns=["Model", "Experiment", "LLM Rating", "Human Rating", "Proximity"])
    
    df = pd.concat([df, human_row], ignore_index=True)
    
    df_pivot = df.pivot(index="Model", columns="Experiment", values="Proximity")
    df_pivot = df_pivot.reindex(df_pivot.index.tolist() + ['Human'])
    df_pivot = df_pivot[~df_pivot.index.duplicated(keep='last')]
    
    annot_data = df.pivot(index="Model", columns="Experiment", values="LLM Rating").reindex(df_pivot.index)
    human_data = df.pivot(index="Model", columns="Experiment", values="Human Rating").reindex(df_pivot.index)
    
    annot_data_rounded = annot_data.round(2)
    human_data_rounded = human_data.round(2)
    
    annot_matrix = annot_data_rounded.astype(str)
    annot_matrix.loc['Human', :] = human_data_rounded.loc['Human'].astype(str)
    
    plt.figure(figsize=(12, 8))
    ax = sns.heatmap(df_pivot, vmin=0, vmax=1, annot=annot_matrix, cmap="viridis", fmt="", linewidths=0.5, 
                     yticklabels=shortened_model_names + ["H"],
                     annot_kws={"size": 10, "va": "center", "ha": "center"})
    ax.collections[0].colorbar.ax.set_title("% Agreement", fontsize=10)
    
    plt.title(f'Gerrig Average Ratings by Model', fontsize=14)
    plt.xlabel("Experiment", fontsize=14)
    plt.ylabel("Model", fontsize=14)
    plt.xticks(rotation=20, ha='right')
    plt.yticks(rotation=0)
    plt.savefig(output_dir / "gerrig_model_heatmap.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Visualization 2: Attack analysis (if data is available)
    try:
        # Process adversarial attack data
        source = "gerrig_results.csv"
        result = process_experiment_data(source)
        
        # Remove control from result
        for experiment in result:
            if 'control' in result[experiment]:
                del result[experiment]['control']
        
        # Average experiment scores
        averaged_scores = average_experiment_scores(normal_dict)
        
        control_ratings = averaged_scores.values()
        experim = list(result.keys())
        attack_names = list(result["Experiment A, Pen Mentioned Not Removed"].keys()) + ["Control"]
        llm = result.values()
        list_values = list(llm)
        flattened_values = [float(v) for d in list_values for v in d.values()]
        llm_ratings = np.array(list(flattened_values) + list(control_ratings))
        
        control_ratings = np.array(list(control_ratings))
        max_llm = max(llm_ratings)
        llm_ratings = np.array(llm_ratings).reshape(12, 8)
        
        agreement_matrix = 1 - (np.abs(llm_ratings - control_ratings))
        
        plt.figure(figsize=(12, 8))
        ax = sns.heatmap(agreement_matrix, vmin=0, vmax=1, annot=llm_ratings, cmap="viridis", cbar=True, 
                        linewidths=0, yticklabels=attack_names, xticklabels=experim)
        ax.collections[0].colorbar.ax.set_title("% Agreement", fontsize=10)
        
        plt.title(f"Gerrig Average Ratings by Attack", fontsize=14)
        plt.xlabel("Experiment Type", fontsize=14)
        plt.xticks(rotation=20, ha='right')
        plt.ylabel("Attack", fontsize=14)
        plt.savefig(output_dir / "gerrig_attack_heatmap.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Attack analysis visualization generated successfully!")
    except Exception as e:
        print(f"Could not generate attack analysis: {e}")
    
    print("All visualizations generated successfully!")


if __name__ == "__main__":
    main()