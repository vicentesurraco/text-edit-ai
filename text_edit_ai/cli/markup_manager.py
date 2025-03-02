import difflib
import re
from typing import List
from .colors import Colors


class MarkupManager:
    """
    Manages the markup of diffs between original and edited text.

    This class provides utilities for tokenizing text, calculating diffs,
    and formatting differences between original and edited content.
    """

    def generate_diff(self, original_text: str, edited_text: str) -> str:
        """
        Generate a word-level diff showing specific changes.

        Args:
            original_text: The original text
            edited_text: The edited text

        Returns:
            Formatted diff text with color markup
        """
        original_tokens = self._tokenize(original_text)
        edited_tokens = self._tokenize(edited_text)
        diff_tokens = self._calculate_diff(original_tokens, edited_tokens)

        diff_text = "".join(diff_tokens)

        return diff_text

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """
        Split text into tokens (words, spaces, and punctuation).

        Args:
            text: The text to tokenize

        Returns:
            A list of token strings
        """
        return re.findall(r"\w+|\S+|\s+", text)

    def _calculate_diff(
        self, original_tokens: List[str], edited_tokens: List[str]
    ) -> List[str]:
        """
        Calculate differences between token lists and produce formatted diff tokens.

        Args:
            original_tokens: List of tokens from the original text
            edited_tokens: List of tokens from the edited text

        Returns:
            List of formatted tokens with diff markup
        """
        matcher = difflib.SequenceMatcher(None, original_tokens, edited_tokens)
        result = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                result.extend(original_tokens[i1:i2])
            elif tag == "delete":
                for token in original_tokens[i1:i2]:
                    result.append(f"{Colors.red}{Colors.STRIKE}{token}{Colors.RESET}")
            elif tag == "insert":
                for token in edited_tokens[j1:j2]:
                    result.append(f"{Colors.green}{token}{Colors.RESET}")
            elif tag == "replace":
                for token in original_tokens[i1:i2]:
                    result.append(f"{Colors.red}{Colors.STRIKE}{token}{Colors.RESET}")
                for token in edited_tokens[j1:j2]:
                    result.append(f"{Colors.green}{token}{Colors.RESET}")

        return result
