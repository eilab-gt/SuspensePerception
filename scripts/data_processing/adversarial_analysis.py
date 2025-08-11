#!/usr/bin/env python3
"""
Adversarial attack analysis with horizontal bar and whisker plots.
Generates boxplots showing rating changes compared to control condition.
"""

import matplotlib.pyplot as plt
import os
import pandas as pd
import glob
import ast
import numpy as np
import re
import seaborn as sns
from pathlib import Path


def parse_adversarial_results(target_experiment="all"):
    """Parse adversarial attack results from CSV files."""
    LOGDIR = Path(__file__).parent.parent.parent / "outputs"
    
    glob_path = os.path.join(LOGDIR, '**/adversarial/**/**/**/**/*.csv')
    glob_list = glob.glob(glob_path)
    
    dfs = []
    
    for dataframe_path in glob_list:
        dataframe_path = dataframe_path.replace(os.sep, "/")
        
        match = re.search(r'/(?P<experiment>[^/]+)_experiment/adversarial/(?P<attack>[^/]+)/(?P<iter>[^/]+)/(?P<model>[^/]+)/(?:[^/]+)/results\.csv$', dataframe_path)
        if match:
            experiment = match.group('experiment')
            attack = match.group('attack')
            iter_num = match.group('iter')
            model = match.group('model')
            
            # Skip if not target experiment
            if target_experiment != "all" and experiment != target_experiment:
                continue
            
            try:
                df = pd.read_csv(dataframe_path)
                df["experiment"] = experiment
                df["attack"] = attack
                df["iter"] = iter_num
                df["model"] = model
                dfs.append(df)
            except Exception as e:
                print(f"Error reading {dataframe_path}: {e}")
                continue
    
    if not dfs:
        print(f"No adversarial data found for experiment: {target_experiment}")
        return None
    
    return pd.concat(dfs)


def parse_experiment(df: pd.DataFrame, experiment_name: str):
    """Parse experiment data and compute mean scores."""
    _df = df[df['experiment'] == experiment_name].drop(columns=['experiment'])
    _df['response'] = _df['response'].apply(ast.literal_eval)
    keys = list(_df['response'].iloc[0].keys())
    _response_df = _df['response'].apply(pd.Series)
    _df = pd.concat([_df, _response_df], axis=1).drop(columns=['response'])
    
    _df['mean_score'] = _df[keys].mean(axis=1)
    _df = _df.groupby(['experiment_name', 'version', 'attack', 'iter'])[keys + ['mean_score']].mean().reset_index()
    _df = _df.groupby(['experiment_name', 'version', 'attack'])[keys + ['mean_score']].agg(['mean', 'std']).reset_index()
    
    return _df


def get_change(df: pd.DataFrame, experiment_names: list[str]):
    """Calculate change from control condition for each attack."""
    mean_score_changes = {}
    mean_std_changes = {}
    
    for experiment_name in experiment_names:
        _df = parse_experiment(df, experiment_name)
        
        control_mean_score = _df.loc[_df['attack'] == 'control', ('mean_score', 'mean')].values[0]
        control_mean_std = _df.loc[_df['attack'] == 'control', ('mean_score', 'std')].values[0]
        
        for attack in _df['attack'].unique():
            if attack == "control":
                continue
            
            if attack not in mean_score_changes:
                mean_score_changes[attack] = []
            if attack not in mean_std_changes:
                mean_std_changes[attack] = []
            
            mean_score = _df.loc[_df['attack'] == attack, ('mean_score', 'mean')]
            mean_score_change = mean_score - control_mean_score
            mean_score_changes[attack].extend(mean_score_change)
            
            mean_std = _df.loc[_df['attack'] == attack, ('mean_score', 'std')]
            mean_std_change = mean_std - control_mean_std
            mean_std_changes[attack].extend(mean_std_change)
    
    return mean_score_changes, mean_std_changes


