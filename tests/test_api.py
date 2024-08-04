import os
from unittest.mock import patch

import openai
import pytest
import requests_mock
import together

from src.thriller.api import generate_response


def test_generate_response_openai(mock_openai):
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    model_config = {
        "api_type": "openai",
        "api_key": "test_api_key",
        "name": "gpt-3.5-turbo",
        "max_tokens": 50,
        "temperature": 0.7,
    }

    response = generate_response(messages, model_config)
    assert response == "This is a mocked response."


def test_generate_response_together(mock_together):
    messages = [{"role": "user", "content": "Hello, how are you?"}]
    model_config = {
        "api_type": "together",
        "api_key": "test_api_key",
        "name": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "max_tokens": 50,
        "temperature": 0.7,
    }

    with patch("together.Together", return_value=mock_together):
        try:
            result = generate_response(messages, model_config)
            # Assert the result
            assert result == "This is a mocked response."
        except together.error.AuthenticationError:
            pytest.skip("Skipping due to AuthenticationError")

    # Verify that the mock was called
    mock_together.chat.completions.create.assert_called_once_with(
        model=model_config["name"],
        messages=messages,
        max_tokens=model_config["max_tokens"],
        temperature=model_config["temperature"],
    )
