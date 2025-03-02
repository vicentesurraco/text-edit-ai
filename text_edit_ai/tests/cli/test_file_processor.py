"""Tests for the FileProcessor class."""

import pytest
from unittest.mock import patch, MagicMock, mock_open
from text_edit_ai.cli.file_processor import FileProcessor


@pytest.fixture
def mock_dependencies():
    """Fixture for mock dependencies."""
    mock_config_manager = MagicMock()
    mock_langchain_manager = MagicMock()
    mock_markup_manager = MagicMock()
    mock_ui_manager = MagicMock()
    mock_session_manager = MagicMock()

    return {
        "config_manager": mock_config_manager,
        "langchain_manager": mock_langchain_manager,
        "markup_manager": mock_markup_manager,
        "ui_manager": mock_ui_manager,
        "session_manager": mock_session_manager,
    }


@pytest.fixture
def file_processor(mock_dependencies):
    """Fixture for a FileProcessor with mocked dependencies."""
    # Patch the SessionManager constructor
    with patch(
        "text_edit_ai.cli.file_processor.SessionManager"
    ) as mock_session_manager_class:
        mock_session_manager_class.return_value = mock_dependencies["session_manager"]

        # Patch the MarkupManager constructor
        with patch(
            "text_edit_ai.cli.file_processor.MarkupManager"
        ) as mock_markup_manager_class:
            mock_markup_manager_class.return_value = mock_dependencies["markup_manager"]

            # Patch the UIManager constructor
            with patch(
                "text_edit_ai.cli.file_processor.UIManager"
            ) as mock_ui_manager_class:
                mock_ui_manager_class.return_value = mock_dependencies["ui_manager"]

                # Create the FileProcessor
                test_file = "test_file.txt"
                fp = FileProcessor(
                    mock_dependencies["config_manager"],
                    mock_dependencies["langchain_manager"],
                    test_file,
                    paragraphs_per_section=3,
                )

                return fp, test_file


def test_init(file_processor, mock_dependencies):
    """Test initialization."""
    fp, test_file = file_processor

    # Check that the attributes were set correctly
    assert fp.config_manager == mock_dependencies["config_manager"]
    assert fp.langchain_manager == mock_dependencies["langchain_manager"]
    assert fp.markup_manager == mock_dependencies["markup_manager"]
    assert fp.file == test_file
    assert fp.output_file == "test_file_edited.txt"
    assert fp.session_manager == mock_dependencies["session_manager"]
    assert fp.ui_manager == mock_dependencies["ui_manager"]


def test_load_file(file_processor):
    """Test loading file content."""
    fp, test_file = file_processor

    with patch(
        "builtins.open", new_callable=mock_open, read_data="Test content"
    ) as mock_file:
        result = fp._load_file()

        # Check that the file was opened correctly
        mock_file.assert_called_once_with(test_file, "r")

        # Check that the content was returned
        assert result == "Test content"


def test_split_into_sections(file_processor):
    """Test splitting content into sections."""
    fp, _ = file_processor
    content = "Paragraph 1\nParagraph 2\n\nParagraph 3"

    result = fp._split_into_sections(content)

    # Check that the content was split correctly
    expected_result = ["Paragraph 1", "Paragraph 2", "Paragraph 3"]
    assert result == expected_result


def test_write_section(file_processor):
    """Test writing a section to the output file."""
    fp, _ = file_processor
    content = "Test section"

    with patch("builtins.open", new_callable=mock_open) as mock_file:
        fp._write_section(content)

        # Check that the file was opened correctly
        mock_file.assert_called_once_with("test_file_edited.txt", "a")

        # Check that the content was written correctly
        mock_file().write.assert_called_once_with("Test section\n\n")


def test_process_with_ai_accept(file_processor, mock_dependencies):
    """Test processing a section with AI and accepting the edit."""
    fp, test_file = file_processor
    section = "Test section"
    file_prompt = "Test file prompt"
    edited_text = "Edited section"
    diff_text = "Diff text"

    # Set up the mocks
    mock_dependencies["config_manager"].get_file_prompt.return_value = file_prompt
    mock_dependencies["langchain_manager"].get_response.return_value = edited_text
    mock_dependencies["markup_manager"].generate_diff.return_value = diff_text
    mock_dependencies["ui_manager"].get_ai_action.return_value = "accept"

    # Call the method
    with patch.object(FileProcessor, "_write_section") as mock_write_section:
        fp._process_with_ai(section)

        # Check that the config manager was called to get the file prompt
        mock_dependencies["config_manager"].get_file_prompt.assert_called_once_with(
            test_file
        )

        # Check that the langchain manager was called to get the response
        mock_dependencies["langchain_manager"].get_response.assert_called_once_with(
            file_prompt, section
        )

        # Check that the markup manager was called to generate the diff
        mock_dependencies["markup_manager"].generate_diff.assert_called_once_with(
            section, edited_text
        )

        # Check that the UI manager was called to get the AI action
        mock_dependencies["ui_manager"].get_ai_action.assert_called_once_with(
            edited_text, diff_text
        )

        # Check that the edited text was written
        mock_write_section.assert_called_once_with(edited_text)

        # Check that the session was advanced
        mock_dependencies["session_manager"].advance.assert_called_once()


