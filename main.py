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


def split_into_sections(content: str) -> list[str]:
    """Split content into \n\n sections."""
    content = content.replace("\n\n", "\n")
    content = content.replace("\n", "\n\n")
    sections = [p.strip() for p in content.split("\n\n") if p.strip()]
    return sections


def change_paragraphs_per_section() -> int:
    """
    Allow user to change the number of paragraphs per section.
    Returns the new number of paragraphs per section.
    """
    while True:
        try:
            return int(input("Enter number of paragraphs per section: ").strip())
        except Exception:
            print("Please enter an integer.")
            continue


def process_file(
    config_manager: ConfigManager,
    prompt_manager: PromptManager,
    langchain_manager: LangchainManager,
    file: str,
    section_prompt: str = "",
    paragraphs_per_section: int = 1,
):
    """
    Process the specified file, starting from the current section.
    """
    # todo: SHOW section, determine whether to skip or edit. if edit, ask for prompt.

    file_config = config_manager.get_file_config(file)
    current_section = int(file_config.get("current_section", 0))
    output_file = file.split(".")[0] + "_edited.txt"

    # Read and split the file into sections
    with open(file, "r") as f:
        content = f.read()

    sections = split_into_sections(content)

    # Group sections according to paragraphs_per_section
    grouped_sections = []
    for i in range(0, len(sections)):
        group = "\n\n".join(sections[i : i + paragraphs_per_section])
        grouped_sections.append(group)

    if current_section >= len(grouped_sections):
        print("All sections have been processed.")
        return

    # Process the current section
    section = grouped_sections[current_section]
    print(f"\n{section}\n")

    while True:  # Initial action loop
        action = input("continue / skip / size / exit: ").strip().lower()
        if action == "size":
            new_paragraphs = change_paragraphs_per_section()
            process_file(
                config_manager,
                prompt_manager,
                langchain_manager,
                file,
                section_prompt,
                new_paragraphs,
            )
            return
        elif action == "exit":
            exit(0)
        elif action == "skip":
            with open(output_file, "a") as out_f:
                out_f.write(section + "\n\n")
            current_section += paragraphs_per_section
            file_config["current_section"] = str(current_section)
            config_manager.save_config()
            process_file(
                config_manager,
                prompt_manager,
                langchain_manager,
                file,
                section_prompt,
                paragraphs_per_section,
            )
            return
        elif action == "continue":
            # AI Processing path
            system_prompt = prompt_manager.get_system_prompt(file)
            res = langchain_manager.get_response(system_prompt, section)
            display_response(res)

            while True:  # AI response action loop
                action = input("accept / skip / edit / size / exit: ").strip().lower()
                if action == "size":
                    new_paragraphs = change_paragraphs_per_section()
                    process_file(
                        config_manager,
                        prompt_manager,
                        langchain_manager,
                        file,
                        section_prompt,
                        new_paragraphs,
                    )
                    return
                elif action == "accept":
                    with open(output_file, "a") as out_f:
                        out_f.write(res + "\n\n")
                    current_section += paragraphs_per_section
                elif action == "skip":
                    with open(output_file, "a") as out_f:
                        out_f.write(section + "\n\n")
                    current_section += paragraphs_per_section
                elif action == "edit":
                    section_prompt = input("Enter new prompt: ")
                    system_prompt = prompt_manager.get_system_prompt(file)
                    res = langchain_manager.get_response(
                        system_prompt + "\n" + section_prompt, section
                    )
                    display_response(res)
                    continue
                elif action == "exit":
                    exit(0)
                else:
                    print("Invalid action. Please try again.")

                file_config["current_section"] = str(current_section)
                if section_prompt:
                    prompt_manager.set_section_prompt(section_prompt, res)
                config_manager.save_config()
                process_file(
                    config_manager,
                    prompt_manager,
                    langchain_manager,
                    file,
                    section_prompt,
                    paragraphs_per_section,
                )
        else:
            print("Invalid action. Please try again.")


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

    if args.prompt and args.file:
        prompt_manager.set_system_prompt(args.file, args.prompt)
        print(f"System prompt set to: {args.prompt} for {args.file}")
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
