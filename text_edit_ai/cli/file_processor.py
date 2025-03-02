from .config_manager import ConfigManager
from .prompt_manager import PromptManager
from .langchain_manager import LangchainManager


class FileProcessor:
    """Handles the processing of a file with AI-assisted editing."""

    def __init__(
        self,
        config_manager: ConfigManager,
        prompt_manager: PromptManager,
        langchain_manager: LangchainManager,
        file: str,
        paragraphs_per_section: int = 1,
    ):
        self.config_manager = config_manager
        self.prompt_manager = prompt_manager
        self.langchain_manager = langchain_manager
        self.file = file
        self.paragraphs_per_section = paragraphs_per_section
        self.output_file = file.split(".")[0] + "_edited.txt"
        self.file_config = config_manager.get_file_config(file)
        self.sections = []
        self.current_section = int(self.file_config.get("current_section", "0"))

    def load_file(self) -> None:
        """Load the file content and split it into sections."""
        with open(self.file, "r") as f:
            content = f.read()
        self.sections = self.split_into_sections(content)

    def get_current_group(self) -> str:
        """Get the current group of sections based on paragraphs_per_section."""
        start = self.current_section
        end = start + self.paragraphs_per_section
        return "\n\n".join(self.sections[start:end])

    def write_section(self, content: str) -> None:
        """Write content to the output file."""
        with open(self.output_file, "a") as out_f:
            out_f.write(content + "\n\n")

    def update_current_section(self) -> None:
        """Increment the current section and save config."""
        self.current_section += self.paragraphs_per_section
        self.file_config["current_section"] = str(self.current_section)
        self.config_manager.save_config()

    def handle_initial_action(self, section: str) -> str:
        """Handle the initial user action for a section."""
        print(f"\n{section}\n")
        while True:
            action = input("continue / skip / size / exit: ").strip().lower()
            if action in {"continue", "skip", "size", "exit"}:
                return action
            print("Invalid action. Please try again.")

    def handle_ai_response(self, section: str) -> str:
        """Handle AI response and subsequent user actions."""
        system_prompt = self.prompt_manager.get_system_prompt(self.file)
        res = self.langchain_manager.get_response(system_prompt, section)
        self.display_response(res)

        while True:
            action = input("accept / skip / edit / size / exit: ").strip().lower()
            if action == "accept":
                self.write_section(res)
                return "next"
            elif action == "skip":
                self.write_section(section)
                return "next"
            elif action == "edit":
                section_prompt = input("Enter new prompt: ")
                system_prompt = self.prompt_manager.get_system_prompt(self.file)
                res = self.langchain_manager.get_response(
                    system_prompt + "\n" + section_prompt, section
                )
                self.display_response(res)
            elif action == "size":
                return "size"
            elif action == "exit":
                return "exit"
            else:
                print("Invalid action. Please try again.")

    def process(self) -> None:
        """Process the file section by section."""
        self.load_file()
        while self.current_section < len(self.sections):
            if self.sections[self.current_section :]:
                section = self.get_current_group()
                action = self.handle_initial_action(section)

                if action == "continue":
                    ai_action = self.handle_ai_response(section)
                    if ai_action == "next":
                        self.update_current_section()
                    elif ai_action == "size":
                        self.paragraphs_per_section = (
                            self.change_paragraphs_per_section()
                        )
                    elif ai_action == "exit":
                        exit(0)
                elif action == "skip":
                    self.write_section(section)
                    self.update_current_section()
                elif action == "size":
                    self.paragraphs_per_section = self.change_paragraphs_per_section()
                elif action == "exit":
                    exit(0)
            else:
                break
        print("All sections have been processed.")

    def split_into_sections(self, content: str) -> list[str]:
        """Split content into sections separated by double newlines."""
        content = content.replace("\n\n", "\n").replace("\n", "\n\n")
        sections = [p.strip() for p in content.split("\n\n") if p.strip()]
        return sections

    def change_paragraphs_per_section(self) -> int:
        """Prompt user to input the number of paragraphs per section."""
        while True:
            try:
                return int(input("Enter number of paragraphs per section: ").strip())
            except ValueError:
                print("Please enter an integer.")

    def display_response(self, response: str) -> None:
        """Display the AI-generated response."""
        print(f"\n{response}\n")
