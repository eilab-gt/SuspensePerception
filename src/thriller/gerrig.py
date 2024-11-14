"""
Defines experiments from Gerrig, R.J. and Bernardo, A.B.I. 1994. Readers as problem-solvers in the experience of suspense. Poetics (Hague, Netherlands). 22, 6 (Dec. 1994), 459–472. DOI:https://doi.org/10.1016/0304-422x(94)90021-3.
"""

from src.thriller.misc import apply_substitutions

change_to_present_tense = False
change_to_future_tense = False

# Define substitution dictionaries
default_substitutions = {
    "author_firstname": "Ian",
    "author_lastname": "Fleming",
    "hero_firstname": "James",
    "hero_lastname": "Bond",
    "book_title_A": "first James Bond novel, 'Casino Royale'",
    "book_title_C": "tenth James Bond novel, 'On Her Majesty's Secret Service'",
    "villain_A": "Le Chiffre",
    "villain_C": "Blofeld",
}

alternative_substitutions = {
    "author_firstname": "Niles",
    "author_lastname": "Feeney",
    "hero_firstname": "Charles",
    "hero_lastname": "Mers",
    "book_title_A": "first Charles Mers novel, 'Meeting at Midnight'",
    "book_title_C": "tenth Charles Mers novel, 'Twenty Miles to the Sea'",
    "villain_A": "Chifrex",
    "villain_C": "Kalweitz",
}

# Store common templates
common_prompt_template = """The following is an excerpt from {author_firstname} {author_lastname}'s {book_title}. In this book, {hero_firstname} {hero_lastname} has been assigned to ‘ruin’ a criminal figure named {villain} by, as it happens, causing {villain} to lose a considerable amount of money gambling. Along the way, {hero_lastname} has acquired a lady interest named Vesper. Although {hero_lastname} has, in fact, brought about the gambling losses, {villain} has laid a successful trap for {hero_lastname}. {hero_lastname} and Vesper are now the prisoners of {villain} and his two gunmen.

Use the passage above to answer the following questions:

***Question 1: "How likely is it that {hero_lastname} will escape from {villain}?"***
1. Not very likely
2. Somewhat likely
3. Slightly likely
4. Neutral or Uncertain
5. Moderately likely
6. Very likely
7. Extremely likely

***Question 2: "How suspenseful do you find this passage to be?"***
1. Not very suspenseful
2. Somewhat suspenseful
3. Slightly suspenseful
4. Neutral or Uncertain
5. Moderately suspenseful
6. Very suspenseful
7. Extremely suspenseful

Answer Question 1, and then answer Question 2.
"""
if change_to_present_tense:
    common_experiment_A_template = """{villain} is standing in the doorway of a room on the right. He crooks a finger at {hero_lastname} in a silent, spidery summons.
    Vesper is being led down a passage towards the back of the house. {hero_lastname} suddenly decides. With a backward kick which connects with the thin man's shins and brings a whistle of pain from him, {hero_lastname} hurls himself down the passage after her. His plan is to do as much damage as possible to the two gunmen and be able to exchange a few hurried words with the girl.
    Like lightning the Corsican slams himself back against the wall of the passage and, as {hero_lastname}'s foot whistles past his hip, he very quickly, but somehow delicately, shoots out his left hand, catches {hero_lastname}'s shoe at the top of its arc, and twists it sharply. As he crashes to the ground, {hero_lastname} rolls agilely and, with a motion {action}, he rights himself with minimal damage.
    "Search him." barks {villain}.
    The two gunmen drag {hero_lastname} to his feet. While the thin man keeps his gun trained on {hero_lastname}'s unquiet chest, the Corsican roughly strips {hero_lastname}'s revolver out of its shoulder holster. He twists {hero_lastname} around brusquely in search of other weaponry. {villain} observes his assistant's work attentively. Then, as if reading {hero_lastname}'s thoughts, he crosses the room and {ending}"""

    common_experiment_B_template = """Filled with confidence after defeating {villain}, {hero_lastname} has extended an invitation to Vesper to dine with him in the hotel restaurant. She has cheerfully accepted.
    {hero_lastname} looks in the mirror of his hotel room to make certain that his black tie is centered in his collar. {grooming_action}
    As {hero_lastname} turns to leave the room, the door bursts in toward him. Three large men leap through, guns drawn. The largest of the men is {villain}, {hero_lastname}'s recently vanquished opponent.
    As the three men approach him, {hero_lastname} suddenly whirls around and catches one of the gunmen squarely in the stomach with a well-placed shove of his heel. Unfortunately, the second gunman has accurately judged the rest of {hero_lastname}'s motion. He catches {hero_lastname}'s shoe at the top of its arc and twists it sharply. As he crashes to the ground, {hero_lastname} rolls agilely and, with a motion in which he takes great pride, he rights himself with minimal damage. {hero_lastname} is unharmed, but he is trapped.
    "Search him." barks {villain}.
    The two gunmen carefully search {hero_lastname}. They roughly strip {hero_lastname}'s revolver out of its shoulder holster. They twist him around in search of other weaponry.
    {villain} observes his assistants' work attentively. He crosses the room to {hero_lastname}, and pats him down once again. {villain} pulls out {hero_lastname}'s pocket comb and runs his finger down its teeth. He smiles broadly, and flips the comb well out of {hero_lastname}'s reach. "Come, my dear friend," says {villain}. "Let's not waste time."
    {hero_lastname} feels puny and impotent."""

    common_experiment_C_template = """{villain} smiles and says, "We must stop meeting like this Mr. {hero_lastname}. I grow weary of pointing a gun at you."
    Before {hero_lastname} can reply, a large bird crashes into the wall of glass that makes up one side of {villain}'s large office. {hero_lastname} takes advantage of the distraction to pull up one corner of the rug on which {villain} stands. {villain} stumbles backwards and his gun shoots up into the air, knocking out the large light that has illuminated the room.
    As {hero_lastname}'s eyes grow accustomed to the dark of the office, he hurries toward the door. He is met there, however, by a very large and very ugly man. Light from the hall spills in, revealing another gun pointing at his chest.
    {villain} picks himself up off the ground and says, "I am not amused by your antics Mr. {hero_lastname}. I hope you understand that my good friend here, Mr. Crushak, is devoted to eliminating such irritations from my life." At this, the large man contorts his face into what he might have intended as a smile. It makes him look no less ugly. {villain} continues, "Tie up Mr. {hero_lastname}."
    Crushak forces {hero_lastname} into a wooden arm chair and carefully pins {hero_lastname} in place by wrapping a piece of piano wire around each of the chair's corners and {hero_lastname}'s arms. Each subsequent twist of the wire bites more painfully into {hero_lastname}'s flesh.
    Crushak grunts to indicate that he is done. {villain} says, "{ending}"""

