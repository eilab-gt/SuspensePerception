import os

import openai
from together import Together


# TODO: needs to return a client
def setup_openai_api(api_key):
    openai.api_key = api_key


def generate_response(messages, model_config):
    api_type = model_config.get("api_type", None)
    if api_type == "openai":
        response = openai.ChatCompletion.create(
            model=model_config["name"],
            messages=messages,
            max_tokens=model_config["max_tokens"],
            temperature=model_config["temperature"],
        )
        return response["choices"][0]["message"]["content"]
    elif api_type == "together":
        client = Together(api_key=model_config["api_key"])
        response = client.chat.completions.create(
            model=model_config["name"],
            messages=messages,
            max_tokens=model_config["max_tokens"],
            temperature=model_config["temperature"],
        )
        return response.choices[0].message.content
    else:
        raise ValueError(f"Unsupported API type: {api_type}")
