import json

data_list = []
with open("research/wilmot2020/test.jsonl", "r") as file:
    for line in file:
        data = json.loads(line)
        data_list.append(data)

story_dict = {}
for story in data_list: 
    sentences = [sentence["text"] for sentence in story["sentences"]]
    story_dict[story["story_id"]] = sentences
wilmot_prompt = """Evaluate each sentence individually in relation to the previous sentence, considering how it impacts the overall suspense. Use a five-point scale to rate the suspense level: 1 for "Big Decrease in Suspense," 2 for "Decrease in Suspense," 3 for "Same Suspense Level," 4 for "Increase in Suspense," and 5 for "Big Increase in Suspense." Suspense is framed as dramatic tension, involving elements of uncertainty, anticipation, or anything that keeps the reader engaged."""
def generate_experiment_texts(experiment_config: dict[str, str]):
    """
    Generate prompts and experiment texts
    Args:
        experiment_config: settings to use in this experiment
    Return:
        Experiment prompts and veçrsion prompts
    """
    # Get experiment prompts
    prompts = {}
    for story_id in story_dict:
        prompts["Experiment" + str(story_id)] = wilmot_prompt


    # Get experiment texts
    texts = {}
    for story_id in story_dict:
        texts["Experiment" + str(story_id)] = [("Normal", story_dict[story_id])]
    return prompts, texts