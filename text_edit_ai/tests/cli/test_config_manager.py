"""Tests for the ConfigManager class."""

import pytest
from unittest.mock import patch, MagicMock
from text_edit_ai.cli.config_manager import ConfigManager
from text_edit_ai.cli.colors import Colors


@pytest.fixture
def mock_config():
    """Fixture for a mock config."""
    mock = MagicMock()
    mock.__contains__.return_value = True
    mock.__getitem__.return_value = {}
    return mock


@pytest.fixture
def config_manager(mock_config):
    """Fixture for a ConfigManager with mocked dependencies."""
    with patch("configparser.ConfigParser", return_value=mock_config):
        with patch("os.path.expanduser", return_value="/mock/home"):
            with patch.object(ConfigManager, "_ensure_color_config"):
                with patch.object(ConfigManager, "save_config"):
                    yield ConfigManager()


def test_get_file_config(config_manager, mock_config):
    """Test getting configuration for a specific file."""
    test_file = "test_file.txt"
    mock_config.__contains__.return_value = False

    config_manager.get_file_config(test_file)

    # Verify a new section was created for the file
    mock_config.__setitem__.assert_called_with(test_file, {})


def test_set_api_key(config_manager, mock_config):
    """Test setting API key."""
    with patch("builtins.input", return_value="test_api_key"):
        with patch.object(ConfigManager, "save_config"):
            result = config_manager.set_api_key()

    assert result == "test_api_key"
    assert mock_config["DEFAULT"]["api_key"] == "test_api_key"


def test_set_model(config_manager, mock_config):
    """Test setting model name."""
    with patch("builtins.input", return_value="test_model"):
        with patch.object(ConfigManager, "save_config"):
            result = config_manager.set_model()

    assert result == "test_model"
    assert mock_config["DEFAULT"]["model"] == "test_model"


def test_set_pos(config_manager, mock_config):
    """Test setting position for a file."""
    test_file = "test_file.txt"
    test_pos = 42
    file_config = {}

    mock_config.__getitem__.return_value = file_config

    with patch.object(ConfigManager, "get_file_config", return_value=file_config):
        with patch.object(ConfigManager, "save_config"):
            config_manager.set_pos(test_file, test_pos)

    assert file_config["position"] == "42"


def test_get_pos(config_manager):
    """Test getting position for a file."""
    test_file = "test_file.txt"
    file_config = {"position": "42"}

    with patch.object(ConfigManager, "get_file_config", return_value=file_config):
        result = config_manager.get_pos(test_file)

    assert result == 42


def test_get_pos_default(config_manager):
    """Test getting default position when not set."""
    test_file = "test_file.txt"
    file_config = {}

    with patch.object(ConfigManager, "get_file_config", return_value=file_config):
        result = config_manager.get_pos(test_file)

    assert result == 0


def test_set_file_prompt(config_manager):
    """Test setting file prompt for a file."""
    test_file = "test_file.txt"
    test_prompt = "Test file prompt"
    file_config = {}

    with patch.object(ConfigManager, "get_file_config", return_value=file_config):
        with patch.object(ConfigManager, "save_config"):
            config_manager.set_file_prompt(test_file, test_prompt)

    assert file_config["file_prompt"] == test_prompt


def test_get_color_default(config_manager, mock_config):
    """Test getting default color when not in config."""
    color_name = "green"
    default_value = Colors.DEFAULT_COLORS[color_name]

    mock_config["COLORS"] = {}

    result = config_manager.get_color(color_name)

    assert result == default_value


def test_set_color(config_manager, mock_config):
    """Test setting color in config."""
    color_name = "custom_color"
    color_value = "AABBCC"

    mock_config["COLORS"] = {}

    with patch.object(ConfigManager, "save_config"):
        config_manager.set_color(color_name, color_value)

    assert mock_config["COLORS"][color_name] == color_value
