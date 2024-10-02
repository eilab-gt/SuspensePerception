import random
import numpy as np
import spacy
import nlpaug.augmenter.word as naw
import nlpaug.augmenter.char as nac
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textattack.transformations import (
    WordSwapEmbedding,
    WordSwapHomoglyphSwap,
    WordSwapRandomCharacterSubstitution,
    BackTranslation
)
from textattack.shared.attacked_text import AttackedText
import logging
from typing import List, Dict, Any, Union
import torch
import textattack
import nltk
nltk.download('averaged_perceptron_tagger')

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

# Initialize sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Set random seed for reproducibility
def set_random_seed(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    textattack.shared.utils.set_seed(seed)

set_random_seed(42)

# Augmentation functions mapping
def apply_synonym_replacement(text: str, params: dict) -> str:
    aug = naw.SynonymAug(
        aug_src=params.get('aug_src', 'wordnet'),
        aug_p=params.get('aug_p', 0.3),
        aug_min=params.get('aug_min', 1),
        aug_max=params.get('aug_max', 10),
        stopwords=params.get('stopwords', None)
    )
    augmented_text = aug.augment(text)
    if augmented_text:
        return augmented_text[0]  # Return the first augmented text
    logger.warning("Synonym replacement returned None, using original text.")
    return text

def apply_antonym_replacement(text: str, params: dict) -> str:
    aug = naw.AntonymAug(
        aug_p=params.get('aug_p', 0.1),
        aug_min=params.get('aug_min', 1),
        aug_max=params.get('aug_max', 10)
    )
    augmented_text = aug.augment(text)
    if augmented_text:
        return augmented_text[0]  # Return the first augmented text
    logger.warning("Antonym replacement returned None, using original text.")
    return text

def apply_introduce_typos(text: str, params: dict) -> str:
    typo_aug = nac.KeyboardAug(
        aug_char_p=params.get('aug_char_p', 0.1),
        aug_word_p=params.get('aug_word_p', 0.3),
        include_special_char=params.get('include_special_char', False),
        aug_char_min=params.get('aug_char_min', 1),
        aug_char_max=params.get('aug_char_max', 10),
        stopwords=params.get('stopwords', None)
        # Removed the 'case' parameter
    )
    augmented_text = typo_aug.augment(text)
    if augmented_text:
        return augmented_text[0]  # Return the first augmented text
    logger.warning("Introduce typos returned None, using original text.")
    return text


def apply_change_character_names(text: str, params: dict) -> str:
    name_list = params.get('name_list', ['Alex', 'Jordan', 'Taylor', 'Riley', 'Morgan'])
    doc = nlp(text)
    names_in_text = {ent.text for ent in doc.ents if ent.label_ == 'PERSON'}
    name_mapping = {name: random.choice(name_list) for name in names_in_text}
    for original_name, new_name in name_mapping.items():
        text = text.replace(original_name, new_name)
    return text

def apply_shuffle_sentences(text: str, params: dict) -> str:
    shuffle_n_times = params.get('shuffle_n_times', 1)
    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    for _ in range(shuffle_n_times):
        random.shuffle(sentences)
    return ' '.join(sentences)

def apply_context_removal(text: str, params: dict) -> str:
    threshold = params.get('sentiment_threshold', 0.5)
    doc = nlp(text)
    new_sentences = []
    for sent in doc.sents:
        sentiment = analyzer.polarity_scores(sent.text)
        if abs(sentiment['compound']) < threshold:
            new_sentences.append(sent.text)
    return ' '.join(new_sentences)

def apply_word_swap_embedding(text: str, params: dict) -> str:
    transformation = WordSwapEmbedding(
        max_candidates=params.get('max_candidates', 5)
    )
    attacked_text = AttackedText(text)
    transformed_texts = transformation(attacked_text)
    if transformed_texts:
        return transformed_texts[0].text  # Get the first transformed text
    logger.warning("Word swap embedding returned no transformations, using original text.")
    return text

def apply_word_swap_homoglyph(text: str, params: dict) -> str:
    # Initialize without unsupported parameters
    transformation = WordSwapHomoglyphSwap()  # No parameters here
    attacked_text = AttackedText(text)
    transformed_texts = transformation(attacked_text)
    if transformed_texts:
        return transformed_texts[0].text  # Get the first transformed text
    logger.warning("Word swap homoglyph returned no transformations, using original text.")
    return text

def apply_sentence_paraphrase(text: str, params: dict) -> str:
    transformation = BackTranslation(
        src_lang=params.get('src_lang', 'en'),
        mid_lang=params.get('mid_lang', 'fr')
    )
    attacked_text = AttackedText(text)
    transformed_texts = transformation(attacked_text)
    if transformed_texts:
        return transformed_texts[0].text  # Get the first transformed text
    logger.warning("Sentence paraphrase returned no transformations, using original text.")
    return text

# Mapping of augmentation names to functions
augmentation_functions = {
    'synonym_replacement': apply_synonym_replacement,
    'antonym_replacement': apply_antonym_replacement,
    'introduce_typos': apply_introduce_typos,
    'change_character_names': apply_change_character_names,
    'shuffle_sentences': apply_shuffle_sentences,
    'context_removal': apply_context_removal,
    'word_swap_embedding': apply_word_swap_embedding,
    'word_swap_homoglyph': apply_word_swap_homoglyph,
    'sentence_paraphrase': apply_sentence_paraphrase,
}

# Normalize input data to ensure consistent structure
def normalize_stories(data: Union[List[Any], str]) -> List[List[str]]:
    if isinstance(data, list):
        if all(isinstance(item, str) for item in data):
            return [data]
        elif all(isinstance(item, list) for item in data):
            return data
        else:
            raise ValueError("List items must be either all strings or all lists.")
    elif isinstance(data, str):
        return [[data]]
    else:
        raise ValueError("Unsupported data format")

# Main augmentation function
def augment_texts(
    stories: List[List[str]],
    config: Dict[str, Any]
) -> List[List[str]]:
    augmented_stories = []
    for story in stories:
        i =0
        # Assuming there's only one passage per story
        if story:  # Check if the story is not empty
            passage = story[0]  # Get the first passage
            augmented_passage = passage
                # Apply augmentations in the specified order
            for augmentation in config.get('augmentation_order', []):
                try:
                    print(i)
                    i+=1
                    aug_params = config.get(augmentation, {})
                    if aug_params.get('enabled', False):
                        logger.info(f"Applying {augmentation}: {aug_params}")
                        if augmentation in augmentation_functions:
                            augmented_passage = augmentation_functions[augmentation](augmented_passage, aug_params)
                        else:
                            logger.error(f"Augmentation function for '{augmentation}' not found.")
                except Exception as e:
                    logger.error(f"Error augmenting passage: {e}")
            # Add the augmented passage to the augmented stories
            augmented_stories.append([augmented_passage])  # Wrap it in a list
        else:
            logger.warning("Empty story encountered; skipping.")
            augmented_stories.append([passage])  # Append original passage if story is empty

    return augmented_stories

def process_and_augment_stories(stories):
    # Normalize the stories using a hypothetical normalize function
    normalized_stories = normalize_stories(stories)

    # Configuration for augmentation
    augmentation_config = {
        'synonym_replacement': {
            'enabled': True,
            'aug_p': 0.7,
            'aug_src': 'wordnet',
            'aug_min': 5,
            'aug_max': 30,
            'stopwords': None,
            'target_words': [
                'room', 'doorway', 'finger', 'summons', 'passage', 'house', 'kick', 'man', 'pain', 
                'gunmen', 'words', 'lightning', 'wall', 'foot', 'hand', 'shoe', 'ground', 
                'damage', 'heart', 'eyes', 'deep', 'black', 'run', 'blood', 'cold', 'dark', 'scar'
            ],
        },
        'shuffle_sentences': {
            'enabled': True,
            'shuffle_n_times': 100
        },
        'introduce_typos': {
            'enabled': True,
            'aug_char_p': 0.8,
            'aug_word_p': 0.8,
        },
        'word_swap_embedding': {
            'enabled': True,
            'max_candidates': 5
        },
        'change_character_names': {
            'enabled': True,
            'name_list': ['Alex', 'Jordan', 'Taylor', 'Riley', 'Morgan']
        },
        'context_removal': {
            'enabled': True,
            'sentiment_threshold': 0.5
        },
        'word_swap_homoglyph': {
            'enabled': True,
            'max_swaps': 100
        },
        'sentence_paraphrase': {
            'enabled': True,
            'src_lang': 'en',
            'mid_lang': 'fr'
        },
        'augmentation_order': [
            'sentence_paraphrase'
            'synonym_replacement',
            'introduce_typos',
            'word_swap_embedding',
            'context_removal',
            'change_character_names',
            'word_swap_homoglyph',
        ]
    }

    augmented_stories = augment_texts(normalized_stories, augmentation_config)
    return augmented_stories

