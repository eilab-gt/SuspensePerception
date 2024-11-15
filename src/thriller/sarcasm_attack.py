import string
import logging
from typing import List, Dict, Any, Union

def sarcasm(stories: List[str]) -> List[List[str]]:
    """every other capitalization ex. hellow world -> HeLlO wOrLd """
    augmented_stories = []
    for story in stories:
        sarcasm_text  = []
        augmented_story = []
        for story in stories:
            letter_index = 0
            for char in story.replace('\n', ''):
                if char in string.ascii_letters:
                    if letter_index % 2 == 0:
                        sarcasm_text.append(char.upper())
                    else:
                        sarcasm_text.append(char.lower())
                    letter_index = letter_index + 1
                else:
                    sarcasm_text.append(char)
            augmented_story.append(''.join(sarcasm_text))
                    
        augmented_stories.append([augmented_story])
    print(augmented_stories)
    return augmented_stories

print("Conversions complete!")

