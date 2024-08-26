# This is Thriller?

## Project Setup

### Creating and Activating the Virtual Environment

To create the virtual environment in the project root and install the required packages, follow these steps:

1. **Create the virtual environment**:
    ```sh
    python -m venv .venv
    ```

2. **Activate the virtual environment**:
    - On Windows:
        ```sh
        .\.venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh
        source .venv/bin/activate
        ```

3. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```


<!-- ### precommit
Q: What is precommit?
A: precommit is a tool for managing and maintaining code quality.
- https://pre-commit.com/ -->

### API keys
To configure your API keys, follow these steps:

1. **Create a `.env` file**:
    - You can create a new `.env` file in the project root directory **OR** copy the provided `.env.sample` file and rename it to `.env`.

2. **Modify the `.env` file**:
    - Open the `.env` file in a text editor.
    - Add your API keys in the following format:
      ```
      API_KEY_NAME=your_api_key_value
      ```
    - Replace `API_KEY_NAME` with the actual name of the API key and `your_api_key_value` with your actual API key.

3. **Save the `.env` file**:
    - Ensure the file is saved in the project root directory.

Example:
```
TOGETHER_API_KEY=foo
OPENAI_API_KEY=bar
ANTHROPIC_API_KEY=baz
```

## How to Run Experiments

### Experiment Configuration

The configuration files (e.g., `gerrig.yaml`, `lehne.yaml`, etc.) contain the following fields:

1. **experiment**:
   - `experiment series`: The name or identifier for the series of experiments being conducted.
   - `output directory`: The directory path where the experiment results will be saved.
   - `use_alternative`: (gerrig-only) A boolean field indicating whether to use the alternative naming scheme used for Gerrig 1994 experiments.

2. **model**: Defines the API type, model names, and generation parameters:
   - `api_type`: API provider (e.g., "together")
   - `name`: List of model names to be tested
   - `max_tokens`: Maximum number of tokens to generate
   - `temperature`: Controls randomness (0.0 for deterministic, higher for more creative)
   - `top_p`: Nucleus sampling parameter
   - `repetition_penalty`: Discourages repetition in generated text
   - `stop`: Stopping criteria for text generation
   - `stream`: Enables streaming of generated text

3. **parse_model**: Configures the model used for parsing responses:
   - Similar fields to the `model` section
   - `prompt`: Specific instructions for parsing the generated responses

### Decoding Strategies

Decoding strategies determine how the model generates text. Each strategy has different settings for `temperature`, `top_p`, and `repetition_penalty`, which influence the randomness and diversity of the output token sequence.

#### Deterministic
- **Temperature**: 0.0
- **Top_p**: 0.9
- **Repetition_penalty**: 1.0

'Deterministic' decoding strategy is used for the most predictable and consistent results across samples. We use it for tasks where accuracy and reliability are crucial, such as data extraction or structured text generation. In our experiments we use 'Deterministic' decoding for the parser.

#### General
- **Temperature**: 0.5
- **Top_p**: 0.9
- **Repetition_penalty**: 1.0

'General' decoding strategy increases the temperature to  creativity and consistency. 'General' works for when variability is acceptable or desired, but the output should still be coherent and relevant.

#### Creative

- **Temperature**: 1.0
- **Top_p**: 0.9
- **Repetition_penalty**: 1.0

'Creative' decoding strategy allows for the greatest amount of diversity among tokens generated in the output sequence. 'Creative' may be more favorable for creative writing, brainstorming, or any task where novel and varied outputs are desired, such as sampling from a distribution.

### Running Experiments

To run an experiment, use the following command:
`python ./src/thriller/Thriller.py -c config.yaml`
where `config.yaml` is the path to the configuration file for the experiment (e.g., `gerrig.yaml`, `lehne.yaml`, etc.)