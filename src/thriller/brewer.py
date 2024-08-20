common_prompt_template_in_between = """
The following is "The Lost Phoebe" by Theodore Dreiser.
After each paragraph, answer these questions:

***Question 1: "To what extent do you feel anticipation, excitement, or anxiety about events yet to come in the passage?"***
1. Not at all
2. Slightly
3. Somewhat
4. Neutral or Uncertain
5. Moderately
6. Very much
7. Extremely

***Question 2: "To what extent do you want to learn more about past events (events which already occurred in the passage up to this point, or which occurred before the passage began)?"***
1. Not at all
2. Slightly
3. Somewhat
4. Neutral or Uncertain
5. Moderately
6. Very much
7. Extremely

***Question 3: "To what extent do you want to learn more about events yet to come in the passage?"***
1. Not at all
2. Slightly
3. Somewhat
4. Neutral or Uncertain
5. Moderately
6. Very much
7. Extremely

***Question 4: "To what extent did you feel surprised by any information or events in the passage?"***
1. No surprise
2. Slightly surprised
3. Somewhat surprised
4. Neutral or Uncertain
5. Moderately surprised
6. Very surprised
7. Extremely surprised

***Question 5: "To what extent did you feel irony in relation to information or events in the passage?"***
1. No irony
2. Slight irony
3. Some irony
4. Neutral or Uncertain
5. Moderate irony
6. Much irony
7. Extreme irony
"""
common_prompt_template_final = """
The passage you have been reading is now over. Please answer the following questions:

***Question 1: "Overall, how much did you enjoy, appreciate, or like the passage?"***
1. Did Not Like
2. Slightly Liked
3. Somewhat Liked
4. Neutral or Uncertain
5. Moderately Liked
6. Liked Very Much
7. Liked Extremely Much

***Question 2: "During your reading, to what extent did you feel either bored or interested while reading the passage?"***
1. Very Bored
2. Slightly Bored
3. Somewhat Bored
4. Neutral or Uncertain
5. Somewhat Interested
6. Very Interested
7. Extremely Interested

***Question 3: "Some of the passages used in this experiment may be stories, and some may not be stories. To what extent do you consider that this passage, as given to you, makes a 'story'?"***
- NS (Not a Story)
- ? (Not Sure)
- S (Is a Story)

***Question 4: "To what extent were you satisfied with the outcome of the passage?"***
1. Very Unsatisfied
2. Slightly Unsatisfied
3. Somewhat Unsatisfied
4. Neutral or Uncertain
5. Somewhat Satisfied
6. Very Satisfied
7. Extremely Satisfied

***Question 5: "To what extent did the passage seem complete?"***
1. Incomplete
2. Slightly Complete
3. Somewhat Complete
4. Neutral or Uncertain
5. Somewhat Complete
6. Very Complete
7. Extremely Complete

***Question 6: "Was the information in the passage correctly arranged? That is, was the information given at the best possible times to produce as effective a story as would be possible from this material?"***
1. Not Arranged Correctly
2. Slightly Arranged Correctly
3. Somewhat Arranged Correctly
4. Neutral or Uncertain
5. Somewhat Arranged Correctly
6. Very Arranged Correctly
7. Extremely Arranged Correctly

***Question 7: "To what extent did you empathize or identify with the character(s) in the passage?"***
1. Not at All
2. Slightly
3. Somewhat
4. Neutral or Uncertain
5. Somewhat
6. A Lot
7. A Great Deal

***Question 8: "To what extent could the information and events in the passage be understood?"***
1. Not Understandable
2. Slightly Understandable
3. Somewhat Understandable
4. Neutral or Uncertain
5. Somewhat Understandable
6. Very Understandable
7. Clearly Understandable

***Question 9: "To what extent did the passage seem to you to have the characteristics of 'a piece of literature'?"***
1. Not Literary
2. Slightly Literary
3. Somewhat Literary
4. Neutral or Uncertain
5. Somewhat Literary
6. Very Literary
7. Extremely Literary

***Question 10: "To what extent do you consider that the passage fits your idea of a 'typical story'?"***
1. Not a Story
2. Slightly a Story
3. Somewhat a Story
4. Neutral or Uncertain
5. Somewhat a Story
6. Very Typical Story
7. Extremely Typical Story

***Question 11: "To what extent did you think that this passage had a point, moral, or message (aside from the point of entertaining the reader)?"***
1. No Point
2. Slight Point
3. Somewhat a Point
4. Neutral or Uncertain
5. Somewhat a Point
6. Very Obvious Point
7. Extremely Obvious Point

If you thought there may have been a point, briefly tell us what it may have been.

***Question 12: "To what extent did you find the passage violent?"***
1. Not Violent
2. Slightly Violent
3. Somewhat Violent
4. Neutral or Uncertain
5. Somewhat Violent
6. Very Violent
7. Extremely Violent

***Question 13: "To what extent did you find the passage erotic?"***
1. Not Erotic
2. Slightly Erotic
3. Somewhat Erotic
4. Neutral or Uncertain
5. Somewhat Erotic
6. Very Erotic
7. Extremely Erotic

***Question 14: "To what extent did you find the passage romantic?"***
1. Not Romantic
2. Slightly Romantic
3. Somewhat Romantic
4. Neutral or Uncertain
5. Somewhat Romantic
6. Very Romantic
7. Extremely Romantic

***Question 15: "To what extent did you think that the author was trying to express an insight about human nature, or a truth about the 'human condition'?"***
1. No Insight
2. Slight Insight
3. Some Insight
4. Neutral or Uncertain
5. Somewhat Insightful
6. Very Insightful
7. Extremely Insightful

***Question 16: "Have you ever either read this passage, or read or seen a story based on it, before?"***
1. No
2. Yes
"""
common_passage_chunks_american_story_1 = """
1   Old Henry Reifsneider and his wife Phoebe had lived together for forty-eight years. They had lived three miles from a small town whose population was steadily falling. This part of the country was not as wealthy as it used to be. It wasn't thickly settled, either. Perhaps there was a house every mile or so, with fields in between. Their own house had been built by Henry's grandfather many years ago. A new part had been added to the original log cabin when Henry married Phoebe. The new part was now weather-beaten. Wind whistled through cracks in the boards. Large, lovely trees surrounded the house. But they made it seem a little damp inside. The furniture like the house, was old. There was a tall cupboard of cherry-wood and a large, old-fashioned bed. The chest of drawers was also high and wide and solidly built. But it had faded, and smelled damp. The carpet that lay under the strong, lasting furniture had been made by Phoebe herself, fifteen years before she died. Now it was worn and faded to a dull grey and pink. The frame that she had made the carpet on was still here. It stood like a dusty, bony skeleton in the East room. All short of broken-down furniture lay around the place. There was a doorless clothes-cupboard. A broken mirror hung in an old cherry-wood frame. It had fallen from a nail and cracked three days before their youngest son, Jerry, died. There was a hat-stand whose china knobs had broken off. And an old-fashioned sewing machine.

2   The orchard to the east of the house was full of rotting apple trees. Their twisted branches were covered with greenish-white moss which looked sad and ghostly in the moonlight. Besides the orchard, several low buildings surrounded the house. They had once housed chickens, a horse or two, a cow, and several pigs. The same grey-green moss covered their roofs. They had not been painted for so long that they had turned a greyish-black. In fact, everything on the farm had aged and faded along with Old Henry and his wife Phoebe. They had lived here, these two, since their marriage forty-eight years before. And Henry had lived here as a child. His father and mother had been old when Henry married. They had invited him to bring his wife to the farm. They had all lived together for ten years before his mother and father died. After that Henry and Phoebe were left alone with their four children. But all sorts of things had happened since then. They had had seven children, but three had died. One girl had gone to Kansas. One boy had gone to Sioux Falls and was never even heard from again. Another boy had gone to Washington. The last girl lived five counties away in the same state. She had so many problems of her own, however, that she rarely gave her parents a thought. Their very ordinary home life had never been attractive to the children. So time had drawn them away. Wherever they were, they gave little thought to their father and mother.

3   Old Henry Reifsneider and his wife Phoebe were a loving couple. You perhaps know how it is with such simple people. They fasten themselves like moss on stones, until they and their circumstances are worn away. The larger world has no call to them; or if it does, they don't hear it. The orchard, the fields, the pigpen and the chicken house measure the range of their human activities. When the wheat is ripe, it is harvested. When the corn is full, it is cut. After that comes winter. The grain is taken to market, the wood is cut for the fires. The work is simple: fire-building, meal-getting, occasional repairing, visiting. There are also changes in the weather—the snow, the rains, and the fair days. Beyond these things, nothing else means very much. All the rest of life is a far-off dream. It shines, far away, like starlight. It sounds as faint as cowbells in the distance. Old Henry and his wife Phoebe were as fond of each other as it is possible for two old people who have nothing else in this life to be fond of. He was a thin old man, seventy when she died. He was a strange, moody person with thick, uncombed grey-black hair and beard. He looked at you out of dull, fish-like, watery eyes. His clothes, like the clothes of many farmers, were old and ill-fitting. They were too large at the neck. The knees and elbows were stretched and worn. Phoebe was thin and shapeless. She looked like an umbrella, dressed in black. As time had passed they had only themselves to look after. Their activities had become fewer and fewer. The herd of pigs was reduced to one.

4   The sleepy horse Henry still kept was neither very clean nor well-fed. Almost all the chickens had disappeared. They had been killed by animals or disease. The once healthy vegetable garden was now only a memory of itself. The flower beds were overgrown. A will had been made which divided the small property equally among the remaining four children. It was so small that it was really of no interest to any of them. Yet Henry and Phoebe lived together in peace and sympathy. Once in a while Old Henry would become moody and annoyed. He would complain that something unimportant had been lost. "Phoebe, where's my corn knife? You never leave my things alone." "Now you be quiet, Henry," his wife would answer in her old cracked voice. "If you don't, I'll leave you I’ll get up and walk out of here one day. Then where would you be? You don't have anybody but me to look after you, so just behave yourself. Your corn knife is in the cupboard where it's always been, unless you put it somewhere else." Old Henry knew his wife would never leave him. But, sometimes he wondered what he would do if she died. That was the one leaving he was afraid of. Every night he wound the old clock and went to lock the doors, and it comforted him to know Phoebe was in bed. If he moved in his sleep she would be there to ask him what he wanted. "Now, Henry, do lie still! You're as restless as a chicken." "Well, I can't sleep, Phoebe." "Well, you don't have to roll over so much. You can let me sleep." This would usually put him to sleep.

5   If she wanted a pail of water, he complained, but it gave him pleasure to bring it. If she rose first to build the fire, he made sure the wood was cut and placed within easy reach. So they divided this simple world nicely between them. In the spring of her sixty-fourth year, Phoebe become sick. Old Henry drove to town and brought back the doctor, But because of her age, her sickness was not curable, and one cold night she died. Henry could have gone to live with his youngest daughter. But it was really too much trouble. He was too weary and used to his home. He wanted to remain near where they had put his Phoebe. His neighbors invited him to stay with them. But he didn't want to. So his friends left him with advice and offers of help. They sent supplies of coffee and bacon and bread. He tried to interest himself in farming to keep himself busy. But it was sad to come into the house in the evening. He could find no shadow of Phoebe, although everything in the house suggested her. At night he read the newspapers that friends had left for him. Or he read in his Bible, which he had forgotten about for years. But he could get little comfort from these things. Mostly he sat and wondered where Phoebe had gone, and how soon he would die. He made coffee every morning and fried himself some bacon at night. But he wasn't hungry. His house was empty; its shadows saddened him. So he lived quite unhappily for five long months. And then a change began.
"""
common_passage__american_story_1 = """Old Henry Reifsneider and his wife Phoebe had lived together for forty-eight years. They had lived three miles from a small town whose population was steadily falling. This part of the country was not as wealthy as it used to be. It wasn't thickly settled, either. Perhaps there was a house every mile or so, with fields in between. Their own house had been built by Henry's grandfather many years ago. A new part had been added to the original log cabin when Henry married Phoebe. The new part was now weather-beaten. Wind whistled through cracks in the boards. Large, lovely trees surrounded the house. But they made it seem a little damp inside. The furniture like the house, was old. There was a tall cupboard of cherry-wood and a large, old-fashioned bed. The chest of drawers was also high and wide and solidly built. But it had faded, and smelled damp. The carpet that lay under the strong, lasting furniture had been made by Phoebe herself, fifteen years before she died. Now it was worn and faded to a dull grey and pink. The frame that she had made the carpet on was still here. It stood like a dusty, bony skeleton in the East room. All short of broken-down furniture lay around the place. There was a doorless clothes-cupboard. A broken mirror hung in an old cherry-wood frame. It had fallen from a nail and cracked three days before their youngest son, Jerry, died. There was a hat-stand whose china knobs had broken off. And an old-fashioned sewing machine. The orchard to the east of the house was full of rotting apple trees. Their twisted branches were covered with greenish-white moss which looked sad and ghostly in the moonlight. Besides the orchard, several low buildings surrounded the house. They had once housed chickens, a horse or two, a cow, and several pigs. The same grey-green moss covered their roofs. They had not been painted for so long that they had turned a greyish-black. In fact, everything on the farm had aged and faded along with Old Henry and his wife Phoebe. They had lived here, these two, since their marriage forty-eight years before. And Henry had lived here as a child. His father and mother had been old when Henry married. They had invited him to bring his wife to the farm. They had all lived together for ten years before his mother and father died. After that Henry and Phoebe were left alone with their four children. But all sorts of things had happened since then. They had had seven children, but three had died. One girl had gone to Kansas. One boy had gone to Sioux Falls and was never even heard from again. Another boy had gone to Washington. The last girl lived five counties away in the same state. She had so many problems of her own, however, that she rarely gave her parents a thought. Their very ordinary home life had never been attractive to the children. So time had drawn them away. Wherever they were, they gave little thought to their father and mother. Old Henry Reifsneider and his wife Phoebe were a loving couple. You perhaps know how it is with such simple people. They fasten themselves like moss on stones, until they and their circumstances are worn away. The larger world has no call to them; or if it does, they don't hear it. The orchard, the fields, the pigpen and the chicken house measure the range of their human activities. When the wheat is ripe, it is harvested. When the corn is full, it is cut. After that comes winter. The grain is taken to market, the wood is cut for the fires. The work is simple: fire-building, meal-getting, occasional repairing, visiting. There are also changes in the weather—the snow, the rains, and the fair days. Beyond these things, nothing else means very much. All the rest of life is a far-off dream. It shines, far away, like starlight. It sounds as faint as cowbells in the distance. Old Henry and his wife Phoebe were as fond of each other as it is possible for two old people who have nothing else in this life to be fond of. He was a thin old man, seventy when she died. He was a strange, moody person with thick, uncombed grey-black hair and beard. He looked at you out of dull, fish-like, watery eyes. His clothes, like the clothes of many farmers, were old and ill-fitting. They were too large at the neck. The knees and elbows were stretched and worn. Phoebe was thin and shapeless. She looked like an umbrella, dressed in black. As time had passed they had only themselves to look after. Their activities had become fewer and fewer. The herd of pigs was reduced to one. The sleepy horse Henry still kept was neither very clean nor well-fed. Almost all the chickens had disappeared. They had been killed by animals or disease. The once healthy vegetable garden was now only a memory of itself. The flower beds were overgrown. A will had been made which divided the small property equally among the remaining four children. It was so small that it was really of no interest to any of them. Yet Henry and Phoebe lived together in peace and sympathy. Once in a while Old Henry would become moody and annoyed. He would complain that something unimportant had been lost. 'Phoebe, where's my corn knife? You never leave my things alone.' 'Now you be quiet, Henry,' his wife would answer in her old cracked voice. 'If you don't, I'll leave you. I’ll get up and walk out of here one day. Then where would you be? You don't have anybody but me to look after you, so just behave yourself. Your corn knife is in the cupboard where it's always been, unless you put it somewhere else.' Old Henry knew his wife would never leave him. But, sometimes he wondered what he would do if she died. That was the one leaving he was afraid of. Every night he wound the old clock and went to lock the doors, and it comforted him to know Phoebe was in bed. If he moved in his sleep she would be there to ask him what he wanted. 'Now, Henry, do lie still! You're as restless as a chicken.' 'Well, I can't sleep, Phoebe.' 'Well, you don't have to roll over so much. You can let me sleep.' This would usually put him to sleep. If she wanted a pail of water, he complained, but it gave him pleasure to bring it. If she rose first to build the fire, he made sure the wood was cut and placed within easy reach. So they divided this simple world nicely between them. In the spring of her sixty-fourth year, Phoebe become sick. Old Henry drove to town and brought back the doctor, But because of her age, her sickness was not curable, and one cold night she died. Henry could have gone to live with his youngest daughter. But it was really too much trouble. He was too weary and used to his home. He wanted to remain near where they had put his Phoebe. His neighbors invited him to stay with them. But he didn't want to. So his friends left him with advice and offers of help. They sent supplies of coffee and bacon and bread. He tried to interest himself in farming to keep himself busy. But it was sad to come into the house in the evening. He could find no shadow of Phoebe, although everything in the house suggested her. At night he read the newspapers that friends had left for him. Or he read in his Bible, which he had forgotten about for years. But he could get little comfort from these things. Mostly he sat and wondered where Phoebe had gone, and how soon he would die. He made coffee every morning and fried himself some bacon at night. But he wasn't hungry. His house was empty; its shadows saddened him. So he lived quite unhappily for five long months. And then a change began."""

def generate_experiment_texts(settings_config: dict[str, str]):
    """
    Generate prompts and experiment texts
    Args:
        settings_config: settings to use in this experiment
    Return:
        Experiment prompts and version prompts
    """
    experiment_A_prompt_chunks = common_prompt_template_in_between
    experiment_A_prompt_full = common_prompt_template_final

    experiment_A_chunks = common_passage_chunks_american_story_1
    experiment_A_full = common_passage__american_story_1

    prompts = {
        "Experiment A Chunks": experiment_A_prompt_chunks,
        "Experiment A Full": experiment_A_prompt_full,
    }

    version_prompts = {
        "Experiment A Chunks": [
            ("American Story 1 Chunks", experiment_A_chunks),
        ],
        "Experiment A Full": [
            ("American Story 1 Full", experiment_A_full),
        ],
    }

    return prompts, version_prompts
