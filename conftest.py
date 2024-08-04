import pytest
from unittest.mock import patch, MagicMock
import openai
from together import Together


@pytest.fixture(scope="session")
def mock_openai():
    with patch("openai.ChatCompletion.create") as mock_create:
        mock_create.return_value = {
            "choices": [{"message": {"content": "This is a mocked response."}}]
        }
        yield mock_create


@pytest.fixture(scope="session")
def mock_together():
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content="This is a mocked response."))
    ]

    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response

    with patch("together.Together", return_value=mock_client):
        yield mock_client
    # mock_client.chat.completions.create.return_value = MagicMock(
    #     choices=[
    #         MagicMock(
    #             message=MagicMock(
    #                 content="This is a mocked response."
    #             )
    #         )
    #     ]
    # )

    # with patch('together.Together', return_value=mock_client) as mock_together:
    #     yield mock_together
