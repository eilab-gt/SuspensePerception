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

    # Visualization 3: Direction change heatmaps
    for idx, (story, llm_data) in enumerate(story_llm_ratings.items()):
        data = []
        data_show = []
        for llm, ratings in llm_data.items():
            max_r = max(ratings)
            for step, rating in enumerate(ratings):
                deviation = 1 - ((abs(rating - human_ratings_list[idx]))/max_r)
                dev = rating - human_ratings_list[idx]
                if dev > 0 and deviation > 0.6:
                    deviation = 1
                    dev = 1
                elif deviation == 0:
                    deviation = 0.5
                    dev = 0
                else:
                    deviation = 0
                    dev = -1
                data.append([step, llm, deviation])
                data_show.append([step, llm, dev])
        
        for step in range(5):
            data.append([step, "Human", 1])
            data_show.append([step, "Human", 1])
        
        df = pd.DataFrame(data, columns=["Step", "LLM", "Deviation"])
        df_show = pd.DataFrame(data_show, columns=["Step", "LLM", "Deviation"])
        df_show_pivot = df_show.pivot(index="Step", columns="LLM", values="Deviation").T
        df_pivot = df.pivot(index="Step", columns="LLM", values="Deviation").T
        df_pivot = df_pivot.loc[[llm for llm in df_pivot.index if llm != "Human"] + ["Human"]]
        df_show_pivot = df_show_pivot.loc[df_pivot.index] 

        plt.figure(figsize=(10, 6))
        sns.heatmap(df_pivot, cmap="viridis", annot=df_show_pivot, fmt=".2f", linewidths=0.5, cbar=True, 
                    yticklabels=shortened_model_names + ["H"], xticklabels=[1,2,3,4,5], vmax=1, vmin=0)
        plt.title(f'Average Ratings Change Direction by Model (1 = Agreement, 0 = Disagreement) for {story}', fontsize=14)
        plt.xlabel('Passage', fontsize=12)
        plt.ylabel('Models', fontsize=12)
        plt.xticks(rotation=0)
        plt.yticks(rotation=0)
        
        # Save figure
        safe_story_name = story.replace(' ', '_')
        plt.savefig(output_dir / f"{safe_story_name}_direction.png", dpi=300, bbox_inches='tight')
        plt.close()

    print("All visualizations generated successfully!")


if __name__ == "__main__":
    main()