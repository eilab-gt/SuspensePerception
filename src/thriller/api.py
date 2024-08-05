import os

import openai
from together import Together


def generate_response(messages, model_config):
    api_type = model_config.get("api_type", None)
    if api_type == "openai":
        response = openai.ChatCompletion.create(
            model=model_config["name"],
            messages=messages,
            max_tokens=model_config["max_tokens"],
            temperature=model_config["temperature"],
            top_p=0.7,  # TODO: add top_p to model_config, change it here
            top_k=50,  # TODO: add top_k to model_config, change it here
            repetition_penalty=1,  # TODO: add repetition_penalty to model_config, change it here
        )
        return response["choices"][0]["message"]["content"]
    elif api_type == "together":
        client = Together(api_key=model_config["api_key"])
        response = client.chat.completions.create(
            model=model_config["name"],
            messages=messages,
            max_tokens=model_config["max_tokens"],
            temperature=model_config["temperature"],
            top_p=0.7,  # TODO: add top_p to model_config, change it here
            top_k=50,  # TODO: add top_k to model_config, change it here
            repetition_penalty=1,  # TODO: add repetition_penalty to model_config, change it here
            stop=["<|eot_id|>"],  # TODO: add stop to model_config, change it here
            stream=True,  # TODO: add stream to model_config, change it here
        )
        return response.choices[0].message.content
    else:
        raise ValueError(f"Unsupported API type: {api_type}")
