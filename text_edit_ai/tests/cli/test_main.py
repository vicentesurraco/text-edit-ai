"""Tests for the main module."""

import unittest
from unittest.mock import patch, MagicMock
import argparse
from text_edit_ai.cli.__main__ import main, setup_terminal_colors


class TestMain(unittest.TestCase):
    """Test cases for the main module."""

    @patch("text_edit_ai.cli.__main__.Colors")
    @patch("os.name", "nt")  # Mock Windows environment
    @patch("os.system")
    def test_setup_terminal_colors_windows(self, mock_system, mock_colors):
        """Test setting up terminal colors on Windows."""
        mock_config_manager = MagicMock()

        setup_terminal_colors(mock_config_manager)

        # Check that the color system was enabled on Windows
        mock_system.assert_called_once_with("color")

        # Check that Colors.initialize was called
        mock_colors.initialize.assert_called_once_with(mock_config_manager)

    @patch("text_edit_ai.cli.__main__.Colors")
    @patch("os.name", "posix")  # Mock Unix environment
    @patch("os.system")
    def test_setup_terminal_colors_unix(self, mock_system, mock_colors):
        """Test setting up terminal colors on Unix."""
        mock_config_manager = MagicMock()

        setup_terminal_colors(mock_config_manager)

        # Check that os.system was not called on Unix
        mock_system.assert_not_called()

        # Check that Colors.initialize was called
        mock_colors.initialize.assert_called_once_with(mock_config_manager)

    @patch("text_edit_ai.cli.__main__.ConfigManager")
    @patch("text_edit_ai.cli.__main__.setup_terminal_colors")
    @patch("text_edit_ai.cli.__main__.argparse.ArgumentParser")
    def test_main_api_key(
        self, mock_arg_parser, mock_setup_colors, mock_config_manager_class
    ):
        """Test main function with --api-key flag."""
        # Set up the mock argument parser
        mock_parser = MagicMock()
        mock_arg_parser.return_value = mock_parser

        # Set up the parsed args
        mock_args = MagicMock()
        mock_args.file = None
        mock_args.api_key = True
        mock_args.model = False
        mock_args.prompt = None
        mock_parser.parse_args.return_value = mock_args

        # Set up the mock config manager
        mock_config_manager = MagicMock()
        mock_config_manager_class.return_value = mock_config_manager

        # Call the function
        main()

        # Check that set_api_key was called
        mock_config_manager.set_api_key.assert_called_once()

    @patch("text_edit_ai.cli.__main__.ConfigManager")
    @patch("text_edit_ai.cli.__main__.setup_terminal_colors")
    @patch("text_edit_ai.cli.__main__.argparse.ArgumentParser")
    def test_main_model(
        self, mock_arg_parser, mock_setup_colors, mock_config_manager_class
    ):
        """Test main function with --model flag."""
        # Set up the mock argument parser
        mock_parser = MagicMock()
        mock_arg_parser.return_value = mock_parser

        # Set up the parsed args
        mock_args = MagicMock()
        mock_args.file = None
        mock_args.api_key = False
        mock_args.model = True
        mock_args.prompt = None
        mock_parser.parse_args.return_value = mock_args

        # Set up the mock config manager
        mock_config_manager = MagicMock()
        mock_config_manager_class.return_value = mock_config_manager

        # Call the function
        main()

        # Check that set_model was called
        mock_config_manager.set_model.assert_called_once_with(mock_args.model)

    @patch("text_edit_ai.cli.__main__.ConfigManager")
    @patch("text_edit_ai.cli.__main__.setup_terminal_colors")
    @patch("text_edit_ai.cli.__main__.LangchainManager")
    @patch("text_edit_ai.cli.__main__.FileProcessor")
    @patch("text_edit_ai.cli.__main__.argparse.ArgumentParser")
    def test_main_process_file(
        self,
        mock_arg_parser,
        mock_file_processor_class,
        mock_langchain_manager_class,
        mock_setup_colors,
        mock_config_manager_class,
    ):
        """Test main function with file to process."""
        # Set up the mock argument parser
        mock_parser = MagicMock()
        mock_arg_parser.return_value = mock_parser

        # Set up the parsed args
        mock_args = MagicMock()
        mock_args.file = "test_file.txt"
        mock_args.api_key = False
        mock_args.model = False
        mock_args.prompt = None
        mock_parser.parse_args.return_value = mock_args

        # Set up the mock config manager
        mock_config_manager = MagicMock()
        mock_config_manager_class.return_value = mock_config_manager

        # Set up the mock langchain manager
        mock_langchain_manager = MagicMock()
        mock_langchain_manager_class.return_value = mock_langchain_manager

        # Set up the mock file processor
        mock_file_processor = MagicMock()
        mock_file_processor_class.return_value = mock_file_processor

        # Call the function
        main()

        # Check that the langchain manager was created
        mock_langchain_manager_class.assert_called_once_with(mock_config_manager)

        # Check that the file processor was created
        mock_file_processor_class.assert_called_once_with(
            mock_config_manager, mock_langchain_manager, "test_file.txt"
        )

        # Check that the file was processed
        mock_file_processor.process.assert_called_once()


if __name__ == "__main__":
    unittest.main()
