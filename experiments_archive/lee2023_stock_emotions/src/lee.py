import sys
from pathlib import Path
import pandas as pd

project_root = str(Path(__file__).resolve().parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.thriller.api import tokenize
from dotenv import load_dotenv

prompt = """
Your task is to classify the tweet into one of the following emotion classes: "amusement, anger, anxiety, belief, confusion, depression, disgust, excitement, optimism, panic, surprise, ambiguous". Use the annotation guide provided below to determine the most appropriate emotion class. Please respond with the emotion class that you believe best describes the tweet.

Annotation Guide:

- **amusement**: the pleasure you get from being entertained or from doing something interesting.  
  *Synonyms:* enjoyment, delight, laughter, pleasure, fun.  
  *Emoji:* 😂
  
- **anger**: a strong feeling of being upset or annoyed because of something wrong, unfair, cruel, or unacceptable.  
  *Synonyms:* rage, outrage, fury, wrath, irritation.  
  *Emoji:* 😡
  
- **anxiety**: a feeling of nervousness or worry about what might happen.  
  *Synonyms:* nervousness, alarm, worry, tension, uneasiness.  
  *Emoji:* 🤡
  
- **belief**: a feeling of certainty that something exists, is true, or is good, associated with the company’s operation.  
  *Synonyms:* trust, faith, confidence, conviction, reliance.  
  *Emoji:* 🔥
  
- **confusion**: a refusal or reluctance to believe.  
  *Synonyms:* scepticism, doubt, disbelief, distrust, uncertainty.  
  *Emoji:* 🤔
  
- **depression**: a state of feeling sad, extreme gloom, inadequacy, and inability to concentrate.  
  *Synonyms:* sadness, despair, giving up, hopelessness, gloom.  
  *Emoji:* 😭
  
- **disgust**: a feeling of very strong dislike or disapproval.  
  *Synonyms:* loathing, dislike, hatred, sicken, abomination.  
  *Emoji:* 💩
  
- **excitement**: a feeling of having great enthusiasm, strong belief, intense enjoyment, or great eagerness.  
  *Synonyms:* enthusiasm, passion, cheerfulness, heat.  
  *Emoji:* 🚀
  
- **optimism**: a feeling of being hopeful about the future or about the success of something in particular.  
  *Synonyms:* hope, wish, desire, want, positiveness.  
  *Emoji:* 💰
  
- **panic**: a very strong feeling of anxiety or fear, which makes you act without thinking carefully.  
  *Synonyms:* horror, terror, fear, dismay, terrify.  
  *Emoji:* 😱
  
- **surprise**: a feeling caused by something that is unexpected or unusual (e.g. earning surprise).  
  *Synonyms:* amazement, astonishment, shock, revelation.  
  *Emoji:* 😲
  
- **ambiguous**: unclassified emotions in the list or when the target of emotion is confused.  
  *Synonyms:* (subject to annotator’s understanding of the text).  
  *Emoji:* 😏
  
  Here is the tweet to classify:
  {tweet}
"""


def generate_experiment_texts(experiment_config):
    """
    Generate prompts and experiment texts from the test_stockemo.csv file
    Args:
        experiment_config: settings to use in this experiment
        num_tweets: number of tweets to return (default: 100)
    Return:
        Experiment prompts and version prompts
    """
    # Get experiment prompts
    prompts = {
        "Experiment": prompt,
    }

    # Read the CSV file
    csv_path = Path(__file__).parent.parent / "research_data" / "test_stockemo.csv"
    df = pd.read_csv(csv_path)

    # Ensure num_tweets is an integer
    num_tweets = experiment_config.get(
        "num_tweets", 10
    )  # Default to 10 if not specified
    if not isinstance(num_tweets, int):
        raise ValueError(f"num_tweets must be an integer, got {type(num_tweets)}")

    # Extract the first num_tweets tweets from the 'processed' column
    tweets = df["original"].head(num_tweets).tolist()

    # Create the texts dictionary
    texts = {
        "Experiment": [
            ("Normal", tweets),
        ],
    }

    return prompts, texts


# Update the main block to use the new parameter
if __name__ == "__main__":
    load_dotenv()
    token_count = len(tokenize(prompt))
    print(f"{'=' * 20}")
    print(f"Prompt token count: {token_count}")
    print(f"{'=' * 20}")
    print(f"Prompt character count: {len(prompt)}")
    print(f"{'=' * 20}")
    _, texts = generate_experiment_texts()
    print(f"First 5 tweets out of {len(texts['Experiment'][0][1])}:")
    for tweet in texts["Experiment"][0][1][:5]:
        print(tweet)
