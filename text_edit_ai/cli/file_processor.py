from .config_manager import ConfigManager
from .langchain_manager import LangchainManager
from .markup_manager import MarkupManager
from .ui_manager import UIManager
from .session_manager import SessionManager


class FileProcessor:
    """Core file processing logic."""

    def __init__(
        self,
        config_manager: ConfigManager,
        langchain_manager: LangchainManager,
        file: str,
        paragraphs_per_section: int = 1,
    ):
        self.config_manager = config_manager
        self.langchain_manager = langchain_manager
        self.markup_manager = MarkupManager()
        self.file = file
        self.output_file = file.split(".")[0] + "_edited.txt"

        self.session_manager = SessionManager(
            config_manager, file, paragraphs_per_section
        )
        self.ui_manager = UIManager()

    def process(self) -> None:
        """Process the file section by section."""
        content = self._load_file()
        sections = self._split_into_sections(content)
        self.session_manager.set_sections(sections)

        while not self.session_manager.is_complete():
            section = self.session_manager.get_current_section()

            action = self.ui_manager.get_initial_action(section)

            if action == "continue":
                self._process_with_ai(section)
            elif action == "skip":
                self._write_section(section)
                self.session_manager.advance()
            elif action == "size":
                new_size = self.ui_manager.get_section_size()
                self.session_manager.set_paragraphs_per_section(new_size)
            elif action == "exit":
                return

        self.ui_manager.show_completion_message()

    def _load_file(self) -> str:
        """Load the file content."""
        with open(self.file, "r") as f:
            return f.read()

    def _split_into_sections(self, content: str) -> list[str]:
        """Split content into sections based on paragraphs."""
        content = content.replace("\n\n", "\n").replace("\n", "\n\n")
        return [p.strip() for p in content.split("\n\n") if p.strip()]

    def _write_section(self, content: str) -> None:
        """Write content to the output file."""
        with open(self.output_file, "a") as out_f:
            out_f.write(content + "\n\n")

    def _process_with_ai(self, section: str) -> None:
        """Process a section with AI assistance."""
        system_prompt = self.config_manager.get_system_prompt(self.file)
        edited = self.langchain_manager.get_response(system_prompt, section)
        diff = self.markup_manager.generate_diff(section, edited)

        while True:
            action = self.ui_manager.get_ai_action(edited, diff)

            if action == "accept":
                self._write_section(edited)
                self.session_manager.advance()
                break
            elif action == "skip":
                self._write_section(section)
                self.session_manager.advance()
                break
            elif action == "section_prompt":
                prompt = self.ui_manager.get_section_prompt()
                if not prompt:  # Canceled
                    continue

                combined_prompt = f"{system_prompt}\n{prompt}"
                edited = self.langchain_manager.get_response(combined_prompt, section)
                diff = self.markup_manager.generate_diff(section, edited)
            elif action == "system_prompt":
                prompt = self.ui_manager.get_system_prompt()
                if not prompt:  # Canceled
                    continue

                self.config_manager.set_system_prompt(self.file, prompt)
                edited = self.langchain_manager.get_response(prompt, section)
                diff = self.markup_manager.generate_diff(section, edited)
            elif action == "size":
                new_size = self.ui_manager.get_section_size()
                self.session_manager.set_paragraphs_per_section(new_size)
                return
            elif action == "exit":
                return "exit"
