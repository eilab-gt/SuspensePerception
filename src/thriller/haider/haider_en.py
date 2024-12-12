"""
Defines experiments from PO-EMO

"""

import pandas as pd
import pdb
from collections import defaultdict

file_path = './src/thriller/haider/poemo.english.emotion.tsv'

common_prompt_template="""
Labeling aesthetic emotions in poetry GUIDELINES
Our project deals with aesthetic emotions that are triggered in the reader while reading poems. The aesthetic experience certainly differs from one reader to another; nevertheless our project aims at achieving agreement among the annotator’s subjective emotions. For this purpose we developed a set of labels (altogether 9 labels) which should be used for annotation. The following manual intends to guide the annotators in labelling their subjective emotion the “right” way. Each label corresponds to one category of emotion. Every category has its own „items“ (as indicated in the parenthesis). The annotators are encouraged to use these items as a template for finding the label matching their emotion by asking:
Can I use these items to describe my current emotions concerning the verse?
If this is the case, the corresponding label is the right one to choose.
• Annoyance (annoys me, angers me, felt frustrated)
Choose this label if you feel annoyed, frustrated or even angry while reading the line/stanza.
• Awe/Sublime (found it overwhelming/sense of greatness)
Choose this label if you feel overwhelmed by the line/stanza, i.e. if you get the impression of facing something sublime or if the line/stanza inspires you with awe (such emotions are often associated with subjects like god, death, life, truth etc.).
• Beauty/Joy (found it beautiful/ pleasing/ makes me happy/ joyful)
Choose this label if you feel pleasure from reading the line/stanza (if the line/stanza puts you into a happy/joyful mood).
• Humor (found it funny/ amusing)
Choose this label if you feel amused by the line/stanza (if the line/stanza even makes you laugh).
• Nostalgia (makes me nostalgic)
Use this label only in addition with another label: + beauty/joy or + sadness!
Choose this label if the line/stanza evokes feelings of nostalgia. Nostalgia is defined as a sentimental longing for things, persons or situations in the past. It’s possible to feel nostalgic about things you haven’t experienced by your own. Notice to annotate your feeling of nostalgia together with +beauty/joy (if positive feelings) or +sadness (if negative feelings).
• Sadness (makes me sad/touches me)
Choose this label if the line/stanza makes you feel sad.
• Suspense (found it gripping/sparked my interest)
Choose this label if the line/stanza keeps you in suspense (if the line/stanza excites you or triggers your
curiosity)
• Uneasiness (found it ugly/unsettling/disturbing/frightening/distasteful)
Choose this label, if you feel discomfort about the line/stanza (if the line/stanza feels distasteful/ugly,
unsettling/disturbing or frightens you).
• Vitality (found it invigorating/spurs me on/inspires me)
Choose this label if the line/stanza has an inciting, encouraging effect. (If the line/stanza conveys a feeling
of movement, energy and vitality which it can pass over to you)

INSTRUCTIONS FOR ANNOTATING
• The annotation should reflect your current feelings while reading the poem.
• Label your emotions after reading each individual line (not sentence!).
• Read the entire stanza before annotating each line.
Use as few emotions as possible!
• Choose at least one label per line.
• You should not use more than two labels per line.
• Choose the emotion most dominant while reading the stanza.
• Choose another emotion if necessary.
• Only change the dominant emotion within a stanza, if unavoidable.
• If you change the non-dominant emotion within a stanza, remember to keep labelling the
dominant emotion additionally to the new emotion.
• Notice that nostalgia always has to be used with an additonal label: beauty/joy or sadness

GOLD STANDARD
The following examples serve as an orientation for the annotators. The exemplarily emotion is highlighted.
When in doubt, then gold standard!

• Annoyance (annoys me, angers me, felt frustrated)
Example 1
In every cry of every Man, [Sadness] [Annoyance]
In every Infants cry of fear, [Sadness] [Annoyance]
In every voice: in every ban, [Sadness] [Annoyance] The mind-forg'd manacles I hear [Sadness] [Annoyance]
How the Chimney-sweepers cry [Sadness] [Annoyance] Every blackning Church appalls, [Sadness] [Annoyance] And the hapless Soldiers sigh [Sadness] [Annoyance] Runs in blood down Palace walls [Sadness] [Annoyance]
But most thro' midnight streets I hear [Sadness] [Annoyance]
How the youthful Harlots curse [Sadness] [Annoyance]
Blasts the new-born Infants tear [Sadness] [Annoyance]
And blights with plagues the Marriage hearse [Sadness] [Annoyance]

• Awe/Sublime (found it overwhelming/sense of greatness)
Example 1
The moving waters at their priestlike task [Awe / Sublime]
Of pure ablution round earth's human shores, [Awe / Sublime]
Or gazing on the new soft-fallen mask [Awe / Sublime]
Of snow upon the mountains and the moors— [Awe / Sublime]

• Beauty/Joy (found it beautiful/ pleasing/ makes me happy/ joyful) 
Example 1
i carry your heart with me(i carry it in [Beauty/Joy]
my heart)i am never without it(anywhere [Beauty/Joy]
i go you go, my dear; and whatever is done [Beauty/Joy]
by only me is your doing, my darling) [Beauty/Joy]
i fear [Beauty/Joy]
no fate(for you are my fate, my sweet)i want [Beauty/Joy]
no world(for beautiful you are my world, my true) [Beauty/Joy] 
and it's you are whatever a moon has always meant [Beauty/Joy] 
and whatever a sun will always sing is you [Beauty/Joy]

• Humor (found it funny/ amusing) 
Example 1
I'm Nobody! Who are you? [Humor]
Are you - Nobody - too? [Humor]
Then there's a pair of us! [Humor]
Dont tell! they'd advertise - you know! [Humor]
How dreary - to be - Somebody! [Humor]
How public - like a Frog - [Humor]
To tell one's name - the livelong June - [Humor] 
To an admiring Bog! [Humor]

• Nostalgia (makes me nostalgic)
Example 1
Thou'll break my heart, thou bonnie bird, [Sadness] 
That sings upon the bough; [Sadness]
Thou minds me o' the happy days [Nostalgia] [Sadness] 
When my fause luve was true. [Nostalgia] [Sadness]

• Sadness (makes me sad/touches me) Example 1
I felt a Funeral, in my Brain, [Sadness]
And Mourners to and fro [Sadness]
Kept treading - treading - till it seemed [Sadness] That Sense was breaking through - [Sadness]

• Suspense (found it gripping/sparked my interest) 
Example 1
The Second Coming! Hardly are those words out [Uneasiness] [Suspense] 
When a vast image out of Spiritus Mundi [Uneasiness] [Suspense]
Troubles my sight: somewhere in sands of the desert [Uneasiness] [Suspense] 
A shape with lion body and the head of a man, [Uneasiness] [Suspense]
A gaze blank and pitiless as the sun, [Uneasiness] [Suspense]
Is moving its slow thighs, while all about it [Uneasiness] [Suspense] 
Reel shadows of the indignant desert birds. [Uneasiness] [Suspense]

• Uneasiness (found it ugly/unsettling/disturbing/frightening/distasteful) 
Example 1
To wait in heavy harness [Uneasiness]
On fluttered folk and wild - [Uneasiness] Your new-caught sullen peoples, [Uneasiness] Half devil and half child. [Uneasiness]

• Vitality (found it invigorating/spurs me on/inspires me) 
Example 1
Be fair or foul or rain or shine [Vitality]
The joys I have possessed, in spite of fate, are mine. [Vitality] Not Heaven itself upon the past has power, [Vitality]
But what has been, has been, and I have had my hour. [Vitality]

Annotate the stanza below
"""

