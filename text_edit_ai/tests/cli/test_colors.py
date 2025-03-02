"""Tests for the Colors class."""

import pytest
from unittest.mock import patch, MagicMock
from text_edit_ai.cli.colors import Colors


@pytest.fixture
def reset_colors():
    """Fixture to reset color attributes before each test."""
    # Reset color attributes before each test
    for color_name in Colors.DEFAULT_COLORS:
        setattr(Colors, color_name, "")
    yield
    # Reset again after test
    for color_name in Colors.DEFAULT_COLORS:
        setattr(Colors, color_name, "")


def test_from_hex(reset_colors):
    """Test converting hex color to ANSI escape sequence."""
    # Test with hex value without #
    result = Colors.from_hex("FF0000")
    assert result == "\033[38;2;255;0;0m"

    # Test with hex value with #
    result = Colors.from_hex("#00FF00")
    assert result == "\033[38;2;0;255;0m"

    # Test with mixed case
    result = Colors.from_hex("00f0F0")
    assert result == "\033[38;2;0;240;240m"


def test_initialize(reset_colors):
    """Test initializing color values from config manager."""
    mock_config_manager = MagicMock()

    # Set up the mock to return specific color values
    def get_color_side_effect(color_name):
        return {
            "green": "00FF00",
            "red": "FF0000",
            "yellow": "FFFF00",
            "blue": "0000FF",
            "purple": "FF00FF",
            "orange": "FFA500",
        }.get(color_name)

    mock_config_manager.get_color.side_effect = get_color_side_effect

    # Initialize colors
    Colors.initialize(mock_config_manager)

    # Check that each color was set correctly
    for color_name in Colors.DEFAULT_COLORS:
        # Get the expected ANSI escape sequence for this color
        expected_value = Colors.from_hex(get_color_side_effect(color_name))
        actual_value = getattr(Colors, color_name)

        assert actual_value == expected_value

        # Check that get_color was called for each color
        mock_config_manager.get_color.assert_any_call(color_name)


def test_reset_value(reset_colors):
    """Test the reset value."""
    assert Colors.reset == "\033[0m"


def test_strike_value(reset_colors):
    """Test the strike value."""
    assert Colors.strike == "\033[9m"
