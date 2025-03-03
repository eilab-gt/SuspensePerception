import random
import numpy as np
import string
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
from textattack.augmentation import Augmenter
from textattack.shared.attacked_text import AttackedText
import logging
from typing import List, Dict, Any, Union
import torch
import difflib
import textattack
from misc import generate_response
import re

import nltk
nltk.download('averaged_perceptron_tagger_eng', quiet=True)
nltk.download("punkt_tab", quiet=True)

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


def apply_synonym_replacement(text: str, params: dict) -> tuple:
    aug = naw.SynonymAug(
        aug_src=params.get('aug_src', 'wordnet'),
        aug_p=params.get('aug_p', 0.3),
        aug_min=params.get('aug_min', 1),
        aug_max=params.get('aug_max', 10),
        stopwords=params.get('stopwords', None)
    )
    
    augmented_text = aug.augment(text)
    if not augmented_text:
        logger.warning("Synonym replacement returned None, using original text.")
        return text, []
    augmented_text = augmented_text[0]
    original_words = text.split()
    augmented_words = augmented_text.split()
    diffs = []

    for i, s in enumerate(difflib.ndiff(original_words, augmented_words)):
        if s[0] == ' ':
            continue
        elif s[0] == '-':
            diffs.append(f"Original: {s[2:]}")
        elif s[0] == '+':
            diffs.append(f"Changed to: {s[2:]}")
    return augmented_text


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
    # Split text into paragraphs
    paragraphs = text.split("\n\n")  # Assuming paragraphs are separated by double newlines
    
    # Split each paragraph into sentences using regex
    paragraph_sentences = [re.split(r'(?<=[.!?])\s+', p) for p in paragraphs]
    
    # Flatten all sentences into a list and shuffle
    all_sentences = [sentence for p in paragraph_sentences for sentence in p]
    shuffle_n_times = params.get('shuffle_n_times', 1)
    for _ in range(shuffle_n_times):
        random.shuffle(all_sentences)
    
    # Reconstruct paragraphs with the same number of sentences
    new_paragraphs = []
    index = 0
    for sentences in paragraph_sentences:
        new_paragraphs.append(" ".join(all_sentences[index:index + len(sentences)]))
        index += len(sentences)
    
    # Join paragraphs back into a string with double newlines
    return "\n\n".join(new_paragraphs)


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
    pct_words_to_swap = params.get('pct_words_to_swap', 0.1)

    augmenter = Augmenter(transformation=transformation, pct_words_to_swap=pct_words_to_swap)
    augmented_text = augmenter.augment(text)
    
    return augmented_text


def apply_word_swap_homoglyph(text: str, params: dict) -> str:
    # Initialize without unsupported parameters
    transformation = WordSwapHomoglyphSwap()  # No parameters here
    
    pct_words_to_swap = params.get('pct_words_to_swap', 0.1)

    augmenter = Augmenter(transformation=transformation, pct_words_to_swap=pct_words_to_swap)
    augmented_text = augmenter.augment(text)

    return augmented_text


def apply_sentence_paraphrase(text: str, params: dict) -> str:
    prompt = params.get("prompt", "Paraphrase the following passage in the driest and most stripped-down manner possible. Retain only the core actions and events, eliminating any descriptive or expressive language. The result should read as plainly as possible while preserving the essential meaning.")
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": text},
    ]
    transformed_texts = generate_response(messages, params)
    if transformed_texts:
        return transformed_texts
    logger.warning("Paragraph returned no transformations, using original text.")
    return text


def apply_backtranslation(text: str, params: dict) -> str:
    transformation = BackTranslation(
        src_lang=params.get('src_lang', 'en'),
        target_lang=params.get('target_lang', 'fr')
    )
    attacked_text = AttackedText(text)
    transformed_texts = transformation(attacked_text)
    if transformed_texts:
        return transformed_texts[0].text  # Get the first transformed text
    logger.warning("Sentence paraphrase returned no transformations, using original text.")
    return text
  

def distraction_insertion(text: str, params: dict) -> str:
    """
    Insert distraction sentences into the text that simultaneously
    introduces and removes a topic/solution from the text.
    """
    distractions = params.get('distractions', [])
    budget = params.get('distractions_per_sentence', 0.2)
    min_sentences = params.get('min_sentences', 1)
    max_sentences = params.get('max_sentences', 20)

    # Split paragraphs while keeping them
    paragraphs = text.split("\n\n")
    all_sentences = [re.split(r'(?<=[.!?])\s+', para) for para in paragraphs]
    
    # Flatten to count total sentences
    sentence_list = [sent for para in all_sentences for sent in para if sent]

    number_of_distractions = min(max(min(int(len(sentence_list) * budget), max_sentences), min_sentences), len(distractions))

    # Select random distraction sentences without repetition
    chosen_distractions = random.sample(distractions, number_of_distractions)

    # Insert them at random positions
    for distraction in chosen_distractions:
        insert_para = random.randint(0, len(all_sentences) - 1)
        insert_sent = random.randint(0, len(all_sentences[insert_para]))

        all_sentences[insert_para].insert(insert_sent, distraction)

    # Reconstruct paragraphs
    text = "\n\n".join(" ".join(para) for para in all_sentences)

    return text 


