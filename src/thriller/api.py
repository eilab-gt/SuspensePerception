"""
API communication files
"""

import openai
from together import Together
import typing


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
            top_p=model_config.get("top_p", None),
            top_k=model_config.get("top_k", None),
            repetition_penalty=model_config["repetition_penalty"],
        )

        return response["choices"][0]["message"]["content"]

    elif api_type == "together":
        client = Together(api_key=model_config["api_key"])
        response = client.chat.completions.create(
            model=model_config["name"],
            messages=messages,
            max_tokens=model_config["max_tokens"],
            temperature=model_config["temperature"],
            top_p=model_config.get("top_p", None),
            top_k=model_config.get("top_k", None),
            repetition_penalty=model_config["repetition_penalty"],
            stop=model_config["stop"],
            stream=model_config["stream"],
        )

        content = ""
        for chunk in response:
            content += chunk.choices[0].delta.content or ""
        return content

    else:
        raise ValueError(f"Unsupported API type: {api_type}")
