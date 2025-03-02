"""Tests for the LangchainManager class."""

import pytest
from unittest.mock import patch, MagicMock
from text_edit_ai.cli.langchain_manager import LangchainManager, SYSTEM_PROMPT


@pytest.fixture
def mock_config_manager():
    """Fixture for a mock config manager."""
    mock = MagicMock()
    mock.get_api_key.return_value = "test_api_key"
    mock.get_model.return_value = "test_model"
    return mock


@pytest.fixture
def mock_model():
    """Fixture for a mock model."""
    return MagicMock()


@pytest.fixture
def langchain_manager(mock_config_manager, mock_model):
    """Fixture for a LangchainManager with mocked dependencies."""
    with patch.object(LangchainManager, "get_model", return_value=mock_model):
        yield LangchainManager(mock_config_manager)


def test_init(langchain_manager, mock_config_manager, mock_model):
    """Test initialization."""
    assert langchain_manager.system_prompt == SYSTEM_PROMPT
    assert langchain_manager.config_manager == mock_config_manager
    assert langchain_manager.api_key == "test_api_key"
    assert langchain_manager.model_name == "test_model"
    assert langchain_manager.model == mock_model


@patch("text_edit_ai.cli.langchain_manager.ChatGoogleGenerativeAI")
@patch("text_edit_ai.cli.langchain_manager.init_chat_model")
def test_get_model_google(mock_init_chat_model, mock_google_ai, mock_config_manager):
    """Test getting a Google model."""
    # Create a new instance without patching get_model
    mock_config_manager.get_model.return_value = "gemini-pro"

    langchain_manager = LangchainManager(mock_config_manager)

    # Check that ChatGoogleGenerativeAI was called with the right parameters
    mock_google_ai.assert_called_once_with(
        model="gemini-pro", google_api_key="test_api_key", temperature=0
    )

    # Check that init_chat_model was not called
    mock_init_chat_model.assert_not_called()


@patch("text_edit_ai.cli.langchain_manager.ChatGoogleGenerativeAI")
@patch("text_edit_ai.cli.langchain_manager.init_chat_model")
def test_get_model_other(mock_init_chat_model, mock_google_ai, mock_config_manager):
    """Test getting a non-Google model."""
    # Create a new instance without patching get_model
    mock_config_manager.get_model.return_value = "gpt-4"

    langchain_manager = LangchainManager(mock_config_manager)

    # Check that init_chat_model was called with the right parameters
    mock_init_chat_model.assert_called_once_with(
        "gpt-4", api_key="test_api_key", temperature=0
    )

    # Check that ChatGoogleGenerativeAI was not called
    mock_google_ai.assert_not_called()


@patch("text_edit_ai.cli.langchain_manager.ChatPromptTemplate")
def test_get_response(mock_prompt_template, langchain_manager, mock_model):
    """Test getting a response from the model."""
    # Set up the mock prompt template
    mock_messages = MagicMock()
    mock_prompt = MagicMock()
    mock_prompt.format_messages.return_value = mock_messages
    mock_prompt_template.from_messages.return_value = mock_prompt

    # Set up the mock model to stream tokens
    token1 = MagicMock()
    token1.content = "Hello"
    token2 = MagicMock()
    token2.content = " world"
    mock_model.stream.return_value = [token1, token2]

    # Call the method
    result = langchain_manager.get_response("Test context", "Test writing")

    # Check the result
    assert result == "Hello world"

    # Check that the prompt template was created correctly
    mock_prompt_template.from_messages.assert_called_once_with(
        [
            ("system", SYSTEM_PROMPT),
            (
                "user",
                "<context>Test context</context><writing>Test writing</writing>",
            ),
        ]
    )

    # Check that the model was called with the messages
    mock_model.stream.assert_called_once_with(mock_messages)