def test_process_with_ai_skip(file_processor, mock_dependencies):
    """Test processing a section with AI and skipping the edit."""
    fp, test_file = file_processor
    section = "Test section"
    file_prompt = "Test file prompt"
    edited_text = "Edited section"
    diff_text = "Diff text"

    # Set up the mocks
    mock_dependencies["config_manager"].get_file_prompt.return_value = file_prompt
    mock_dependencies["langchain_manager"].get_response.return_value = edited_text
    mock_dependencies["markup_manager"].generate_diff.return_value = diff_text
    mock_dependencies["ui_manager"].get_ai_action.return_value = "skip"

    # Call the method
    with patch.object(FileProcessor, "_write_section") as mock_write_section:
        fp._process_with_ai(section)

        # Check that the original section was written
        mock_write_section.assert_called_once_with(section)

        # Check that the session was advanced
        mock_dependencies["session_manager"].advance.assert_called_once()


def test_process_with_ai_section_prompt(file_processor, mock_dependencies):
    """Test processing a section with AI and providing a section prompt."""
    fp, test_file = file_processor
    section = "Test section"
    file_prompt = "Test file prompt"
    section_prompt = "Test section prompt"
    edited_text1 = "Edited section 1"
    edited_text2 = "Edited section 2"
    diff_text1 = "Diff text 1"
    diff_text2 = "Diff text 2"

    # Set up the mocks
    mock_dependencies["config_manager"].get_file_prompt.return_value = file_prompt
    mock_dependencies["langchain_manager"].get_response.side_effect = [
        edited_text1,
        edited_text2,
    ]
    mock_dependencies["markup_manager"].generate_diff.side_effect = [
        diff_text1,
        diff_text2,
    ]
    mock_dependencies["ui_manager"].get_ai_action.side_effect = [
        "section_prompt",
        "accept",
    ]
    mock_dependencies["ui_manager"].get_section_prompt.return_value = section_prompt

    # Call the method
    with patch.object(FileProcessor, "_write_section") as mock_write_section:
        fp._process_with_ai(section)

        # Check that the section prompt was requested
        mock_dependencies["ui_manager"].get_section_prompt.assert_called_once()

        # Check that the langchain manager was called with the combined prompt
        mock_dependencies["langchain_manager"].get_response.assert_any_call(
            f"{file_prompt}\n{section_prompt}", section
        )

        # Check that the edited text was written
        mock_write_section.assert_called_once_with(edited_text2)


def test_process_with_ai_file_prompt(file_processor, mock_dependencies):
    """Test processing a section with AI and providing a file prompt."""
    fp, test_file = file_processor
    section = "Test section"
    old_file_prompt = "Old file prompt"
    new_file_prompt = "New file prompt"
    edited_text1 = "Edited section 1"
    edited_text2 = "Edited section 2"
    diff_text1 = "Diff text 1"
    diff_text2 = "Diff text 2"

    # Set up the mocks
    mock_dependencies["config_manager"].get_file_prompt.return_value = old_file_prompt
    mock_dependencies["langchain_manager"].get_response.side_effect = [
        edited_text1,
        edited_text2,
    ]
    mock_dependencies["markup_manager"].generate_diff.side_effect = [
        diff_text1,
        diff_text2,
    ]
    mock_dependencies["ui_manager"].get_ai_action.side_effect = [
        "file_prompt",
        "accept",
    ]
    mock_dependencies["ui_manager"].get_file_prompt.return_value = new_file_prompt

    # Call the method
    with patch.object(FileProcessor, "_write_section") as mock_write_section:
        fp._process_with_ai(section)

        # Check that the file prompt was requested
        mock_dependencies["ui_manager"].get_file_prompt.assert_called_once()

        # Check that the config manager was called to set the file prompt
        mock_dependencies["config_manager"].set_file_prompt.assert_called_once_with(
            test_file, new_file_prompt
        )

        # Check that the langchain manager was called with the new prompt
        mock_dependencies["langchain_manager"].get_response.assert_any_call(
            new_file_prompt, section
        )

        # Check that the edited text was written
        mock_write_section.assert_called_once_with(edited_text2)


def test_process_with_ai_size(file_processor, mock_dependencies):
    """Test processing a section with AI and changing the section size."""
    fp, test_file = file_processor
    section = "Test section"
    file_prompt = "Test file prompt"
    new_size = 5

    # Set up the mocks
    mock_dependencies["config_manager"].get_file_prompt.return_value = file_prompt
    mock_dependencies["ui_manager"].get_ai_action.return_value = "size"
    mock_dependencies["ui_manager"].get_section_size.return_value = new_size

    # Call the method
    result = fp._process_with_ai(section)

    # Check that the section size was requested
    mock_dependencies["ui_manager"].get_section_size.assert_called_once()

    # Check that the session manager was called to set the section size
    mock_dependencies[
        "session_manager"
    ].set_paragraphs_per_section.assert_called_once_with(new_size)

    # Check that the method returned None (no exit)
    assert result is None