elif change_to_future_tense:
    common_experiment_A_template = """{villain} will be standing in the doorway of a room on the right. He will crook a finger at {hero_lastname} in a silent, spidery summons.
    Vesper will be being led down a passage towards the back of the house. {hero_lastname} will suddenly decide. With a backward kick which will connect with the thin man's shins and bring a whistle of pain from him, {hero_lastname} will hurl himself down the passage after her. His plan will be to do as much damage as possible to the two gunmen and be able to exchange a few hurried words with the girl.
    Like lightning the Corsican will slam himself back against the wall of the passage and, as {hero_lastname}'s foot will whistle past his hip, he will very quickly, but somehow delicately, shoot out his left hand, catch {hero_lastname}'s shoe at the top of its arc, and twist it sharply. As he will crash to the ground, {hero_lastname} will roll agilely and, with a motion {action}, he will right himself with minimal damage.
    "Search him." will bark {villain}.
    The two gunmen will drag {hero_lastname} to his feet. While the thin man will keep his gun trained on {hero_lastname}'s unquiet chest, the Corsican will roughly strip {hero_lastname}'s revolver out of its shoulder holster. He will twist {hero_lastname} around brusquely in search of other weaponry. {villain} will observe his assistant's work attentively. Then, as if reading {hero_lastname}'s thoughts, he will cross the room and {ending}"""

    common_experiment_B_template = """Filled with confidence after defeating {villain}, {hero_lastname} will have extended an invitation to Vesper to dine with him in the hotel restaurant. She will have cheerfully accepted.
    {hero_lastname} will look in the mirror of his hotel room to make certain that his black tie will be centered in his collar. {grooming_action}
    As {hero_lastname} will turn to leave the room, the door will burst in toward him. Three large men will leap through, guns drawn. The largest of the men will be {villain}, {hero_lastname}'s recently vanquished opponent.
    As the three men will approach him, {hero_lastname} will suddenly whirl around and catch one of the gunmen squarely in the stomach with a well-placed shove of his heel. Unfortunately, the second gunman will have accurately judged the rest of {hero_lastname}'s motion. He will catch {hero_lastname}'s shoe at the top of its arc and twist it sharply. As he will crash to the ground, {hero_lastname} will roll agilely and, with a motion in which he will take great pride, he will right himself with minimal damage. {hero_lastname} will be unharmed, but he will be trapped.
    "Search him." will bark {villain}.
    The two gunmen will carefully search {hero_lastname}. They will roughly strip {hero_lastname}'s revolver out of its shoulder holster. They will twist him around in search of other weaponry.
    {villain} will observe his assistants' work attentively. He will cross the room to {hero_lastname}, and pat him down once again. {villain} will pull out {hero_lastname}'s pocket comb and run his finger down its teeth. He will smile broadly, and flip the comb well out of {hero_lastname}'s reach. "Come, my dear friend," will say {villain}. "Let's not waste time."
    {hero_lastname} will feel puny and impotent."""

    common_experiment_C_template = """{villain} will smile and say, "We must stop meeting like this Mr. {hero_lastname}. I grow weary of pointing a gun at you."
    Before {hero_lastname} will be able to reply, a large bird will crash into the wall of glass that will make up one side of {villain}'s large office. {hero_lastname} will take advantage of the distraction to pull up one corner of the rug on which {villain} will stand. {villain} will stumble backwards and his gun will shoot up into the air, knocking out the large light that will have illuminated the room.
    As {hero_lastname}'s eyes will grow accustomed to the dark of the office, he will hurry toward the door. He will be met there, however, by a very large and very ugly man. Light from the hall will spill in, revealing another gun pointing at his chest.
    {villain} will pick himself up off the ground and say, "I am not amused by your antics Mr. {hero_lastname}. I hope you understand that my good friend here, Mr. Crushak, is devoted to eliminating such irritations from my life." At this, the large man will contort his face into what he might have intended as a smile. It will make him look no less ugly. {villain} will continue, "Tie up Mr. {hero_lastname}."
    Crushak will force {hero_lastname} into a wooden arm chair and carefully pin {hero_lastname} in place by wrapping a piece of piano wire around each of the chair's corners and {hero_lastname}'s arms. Each subsequent twist of the wire will bite more painfully into {hero_lastname}'s flesh.
    Crushak will grunt to indicate that he will be done. {villain} will say, "{ending}"""

