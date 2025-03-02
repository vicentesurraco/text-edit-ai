import os
from .config_manager import ConfigManager
from .langchain_manager import LangchainManager
from .file_processor import FileProcessor
from .colors import Colors
import argparse


def setup_terminal_colors(config_manager):
    """
    Configure terminal to support ANSI color codes and initialize Colors
    """
    if os.name == "nt":  # Windows
        os.system("color")

    Colors.initialize(config_manager)


def main():
    """Main entry point for the CLI."""
    config_manager = ConfigManager()
    setup_terminal_colors(config_manager)

    parser = argparse.ArgumentParser(description="AI Book Editor")
    parser.add_argument("file", nargs="?", help="The book file to edit")
    parser.add_argument("--prompt", help="Set the system prompt for this file")
    parser.add_argument("--api-key", action="store_true", help="Set the API key")
    parser.add_argument(
        "--model",
        action="store_true",
        help="Specific name of the model (e.g. gemini-2.0-flash)",
    )

    args = parser.parse_args()

    if args.api_key:
        config_manager.set_api_key()
        return

    if args.model:
        config_manager.set_model(args.model)
        return

    langchain_manager = LangchainManager(config_manager)

    if args.prompt and args.file:
        config_manager.set_system_prompt(args.file, args.prompt)
        print(f"System prompt set to: {args.prompt} for {args.file}")
        return

    if not args.file:
        print("Please specify a file to edit.")
        return

    processor = FileProcessor(config_manager, langchain_manager, args.file)
    processor.process()


if __name__ == "__main__":
    main()
