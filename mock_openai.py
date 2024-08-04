import requests_mock


def mock_openai_api():
    adapter = requests_mock.Adapter()
    mock = requests_mock.Mocker(adapter=adapter)

    openai_api_url = "https://api.openai.com/v1"

    # Mock response for chat completion
    mock.post(
        f"{openai_api_url}/chat/completions",
        json={"choices": [{"message": {"content": "This is a mocked response."}}]},
    )

    return mock
