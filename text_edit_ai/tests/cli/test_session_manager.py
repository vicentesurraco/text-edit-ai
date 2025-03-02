"""Tests for the SessionManager class."""

import pytest
from unittest.mock import patch, MagicMock
from text_edit_ai.cli.session_manager import SessionManager


@pytest.fixture
def mock_config_manager():
    """Fixture for a mock config manager."""
    mock = MagicMock()
    mock_file_config = {}
    mock.get_file_config.return_value = mock_file_config
    return mock, mock_file_config


@pytest.fixture
def session_manager(mock_config_manager):
    """Fixture for a SessionManager with mocked dependencies."""
    mock_cm, mock_file_config = mock_config_manager
    test_file = "test_file.txt"
    return SessionManager(mock_cm, test_file, paragraphs_per_section=2), test_file


def test_init(mock_config_manager, session_manager):
    """Test initialization."""
    mock_cm, mock_file_config = mock_config_manager
    sm, test_file = session_manager

    # Check that the config manager was used to get the file config
    mock_cm.get_file_config.assert_called_once_with(test_file)

    # Check that the attributes were set correctly
    assert sm.config_manager == mock_cm
    assert sm.file == test_file
    assert sm.file_config == mock_file_config
    assert sm.paragraphs_per_section == 2
    assert sm.current_section == 0
    assert sm.sections == []


def test_init_with_current_section(mock_config_manager):
    """Test initialization with existing current_section."""
    mock_cm, mock_file_config = mock_config_manager

    # Set up the mock file config to have a current_section
    mock_file_config["current_section"] = "5"

    # Create a new session manager
    test_file = "test_file.txt"
    session_manager = SessionManager(mock_cm, test_file, paragraphs_per_section=2)

    # Check that the current_section was loaded from the config
    assert session_manager.current_section == 5


def test_set_sections(session_manager):
    """Test setting sections."""
    sm, _ = session_manager
    test_sections = ["Section 1", "Section 2", "Section 3"]

    sm.set_sections(test_sections)

    assert sm.sections == test_sections


def test_get_current_section_single(session_manager):
    """Test getting current section with one paragraph."""
    sm, _ = session_manager

    # Set up the session manager with sections and paragraphs_per_section=1
    test_sections = ["Section 1", "Section 2", "Section 3"]
    sm.set_sections(test_sections)
    sm.paragraphs_per_section = 1
    sm.current_section = 1

    # Get the current section
    result = sm.get_current_section()

    # Check that we got the correct section
    assert result == "Section 2"


def test_get_current_section_multiple(session_manager):
    """Test getting current section with multiple paragraphs."""
    sm, _ = session_manager

    # Set up the session manager with sections and paragraphs_per_section=2
    test_sections = ["Section 1", "Section 2", "Section 3", "Section 4"]
    sm.set_sections(test_sections)
    sm.paragraphs_per_section = 2
    sm.current_section = 1

    # Get the current section
    result = sm.get_current_section()

    # Check that we got the correct sections joined with newlines
    assert result == "Section 2\n\nSection 3"


def test_get_current_section_at_end(session_manager):
    """Test getting current section at the end of the file."""
    sm, _ = session_manager

    # Set up the session manager with sections and current_section at the end
    test_sections = ["Section 1", "Section 2", "Section 3"]
    sm.set_sections(test_sections)
    sm.paragraphs_per_section = 2
    sm.current_section = 2

    # Get the current section
    result = sm.get_current_section()

    # Check that we got only the last section
    assert result == "Section 3"


def test_advance(session_manager, mock_config_manager):
    """Test advancing to the next section."""
    sm, _ = session_manager
    _, mock_file_config = mock_config_manager

    # Set up the session manager
    sm.current_section = 1
    sm.paragraphs_per_section = 2

    # Advance to the next section
    sm.advance()

    # Check that the current_section was updated
    assert sm.current_section == 3

    # Check that the file_config was updated
    assert mock_file_config["current_section"] == "3"

    # Check that the config was saved
    sm.config_manager.save_config.assert_called_once()


def test_is_complete_true(session_manager):
    """Test is_complete when all sections have been processed."""
    sm, _ = session_manager

    # Set up the session manager with sections and current_section past the end
    test_sections = ["Section 1", "Section 2", "Section 3"]
    sm.set_sections(test_sections)
    sm.current_section = 3

    # Check if complete
    result = sm.is_complete()

    # Should be complete
    assert result is True


def test_is_complete_false(session_manager):
    """Test is_complete when there are still sections to process."""
    sm, _ = session_manager

    # Set up the session manager with sections and current_section in the middle
    test_sections = ["Section 1", "Section 2", "Section 3"]
    sm.set_sections(test_sections)
    sm.current_section = 1

    # Check if complete
    result = sm.is_complete()

    # Should not be complete
    assert result is False


def test_set_paragraphs_per_section(session_manager):
    """Test setting the number of paragraphs per section."""
    sm, _ = session_manager

    # Set paragraphs_per_section
    sm.set_paragraphs_per_section(5)

    # Check that it was updated
    assert sm.paragraphs_per_section == 5
