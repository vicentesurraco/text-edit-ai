from .config_manager import ConfigManager


class PromptManager:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager

    def get_system_prompt(self, file):
        return self.config_manager.get_system_prompt(file)

    def set_system_prompt(self, file, system_prompt):
        return self.config_manager.set_system_prompt(file, system_prompt)
