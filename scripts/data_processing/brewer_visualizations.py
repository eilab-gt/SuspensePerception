#!/usr/bin/env python3
"""
Brewer visualization script - exact copy from notebook.
Generates all visualizations from the original notebook.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import ast
import os
import json
from collections import defaultdict
from pathlib import Path

# Human baseline ratings - exactly from notebook
human_ratings = {
    'Story': ['American Story Old Phoebe', 'American Story Birthday', 'American Story Flying', 'American Story Lottery', 'American Story Ylla'],
    'Suspense': [3.4, 3.2, 3.6, 4.5, 5.1],
}

def get_llm_ratings(llm_rating_sources: list[str]) -> dict[str, dict[str, list[float]]]:
    """Exact copy of get_llm_ratings from notebook."""
    llm_ratings = defaultdict(lambda: defaultdict(list))  

    for source in llm_rating_sources:
        # Adapt path construction for script location
        # From scripts/data_processing, go up 2 levels to project root
        project_root = Path(__file__).parent.parent.parent
        source_path = str(project_root / "outputs" / source)
        
        for root, _, files in os.walk(source_path):
            model_name = os.path.basename(os.path.dirname(root))
            
            for file in files:
                if file.endswith(".csv"):
                    file_path = os.path.join(root, file)
                    df = pd.read_csv(file_path, header=None, names=['experiment_name', 'version', 'response'])

                    for _, row in df.iterrows():
                        if 'Chunks' in row['version']:
                            story_name = row['version'].split(' Chunks')[0]
                            response = row["response"]
                            
                            try:
                                response_dict = json.loads(response.replace("'", "\""))
                            except json.JSONDecodeError:
                                try:
                                    response_dict = ast.literal_eval(response)
                                except (ValueError, SyntaxError):
                                    print(f"Skipping malformed response: {response}")
                                    continue  

                            selected_values = [response_dict.get(str(key)) for key in ['0', '3', '6', '9', '12']]
                            selected_values = [v for v in selected_values if v is not None]

                            if selected_values:
                                llm_ratings[model_name][story_name] = selected_values

    return llm_ratings


def average_ratings_across_sources(*llm_rating_sources):
    """Exact copy of average_ratings_across_sources from notebook."""
    averaged_data = defaultdict(lambda: defaultdict(list))
    
    for source in llm_rating_sources:
        llm_ratings = get_llm_ratings(source)
        
        for model, stories in llm_ratings.items():
            for story, ratings_list in stories.items():
                if story not in averaged_data[model]:
                    averaged_data[model][story] = []
                
                averaged_data[model][story].append(ratings_list)
    
    for model, stories in averaged_data.items():
        for story, ratings_lists in stories.items():
            averaged_ratings = [
                sum(ratings) / len(ratings) for ratings in zip(*ratings_lists)
            ]
            averaged_data[model][story] = [round(rating, 2) for rating in averaged_ratings]
    
    return averaged_data


def main():
    """Main function matching notebook execution."""
    
    # Create output directory
    output_dir = Path("scripts/analysis_results/brewer")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Exact sources from notebook
    llm_rating_sources1 = ['brewer_experiment/final/paper/exp1']
    llm_rating_sources2 = ['brewer_experiment/final/paper/exp2']
    llm_rating_sources3 = ['brewer_experiment/final/paper/exp3']

    # Get averaged ratings
    averaged_llm_ratings = average_ratings_across_sources(llm_rating_sources1, llm_rating_sources2, llm_rating_sources3)
    print(averaged_llm_ratings)

    # Convert to story-centric format
    story_llm_ratings = defaultdict(lambda: defaultdict(list))
    for llm, stories in averaged_llm_ratings.items():
        for story, ratings in stories.items():
            story_llm_ratings[story][llm] = ratings
    story_llm_ratings = dict(story_llm_ratings)
    print(story_llm_ratings)

    # Calculate stepwise averages
    stepwise_story_averages = {}
    for story, llm_ratings in story_llm_ratings.items():
        step_ratings = defaultdict(list)
        for llm, ratings in llm_ratings.items():
            for i, rating in enumerate(ratings):
                step_ratings[i].append(rating)

        step_means = []
        max_step = max(step_ratings.keys()) 
        for i in range(max_step + 1):
            if step_ratings[i]:
                step_means.append(np.mean(step_ratings[i]))
            else:
                step_means.append(None)

        stepwise_story_averages[story] = step_means
    print(stepwise_story_averages)

    # Visualization 1: Line plots with confidence intervals
    human_ratings_list = [3.4, 3.2, 3.6, 4.5, 5.1]  

    for idx, (story, llm_data) in enumerate(story_llm_ratings.items()):
        plt.figure(figsize=(10, 6))
        for llm, ratings in llm_data.items():
            steps = np.array(range(len(ratings)))
            mean_ratings = np.array(ratings)
            # Removed fill_between for shaded areas
            
            # Get shortened model name
            if 'gemma-2-27b' in llm:
                label = 'gemma-2-27b-it'
            elif 'Llama-3-70b' in llm:
                label = 'Llama-3-70b-chat-hf'
            elif 'gemma-2-9b' in llm:
                label = 'gemma-2-9b-it'
            elif 'Qwen2-72B' in llm:
                label = 'Qwen2-72B-Instruct'
            elif 'Mixtral-8x7B' in llm:
                label = 'Mixtral-8x7B-Instruct-v0.1'
            elif 'Mistral-7B' in llm:
                label = 'Mistral-7B-Instruct-v0.3'
            elif 'Llama-3-8b' in llm:
                label = 'Llama-3-8b-chat-hf'
            else:
                label = llm
            
            sns.lineplot(x=steps, y=mean_ratings, label=label, marker="o", linewidth=1)
        
        steps2 = np.array(range(len(ratings)))
        mean_ratings2 = np.array(stepwise_story_averages[story])
        # Removed fill_between for shaded areas
        sns.lineplot(x=steps2, y=mean_ratings2, label="Average", marker="o", linewidth=3, color='blue')
        
        human_steps = np.array(range(5))
        human_mean = np.full_like(human_steps, human_ratings_list[idx])
        sns.lineplot(
            x=human_steps, 
            y=human_mean, 
            label="Human", 
            marker="o", 
            linewidth=2.5, 
            color="black"
        )
        
        plt.title(f'LLM and Human Ratings Evolution for {story}', fontsize=14)
        plt.xlabel('Step', fontsize=12)
        plt.ylabel('Rating', fontsize=12)
        plt.legend(title='Model', loc='upper left', bbox_to_anchor=(1, 1))
        plt.xticks(sorted(steps))  
        plt.tight_layout()
        
        # Save figure
        safe_story_name = story.replace(' ', '_')
        plt.savefig(output_dir / f"{safe_story_name}_ratings.png", dpi=300, bbox_inches='tight')
        plt.close()

    # Visualization 2: Agreement heatmaps
    llm_names = list(next(iter(story_llm_ratings.values())).keys()) 
    shortened_model_names = ["Q-72B", "G-27B", "G-9B", "L3-70B", "L3-8B", "M-7B", "Mx-7B"]

    for idx, (story, llm_data) in enumerate(story_llm_ratings.items()):
        data = []
        actual_values = []
        deviations = []
        llm_ratings_vals = []

        for llm, ratings in llm_data.items():
            for step, rating in enumerate(ratings):
                deviation = abs(rating - human_ratings_list[idx])
                data.append([llm, step, deviation])
                actual_values.append([llm, step, rating])
                deviations.append(deviation)
                llm_ratings_vals.append(rating)

        llm_ratings_arr = np.array(llm_ratings_vals + human_ratings_list[idx:idx + 1])

        max_diff = np.max(np.abs(llm_ratings_arr - human_ratings_list[idx])) if max(deviations) != 0 else 1
        agreement_matrix = 1 - (np.abs(llm_ratings_arr - human_ratings_list[idx]) / max_diff)

        df = pd.DataFrame(data, columns=["LLM", "Step", "Deviation"])
        df_pivot = df.pivot(index="LLM", columns="Step", values="Deviation")
        
        df_pivot_normalized = 1 - (df_pivot / max_diff)

        human_row = pd.DataFrame([human_ratings_list], index=["H"], columns=df_pivot.columns)
        df_pivot = pd.concat([df_pivot, human_row])
        df_pivot_normalized = pd.concat([df_pivot_normalized, pd.DataFrame([[1]*len(df_pivot.columns)], index=["H"], columns=df_pivot.columns)])

        df_annotations = pd.DataFrame(actual_values, columns=["LLM", "Step", "Rating"]).pivot(index="LLM", columns="Step", values="Rating")
        human_annotations = pd.DataFrame([[human_ratings_list[idx]] * len(df_annotations.columns)], index=["H"], columns=df_annotations.columns)
        df_annotations = pd.concat([df_annotations, human_annotations])
        
        plt.figure(figsize=(10, 6))
        sns.heatmap(df_pivot_normalized, annot=df_annotations, cmap="viridis", fmt=".2f", linewidths=0.5,
                    yticklabels=shortened_model_names + ["H"], xticklabels=[1,2,3,4,5])
        
        plt.title(f'Brewer Average Ratings by Model {story} Passages (1 = Agreement, 0 = Disagreement)', fontsize=14)
        plt.xlabel('Passage', fontsize=12)
        plt.ylabel('Model', fontsize=12)
        plt.xticks(rotation=0)
        plt.yticks(rotation=0)
        
        # Save figure
        safe_story_name = story.replace(' ', '_')
        plt.savefig(output_dir / f"{safe_story_name}_heatmap.png", dpi=300, bbox_inches='tight')
        plt.close()

    # Visualization 3: Model consensus vs human direction changes
    for idx, (story, llm_data) in enumerate(story_llm_ratings.items()):
        # Calculate direction changes for each model
        model_directions = {}
        for llm, ratings in llm_data.items():
            directions = []
            for i in range(1, len(ratings)):
                change = ratings[i] - ratings[i-1]
                if change > 0.1:  # Threshold for meaningful change
                    directions.append(1)  # Increase
                elif change < -0.1:
                    directions.append(-1)  # Decrease
                else:
                    directions.append(0)  # No change
            model_directions[llm] = directions
        
        # Calculate consensus for each transition
        consensus_data = []
        human_direction = 0  # Human rating is constant
        
        # Find the minimum number of transitions across all models
        min_transitions = min(len(directions) for directions in model_directions.values()) if model_directions else 0
        
        for transition_idx in range(min(4, min_transitions)):  # Up to 4 transitions
            # Get all model predictions for this transition
            predictions = []
            for model in model_directions:
                if transition_idx < len(model_directions[model]):
                    predictions.append(model_directions[model][transition_idx])
            
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
            
            # Agreement with human (human rating is constant, so always "no change")
            agrees_with_human = (consensus_value == human_direction) if consensus_value is not None else False
            
            consensus_data.append({
                'Transition': f'{transition_idx+1}→{transition_idx+2}',
                'Consensus': consensus,
                'Confidence': confidence,
                'Human': 'No Change',
                'Agreement': agrees_with_human,
                'Models_Up': increase_count,
                'Models_Down': decrease_count,
                'Models_Same': no_change_count
            })
        
        # Create bar plot visualization
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), height_ratios=[3, 1])
        
        # Main consensus bar plot
        transitions = [d['Transition'] for d in consensus_data]
        x_pos = np.arange(len(transitions))
        
        # Color bars based on consensus
        colors = []
        heights = []
        labels = []
        for d in consensus_data:
            if d['Consensus'] == 'Increase':
                colors.append('#2ecc71')  # Green
                heights.append(d['Confidence'])
                labels.append(f"↑ {d['Confidence']:.0%}")
            elif d['Consensus'] == 'Decrease':
                colors.append('#e74c3c')  # Red
                heights.append(-d['Confidence'])
                labels.append(f"↓ {d['Confidence']:.0%}")
            elif d['Consensus'] == 'No Change':
                colors.append('#95a5a6')  # Gray
                heights.append(d['Confidence'] * 0.5)
                labels.append(f"− {d['Confidence']:.0%}")
            else:  # No consensus
                colors.append('#f39c12')  # Orange
                heights.append(0)
                labels.append("No Consensus")
        
        bars = ax1.bar(x_pos, heights, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        # Add value labels on bars
        for i, (bar, label) in enumerate(zip(bars, labels)):
            height = bar.get_height()
            if height != 0:
                ax1.text(bar.get_x() + bar.get_width()/2, height/2, label,
                        ha='center', va='center', fontsize=11, fontweight='bold')
            else:
                ax1.text(bar.get_x() + bar.get_width()/2, 0.05, label,
                        ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        ax1.set_ylim(-1.1, 1.1)
        ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(transitions)
        ax1.set_ylabel('Consensus Strength', fontsize=12)
        ax1.set_title(f'Model Consensus on Rating Changes: {story}', fontsize=14, fontweight='bold')
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
        
        # Stack plot for vote distribution with count labels
        bars1 = ax2.bar(x_pos, vote_data[0], color='#2ecc71', alpha=0.6, label='Increase')
        bars2 = ax2.bar(x_pos, vote_data[1], bottom=vote_data[0], color='#e74c3c', alpha=0.6, label='Decrease')
        bars3 = ax2.bar(x_pos, vote_data[2], bottom=vote_data[0]+vote_data[1], color='#95a5a6', alpha=0.6, label='No Change')
        
        # Add count labels on each bar segment
        for i, (b1, b2, b3) in enumerate(zip(bars1, bars2, bars3)):
            # Label for "Increase" segment
            if vote_data[0][i] > 0:
                height1 = b1.get_height()
                ax2.text(b1.get_x() + b1.get_width()/2, height1/2, 
                        str(int(vote_data[0][i])),
                        ha='center', va='center', fontsize=9, fontweight='bold', color='white')
            
            # Label for "Decrease" segment
            if vote_data[1][i] > 0:
                height2 = b2.get_height()
                y_pos2 = vote_data[0][i] + height2/2
                ax2.text(b2.get_x() + b2.get_width()/2, y_pos2,
                        str(int(vote_data[1][i])),
                        ha='center', va='center', fontsize=9, fontweight='bold', color='white')
            
            # Label for "No Change" segment
            if vote_data[2][i] > 0:
                height3 = b3.get_height()
                y_pos3 = vote_data[0][i] + vote_data[1][i] + height3/2
                ax2.text(b3.get_x() + b3.get_width()/2, y_pos3,
                        str(int(vote_data[2][i])),
                        ha='center', va='center', fontsize=9, fontweight='bold', color='white')
        
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels(transitions)
        ax2.set_ylabel('Model Votes', fontsize=10)
        ax2.set_xlabel('Passage Transition', fontsize=12)
        ax2.set_title('Vote Distribution (# of models)', fontsize=10, style='italic')
        ax2.legend(loc='upper right', fontsize=9, ncol=3)
        ax2.set_ylim(0, len(model_directions))
        ax2.set_yticks([])  # Remove y-axis ticks since we have labels
        
        plt.tight_layout()
        
        # Save figure
        safe_story_name = story.replace(' ', '_')
        plt.savefig(output_dir / f"{safe_story_name}_consensus.png", dpi=300, bbox_inches='tight')
        plt.close()

    print("All visualizations generated successfully!")


if __name__ == "__main__":
    main()