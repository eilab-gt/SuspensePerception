# Thriller Notes

## OpenDevin
"""
Our objective is to build a research experiment together where we will measuring the ability of Large Language Models to correctly infer human emotional states when reading text from stories.
Your first task is to learn what the existing code does, and think about the broader project context, so we can improve the code and keep building. Please browse to our project folder `Thriller` and scan the files there. In particular you will need to read the contents of `gerrig.ipynb` which contains the code I have written so far. The notebook contains code where we query a LLM using Together.AI's API. Please begin your task now.
"""

## TODOs
Write python modules we can call from CLI so be sure to use if __name__ == '__main__' style.
Import and implement `argparse` and use args.model_id to pass in the model we are calling.
Add the config fields from the YAML into the argaparse so either can be used.
There should an arg to specify the config file or use the arg inputs

- Make sure your functions have docstrings; add comments when appropriate in functions
- Classify as YES/NO by using a Likert scle and collapsing down the values to a binarized label
- Write a function inputting dataframe to visualize the extracted data using histograms and box plots