def apply_caesar(text: str, params : dict) -> str:
    """
    Caesar cipher the text
    """
    step = params.get('step', 3)
    alphabets = params.get('alphabets', (string.ascii_lowercase, string.ascii_uppercase, string.digits))

    def shift(alphabet):
        return alphabet[step:] + alphabet[:step]
    
    shifted_alphabets = tuple(map(shift, alphabets))
    joined_aphabets = ''.join(alphabets)
    joined_shifted_alphabets = ''.join(shifted_alphabets)
    table = str.maketrans(joined_aphabets, joined_shifted_alphabets)
    return text.translate(table)

  
def swap_words_in_sentences(text: str, params: dict)  -> str:
    sentences = nltk.sent_tokenize(text)
    swapped_sentences = []
    num_swaps = params.get('num_swaps', 2)
    
    for sentence in sentences:
        words = sentence.split()
        for _ in range(num_swaps):
            if len(words) > 1:
                idx1, idx2 = random.sample(range(len(words)), 2)
                words[idx1], words[idx2] = words[idx2], words[idx1]
        swapped_sentence = " ".join(words)
        swapped_sentences.append(swapped_sentence)
    swapped_paragraph = " ".join(swapped_sentences)
    return swapped_paragraph
  

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
    'backtranslation': apply_backtranslation,
    'distraction_insertion': distraction_insertion,
    'swap_words' : swap_words_in_sentences,
    'caesar_cipher': apply_caesar
}


# Normalize input data to ensure consistent structure
def normalize_stories(data: Union[List[Any], str]) -> List[str]:
    if isinstance(data, list):
        return data
    elif isinstance(data, str):
        return [data]
    else:
        raise ValueError("Unsupported data format")


# Main augmentation function
def augment_texts(story: List[str], config: Dict[str, Any]) -> List[str]:
    augmented_story = []

    augmentations = config.get('augmentation_order', [])
    if not augmentations:
        return story
    
    augmentation = augmentations[0]
    aug_params = config.get(augmentation, {})

    is_aug_enabled = aug_params.get('enabled', False)
    if not is_aug_enabled:
        return story
    
    # If augumentation applied to whole story, merge passages together
    is_per_passage = aug_params.get('is_per_passage', True)
    if not is_per_passage:
        story = ["\n\n".join(story)]

    for passage in story:
        augmented_passage = passage

        if passage:
            try:
                logger.info(f"Applying {augmentation}: {aug_params}")
                if augmentation in augmentation_functions:
                    augmented_passage = augmentation_functions[augmentation](augmented_passage, aug_params)
                else:
                    logger.error(f"Augmentation function for '{augmentation}' not found.")
            except Exception as e:
                logger.error(f"Error augmenting passage: {e}")
        else:
            logger.warning("Empty story encountered; skipping.")

        augmented_story.append(augmented_passage)

    # If augumentation applied to whole story, unmerge passages
    if not is_per_passage:
        augmented_story = augmented_story[0].strip().split("\n\n")

    return augmented_story



    # augumented_story = []

    # passage = ""

    # for passage in story:
    #     augmented_passage = passage

    #     if passage:

    #         leading_numbers = []
    #         # Save leading numbers for later:
    #         for m in re.finditer(r"(?<=^)(\d+)(?=\s+[^\s])", augmented_passage):
    #             leading_numbers.append(m)

    #         # Remove leading numbers:
    #         for m in leading_numbers[::-1]:
    #             augmented_passage = augmented_passage[:m.start()] + " " + augmented_passage[m.end():]


    #         for augmentation in config.get('augmentation_order', []):
    #             try:
    #                 aug_params = config.get(augmentation, {})
    #                 if aug_params.get('enabled', False):
    #                     logger.info(f"Applying {augmentation}: {aug_params}")
    #                     if augmentation in augmentation_functions:
    #                         augmented_passage = augmentation_functions[augmentation](augmented_passage, aug_params)
    #                     else:
    #                         logger.error(f"Augmentation function for '{augmentation}' not found.")
    #             except Exception as e:
    #                 logger.error(f"Error augmenting passage: {e}")
    #     else:
    #         logger.warning("Empty story encountered; skipping.")
            
    #     # Add leading numbers back:
    #     for m in leading_numbers:
    #         to_add = m.group() + " " if augmented_passage[m.start()] != " " else m.group()
    #         augmented_passage = augmented_passage[:m.start()] + to_add + augmented_passage[m.start():]
        
    #     augumented_story.append(augmented_passage)

    # return augumented_story


