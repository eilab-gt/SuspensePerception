from together import Together


def setup_together_api(api_key):
    Together.api_key = api_key


def generate_response(messages, model_config):
    try:
        output = Together.chat(
            model=model_config["name"],
            messages=messages,
            max_tokens=model_config["max_tokens"],
            temperature=model_config["temperature"],
            top_k=model_config["top_k"],
            top_p=model_config["top_p"],
            repetition_penalty=model_config["repetition_penalty"],
            # stop=["Human:", "Assistant:"],
        )
        return output["output"]["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error generating response: {e}")
        return None


def format_system_message(message):
    return {"role": "system", "content": message}


def format_user_message(message):
    return {"role": "user", "content": message}
