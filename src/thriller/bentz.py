"""
Define Bentz experiments from Bentz, M., Cortez Espinoza, M., Simeonova, V., Köppe, T., & Onea, E. (2024). Measuring Suspense in Real Time: A New Experimental Methodology. Scientific Study of Literature, 12(1), 92–112. DOI: https://doi.org/10.61645/ssol.182
"""

common_prompt_template = """"""

experiment_text = """"""

def generate_experiment_texts(experiment_config: dict[str, str]):
    """
    Generate prompts and experiment texts
    Args:
        experiment_config: settings to use in this experiment
    Return:
        Experiment prompts and version prompts
    """
    # Get experiment prompts
    prompts = {
        "Experiment": common_prompt_template,
    }

    # Get experiment texts
    experiment_texts = experiment_text.strip().split("\n\n")
    texts = {
        "Experiment": [
            ("Normal", experiment_texts),
        ],
    }

    return prompts, texts