def test_process_with_ai_exit(file_processor, mock_dependencies):
    """Test processing a section with AI and exiting."""
    fp, test_file = file_processor
    section = "Test section"
    file_prompt = "Test file prompt"

    # Set up the mocks
    mock_dependencies["config_manager"].get_file_prompt.return_value = file_prompt
    mock_dependencies["ui_manager"].get_ai_action.return_value = "exit"

    # Call the method
    result = fp._process_with_ai(section)

    # Check that the method returned "exit"
    assert result == "exit"


def test_process(file_processor, mock_dependencies):
    """Test processing the file."""
    fp, _ = file_processor

    # Set up the mocks
    content = "Paragraph 1\nParagraph 2\nParagraph 3"
    sections = ["Paragraph 1", "Paragraph 2", "Paragraph 3"]

    with patch.object(FileProcessor, "_load_file", return_value=content):
        with patch.object(FileProcessor, "_split_into_sections", return_value=sections):
            # Set up the session manager to process two sections and then be complete
            mock_dependencies["session_manager"].is_complete.side_effect = [
                False,
                False,
                True,
            ]
            mock_dependencies[
                "session_manager"
            ].get_current_section.return_value = "Current section"

            # Set up the UI manager to continue for the first section and skip for the second
            mock_dependencies["ui_manager"].get_initial_action.side_effect = [
                "continue",
                "skip",
            ]

            # Call the method
            with patch.object(
                FileProcessor, "_process_with_ai"
            ) as mock_process_with_ai:
                with patch.object(
                    FileProcessor, "_write_section"
                ) as mock_write_section:
                    fp.process()

                    # Check that the sections were set in the session manager
                    mock_dependencies[
                        "session_manager"
                    ].set_sections.assert_called_once_with(sections)

                    # Check that is_complete was called three times
                    assert (
                        mock_dependencies["session_manager"].is_complete.call_count == 3
                    )

                    # Check that get_current_section was called twice
                    assert (
                        mock_dependencies[
                            "session_manager"
                        ].get_current_section.call_count
                        == 2
                    )

                    # Check that get_initial_action was called twice
                    assert (
                        mock_dependencies["ui_manager"].get_initial_action.call_count
                        == 2
                    )

                    # Check that process_with_ai was called once (for the first section)
                    mock_process_with_ai.assert_called_once_with("Current section")

                    # Check that write_section was called once (for the second section)
                    mock_write_section.assert_called_once_with("Current section")

                    # Check that advance was called once (for the second section)
                    mock_dependencies["session_manager"].advance.assert_called_once()

                    # Check that show_completion_message was called
                    mock_dependencies[
                        "ui_manager"
                    ].show_completion_message.assert_called_once()


def test_process_size(file_processor, mock_dependencies):
    """Test processing the file and changing the section size."""
    fp, _ = file_processor

    # Set up the mocks
    content = "Paragraph 1\nParagraph 2\nParagraph 3"
    sections = ["Paragraph 1", "Paragraph 2", "Paragraph 3"]
    new_size = 5

    with patch.object(FileProcessor, "_load_file", return_value=content):
        with patch.object(FileProcessor, "_split_into_sections", return_value=sections):
            # Set up the session manager to process one section and then be complete
            mock_dependencies["session_manager"].is_complete.side_effect = [False, True]
            mock_dependencies[
                "session_manager"
            ].get_current_section.return_value = "Current section"

            # Set up the UI manager to request a size change
            mock_dependencies["ui_manager"].get_initial_action.return_value = "size"
            mock_dependencies["ui_manager"].get_section_size.return_value = new_size

            # Call the method
            fp.process()

            # Check that get_section_size was called
            mock_dependencies["ui_manager"].get_section_size.assert_called_once()

            # Check that set_paragraphs_per_section was called with the new size
            mock_dependencies[
                "session_manager"
            ].set_paragraphs_per_section.assert_called_once_with(new_size)


def test_process_exit(file_processor, mock_dependencies):
    """Test processing the file and exiting."""
    fp, _ = file_processor

    # Set up the mocks
    content = "Paragraph 1\nParagraph 2\nParagraph 3"
    sections = ["Paragraph 1", "Paragraph 2", "Paragraph 3"]

    with patch.object(FileProcessor, "_load_file", return_value=content):
        with patch.object(FileProcessor, "_split_into_sections", return_value=sections):
            # Set up the session manager
            mock_dependencies["session_manager"].is_complete.return_value = False
            mock_dependencies[
                "session_manager"
            ].get_current_section.return_value = "Current section"

            # Set up the UI manager to request exit
            mock_dependencies["ui_manager"].get_initial_action.return_value = "exit"

            # Call the method
            fp.process()

            # Check that show_completion_message was not called
            mock_dependencies["ui_manager"].show_completion_message.assert_not_called()
