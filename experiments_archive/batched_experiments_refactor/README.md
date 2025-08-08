# Batched Experiments Refactor Archive

**Status**: Archived | **Last Active**: February 2025 | **Author**: Rodrigo Loza

## Overview

This branch contains a major architectural refactoring that modernizes the experiment execution framework using Hydra configuration management and adds support for distributed computing via MPI.

## Key Architectural Changes

### 1. Configuration Management Migration
**FROM**: Individual YAML files at root level
```
bentz.yaml
brewer.yaml
delatorre.yaml
gerrig.yaml
lehne.yaml
```

**TO**: Modular Hydra-based configuration structure
```
src/config/
├── aug/             # Augmentation configurations
├── exp/             # Experiment configurations
├── model/           # Model configurations
├── parse_model/     # Parser model configs
└── text/            # Text-specific experiment configs
```

### 2. Main Entry Point Refactor
- **Old**: `src/thriller/Thriller.py` - Monolithic script
- **New**: `src/thriller/main.py` - Hydra-decorated modular entry point

### 3. Key Features Added

#### Hydra Integration
```python
@hydra.main(config_path="../config", config_name="default", version_base=None)
def main(args):
    # Modern config composition with overrides
```

#### MPI Support for Distributed Computing
```python
if is_mpi:
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    # Parallel experiment execution
```

#### Centralized Constants
New `constants.py` file with:
- `SUPPORTED_API_TYPES`
- `AVAILABLE_ATTACKS`

### 4. Improved Experiment Orchestration
- Batch processing of experiment combinations
- Dynamic override management
- Better separation of concerns
- Cleaner error handling

## Archive Contents

```
batched_experiments_refactor/
├── README.md                    # This file
├── config/                      # New Hydra config structure
│   ├── aug/default.yaml        # Augmentation configs
│   ├── exp/default.yaml        # Experiment configs
│   ├── model/                  # Model configurations
│   │   ├── default.yaml
│   │   └── together.yaml
│   ├── parse_model/default.yaml
│   └── text/                   # Text experiment configs
│       ├── bentz.yaml
│       ├── brewer.yaml
│       ├── delatorre.yaml
│       ├── gerrig.yaml
│       └── lehne.yaml
├── src/
│   ├── main.py                 # New Hydra-based entry point
│   └── constants.py            # Centralized constants
├── patches/
│   └── code_changes.patch      # Full diff of changes
└── docs/
    ├── commit_history.txt       # Commit history
    └── change_summary.txt       # Statistical summary
```

## Technical Impact

### Pros
- **Modern Config Management**: Hydra provides powerful config composition
- **Distributed Computing**: MPI support enables parallel experiment execution
- **Better Organization**: Clear separation of configs by type
- **Scalability**: Better suited for large-scale experiments
- **Maintainability**: Cleaner code structure

### Cons
- **Breaking Changes**: Incompatible with current workflow
- **Incomplete**: Only one commit, likely untested
- **Dependencies**: Requires Hydra and potentially MPI4PY
- **Learning Curve**: Team needs to understand Hydra patterns

## Git History

Original branch: `origin/refactor/batched-experiments`
Merged with: `--strategy=ours` to preserve history without affecting main codebase
Commit: 6eccf42f46211f70c2590b264ddf0f42ccc760eb

## Migration Guide (If Ever Adopted)

1. **Install Dependencies**:
   ```bash
   pip install hydra-core omegaconf mpi4py
   ```

2. **Migrate Configs**:
   - Move experiment configs to `src/config/text/`
   - Move model configs to `src/config/model/`
   - Update paths in code

3. **Update Entry Point**:
   - Replace `Thriller.py` usage with `main.py`
   - Use Hydra overrides instead of direct YAML loading

4. **Run with Hydra**:
   ```bash
   python src/thriller/main.py text=brewer model=together
   ```

5. **Run with MPI** (for parallel execution):
   ```bash
   mpirun -n 4 python src/thriller/main.py
   ```

## Decision to Archive

This refactor was archived rather than merged because:
- **Too Disruptive**: Would break all existing workflows and scripts
- **Incomplete**: Only one commit suggests it wasn't fully tested
- **Risk/Reward**: Benefits don't outweigh the migration effort at this time
- **Alternative Path**: Could be reference for future incremental improvements

## Future Considerations

If the project scales significantly, this refactor provides a good blueprint for:
- Implementing configuration management with Hydra
- Adding distributed computing capabilities
- Improving code organization
- Standardizing experiment execution

The ideas here are solid and could be adopted incrementally rather than as a complete rewrite.