texts = {
    "Experiment A": []
}

prompts = {
    "Experiment A": common_prompt_template
}

def extract_poems(poems):
    poem_tuples = []
    for poem in poems:
        if not poem:  # skip if the poem is empty
            continue
        
        # Extract the title from the first stanza
        title = poem[0][0][0]
        
        # Initialize a list to hold all stanzas
        poem_text = []
        
        # Iterate through each stanza after the title
        for stanza in poem[1:]:
            # Join each line in the stanza with a new line
            stanza_text = "\n".join(line[0] for line in stanza)
            poem_text.append(stanza_text)

        poem_tuples.append((title, poem_text))
    
    return poem_tuples

def readPoems(fn):
  poems = []
  poem = []
  stanza = []
  prev_line = None
  for line in open(fn):
    line = line.strip()
    if line=="": 
      if prev_line=="":
        if poem!=[]: 
          poems.append(poem)
          poem=[]
      else:
        if stanza!=[]: poem.append(stanza)
        stanza = []
    else:
      stanza.append(line.split("\t"))
    prev_line = line 
  if poem!=[]: poems.append(poem)
  return poems
            
import csv

def write_poems_to_csv(poems, csv_filename):
    # Open CSV file for writing
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write header
        writer.writerow([
            'poem_id', 'stanza_id', 'line_id', 'total_lines_in_stanza', 
            'total_stanzas_in_poem', 'id_stanza_in_poem', 'id_line_in_stanza', 
            'title', 'line_text', 'emotion1anno1', 'emotion2anno1', 'emotion1anno2', 'emotion2anno2'
        ])

        # Initialize dictionary to store count of lines with different number of elements
        element_count_dict = defaultdict(int)
        
        # Iterate through poems to extract details
        for poem_id, poem in enumerate(poems):
            title = poem[0][0][0] if poem and poem[0] and poem[0][0] else ""
            total_stanzas_in_poem = len(poem) - 1  # Exclude title stanza
            
            for stanza_id, stanza in enumerate(poem[1:], start=1):
                total_lines_in_stanza = len(stanza)
                
                for line_id, line in enumerate(stanza):
                    a0,a1 = line[1],line[2]

                    parts = a0.split(" --- ")

                    emo1anno1 = parts[0]
                    emo2anno1 = parts[1] if len(parts) > 1 else None  

                    parts = a1.split(" --- ")

                    emo1anno2 = parts[0]
                    emo2anno2 = parts[1] if len(parts) > 1 else None  

                    line_text = line[0] if len(line) > 0 else ""
                    
                    # Update element count dictionary
                    element_count_dict[len(line)] += 1

                    # Write row to CSV
                    writer.writerow([
                        poem_id + 1, stanza_id, line_id + 1, total_lines_in_stanza,
                        total_stanzas_in_poem, stanza_id, line_id + 1, title,
                        line_text, emo1anno1, emo2anno1, emo1anno2, emo2anno2
                    ])
        
        # Print the dictionary with the count of lines having different numbers of elements
        print("Element Count Dictionary:", dict(element_count_dict))



