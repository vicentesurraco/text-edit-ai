class Colors:
    """ANSI color codes for terminal output."""

    DEFAULT_COLORS = {
        "green": "4E9A06",
        "red": "CC0000",  
        "yellow": "C4A000",
        "blue": "3465A4",
        "grey": "555753",
        "purple": "75507B",
        "orange": "CE5C00",
    }

    # These will be populated dynamically when initialize() is called
    green = ""
    red = ""
    yellow = ""
    blue = ""
    grey = ""
    purple = ""
    orange = ""

    # Non-color values
    strike = "\033[9m"
    reset = "\033[0m"

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
        for color_name in cls.DEFAULT_COLORS:
            config_value = config_manager.get_color(color_name)
            setattr(cls, color_name, cls.from_hex(config_value))
