import pandas as pd
prompt_LLM = """Given the following input text, evaluate it and categorize the emotion it conveys using one of the defined emotions below: 
1. Amusement: The pleasure that you get from being entertained or from doing something interesting.
Synonyms: Enjoyment, delight, laughter, pleasure, fun

2. Anger: A strong feeling of being upset or annoyed because of something wrong, unfair, cruel, or unacceptable.
Synonyms: Rage, outrage, fury, wrath, irritation

3. Anxiety: A feeling of nervousness or worry about what might happen.
Synonyms: Nervousness, alarm, worry, tension, uneasiness

4. Belief: A feeling of certainty that something exists, is true, or is good, associated with the company’s operation.
Synonyms: Trust, faith, confidence, conviction, reliance

5. Confusion: A refusal or reluctance to believe.
Synonyms: Scepticism, doubt, disbelief, distrust, uncertainty

6. Depression: A state of feeling sad, extreme gloom, inadequacy, and inability to concentrate.
Synonyms: Sadness, despair, giving up, hopelessness, gloom

7. Disgust: A feeling of very strong dislike or disapproval.
Synonyms: Loathing, dislike, hatred, sicken, abomination

8. Excitement: A feeling of having great enthusiasm, strong belief, intense enjoyment, or great eagerness.
Synonyms: Enthusiasm, passion, cheerfulness, heat

9. Optimism: A feeling of being hopeful about the future or about the success of something in particular.
Synonyms: Hope, wish, desire, want, positiveness

10. Panic: A very strong feeling of anxiety or fear, which makes you act without thinking carefully.
Synonyms: Horror, terror, fear, dismay, terrify

11. Surprise: A feeling caused by something that is unexpected or unusual (e.g., earning surprise).
Synonyms: Amazement, astonishment, shock, revelation

12. Ambiguous: Unclassified emotions in the list or when the target of emotion is confused.
Synonyms: (Subject to annotator’s understanding of the text)

The answer should include the number in front of the emotion
"""

data1 = pd.read_csv("src/thriller/test_stockemo.csv")
data2 = pd.read_csv("src/thriller/train_stockemo.csv")
data3 = pd.read_csv("src/thriller/val_stockemo.csv")

procesed1 = data1["processed"].tolist()
procesed2 = data2["processed"].tolist()
procesed3 = data3["processed"].tolist()
combined = procesed1 + procesed2 + procesed3

def generate_experiment_texts(settings_config: dict[str, str]):
    """
    Generate prompts and experiment texts
    Args:
        settings_config: settings to use in this experiment
    Return:
        Experiment prompts and version prompts
    """

    prompts = {
        "Experiment Tweet": prompt_LLM,
    }

    version_prompts = {
        "Experiment Tweet":[
        ("All tweets", combined),
        ]
    }

    return prompts, version_prompts


