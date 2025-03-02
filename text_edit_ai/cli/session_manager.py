from .config_manager import ConfigManager


class SessionManager:
    """Manages editing session state and progress."""

    def __init__(
        self, config_manager: ConfigManager, file: str, paragraphs_per_section: int = 1
    ):
        self.config_manager = config_manager
        self.file = file
        self.file_config = config_manager.get_file_config(file)
        self.paragraphs_per_section = paragraphs_per_section
        self.current_section = int(self.file_config.get("current_section", "0"))
        self.sections = []

    def set_sections(self, sections: list[str]) -> None:
        """Set the sections for the session."""
        self.sections = sections

    def get_current_section(self) -> str:
        """Get the current section or group of sections."""
        start = self.current_section
        end = min(start + self.paragraphs_per_section, len(self.sections))
        return "\n\n".join(self.sections[start:end])

    def advance(self) -> None:
        """Move to the next section."""
        self.current_section += self.paragraphs_per_section
        self.file_config["current_section"] = str(self.current_section)
        self.config_manager.save_config()

    def is_complete(self) -> bool:
        """Check if all sections have been processed."""
        return self.current_section >= len(self.sections)

    def set_paragraphs_per_section(self, num: int) -> None:
        """Set the number of paragraphs to process at once."""
        self.paragraphs_per_section = num
