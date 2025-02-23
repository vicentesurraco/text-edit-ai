import keyring
import os


class APIManager:
    def __init__(self):
        self.api_key = os.environ.get("BOOK_EDITOR_API_KEY")

    def get_api_key(self):
        """
        Retrieve the API key from secure storage or prompt the user to enter it.
        Check environment variables first, then keyring.
        """
        if self.api_key:
            return self.api_key
        self.api_key = keyring.get_password("book_editor", "api_key")
        if self.api_key:
            return self.api_key
        self.api_key = input("Enter your API key: ")
        keyring.set_password("book_editor", "api_key", self.api_key)
        return self.api_key

    def set_api_key(self):
        """
        Prompt the user to enter their API key and store it securely.
        """
        self.api_key = input("Enter your API key: ")
        keyring.set_password("book_editor", "api_key", self.api_key)
        print("API key set successfully.")
