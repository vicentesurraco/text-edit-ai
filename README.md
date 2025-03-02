# AI Text Editor

A command-line tool for editing text with the assistance of AI, using language models to suggest improvements or changes to text sections.

## Installation

1. Clone the repository:
   Run `git clone https://github.com/vicentesurraco/text-edit-ai.git` and then `cd text-edit-ai`.

2. Install the required dependencies:
   Run `uv sync --lockfile uv.lock`.

   **Note:** Ensure you have Python 3.8 or higher installed, and `uv` installed globally.

## Usage

Run the tool with the following command:
`uv run -m text_edit_ai.cli [file] [options]`

### Options

- `--api-key`: Set the API key for the language model.
- `--prompt "Your prompt"`: Set a custom system prompt for the specified file.

### Examples

- To edit a text file named `my_book.txt`:
  `uv run -m text_edit_ai.cli my_book.txt`

- To set the API key:
  `uv run -m text_edit_ai.cli --api-key`

- To set a custom system prompt for `my_book.txt`:
  `uv run -m text_edit_ai.cli my_book.txt --prompt "Improve the clarity and conciseness of this text."`

## Configuration

The tool stores configurations in `~/.ai_text_editor.cfg`:

- **API Keys**: Securely stores your language model API key
- **Prompts**: File-specific system prompts
- **Colors**: Customizable color schemes for the UI
- **File Position**: Remembers where you left off in each file

### Customizing Colors

The color scheme can be customized by editing the `~/.ai_text_editor.cfg` file directly.
Under the `[COLORS]` section, you can modify any of these colors by changing their hex values:

```
[COLORS]
green = 7EC752 # Used for accept/continue/added markup
red = FF6D52 # Used for exit/removed markup
yellow = FFBA08 # Used for skip
blue = 5BC0BE # Used for size
grey = C8C8A9 # Used for section headers
purple = DF78EF # Used for markup display
orange = FF9300 # Used for prompt options
```

## Workflow

1. **Process the file**: Pass the file path as a positional argument; the tool splits it into sections based on double newlines.

2. **Process sections**: For each section, the user is prompted to:
   - `continue`: Use AI to suggest edits.
   - `skip`: Keep the section as is.
   - `size`: Change the number of paragraphs per section.
   - `exit`: Exit the program.

3. **AI suggestions**: If `continue` is chosen, the AI provides an edited version of the section. The user can then:
   - `accept`: Save the AI's suggestion.
   - `skip`: Keep the original section.
   - `section prompt`: Provide a new prompt for the AI to re-edit the current section.
   - `system prompt`: Change the system prompt used for all future edits.
   - `markup`: View changes with colorized markup showing additions and deletions.
   - `size`: Change the number of paragraphs per section.
   - `exit`: Exit the program.

4. **Output**: Edited or skipped sections are appended to a new file named `[original_filename]_edited.txt`.