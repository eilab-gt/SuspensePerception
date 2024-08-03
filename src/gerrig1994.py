#!/usr/bin/env python3

import argparse

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


# Function to apply substitutions
def apply_substitutions(template, substitutions):
    for key, value in substitutions.items():
        template = template.replace(f"{{{key}}}", value)
    return template


# Store common templates
common_prompt_template = """The following is an excerpt from {author_firstname} {author_lastname}'s {book_title}. In this book, {hero_firstname} {hero_lastname} has been assigned to ‘ruin’ a criminal figure named {villain} by, as it happens, causing {villain} to lose a considerable amount of money gambling. Along the way, {hero_lastname} has acquired a lady interest named Vesper. Although {hero_lastname} has, in fact, brought about the gambling losses, {villain} has laid a successful trap for {hero_lastname}. {hero_lastname} and Vesper are now the prisoners of {villain} and his two gunmen.

\"\"\"
{STORY}
\"\"\"

Use the passage above to answer the following questions:

***Question 1: "How likely is it that {hero_lastname} will escape from {villain}?"***
1. Not very likely
2. Somewhat likely
3. Moderately likely
4. Likely
5. Quite likely
6. Very likely
7. Extremely likely

***Question 2: "How suspenseful do you find this passage to be?"***
1. Not very suspenseful
2. Somewhat suspenseful
3. Moderately suspenseful
4. Suspenseful
5. Quite suspenseful
6. Very suspenseful
7. Extremely suspenseful

Answer the questions. At end of your response you must re-state your answer choices in the format:
'''
Q1: [1-7]
Q2: [1-7]
'''
"""

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


# Function to generate prompts and experiment texts
def generate_experiment_texts(substitutions):
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
            "ending": "snatched away {hero_lastname}’s fountain pen. “Come my dear friend,” said {villain}. “Let’s not waste time.”",
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
            "grooming_action": "He noticed that he had a white thread on his lapel, and removed it. {hero_lastname} smiled at the elegant figure he presented.",
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
            "ending": "My dear Mr. {hero_lastname}. You came here as my guest and now I find you going through my personal belongings. I don’t think you have behaved very well. I will leave you here with Mr. Crushak to contemplate your rude behavior.",
        },
    )
    experiment_C_prior_solution_mentioned_and_removed = apply_substitutions(
        common_experiment_C_template,
        {
            **substitutions,
            "villain": substitutions["villain_C"],
            "ending": "My dear Mr. {hero_lastname}. The last time I held you in captivity, you were able to outwit my guard. He died soon after that in an automobile accident. Poor fellow. Crushak here will be responsible for you this time. He has orders to shoot you if you even attempt to speak to him.",
        },
    )
    experiment_C_prior_solution_mentioned_not_removed = apply_substitutions(
        common_experiment_C_template,
        {
            **substitutions,
            "villain": substitutions["villain_C"],
            "ending": "My dear Mr. {hero_lastname}. The last time I held you in captivity, you were able to outwit my guard. He died soon after that in an automobile accident. Poor fellow. Crushak here will be responsible for you this time.",
        },
    )

    prompts = {
        "Experiment A": experiment_A_prompt,
        "Experiment B": experiment_B_prompt,
        "Experiment C": experiment_C_prompt,
    }

    version_prompts = {
        "Experiment A": [
            experiment_A_pen_not_mentioned,
            experiment_A_pen_mentioned_removed,
            experiment_A_pen_mentioned_not_removed,
        ],
        "Experiment B": [experiment_B_unused_comb, experiment_B_used_comb],
        "Experiment C": [
            experiment_C_prior_solution_not_mentioned,
            experiment_C_prior_solution_mentioned_and_removed,
            experiment_C_prior_solution_mentioned_not_removed,
        ],
    }

    return prompts, version_prompts


# Define the function to save prompts to a file
def save_prompts_to_file(prompts, version_prompts, filename):
    with open(filename, "w") as f:
        for exp, prompt in prompts.items():
            f.write(f"# {exp} Prompt\n\n")
            f.write(prompt + "\n\n")

        for exp, versions in version_prompts.items():
            f.write(f"## {exp} Versions\n\n")
            for idx, version in enumerate(versions):
                f.write(f"### Version {idx + 1}\n\n")
                f.write(version + "\n\n")


# Set up argument parsing
def main():
    parser = argparse.ArgumentParser(
        description="Generate and save experiment prompts."
    )
    parser.add_argument(
        "output_file", type=str, help="The output file to save the prompts."
    )
    parser.add_argument(
        "--use-alternative",
        action="store_true",
        help="Use alternative names and titles.",
    )

    args = parser.parse_args()

    # Generate texts based on the selected flag
    if args.use_alternative:
        prompts, version_prompts = generate_experiment_texts(alternative_substitutions)
    else:
        prompts, version_prompts = generate_experiment_texts(default_substitutions)

    # Save the prompts to the specified file
    save_prompts_to_file(prompts, version_prompts, args.output_file)


if __name__ == "__main__":
    main()
