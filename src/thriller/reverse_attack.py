import pysbd
import re
import logging
from typing import List, Dict, Any, Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
example:
.Chiffre Le barked ”.him Search“ .Bond searched carefully gunmen two The
"""
def reverse_sentences(stories: List[str]) ->List[List[str]] :
    augmented_stories = []
    for story in stories:
        reversed_text = []
        seg = pysbd.Segmenter(language="en", clean=False)
        sentences = seg.segment(story)

        reversed_line = ""
        for sentence in sentences:
            # words = ['Blofeld', 'smiled', 'and', 'said,',...'weary', 'of', 'pointing', 'a', 'gun', 'at', 'you.”']
            words =  sentence.split()
            reversed_sentence = ""
            for word in words:
                split_word  = re.split(r'([.!?,“])', word)
                reversed_word = "".join(split_word[::-1])
                reversed_sentence += "".join(reversed_word[::-1]) + " "
            reversed_line += "".join(reversed_sentence[::-1])

        reversed_text.append(reversed_line)
        augmented_stories.append([reversed_text])
    print(augmented_stories)
    return augmented_stories


def reverse_words(stories: List[str]) -> List[List[str]]:
    augmented_stories = []
    for story in stories:
        reversed_text = []
        seg = pysbd.Segmenter(language="en", clean=False)
        sentences = seg.segment(story)
        
        reversed_line = ""
        for sentence in sentences:
            words = sentence.split()
            reversed_sentence = ""
            for word in words:
                split_words = re.split(r'([.!?,“])', word)
                reversed_split_word = [split_word[::-1] for split_word in split_words]
                reversed_sentence += "".join(reversed_split_word) + " "
            reversed_line += reversed_sentence
            
        reversed_text.append(reversed_line)
        augmented_stories.append([reversed_text])
    print(augmented_stories)
    return augmented_stories

print("Conversions complete!")