def generate_experiment_texts(experiment_config: dict[str, str]):
    """
    Generate prompts and experiment texts
    Args:
        experiment_config: settings to use in this experiment
    Return:
        Experiment prompts and version prompts
    """

    # UNCOMMENT FOR ONE TIME PARSING TSV file to CSV, after which we read from the csv file hence these can be commented
    # poems = readPoems(file_path)
    csv_filename = './src/thriller/haider/poems.csv'
    # write_poems_to_csv(poems, csv_filename)

    with open(csv_filename, mode='r', newline='', encoding='utf-8') as file:
        reader = list(csv.DictReader(file))

    updated_rows = []
    current_poem_id = None
    current_stanza_id = None
    stanza_lines = []
    poem_tuples = []
    poem_text = []

    for row in reader:
        poem_id = row['poem_id']
        if (current_poem_id is not None) and (poem_id != current_poem_id):
            if stanza_lines:
                # Process the previous stanza
                stanza_text = "\n".join(stanza_lines)
                poem_text.append(stanza_text)
                stanza_lines = []
            poem_tuples.append((poem_title, poem_text))
            poem_text = []
        stanza_id = row['stanza_id']
        line_text = row['line_text']
        poem_title = row['title']
        
        # Detect when we are in a new stanza
        if (poem_id, stanza_id) != (current_poem_id, current_stanza_id):
            if stanza_lines:
                # Process the previous stanza
                stanza_text = "\n".join(stanza_lines)
                poem_text.append(stanza_text)
                stanza_lines = []

        stanza_lines.append(line_text)
        # Update the current stanza tracking variables
        current_poem_id, current_stanza_id = poem_id, stanza_id
    
    # saves last poem
    if poem_text:
       if stanza_lines:
            # Process the previous stanza
            stanza_text = "\n".join(stanza_lines)
            poem_text.append(stanza_text)
            stanza_lines = []
       poem_tuples.append((poem_title, poem_text))
       poem_text = []
    
    texts["Experiment A"]=poem_tuples
    return prompts, texts