def create_horizontal_boxplot(gerrig_changes, delatorre_changes, combined_changes, output_dir):
    """Create horizontal box and whisker plot for adversarial attacks."""
    # Create list to store data
    data = []
    
    # Format attack names to title case
    def format_attack_name(attack):
        """Convert snake_case to Title Case."""
        return ' '.join(word.capitalize() for word in attack.split('_'))
    
    for attack, scores in gerrig_changes.items():
        for score in scores:
            data.append((format_attack_name(attack), score, "Gerrig"))
    for attack, scores in delatorre_changes.items():
        for score in scores:
            data.append((format_attack_name(attack), score, "Delatorre"))
    for attack, scores in combined_changes.items():
        for score in scores:
            data.append((format_attack_name(attack), score, "Combined"))
    
    # Create DataFrame
    diff_df = pd.DataFrame(data, columns=['Attack Type', 'Score Change', 'Source'])
    
    # Define custom colors matching the reference (blue, purple, orange)
    custom_colors = ['#5A9FCC', '#9B6BA6', '#D4A76A']  # Blue, Purple, Orange
    
    # Sort attack types for consistent ordering
    attack_order = sorted(diff_df['Attack Type'].unique())
    
    # Plot with separate boxes per attack type
    plt.figure(figsize=(14, 8))
    ax = sns.boxplot(
        data=diff_df,
        y='Attack Type',   # Horizontal orientation
        x='Score Change',  
        hue='Source',
        order=attack_order,
        palette=custom_colors,
        flierprops=dict(marker='o', markersize=6, markerfacecolor="red", markeredgecolor="red", alpha=0.5),
        width=0.6,
        linewidth=1.2
    )
    
    # Add a vertical line at x=0 with label
    ax.axvline(x=0, color='black', linestyle='-', linewidth=1.5, alpha=0.7)
    
    # Add "Control" and "Baseline" annotations
    ax.text(-0.05, -0.5, 'Control', fontsize=10, ha='right', va='top', 
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray'))
    ax.text(-0.05, 0.5, 'Baseline', fontsize=10, ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray'))
    
    # Improve visualization
    plt.title('Impact of Adversarial Attacks on Suspense Perception Ratings', fontsize=16, fontweight='bold')
    plt.xlabel('Difference from Control', fontsize=12)
    plt.ylabel('Attack Type', fontsize=12)
    
    # Set x-axis limits to match reference
    plt.xlim(-3, 2)
    
    # Add subtle grid
    ax.grid(axis='x', linestyle='-', alpha=0.2, color='gray')
    ax.set_axisbelow(True)
    
    # Customize legend
    plt.legend(title="Experiment", title_fontsize=11, fontsize=10, 
              loc='lower right', frameon=True, fancybox=True, shadow=False)
    
    # Remove top and right spines for cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save figure
    plt.savefig(output_dir / "adversarial_horizontal_boxplot.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Generated adversarial_horizontal_boxplot.png")


def main():
    """Main function to generate adversarial analysis plots."""
    # Create output directory
    output_dir = Path("scripts/analysis_results/adversarial")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Parse all adversarial results
    print("Parsing adversarial results...")
    df = parse_adversarial_results("all")
    
    if df is None:
        print("No adversarial data found to process")
        return
    
    # Check which experiments have data
    experiments = df['experiment'].unique()
    print(f"Found adversarial data for experiments: {list(experiments)}")
    
    # Initialize change dictionaries
    gerrig_mean_score_change = {}
    delatorre_mean_score_change = {}
    combined_mean_score_change = {}
    
    # Calculate changes for available experiments
    if 'gerrig' in experiments:
        gerrig_mean_score_change, _ = get_change(df, ["gerrig"])
        print(f"Processed Gerrig: {len(gerrig_mean_score_change)} attack types")
    
    if 'delatorre' in experiments:
        delatorre_mean_score_change, _ = get_change(df, ["delatorre"])
        print(f"Processed Delatorre: {len(delatorre_mean_score_change)} attack types")
    
    # Combined analysis if both experiments exist
    available_experiments = [exp for exp in ['gerrig', 'delatorre'] if exp in experiments]
    if available_experiments:
        combined_mean_score_change, _ = get_change(df, available_experiments)
        print(f"Processed Combined: {len(combined_mean_score_change)} attack types")
    
    # Create horizontal boxplot if we have data
    if gerrig_mean_score_change or delatorre_mean_score_change:
        print("\nGenerating horizontal box and whisker plot...")
        create_horizontal_boxplot(
            gerrig_mean_score_change,
            delatorre_mean_score_change,
            combined_mean_score_change,
            output_dir
        )
        
        # Also save parsed data for future use
        for exp in experiments:
            out = parse_experiment(df, exp)
            out.to_csv(output_dir / f'{exp}_adversarial_results.csv', index=False)
            print(f"Saved {exp}_adversarial_results.csv")
        
        print("\nAdversarial analysis complete!")
    else:
        print("No adversarial data to plot")


if __name__ == "__main__":
    main()