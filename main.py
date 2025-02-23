from config_manager import ConfigManager
from prompt_manager import PromptManager
from langchain_manager import LangchainManager
import argparse


def save_progress():
    pass


def show_diff():
    pass


def get_next_pos(pos, file):
    pass


def display_response(res):
    pass


def change_response_size():
    pass


def process_file(
    config_manager: ConfigManager,
    prompt_manager: PromptManager,
    langchain_manager: LangchainManager,
    file: str,
    section_prompt: str = "",
):
    """
    Process the specified file, starting from the current section.
    """
    # todo: SHOW section, determine whether to skip or edit. if edit, ask for prompt.

    config = config_manager.config
    file_config = config_manager.get_file_config(config, file)
    current_section = int(config_manager.file_config.get("current_section", 0))
    output_file = file + "_edited.txt"

    # Read and split the file into sections (paragraphs)
    with open(file, "r") as f:
        content = f.read()
    sections = [p.strip() for p in content.split("\n\n") if p.strip()]

    if current_section >= len(sections):
        print("All sections have been processed.")
        return

    # Process the current section
    section = sections[current_section]
    system_prompt = prompt_manager.get_system_prompt(file)
    res = langchain_manager.get_response(
        system_prompt,
    )
    display_response(res)

    # Ask the user for action
    action = input("accept / skip / edit prompt: ").strip().lower()
    if action == "accept":
        with open(output_file, "a") as out_f:
            out_f.write(res + "\n\n")
        current_section += 1
    elif action == "skip":
        with open(output_file, "a") as out_f:
            out_f.write(section + "\n\n")
        current_section += 1
        res = ""
    elif action == "edit prompt":
        section_prompt = input("Enter new prompt: ")
        process_file(
            config_manager, prompt_manager, langchain_manager, file, section_prompt
        )
        return
    else:
        print("Invalid action. Exiting.")
        return

    # Update progress
    file_config["current_section"] = str(current_section)
    prompt_manager.set_section_prompt(section_prompt, res)
    config_manager.save_config(config)


def main():
    """
    Main entry point for the CLI.
    """
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

    if args.set_prompt and args.file:
        prompt_manager.set_system_prompt(args.file, args.set_prompt)
        print(f"System prompt set to: {args.set_prompt} for {args.file}")
        return

    if not args.file:
        print("Please specify a file to edit.")
        return

    process_file(
        config_manager,
        prompt_manager,
        langchain_manager,
        args.file,
    )


if __name__ == "__main__":
    main()
