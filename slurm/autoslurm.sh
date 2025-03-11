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
    # "sentence_paraphrase"
    "synonym_replacement"
    "antonym_replacement"
    "caesar_cypher"
    "" # no augmentation
)

experiments=(
    gerrig.yaml
    delatorre.yaml
    # brewer.yaml
    # lehne.yaml
)

for ((j=0; j<1; j++)); do
    for experiment in "${experiments[@]}"; do
        for augmentation in "${augmentations[@]}"; do

            experiment_name="${experiment%.yaml}"

            OUTPUT_DIR="outputs/${experiment_name}_experiment/adversarial/${augmentation}/e${j}/"

            JOBNAME="${experiment_name}_${augmentation}"

            export EXPERIMENT="${experiment}"
            export OVERRIDES="augmentation.augmentation_order=[\"$augmentation\"] experiment.output_dir=\"${OUTPUT_DIR}\""
            echo "Running experiment $EXPERIMENT with augmentation $OVERRIDES"

            sbatch -J$JOBNAME --dependency=singleton slurm/entrypoint.sh

        done
    done
done