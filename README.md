# TODOs
- can we also save the FULL raw output, or at least make sure our JSON contains the actual metadata? Ideally we would be able to have an unstructured data lake of json returns with the meta data present there  needed to parse and extract
- need to add a config setting in yaml for deterministic/standard/creative rather than editing the decoding parameters manually
- `visualize.ipynb` needs to become code files
- need to get the PDFs of the research papers into the repo
- we need to add a "failed to answer" option for when the model could not handle the quesiton
- make the output dir depend on the config itself i.e. ./outputs/`experiment_series`/`text_version`/`decoding_strategy`/

# This is Thriller?

## Project Setup

### venv
How to create venv?
 - `pip install foo`

### precommit
What is precommit?
- https://pre-commit.com/

### API keys
API Keys?
- lorem ipsum
How to configure your API keys?
- Determine API keys using an `.env` file using the provided `.env.sample` template.

## Running Experiments

### Experiment Configuration
Configure your experiemnt config files, e.g. `config.yaml`

### Data Collection
> python ./src/thriller/Thriller.py -c config.yaml


### decoding strategies used

#### deterministic
  temperature: 0.0
  top_p: 0.9
  repetition_penalty: 1.0

#### average
  temperature: 0.5
  top_p: 0.9
  repetition_penalty: 1.0

#### creative
  temperature: 1.0
  top_p: 0.9
  repetition_penalty: 1.0