else:
    # ORIGINAL TEXT IN PAST TENSE
    common_experiment_A_template = """{villain} was standing in the doorway of a room on the right. He crooked a finger at {hero_lastname} in a silent, spidery summons.
    Vesper was being led down a passage towards the back of the house. {hero_lastname} suddenly decided. With a backward kick which connected with the thin man’s shins and brought a whistle of pain from him, {hero_lastname} hurled himself down the passage after her. His plan was to do as much damage as possible to the two gunmen and be able to exchange a few hurried words with the girl.
    Like lightning the Corsican slammed himself back against the wall of the passage and, as {hero_lastname}’s foot whistled past his hip, he very quickly, but somehow delicately, shot out his left hand, caught {hero_lastname}’s shoe at the top of its arc, and twisted it sharply. As he crashed to the ground, {hero_lastname} rolled agilely and, with a motion {action}, he righted himself with minimal damage.
    “Search him.” barked {villain}.
    The two gunmen dragged {hero_lastname} to his feet. While the thin man kept his gun trained on {hero_lastname}’s unquiet chest, the Corsican roughly stripped {hero_lastname}’s revolver out of its shoulder holster. He twisted {hero_lastname} around brusquely in search of other weaponry. {villain} observed his assistant’s work attentively. Then, as if reading {hero_lastname}’s thoughts, he crossed the room and {ending}"""

    common_experiment_B_template = """Filled with confidence after defeating {villain}, {hero_lastname} had extended an invitation to Vesper to dine with him in the hotel restaurant. She had cheerfully accepted.
    {hero_lastname} looked in the mirror of his hotel room to make certain that his black tie was centered in his collar. {grooming_action}
    As {hero_lastname} turned to leave the room, the door burst in toward him. Three large men leapt through, guns drawn. The largest of the men was {villain}, {hero_lastname}’s recently vanquished opponent.
    As the three men approached him, {hero_lastname} suddenly whirled around and caught one of the gunmen squarely in the stomach with a well-placed shove of his heel. Unfortunately, the second gunman had accurately judged the rest of {hero_lastname}’s motion. He caught {hero_lastname}’s shoe at the top of its arc and twisted it sharply. As he crashed to the ground, {hero_lastname} rolled agilely and, with a motion in which he took great pride, he righted himself with minimal damage. {hero_lastname} was unharmed, but he was trapped.
    “Search him.” barked {villain}.
    The two gunmen carefully searched {hero_lastname}. They roughly stripped {hero_lastname}’s revolver out of its shoulder holster. They twisted him around in search of other weaponry.
    {villain} observed his assistants' work attentively. He crossed the room to {hero_lastname}, and patted him down once again. {villain} pulled out {hero_lastname}’s pocket comb and ran his finger down its teeth. He smiled broadly, and flipped the comb well out of {hero_lastname}’s reach. “Come, my dear friend,” said {villain}. “Let’s not waste time.”
    {hero_lastname} felt puny and impotent."""

    common_experiment_C_template = """{villain} smiled and said, “We must stop meeting like this Mr. {hero_lastname}. I grow weary of pointing a gun at you.”
    Before {hero_lastname} could reply, a large bird crashed into the wall of glass that made up one side of {villain}’s large office. {hero_lastname} took advantage of the distraction to pull up one corner of the rug on which {villain} stood. {villain} stumbled backwards and his gun shot up into the air, knocking out the large light that had illuminated the room.
    As {hero_lastname}’s eyes grew accustomed to the dark of the office, he hurried toward the door. He was met there, however, by a very large and very ugly man. Light from the hall spilled in, revealing another gun pointing at his chest.
    {villain} picked himself up off the ground and said, “I am not amused by your antics Mr. {hero_lastname}. I hope you understand that my good friend here, Mr. Crushak, is devoted to eliminating such irritations from my life.” At this, the large man contorted his face into what he might have intended as a smile. It made him look no less ugly. {villain} continued, “Tie up Mr. {hero_lastname}.”
    Crushak forced {hero_lastname} into a wooden arm chair and carefully pinned {hero_lastname} in place by wrapping a piece of piano wire around each of the chair’s corners and {hero_lastname}’s arms. Each subsequent twist of the wire bit more painfully into {hero_lastname}’s flesh.
    Crushak grunted to indicate that he was done. {villain} said, “{ending}”"""

