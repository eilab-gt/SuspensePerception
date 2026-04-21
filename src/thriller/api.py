"""
Helper functions for generating responses from LLMs using APIs
"""

import typing
from pathlib import Path
import openai
from together import Together
import tiktoken


def _optional_request_args(
    model_config: dict[str, typing.Any], keys: tuple[str, ...]
) -> dict[str, typing.Any]:
    return {
        key: model_config[key]
        for key in keys
        if key in model_config and model_config[key] is not None
    }


def _extract_choice_content(response) -> str:
    if isinstance(response, dict):
        return response["choices"][0]["message"]["content"]

    choices = getattr(response, "choices", None)
    if choices:
        choice = choices[0]
        message = getattr(choice, "message", None)
        if message is not None:
            content = getattr(message, "content", None)
            if isinstance(content, str):
                return content

        delta = getattr(choice, "delta", None)
        if delta is not None:
            content = getattr(delta, "content", None)
            if isinstance(content, str):
                return content

    content = ""
    try:
        iterator = iter(response)
    except TypeError:
        return content

    for chunk in iterator:
        chunk_choices = getattr(chunk, "choices", None)
        if not chunk_choices:
            continue
        delta = getattr(chunk_choices[0], "delta", None)
        content += getattr(delta, "content", "") or ""

    return content


def generate_response(
    messages: list[dict[str, str]], model_config: dict[str, typing.Any]
) -> str:
    """
    Probe a given LLM model for a response.
    Args:
        messages: A list of messages comprising the conversation so far.
                  Each message is a object with two required fields:
                    - role: the role of the messenger (either `system`, `user`, `assistant` or `tool`)
                    - content: the content of the message (e.g., "Write me a beautiful poem")
        model_config: Dictionary of model parameters.
                      Mandatory parameters are `api_type`, `name`, `max_tokens`, `temperature`
    Return:
        LLM model's response
    """
    api_type = model_config.get("api_type", None)

    if api_type == "openai":
        response = openai.ChatCompletion.create(
            model=model_config["name"],
            messages=messages,
            max_tokens=model_config["max_tokens"],
            temperature=model_config["temperature"],
            **_optional_request_args(model_config, ("top_p", "stop")),
        )

        return _extract_choice_content(response)

    elif api_type == "together":
        client = Together(api_key=model_config["api_key"])
        response = client.chat.completions.create(
            model=model_config["name"],
            messages=messages,
            max_tokens=model_config["max_tokens"],
            temperature=model_config["temperature"],
            **_optional_request_args(
                model_config,
                ("top_p", "top_k", "repetition_penalty", "stop", "stream"),
            ),
        )
        return _extract_choice_content(response)

    else:
        raise ValueError(f"Unsupported API type: {api_type}")


def save_raw_api_output(output: str, filename: str, output_path: Path) -> None:
    """
    Save text to a JSON file
    Args:
        output: data to save
        filename: name of the output JSON file
        output_path: path to the output directory
    """
    raw_output_dir = Path(output_path) / "raw_outputs"
    raw_output_dir.mkdir(parents=True, exist_ok=True)

    with open(raw_output_dir / filename, "w", encoding="utf-8") as f:
        f.write(output)


def tokenize(text: str, model: str) -> list[int]:
    # Initialize the tokenizer
    encoding = tiktoken.encoding_for_model(model)

    # Tokenize the text
    tokens = encoding.encode(text)

    return tokens


def tokenize_and_trim(text: str, max_tokens: int, model: str) -> str:
    """
    Tokenize and trim text to the maximum number of tokens allowed by the model.
    Args:
        text: The text to tokenize and trim.
        max_tokens: The maximum number of tokens allowed by the model.
        model: The model to use for tokenization.
    Returns:
        The trimmed text.
    """
    # Initialize the tokenizer
    encoding = tiktoken.encoding_for_model(model)

    # Tokenize the text
    tokens = encoding.encode(text)

    # If the number of tokens exceeds the limit, trim the text
    if len(tokens) > max_tokens:
        trimmed_tokens = tokens[:max_tokens]
        trimmed_text = encoding.decode(trimmed_tokens)
        return trimmed_text

    return text
