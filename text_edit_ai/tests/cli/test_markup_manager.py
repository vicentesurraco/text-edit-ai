"""Tests for the MarkupManager class."""

import pytest
from unittest.mock import patch
from text_edit_ai.cli.markup_manager import MarkupManager
from text_edit_ai.cli.colors import Colors


@pytest.fixture
def markup_manager():
    """Fixture for a MarkupManager."""
    # Set up some test values for Colors
    Colors.red = "[RED]"
    Colors.green = "[GREEN]"
    Colors.strike = "[STRIKE]"
    Colors.reset = "[RESET]"

    return MarkupManager()


def test_tokenize(markup_manager):
    """Test tokenizing text."""
    text = "Hello, world! This is a test."

    tokens = markup_manager._tokenize(text)

    expected_tokens = [
        "Hello",
        ",",
        " ",
        "world",
        "!",
        " ",
        "This",
        " ",
        "is",
        " ",
        "a",
        " ",
        "test",
        ".",
    ]
    assert tokens == expected_tokens


def test_calculate_diff_equal(markup_manager):
    """Test calculating diff with equal tokens."""
    original_tokens = ["Hello", " ", "world"]
    edited_tokens = ["Hello", " ", "world"]

    result = markup_manager._calculate_diff(original_tokens, edited_tokens)

    # Equal tokens should be returned as-is
    assert result == original_tokens


def test_calculate_diff_delete(markup_manager):
    """Test calculating diff with deleted tokens."""
    original_tokens = ["Hello", " ", "world", "!"]
    edited_tokens = ["Hello", " ", "world"]

    result = markup_manager._calculate_diff(original_tokens, edited_tokens)

    # The last token should be marked as deleted
    expected_result = ["Hello", " ", "world", f"[RED][STRIKE]![RESET]"]
    assert result == expected_result


def test_calculate_diff_insert(markup_manager):
    """Test calculating diff with inserted tokens."""
    original_tokens = ["Hello", " ", "world"]
    edited_tokens = ["Hello", " ", "world", "!"]

    result = markup_manager._calculate_diff(original_tokens, edited_tokens)

    # The last token should be marked as inserted
    expected_result = ["Hello", " ", "world", f"[GREEN]![RESET]"]
    assert result == expected_result


def test_calculate_diff_replace(markup_manager):
    """Test calculating diff with replaced tokens."""
    original_tokens = ["Hello", " ", "world"]
    edited_tokens = ["Hello", " ", "there"]

    result = markup_manager._calculate_diff(original_tokens, edited_tokens)

    # The last token should be marked as deleted and the new one as inserted
    expected_result = [
        "Hello",
        " ",
        f"[RED][STRIKE]world[RESET]",
        f"[GREEN]there[RESET]",
    ]
    assert result == expected_result


def test_generate_diff(markup_manager):
    """Test generating a diff between original and edited text."""
    original_text = "Hello world!"
    edited_text = "Hello there!"

    # Mock the internal methods to control their behavior
    with patch.object(MarkupManager, "_tokenize") as mock_tokenize:
        with patch.object(MarkupManager, "_calculate_diff") as mock_calculate_diff:
            # Set up the mocks
            mock_tokenize.side_effect = [
                ["Hello", " ", "world", "!"],  # Original tokens
                ["Hello", " ", "there", "!"],  # Edited tokens
            ]
            mock_calculate_diff.return_value = [
                "Hello",
                " ",
                f"[RED][STRIKE]world[RESET]",
                f"[GREEN]there[RESET]",
                "!",
            ]

            # Call the method
            result = markup_manager.generate_diff(original_text, edited_text)

            # Check the result
            expected_result = "Hello [RED][STRIKE]world[RESET][GREEN]there[RESET]!"
            assert result == expected_result

            # Check that the internal methods were called correctly
            mock_tokenize.assert_any_call(original_text)
            mock_tokenize.assert_any_call(edited_text)
            mock_calculate_diff.assert_called_once_with(
                ["Hello", " ", "world", "!"], ["Hello", " ", "there", "!"]
            )


def test_generate_diff_integration(markup_manager):
    """Integration test for generating a diff."""
    # Test with a simple example
    original_text = "Hello world!"
    edited_text = "Hello there!"

    result = markup_manager.generate_diff(original_text, edited_text)

    # The word "world" should be marked as deleted and "there" as inserted
    assert "[RED][STRIKE]world[RESET]" in result
    assert "[GREEN]there[RESET]" in result

    # Test with a more complex example
    original_text = "This is a test sentence with some words."
    edited_text = "This is a modified sentence with different words."

    result = markup_manager.generate_diff(original_text, edited_text)

    # The word "test" should be marked as deleted and "modified" as inserted
    assert "[RED][STRIKE]test[RESET]" in result
    assert "[GREEN]modified[RESET]" in result

    # The word "some" should be marked as deleted and "different" as inserted
    assert "[RED][STRIKE]some[RESET]" in result
    assert "[GREEN]different[RESET]" in result
