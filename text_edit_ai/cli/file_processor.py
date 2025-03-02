from .config_manager import ConfigManager
from .prompt_manager import PromptManager
from .langchain_manager import LangchainManager
from .markup_manager import MarkupManager
from .colors import Colors


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
        self.markup_manager = MarkupManager()
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
        print(f"\n{Colors.grey}=== ORIGINAL ==={Colors.RESET}")
        print(f"\n{section}\n")
        print(f"{Colors.grey}=== ORIGINAL ==={Colors.RESET}\n")
        while True:
            action = (
                input(
                    f"{Colors.green}(c)ontinue{Colors.RESET} / {Colors.yellow}(s)kip{Colors.RESET} / {Colors.blue}si(z)e{Colors.RESET} / {Colors.red}e(x)it{Colors.RESET}: "
                )
                .strip()
                .lower()
            )
            if action in {"continue", "c", "skip", "s", "size", "z", "exit", "x"}:
                if action == "c":
                    return "continue"
                if action == "s":
                    return "skip"
                if action == "z":
                    return "size"
                if action == "x":
                    return "exit"
                return action
            print("Invalid action. Please try again.")

    def handle_ai_response(self, section: str) -> str:
        """Handle AI response and subsequent user actions."""
        system_prompt = self.prompt_manager.get_system_prompt(self.file)
        res = self.langchain_manager.get_response(system_prompt, section)
        diff_text = self.markup_manager.generate_diff(section, res)

        self.display_edited(res)

        while True:
            action = (
                input(
                    f"{Colors.green}(a)ccept{Colors.RESET} / "
                    f"{Colors.yellow}(s)kip{Colors.RESET} / "
                    f"{Colors.orange}se(c)tion prompt{Colors.RESET} / "
                    f"{Colors.orange}s(y)stem prompt{Colors.RESET} / "
                    f"{Colors.blue}si(z)e{Colors.RESET} / "
                    f"{Colors.red}e(x)it{Colors.RESET} / "
                    f"{Colors.purple}(m)arkup{Colors.RESET}: "
                )
                .strip()
                .lower()
            )

            if action == "accept" or action == "a":
                self.write_section(res)
                return "next"
            elif action == "skip" or action == "s":
                self.write_section(section)
                return "next"
            elif action == "section" or action == "c":
                section_prompt = input(
                    "Enter section prompt (will be appended to system prompt, empty to cancel): "
                )
                if section_prompt.strip().lower() in ["", "cancel"]:
                    continue
                system_prompt = self.prompt_manager.get_system_prompt(self.file)
                res = self.langchain_manager.get_response(
                    system_prompt + "\n" + section_prompt, section
                )
                diff_text = self.markup_manager.generate_diff(section, res)
                self.display_edited(res)
            elif action == "system" or action == "y":
                system_prompt = input(
                    "Enter new system prompt (will overwrite existing system prompt, empty to cancel): "
                )
                if system_prompt.strip().lower() in ["", "cancel"]:
                    continue
                self.prompt_manager.set_system_prompt(self.file, system_prompt)
                res = self.langchain_manager.get_response(system_prompt, section)
                diff_text = self.markup_manager.generate_diff(section, res)
                self.display_edited(res)
            elif action == "markup" or action == "m":
                self.display_markup(diff_text)
            elif action == "size" or action == "z":
                return "size"
            elif action == "exit" or action == "x":
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

    def display_edited(self, edited_text: str) -> None:
        """Display the edited text."""
        print(f"\n{Colors.grey}=== AI EDIT ==={Colors.RESET}")
        print(f"\n{edited_text}\n")
        print(f"{Colors.grey}=== AI EDIT ==={Colors.RESET}\n")

    def display_markup(self, diff_text: str) -> None:
        """Display the markup text when requested."""
        print(f"\n{Colors.purple}=== MARKUP ==={Colors.RESET}")
        print(f"\n{diff_text}\n")
        print(f"{Colors.purple}=== MARKUP ==={Colors.RESET}\n")

    def display_response(self, original: str, response: str) -> str:
        """
        Display the AI-generated response and return the diff text.

        Args:
            original: The original text
            response: The AI-generated response

        Returns:
            The diff text for potential later display
        """
        diff_text = self.markup_manager.generate_diff(original, response)
        self.display_edited(response)
        return diff_text
