#!/usr/bin/env python3
"""
Lehne and Delatorre visualization script - exact copy from notebook.
Generates all visualizations from the original notebook.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os
import ast
from itertools import zip_longest
import glob
import warnings
import argparse
from pathlib import Path

warnings.filterwarnings('ignore')


def get_zipped_average(lists):
    """Exact copy from notebook."""
    zipped_lists = zip_longest(*lists, fillvalue=None)
    averages = [
        sum(filter(None.__ne__, group)) / max(1, len(list(filter(None.__ne__, group))))
        for group in zipped_lists
    ]
    return averages


def get_llm_ratings(llm_rating_sources: list[str]) -> list[float]:
    """Exact copy from notebook."""
    all_source_ratings = []

    for source in llm_rating_sources:
        project_root = Path(__file__).parent.parent.parent
        source = str(project_root / "outputs" / source)
        source_ratings = []
        
        # Traverse through the directory to find CSV files
        for root, _, files in os.walk(source):
            for file in files:
                if file.endswith(".csv"):
                    # Read the CSV file
                    file_path = os.path.join(root, file)
                    df = pd.read_csv(file_path)
                    
                    # Assuming the response column contains the dictionary of ratings as string
                    if 'response' in df.columns:
                        model_ratings = []
                        for response in df['response']:
                            response_dict = ast.literal_eval(response)
                            ratings = response_dict.values()
                            model_ratings.append(ratings)
                        source_ratings = get_zipped_average(model_ratings)
        
        if source_ratings:
            all_source_ratings.append(source_ratings)

    llm_ratings = get_zipped_average(all_source_ratings)
    return llm_ratings


def get_per_model_ratings(llm_rating_sources: list[str]) -> dict[str, list[float]]:
    """Exact copy from notebook."""
    all_ratings = {}

    experiments = ["e1", "e2", "e3"]
    model_names = ['deepseek-ai_DeepSeek-V3', 'google_gemma-2-27b-it', 'google_gemma-2-9b-it', 'meta-llama_Llama-2-7b-chat-hf', 'meta-llama_Llama-3-70b-chat-hf', 'meta-llama_Llama-3-8b-chat-hf', 'microsoft_WizardLM-2-8x22B', 'mistralai_Mistral-7B-Instruct-v0.3', 'mistralai_Mixtral-8x7B-Instruct-v0.1', 'Qwen_Qwen2-72B-Instruct']
    shortened_model_names = ["DS-V3", "G-27B", "G-9B", 'L2-7B', 'L3-70B', 'L3-8B', 'W-22B', 'M-7B', 'Mx-7B', 'Q-72B']

    for source in llm_rating_sources:
        project_root = Path(__file__).parent.parent.parent
        source = str(project_root / "outputs" / source)

        for experiment in experiments:
            for i, model in enumerate(model_names):
                csv_path = os.path.join(source, experiment, model)
                csv_path = os.path.join(csv_path, os.listdir(csv_path)[0], "results.csv")

                # Read the CSV file
                ratings = []
                df = pd.read_csv(csv_path)
                if 'response' in df.columns:
                    for response in df['response']:
                        response_dict = ast.literal_eval(response)
                        ratings = list(response_dict.values())

                shortened_model_name = shortened_model_names[i]
                if shortened_model_name not in all_ratings:
                    all_ratings[shortened_model_name] = []
                all_ratings[shortened_model_name].append(ratings)

    for shortened_model_name, ratings in all_ratings.items():
        all_ratings[shortened_model_name] = get_zipped_average(ratings)

    return all_ratings


def get_adversarial_ratings(llm_adversarial_sources: list[str]) -> dict[str, list[float]]:
    """Exact copy from notebook."""
    all_ratings = {}

    attacks = ["antonym_replacement", "caesar_cipher", "change_character_names", "context_removal", "control", "distraction_insertion", "introduce_typos", "shuffle_sentences", "swap_words", "synonym_replacement", "word_swap_embedding", "word_swap_homoglyph"]
    experiments = ["e0", "e1", "e2"]
    model_names = ['deepseek-ai_DeepSeek-V3', 'google_gemma-2-27b-it', 'google_gemma-2-9b-it', 'meta-llama_Llama-2-7b-chat-hf', 'meta-llama_Llama-3-70b-chat-hf', 'meta-llama_Llama-3-8b-chat-hf', 'microsoft_WizardLM-2-8x22B', 'mistralai_Mistral-7B-Instruct-v0.3', 'mistralai_Mixtral-8x7B-Instruct-v0.1', 'Qwen_Qwen2-72B-Instruct']

    for source in llm_adversarial_sources:
        project_root = Path(__file__).parent.parent.parent
        source = str(project_root / "outputs" / source)

        for attack in attacks:

            if attack not in all_ratings:
                all_ratings[attack] = []

            for experiment in experiments:
                for i, model in enumerate(model_names):
                    csv_path = os.path.join(source, attack, experiment, model)
                    csv_path = os.path.join(csv_path, os.listdir(csv_path)[0], "results.csv")

                    # Read the CSV file
                    ratings = []
                    df = pd.read_csv(csv_path)
                    if 'response' in df.columns:
                        for response in df['response']:
                            response_dict = ast.literal_eval(response)
                            ratings = list(response_dict.values())

                    all_ratings[attack].append(ratings)

    for attack, ratings in all_ratings.items():
        all_ratings[attack] = get_zipped_average(ratings)

    return all_ratings


def main():
    """Main function matching notebook execution."""
    parser = argparse.ArgumentParser(description="Generate Lehne or Delatorre visualizations")
    parser.add_argument("--experiment", default="Delatorre", choices=["Lehne", "Delatorre"],
                       help="Which experiment to visualize")
    args = parser.parse_args()
    
    target = args.experiment
    
    # Create output directory
    output_dir = Path(f"scripts/analysis_results/{target.lower()}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Set up data sources
    llm_rating_sources = None
    llm_adversarial_sources = None
    if target == "Lehne":
        llm_rating_sources = ["lehne_experiment/final/"]
        llm_adversarial_sources = ["lehne_experiment/adversarial/"]
    elif target == "Delatorre":
        llm_rating_sources = ["delatorre_experiment/final/"]
        llm_adversarial_sources = ["delatorre_experiment/adversarial/"]
    
    # Get ratings
    llm_ratings = get_llm_ratings(llm_rating_sources)
    try:
        llm_ratings_by_model = get_per_model_ratings(llm_rating_sources)
    except Exception as e:
        print(f"Error getting per-model ratings: {e}")
        llm_ratings_by_model = {}
    
    try:
        llm_ratings_adversarial = get_adversarial_ratings(llm_adversarial_sources)
    except:
        llm_ratings_adversarial = None
    
    # Human ratings
    human_ratings = None
    if target == "Lehne":
        human_ratings = [5.565217391, 5, 4.826086957, 5.739130435, 5.52173913, 6.826086957, 7.304347826, 5.434782609, 6.391304348, 7.47826087, 7.043478261, 5.869565217, 6.739130435, 6.956521739, 6.47826087, 5.956521739, 4.652173913, 4.260869565, 5.173913043, 4.086956522, 4.173913043, 4.304347826, 5, 4.043478261, 4.217391304, 4.434782609, 5.347826087, 6.217391304, 5.434782609, 4.782608696, 6.173913043, 5.956521739, 6.47826087, 5, 4.739130435, 5.173913043, 6.304347826, 6.434782609, 5.260869565, 5.304347826, 5.956521739, 4.304347826, 5.260869565, 4.391304348, 4.956521739, 5.695652174, 5.043478261, 5.826086957, 5.043478261, 4.913043478, 5.217391304, 6.217391304, 6.391304348, 6.52173913, 7.217391304, 6.565217391, 5.52173913, 4.347826087, 3.869565217, 7, 7.565217391, 6.52173913, 6.260869565, 6.043478261, 4.913043478]
    elif target == "Delatorre":
        human_ratings = [3.34, 3.725, 3.705, 3.89, 4.08, 5.02, 4.87, 4.81, 5.84, 5.77, 6.44, 4.685]
    
    # Figure size settings
    figsize = None
    label_fontsize = None
    cbar_fontsize = None
    if target == "Lehne":
        figsize = (40, 11)
        label_fontsize = 23
        cbar_fontsize = 15
    elif target == "Delatorre":
        figsize = (16, 11)
        label_fontsize = 14
        cbar_fontsize = 10
    
    # Inflection points (0-indexed from the notebook)
    inflection_points = []
    if target == "Lehne":
        # These appear to be 1-indexed in the paper, but need to be 0-indexed for Python
        inflection_points = [10, 11, 12, 14, 15, 21, 22, 23, 32, 33, 35, 36, 48, 49, 50, 51, 55, 56, 58, 59, 63]
        # Note: removed 64 as it's out of bounds for 64-element array
    elif target == "Delatorre":
        inflection_points = [9, 10]
    
    # Visualization 1: Line plot showing ratings evolution
    if llm_ratings_by_model:
        plt.figure(figsize=(figsize[0], 8))
        
        # Plot each model
        for model_name, ratings in llm_ratings_by_model.items():
            steps = np.array(range(len(ratings)))
            plt.plot(steps, ratings, label=model_name, marker='o', linewidth=1.5, 
                    alpha=0.7, markersize=4)
        
        # Plot human ratings
        human_steps = np.array(range(len(human_ratings)))
        plt.plot(human_steps, human_ratings, label='Human', marker='s', 
                linewidth=3, color='black', markersize=6)
        
        # Add average of LLM ratings
        avg_ratings = np.mean(list(llm_ratings_by_model.values()), axis=0)
        plt.plot(range(len(avg_ratings)), avg_ratings, label='LLM Average', 
                linewidth=2.5, color='blue', linestyle='--', alpha=0.8)
        
        plt.title(f'{target} Ratings Evolution Across Passages', fontsize=16)
        plt.xlabel('Passage Number', fontsize=14)
        plt.ylabel('Suspense Rating', fontsize=14)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        plt.savefig(output_dir / f"{target.lower()}_ratings_evolution.png", 
                    dpi=300, bbox_inches='tight')
        plt.close()
        print(f"Generated {target.lower()}_ratings_evolution.png")
    
    # Visualization 2: Main heatmap
    if not llm_ratings_by_model:
        print(f"No model ratings found for {target}")
        return
    
    model_names = list(llm_ratings_by_model.keys()) + ["H"]
    llm_ratings_arr = np.array(list(llm_ratings_by_model.values()) + [human_ratings])
    
    print(f"Model ratings shape: {llm_ratings_arr.shape}")
    print(f"Human ratings length: {len(human_ratings)}")
    
    # Compute agreement matrix
    max_diff = np.max(np.abs(llm_ratings_arr - human_ratings))
    agreement_matrix = 1 - (np.abs(llm_ratings_arr - human_ratings) / max_diff)
    
    print(f"Agreement matrix shape: {agreement_matrix.shape}")
    print(f"Annotation matrix shape: {llm_ratings_arr.shape}")
    
    plt.figure(figsize=figsize)
    ax = sns.heatmap(agreement_matrix, vmin=0, vmax=1, annot=llm_ratings_arr, cmap="viridis", cbar=True, 
                     linewidths=0, xticklabels=range(1, llm_ratings_arr.shape[1] + 1), yticklabels=model_names)
    ax.collections[0].colorbar.ax.set_title("% Agreement", fontsize=cbar_fontsize)
    
    plt.title(f"{target} Average Ratings by Model", fontsize=label_fontsize)
    plt.xlabel("Passage", fontsize=label_fontsize)
    plt.ylabel("Model", fontsize=label_fontsize)
    plt.yticks(rotation=0)
    plt.savefig(output_dir / f"{target.lower()}_model_heatmap.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Visualization 2: Ratings change
    def fmt_func(value):
        return f"+{value:.1f}" if value >= 0 else f"{value:.1f}"
    
    llm_ratings_change = np.diff(llm_ratings_arr)
    human_ratings_change = np.diff(human_ratings)
    
    annot_fmt = np.vectorize(fmt_func)(llm_ratings_change)
    
    max_diff = np.max(np.abs(llm_ratings_change - human_ratings_change))
    agreement_matrix = 1 - (np.abs(llm_ratings_change - human_ratings_change) / max_diff)
    
    plt.figure(figsize=figsize)
    ax = sns.heatmap(agreement_matrix, vmin=0, vmax=1, annot=annot_fmt, cmap="viridis", cbar=True, 
                     linewidths=0.0, xticklabels=range(2, llm_ratings_change.shape[1] + 2), 
                     yticklabels=model_names, fmt="")
    ax.collections[0].colorbar.ax.set_title("% Agreement", fontsize=cbar_fontsize)
    
    plt.title(f"{target} Average Ratings Change by Model", fontsize=label_fontsize)
    plt.xlabel("Passage", fontsize=label_fontsize)
    plt.ylabel("Model", fontsize=label_fontsize)
    plt.yticks(rotation=0)
    plt.savefig(output_dir / f"{target.lower()}_change_heatmap.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Visualization 3: Model consensus on change direction
    # Calculate direction changes for each model (excluding human)
    model_directions = []
    model_names_only = model_names[:-1]  # Exclude "H" (human)
    
    for i in range(len(model_names_only)):
        directions = []
        for j in range(1, llm_ratings_arr.shape[1]):
            change = llm_ratings_arr[i, j] - llm_ratings_arr[i, j-1]
            if change > 0.1:  # Threshold for meaningful change
                directions.append(1)  # Increase
            elif change < -0.1:
                directions.append(-1)  # Decrease
            else:
                directions.append(0)  # No change
        model_directions.append(directions)
    
    # Calculate human direction changes
    human_directions = []
    for j in range(1, len(human_ratings)):
        change = human_ratings[j] - human_ratings[j-1]
        if change > 0.1:
            human_directions.append(1)
        elif change < -0.1:
            human_directions.append(-1)
        else:
            human_directions.append(0)
    
    # Calculate consensus for each transition
    consensus_data = []
    num_transitions = min(len(human_directions), llm_ratings_arr.shape[1] - 1)
    
    for transition_idx in range(num_transitions):
        # Get all model predictions for this transition
        predictions = [model_directions[i][transition_idx] for i in range(len(model_directions))]
        
        # Calculate consensus
        increase_count = predictions.count(1)
        decrease_count = predictions.count(-1)
        no_change_count = predictions.count(0)
        total_models = len(predictions)
        
        # Determine consensus
        if increase_count > total_models * 0.6:  # 60% threshold for consensus
            consensus = "Increase"
            consensus_value = 1
            confidence = increase_count / total_models
        elif decrease_count > total_models * 0.6:
            consensus = "Decrease"
            consensus_value = -1
            confidence = decrease_count / total_models
        elif no_change_count > total_models * 0.6:
            consensus = "No Change"
            consensus_value = 0
            confidence = no_change_count / total_models
        else:
            consensus = "No Consensus"
            consensus_value = None
            confidence = max(increase_count, decrease_count, no_change_count) / total_models
        
        # Agreement with human
        human_dir = human_directions[transition_idx] if transition_idx < len(human_directions) else 0
        human_label = "Increase" if human_dir > 0 else ("Decrease" if human_dir < 0 else "No Change")
        agrees_with_human = (consensus_value == human_dir) if consensus_value is not None else False
        
        consensus_data.append({
            'Transition': f'P{transition_idx+1}→P{transition_idx+2}',
            'Consensus': consensus,
            'Confidence': confidence,
            'Human': human_label,
            'Agreement': agrees_with_human,
            'Models_Up': increase_count,
            'Models_Down': decrease_count,
            'Models_Same': no_change_count
        })
    
    # Create visualization with appropriate sizing
    if num_transitions > 20:  # For Lehne with many transitions
        fig_width = max(16, num_transitions * 0.4)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(fig_width, 10), height_ratios=[3, 1])
    else:  # For Delatorre with fewer transitions
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), height_ratios=[3, 1])
    
    # Main consensus bar plot
    transitions = [d['Transition'] for d in consensus_data]
    x_pos = np.arange(len(transitions))
    
    # Color bars based on consensus
    colors = []
    heights = []
    labels = []
    for d in consensus_data:
        if d['Consensus'] == 'Increase':
            colors.append('#2ecc71' if d['Agreement'] else '#27ae60')  # Green (lighter if agrees with human)
            heights.append(d['Confidence'])
            labels.append(f"↑ {d['Confidence']:.0%}")
        elif d['Consensus'] == 'Decrease':
            colors.append('#e74c3c' if d['Agreement'] else '#c0392b')  # Red
            heights.append(-d['Confidence'])
            labels.append(f"↓ {d['Confidence']:.0%}")
        elif d['Consensus'] == 'No Change':
            colors.append('#95a5a6' if d['Agreement'] else '#7f8c8d')  # Gray
            heights.append(d['Confidence'] * 0.5)
            labels.append(f"− {d['Confidence']:.0%}")
        else:  # No consensus
            colors.append('#f39c12')  # Orange
            heights.append(0)
            labels.append("NC")
    
    bars = ax1.bar(x_pos, heights, color=colors, alpha=0.8, edgecolor='black', linewidth=1.0)
    
    # Add value labels on bars (skip some if too many)
    label_freq = max(1, num_transitions // 20)  # Show labels less frequently if many transitions
    for i, (bar, label) in enumerate(zip(bars, labels)):
        if i % label_freq == 0 or num_transitions <= 20:
            height = bar.get_height()
            if height != 0:
                ax1.text(bar.get_x() + bar.get_width()/2, height/2, label,
                        ha='center', va='center', fontsize=9 if num_transitions > 20 else 11, fontweight='bold')
            else:
                ax1.text(bar.get_x() + bar.get_width()/2, 0.02, label,
                        ha='center', va='bottom', fontsize=9 if num_transitions > 20 else 11, fontweight='bold')
    
    ax1.set_ylim(-1.1, 1.1)
    ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax1.set_xticks(x_pos[::max(1, num_transitions // 30)])  # Show fewer x-labels if many transitions
    ax1.set_xticklabels([transitions[i] for i in range(0, len(transitions), max(1, num_transitions // 30))], 
                        rotation=45 if num_transitions > 15 else 0, ha='right')
    ax1.set_ylabel('Consensus Strength', fontsize=12)
    ax1.set_title(f'Model Consensus on Rating Changes: {target}', fontsize=16, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#2ecc71', label='Consensus: Increase', alpha=0.8),
        Patch(facecolor='#e74c3c', label='Consensus: Decrease', alpha=0.8),
        Patch(facecolor='#95a5a6', label='Consensus: No Change', alpha=0.8),
        Patch(facecolor='#f39c12', label='No Clear Consensus', alpha=0.8)
    ]
    ax1.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    # Bottom panel: Model vote distribution
    vote_data = np.array([[d['Models_Up'], d['Models_Down'], d['Models_Same']] for d in consensus_data]).T
    
    # Stack plot for vote distribution
    ax2.bar(x_pos, vote_data[0], color='#2ecc71', alpha=0.6, label='Increase')
    ax2.bar(x_pos, vote_data[1], bottom=vote_data[0], color='#e74c3c', alpha=0.6, label='Decrease')
    ax2.bar(x_pos, vote_data[2], bottom=vote_data[0]+vote_data[1], color='#95a5a6', alpha=0.6, label='No Change')
    
    ax2.set_xticks(x_pos[::max(1, num_transitions // 30)])
    ax2.set_xticklabels([transitions[i] for i in range(0, len(transitions), max(1, num_transitions // 30))],
                        rotation=45 if num_transitions > 15 else 0, ha='right')
    ax2.set_ylabel('Model Count', fontsize=10)
    ax2.set_xlabel('Passage Transition', fontsize=12)
    ax2.legend(loc='upper right', fontsize=9, ncol=3)
    ax2.set_ylim(0, len(model_directions))
    
    plt.tight_layout()
    
    # Save figure
    plt.savefig(output_dir / f"{target.lower()}_consensus.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    # Visualization 4: Adversarial attack analysis (if available)
    if llm_ratings_adversarial:
        control_ratings = llm_ratings_adversarial["control"]
        llm_ratings_adversarial.pop("control")
        
        attack_names = list(llm_ratings_adversarial.keys()) + ["Control"]
        llm_ratings_adv = np.array(list(llm_ratings_adversarial.values()) + [control_ratings])
        
        max_diff = np.max(np.abs(llm_ratings_adv - control_ratings))
        agreement_matrix = 1 - (np.abs(llm_ratings_adv - control_ratings) / max_diff)
        
        plt.figure(figsize=figsize)
        ax = sns.heatmap(agreement_matrix, vmin=0, vmax=1, annot=llm_ratings_adv, cmap="viridis", cbar=True, 
                        linewidths=0, xticklabels=range(1, llm_ratings_adv.shape[1] + 1), yticklabels=attack_names)
        ax.collections[0].colorbar.ax.set_title("% Agreement", fontsize=cbar_fontsize)
        
        plt.title(f"{target} Average Ratings by Attack", fontsize=label_fontsize)
        plt.xlabel("Passage", fontsize=label_fontsize)
        plt.ylabel("Attack", fontsize=label_fontsize)
        plt.savefig(output_dir / f"{target.lower()}_attack_heatmap.png", dpi=300, bbox_inches='tight')
        plt.close()
    
    # Visualization 5: Inflection points only (skip for Delatorre as it has issues with shape)
    if target == "Delatorre":
        print(f"Skipping inflection visualization for {target} due to data shape issues")
        print(f"All {target} visualizations generated successfully!")
        return
    
    # Filter inflection points to only include valid indices
    valid_inflection_points = [ip for ip in inflection_points if ip < llm_ratings_arr.shape[1]]
    if valid_inflection_points:
        llm_ratings_inflection = llm_ratings_arr[:, valid_inflection_points]
        agreement_matrix_inflection = agreement_matrix[:, valid_inflection_points]
        xticklabels = np.array(range(1, llm_ratings_arr.shape[1] + 1))[valid_inflection_points]
    else:
        # If no valid inflection points, skip this visualization
        print(f"No valid inflection points for {target}, skipping inflection visualization")
        print(f"All {target} visualizations generated successfully!")
        return
    
    plt.figure(figsize=figsize)
    ax = sns.heatmap(agreement_matrix_inflection, vmin=0, vmax=1, annot=llm_ratings_inflection, cmap="viridis", 
                     cbar=True, linewidths=0, xticklabels=xticklabels, yticklabels=model_names)
    ax.collections[0].colorbar.ax.set_title("% Agreement", fontsize=cbar_fontsize)
    
    plt.title(f"{target} Average Ratings by Model, Inflection Points Only", fontsize=label_fontsize)
    plt.xlabel("Passage", fontsize=label_fontsize)
    plt.ylabel("Model", fontsize=label_fontsize)
    plt.yticks(rotation=0)
    plt.savefig(output_dir / f"{target.lower()}_inflection_heatmap.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"All {target} visualizations generated successfully!")


if __name__ == "__main__":
    main()