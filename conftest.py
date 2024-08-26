from unittest.mock import MagicMock, patch

import pytest

mock_response = "This is a mocked response."


@pytest.fixture
def response():
    return mock_response


@pytest.fixture(scope="session")
def mock_openai():
    with patch("openai.ChatCompletion.create") as mock_create:
        mock_create.return_value = {"choices": [{"message": {"content": response()}}]}
        yield mock_create


@pytest.fixture(scope="session")
def mock_together():
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content=mock_response))]

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch("together.Together", return_value=mock_client):
        yield mock_client
    # mock_client.chat.completions.create.return_value = MagicMock(
    #     choices=[
    #         MagicMock(
    #             message=MagicMock(
    #                 content=mock_response
    #             )
    #         )
    #     ]
    # )
    # with patch('together.Together', return_value=mock_client) as mock_together:
    #     yield mock_together
