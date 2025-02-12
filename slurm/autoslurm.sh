#!/bin/bash

augmentations=(
    "distraction_insertion"
    "swap_words"
    "shuffle_sentences"
    "introduce_typos"
    "word_swap_embedding"
    "change_character_names"
    "context_removal"
    "word_swap_homoglyph"
    "sentence_paraphrase"
    "synonym_replacement"
    "antonym_replacement"
    "caesar_cypher"
    "" # no augmentation
)

experiments=(
    # gerrig.yaml
    # delatorre.yaml
    # brewer.yaml
    lehne.yaml
)

i=0
for experiment in "${experiments[@]}"; do
    for augmentation in "${augmentations[@]}"; do

        experiment_name="${experiment%.yaml}"

        OUTPUT_DIR="outputs/${experiment_name}_experiment/adversarial/${augmentation}/e3/"

        export EXPERIMENT="${experiment}"
        export OVERRIDES="augmentation.augmentation_order=[\"$augmentation\"] experiment.output_dir=\"${OUTPUT_DIR}\""
        echo "Running experiment $EXPERIMENT with augmentation $OVERRIDES"
        i=$((i + 1))

        sbatch slurm/entrypoint.sh
    done
done