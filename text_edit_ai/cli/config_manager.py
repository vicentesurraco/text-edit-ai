import configparser
import os
from .colors import Colors


class ConfigManager:
    CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".ai_text_editor.cfg")

    def __init__(self):
        self.config = self.get_config()
        self._ensure_color_config()

    def get_config(self):
        """
        Load and return the configuration file.
        If it doesn't exist, create an empty config.
        """
        self.config = configparser.ConfigParser()
        self.config.read(self.CONFIG_FILE)

        if "DEFAULT" not in self.config:
            self.config["DEFAULT"] = {}

        return self.config

    def _ensure_color_config(self):
        """Ensure color configuration exists with defaults."""
        if "COLORS" not in self.config:
            self.config["COLORS"] = {}

        for color_name, hex_value in Colors.DEFAULT_COLORS.items():
            if color_name not in self.config["COLORS"]:
                self.config["COLORS"][color_name] = hex_value

        self.save_config()

    def get_color(self, color_name):
        """Get a color value from config."""
        color_value = self.config["COLORS"].get(color_name.lower())

        if not color_value:
            color_value = Colors.DEFAULT_COLORS.get(color_name.lower(), "FFFFFF")

        return color_value

    def set_color(self, color_name, hex_value):
        """Set a color value in config."""
        if "COLORS" not in self.config:
            self.config["COLORS"] = {}
        self.config["COLORS"][color_name.lower()] = hex_value
        self.save_config()

    def save_config(self):
        """
        Save the configuration to the file.
        """
        with open(self.CONFIG_FILE, "w") as configfile:
            self.config.write(configfile)

    def get_file_config(self, file):
        """
        Get or create the configuration section for a specific file.
        """
        if file not in self.config:
            self.config[file] = {}
        return self.config[file]

    def get_api_key(self):
        """Get API key from config, set it if None"""
        api_key = self.config["DEFAULT"].get("api_key")
        if not api_key:
            return self.set_api_key()
        return api_key

    def set_api_key(self):
        """Set API key in config"""
        api_key = input("Enter your API key: ")
        self.config["DEFAULT"]["api_key"] = api_key
        self.save_config()
        print("API key set successfully.")
        return api_key

    def get_model(self):
        """Get model name from config, or return the default if not set"""
        model = self.config["DEFAULT"].get("model")
        if not model:
            return self.set_model()
        return model

    def set_model(self):
        """Set model name in config"""
        model = input("Enter the model name: ")
        self.config["DEFAULT"]["model"] = model
        self.save_config()
        print(f"Model set to: {model}")
        return model

    def set_pos(self, file, pos):
        """
        Set the position for the specified file.
        """
        file_config = self.get_file_config(file)
        file_config["position"] = str(pos)
        self.save_config()

    def get_pos(self, file):
        """
        Get the position for the specified file.
        Returns 0 if not set.
        """
        file_config = self.get_file_config(file)
        return int(file_config.get("position", "0"))

    def set_system_prompt(self, file, system_prompt):
        """
        Set the system prompt for the specified file.
        """
        file_config = self.get_file_config(file)
        file_config["system_prompt"] = system_prompt
        self.save_config()

    def get_system_prompt(self, file):
        """
        Get the system prompt for the specified file.
        Returns an empty string if not set.
        """
        file_config = self.get_file_config(file)
        return file_config.get("system_prompt", "")