def get_default_augmentation_config():
    return {
        'synonym_replacement': {
            'enabled': True,
            'aug_p': 0.8,
            'aug_src': 'wordnet',
            'model_path':'bert-base-uncased',
            'aug_min': 20,
            'aug_max': 50,
            'stopwords': None,
            'is_per_passage': True,
        },
        'distraction_insertion': {
            'enabled': True,
            'distractions': [
                "He looked for his hidden watch, but couldn't find it.",
                "She reached for the letter on the table, but it wasn't there.",
                "He felt for his keys in his pocket, but found nothing.",
                "The cat sat on the windowsill, or at least he thought it had.",
                "She turned the page of the book, but there was no text.",
                "He grabbed his phone to check the time, but his hands were empty.",
                "The wind carried the sound of bells, but no bells were ringing.",
                "She opened the drawer for the scissors, but it was empty.",
                "He stepped onto the path that had been there yesterday, but now it was gone.",
                "The reflection in the mirror blinked, but he hadn't moved.",
                "She picked up the pen to write, but there was no ink.",
                "He searched his bag for his wallet, but he must have left it at home.",
                "The clock chimed midnight, yet there was no clock in the room.",
                "She reached out to grab the railing, but her hand met only air.",
                "He pulled his coat tighter, but realized he wasn't wearing one.",
                "The photograph on the desk showed a familiar face, but the next time he looked, it was blank.",
                "She put the teacup back on the shelf, but she had never taken it down.",
                "He felt the weight of the book in his hands, until he didn't.",
                "The candle flickered, but there was no flame.",
                "She tucked the loose strand of hair behind her ear, but it wasn't there.",
                "The footprints in the snow led nowhere, then disappeared.",
            ],
            'distractions_per_sentence': 0.2,
            'min_sentences': 1,
            'max_sentences': 20,
            'is_per_passage': False,
        },
        'swap_words' : {
            'enabled' : True,
            'num_swaps' : 30,
            'is_per_passage': True,
        },
        'shuffle_sentences': {
            'enabled': True,
            'shuffle_n_times': 100,
            'is_per_passage': False,
        },
        'introduce_typos': {
            'enabled': True,
            'aug_char_p': 0.8,
            'aug_word_p': 0.8,
            'is_per_passage': True,
        },
        'word_swap_embedding': {
            'enabled': True,
            'max_candidates': 5,
            'is_per_passage': True,
        },
        'change_character_names': {
            'enabled': True,
            'name_list': ['Alex', 'Jordan', 'Taylor', 'Riley', 'Morgan'],
            'is_per_passage': True,
        },
        'context_removal': {
            'enabled': True,
            'sentiment_threshold': 0.5,
            'is_per_passage': True,
        },
        'word_swap_homoglyph': {
            'enabled': True,
            'max_swaps': 100,
            'is_per_passage': True,
        },
        'sentence_paraphrase': {
            'enabled': True,
            'api_type': "together",
            'name': "meta-llama/Llama-3-8b-chat-hf",
            'prompt': 'Paraphrase the following passage in the driest and most stripped-down manner possible. Retain only the core actions and events, eliminating any descriptive or expressive language. The result should read as plainly as possible while preserving the essential meaning.',
            'max_tokens': 1000,
            'temperature': 0.0,
            'top_p': 0.9,
            'repetition_penalty': 1.0,
            'stop': ["<|eot_id|>"],
            'stream': True,
            'is_per_passage': True,
        },
        'backtranslation': {
            'enabled': True,
            'src_lang': 'en',
            'target_lang': 'fr',
            'is_per_passage': True,
        },
        'caesar_cipher': {
            'enabled': True,
            'step': 3,
            'alphabets': (string.ascii_lowercase, string.ascii_uppercase, string.digits),
            'is_per_passage': True,
        },

        'has_passage_numbers': False,

        # Commented out, but left here to show available augmentations
        # By default all of them are disabled
        'augmentation_order': [
            # 'distraction_insertion',
            # 'swap_words',
            # 'shuffle_sentences',
            # 'introduce_typos',
            # 'word_swap_embedding',
            # 'change_character_names',
            # 'context_removal',
            # 'word_swap_homoglyph',
            # 'sentence_paraphrase',
            # 'backtranslation',
            # 'synonym_replacement',
        ]
    }

def process_and_augment_stories(story, augmentation_config):
    # Normalize the story using a hypothetical normalize function
    normalized_story = normalize_stories(story)

    # Configuration for augmentation
    augmented_story = augment_texts(normalized_story, augmentation_config)

    # Add passage numbers if set
    has_passage_numbers = augmentation_config.get('has_passage_numbers', False)
    if has_passage_numbers:
        for i, augmented_passage in enumerate(augmented_story):
            augmented_passage = f"{str(i + 1)} {augmented_passage}"
            augmented_story[i] = augmented_passage

    return augmented_story
