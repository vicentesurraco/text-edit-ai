class Colors:
    """ANSI color codes for terminal output."""

    # These will be populated dynamically when initialize() is called
    green = ""
    red = ""
    yellow = ""
    blue = ""
    grey = ""
    purple = ""
    orange = ""

    # Non-color values
    STRIKE = "\033[9m"
    RESET = "\033[0m"

    @staticmethod
    def from_hex(hex_color: str) -> str:
        """Convert a hex color code to ANSI 24-bit true color escape sequence."""
        # Remove the # if present
        hex_color = hex_color.lstrip("#")

        # Convert hex to RGB decimal values
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        # Return the ANSI escape sequence
        return f"\033[38;2;{r};{g};{b}m"

    @classmethod
    def initialize(cls, config_manager):
        """Initialize color values from config manager."""
        cls.green = cls.from_hex(config_manager.get_color("GREEN"))
        cls.red = cls.from_hex(config_manager.get_color("RED"))
        cls.yellow = cls.from_hex(config_manager.get_color("YELLOW"))
        cls.blue = cls.from_hex(config_manager.get_color("BLUE"))
        cls.grey = cls.from_hex(config_manager.get_color("GREY"))
        cls.purple = cls.from_hex(config_manager.get_color("PURPLE"))
        cls.orange = cls.from_hex(config_manager.get_color("ORANGE"))