def generate_experiment_texts(experiment_config: dict[str, str]):
    """
    Generate prompts and experiment texts
    Args:
        experiment_config: settings to use in this experiment
    Return:
        Experiment prompts and version prompts
    """
    substitutions = (
        alternative_substitutions
        if experiment_config["use_alternative"]
        else default_substitutions
    )

    # Get experiment prompts

    experiment_A_prompt = apply_substitutions(
        common_prompt_template,
        {
            **substitutions,
            "book_title": substitutions["book_title_A"],
            "villain": substitutions["villain_A"],
        },
    )

    experiment_B_prompt = apply_substitutions(
        common_prompt_template,
        {
            **substitutions,
            "book_title": substitutions["book_title_A"],
            "villain": substitutions["villain_A"],
        },
    )

    experiment_C_prompt = apply_substitutions(
        common_prompt_template,
        {
            **substitutions,
            "book_title": substitutions["book_title_C"],
            "villain": substitutions["villain_C"],
        },
    )

    prompts = {
        "Experiment A": experiment_A_prompt,
        "Experiment B": experiment_B_prompt,
        "Experiment C": experiment_C_prompt,
    }

    # Get experiment texts

    experiment_A_pen_not_mentioned = apply_substitutions(
        common_experiment_A_template,
        {
            **substitutions,
            "villain": substitutions["villain_A"],
            "action": "in which he took great pride",
            "ending": "said, “Come my dear friend. Let’s not waste time.”",
        },
    )

    experiment_A_pen_mentioned_removed = apply_substitutions(
        common_experiment_A_template,
        {
            **substitutions,
            "villain": substitutions["villain_A"],
            "action": "that he hoped went unnoticed, moved his fountain pen deeper into his breast pocket",
            "ending": f"snatched away {substitutions['hero_lastname']}’s fountain pen. “Come my dear friend,” said {substitutions['villain_A']}. “Let’s not waste time.”",
        },
    )

    experiment_A_pen_mentioned_not_removed = apply_substitutions(
        common_experiment_A_template,
        {
            **substitutions,
            "villain": substitutions["villain_A"],
            "action": "that he hoped went unnoticed, moved his fountain pen deeper into his breast pocket",
            "ending": "said, “Come my dear friend. Let’s not waste time.”",
        },
    )

    experiment_B_unused_comb = apply_substitutions(
        common_experiment_B_template,
        {
            **substitutions,
            "villain": substitutions["villain_A"],
            "grooming_action": f"He noticed that he had a white thread on his lapel, and removed it. {substitutions['hero_lastname']} smiled at the elegant figure he presented.",
        },
    )

    experiment_B_used_comb = apply_substitutions(
        common_experiment_B_template,
        {
            **substitutions,
            "villain": substitutions["villain_A"],
            "grooming_action": "He noticed that his hair was just the least bit mussed, so he extracted his comb from his pocket and smoothed his wandering locks back into place.",
        },
    )

    experiment_C_prior_solution_not_mentioned = apply_substitutions(
        common_experiment_C_template,
        {
            **substitutions,
            "villain": substitutions["villain_C"],
            "ending": f"My dear Mr. {substitutions['hero_lastname']}. You came here as my guest and now I find you going through my personal belongings. I don’t think you have behaved very well. I will leave you here with Mr. Crushak to contemplate your rude behavior.",
        },
    )

    experiment_C_prior_solution_mentioned_and_removed = apply_substitutions(
        common_experiment_C_template,
        {
            **substitutions,
            "villain": substitutions["villain_C"],
            "ending": f"My dear Mr. {substitutions['hero_lastname']}. The last time I held you in captivity, you were able to outwit my guard. He died soon after that in an automobile accident. Poor fellow. Crushak here will be responsible for you this time. He has orders to shoot you if you even attempt to speak to him.",
        },
    )

    experiment_C_prior_solution_mentioned_not_removed = apply_substitutions(
        common_experiment_C_template,
        {
            **substitutions,
            "villain": substitutions["villain_C"],
            "ending": f"My dear Mr. {substitutions['hero_lastname']}. The last time I held you in captivity, you were able to outwit my guard. He died soon after that in an automobile accident. Poor fellow. Crushak here will be responsible for you this time.",
        },
    )

    texts = {
        "Experiment A": [
            ("Pen Not Mentioned", [experiment_A_pen_not_mentioned]),
            ("Pen Mentioned Removed", [experiment_A_pen_mentioned_removed]),
            ("Pen Mentioned Not Removed", [experiment_A_pen_mentioned_not_removed]),
        ],
        "Experiment B": [
            ("Unused Comb", [experiment_B_unused_comb]),
            ("Used Comb", [experiment_B_used_comb]),
        ],
        "Experiment C": [
            ("Prior Solution Not Mentioned", [experiment_C_prior_solution_not_mentioned]),
            (
                "Prior Solution Mentioned and Removed",
                [experiment_C_prior_solution_mentioned_and_removed],
            ),
            (
                "Prior Solution Mentioned Not Removed",
                [experiment_C_prior_solution_mentioned_not_removed],
            ),
        ],
    }

    return prompts, texts
