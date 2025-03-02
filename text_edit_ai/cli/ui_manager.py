from .colors import Colors


class UIManager:
    """Handles user interface interactions."""

    def get_initial_action(self, section: str) -> str:
        """Get initial action from user for a section."""
        print(f"\n{Colors.grey}=== ORIGINAL ==={Colors.RESET}")
        print(f"\n{section}\n")
        print(f"{Colors.grey}=== ORIGINAL ==={Colors.RESET}\n")

        while True:
            action = (
                input(
                    f"{Colors.green}(c)ontinue{Colors.RESET} / "
                    f"{Colors.yellow}(s)kip{Colors.RESET} / "
                    f"{Colors.blue}si(z)e{Colors.RESET} / "
                    f"{Colors.red}e(x)it{Colors.RESET}: "
                )
                .strip()
                .lower()
            )

            if action in {"continue", "c"}:
                return "continue"
            elif action in {"skip", "s"}:
                return "skip"
            elif action in {"size", "z"}:
                return "size"
            elif action in {"exit", "x"}:
                return "exit"
            else:
                print("Invalid action. Please try again.")

    def get_ai_action(self, edited_text: str, diff_text: str) -> str:
        """Get user action after AI edit."""
        self.display_edited(edited_text)

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

            if action in {"accept", "a"}:
                return "accept"
            elif action in {"skip", "s"}:
                return "skip"
            elif action in {"section", "c"}:
                return "section_prompt"
            elif action in {"system", "y"}:
                return "system_prompt"
            elif action in {"markup", "m"}:
                self.display_markup(diff_text)
                # Continue loop to show options again
            elif action in {"size", "z"}:
                return "size"
            elif action in {"exit", "x"}:
                return "exit"
            else:
                print("Invalid action. Please try again.")

    def get_section_prompt(self) -> str:
        """Get a section-specific prompt from the user."""
        prompt = input("Enter section prompt (empty to cancel): ")
        if prompt.strip().lower() in ["", "cancel"]:
            print("Section prompt change canceled.")
            return ""
        return prompt

    def get_system_prompt(self) -> str:
        """Get a new system prompt from the user."""
        prompt = input("Enter new system prompt (empty to cancel): ")
        if prompt.strip().lower() in ["", "cancel"]:
            print("System prompt change canceled.")
            return ""
        return prompt

    def get_section_size(self) -> int:
        """Get the number of paragraphs per section."""
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
        """Display the markup text."""
        print(f"\n{Colors.purple}=== MARKUP ==={Colors.RESET}")
        print(f"\n{diff_text}\n")
        print(f"{Colors.purple}=== MARKUP ==={Colors.RESET}\n")

    def show_completion_message(self) -> None:
        """Show completion message."""
        print("All sections have been processed.")
