from .config_manager import ConfigManager
from .prompt_manager import PromptManager
from .langchain_manager import LangchainManager
from .file_processor import FileProcessor
import argparse


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="AI Book Editor")
    parser.add_argument("file", nargs="?", help="The book file to edit")
    parser.add_argument("--prompt", help="Set the system prompt for this file")
    parser.add_argument("--api-key", action="store_true", help="Set the API key")

    args = parser.parse_args()

    config_manager = ConfigManager()
    prompt_manager = PromptManager(config_manager)

    if args.api_key:
        config_manager.set_api_key()
        return

    langchain_manager = LangchainManager(config_manager.get_api_key())

    if args.prompt and args.file:
        prompt_manager.set_system_prompt(args.file, args.prompt)
        print(f"System prompt set to: {args.prompt} for {args.file}")
        return

    if not args.file:
        print("Please specify a file to edit.")
        return

    processor = FileProcessor(
        config_manager, prompt_manager, langchain_manager, args.file
    )
    processor.process()


if __name__ == "__main__":
    main()
