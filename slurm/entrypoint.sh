#!/bin/bash
#SBATCH --job-name="thriller"
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=6
#SBATCH --qos="short"

echo "Starting job $SLURM_JOB_ID"

cd ~/flash/thriller
source ~/miniconda3/bin/activate
conda activate thriller

srun python src/thriller/Thriller.py -c $EXPERIMENT -o $OVERRIDES