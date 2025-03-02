"""Tests for the UIManager class."""

import pytest
from unittest.mock import patch
from text_edit_ai.cli.ui_manager import UIManager
from text_edit_ai.cli.colors import Colors


@pytest.fixture
def ui_manager():
    """Fixture for a UIManager."""
    # Set up some test values for Colors
    Colors.purple = "[PURPLE]"
    Colors.green = "[GREEN]"
    Colors.yellow = "[YELLOW]"
    Colors.blue = "[BLUE]"
    Colors.red = "[RED]"
    Colors.orange = "[ORANGE]"
    Colors.reset = "[RESET]"

    return UIManager()


def test_get_initial_action_skip(ui_manager):
    """Test getting initial action with 'skip' response."""
    with patch("builtins.input", return_value="s"):
        result = ui_manager.get_initial_action("Test section")

        assert result == "skip"


def test_get_initial_action_size(ui_manager):
    """Test getting initial action with 'size' response."""
    with patch("builtins.input", return_value="z"):
        result = ui_manager.get_initial_action("Test section")

        assert result == "size"


def test_get_initial_action_exit(ui_manager):
    """Test getting initial action with 'exit' response."""
    with patch("builtins.input", return_value="x"):
        result = ui_manager.get_initial_action("Test section")

        assert result == "exit"


def test_get_initial_action_invalid(ui_manager):
    """Test getting initial action with invalid response."""
    with patch("builtins.input", side_effect=["invalid", "c"]):
        with patch("builtins.print") as mock_print:
            result = ui_manager.get_initial_action("Test section")

            assert result == "continue"
            mock_print.assert_any_call("Invalid action. Please try again.")


def test_get_ai_action_skip(ui_manager):
    """Test getting AI action with 'skip' response."""
    with patch("builtins.input", return_value="s"):
        result = ui_manager.get_ai_action("Edited text", "Diff text")

        assert result == "skip"


def test_get_ai_action_section_prompt(ui_manager):
    """Test getting AI action with 'section_prompt' response."""
    with patch("builtins.input", return_value="c"):
        result = ui_manager.get_ai_action("Edited text", "Diff text")

        assert result == "section_prompt"


def test_get_ai_action_size(ui_manager):
    """Test getting AI action with 'size' response."""
    with patch("builtins.input", return_value="z"):
        result = ui_manager.get_ai_action("Edited text", "Diff text")

        assert result == "size"


def test_get_ai_action_exit(ui_manager):
    """Test getting AI action with 'exit' response."""
    with patch("builtins.input", return_value="x"):
        result = ui_manager.get_ai_action("Edited text", "Diff text")

        assert result == "exit"


def test_get_ai_action_invalid(ui_manager):
    """Test getting AI action with invalid response."""
    with patch("builtins.input", side_effect=["invalid", "a"]):
        with patch("builtins.print") as mock_print:
            result = ui_manager.get_ai_action("Edited text", "Diff text")

            assert result == "accept"
            mock_print.assert_any_call("Invalid action. Please try again.")


def test_get_section_prompt(ui_manager):
    """Test getting section prompt."""
    with patch("builtins.input", return_value="Test section prompt"):
        result = ui_manager.get_section_prompt()

        assert result == "Test section prompt"


def test_get_section_prompt_empty(ui_manager):
    """Test getting empty section prompt."""
    with patch("builtins.input", return_value=""):
        with patch("builtins.print") as mock_print:
            result = ui_manager.get_section_prompt()

            assert result == ""
            mock_print.assert_called_once_with("Section prompt change canceled.")


def test_get_file_prompt(ui_manager):
    """Test getting file prompt."""
    with patch("builtins.input", return_value="Test file prompt"):
        result = ui_manager.get_file_prompt()

        assert result == "Test file prompt"


def test_get_file_prompt_empty(ui_manager):
    """Test getting empty file prompt."""
    with patch("builtins.input", return_value=""):
        with patch("builtins.print") as mock_print:
            result = ui_manager.get_file_prompt()

            assert result == ""
            mock_print.assert_called_once_with("File prompt change canceled.")


def test_get_section_size(ui_manager):
    """Test getting section size."""
    with patch("builtins.input", return_value="5"):
        result = ui_manager.get_section_size()

        assert result == 5


def test_get_section_size_invalid(ui_manager):
    """Test getting invalid section size."""
    with patch("builtins.input", side_effect=["invalid", "5"]):
        with patch("builtins.print") as mock_print:
            result = ui_manager.get_section_size()

            assert result == 5
            mock_print.assert_called_once_with("Please enter an integer.")


def test_show_completion_message(ui_manager):
    """Test showing completion message."""
    with patch("builtins.print") as mock_print:
        ui_manager.show_completion_message()

        mock_print.assert_called_once_with("All sections have been processed.")
