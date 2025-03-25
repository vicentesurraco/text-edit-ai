# AI Text Editor

A command-line tool for editing text with the assistance of AI, using language models to suggest improvements or changes to text sections.

## Installation

1. Clone the repository:
   Run `git clone https://github.com/vicentesurraco/text-edit-ai.git` and then `cd text-edit-ai`.

2. Install the required dependencies:
   Run `uv sync --lockfile uv.lock`.

   **Note:** Ensure you have Python 3.9 or higher installed, and `uv` installed globally.

## Usage

Run the tool with the following command:
`uv run -m text_edit_ai.cli [file] [options]`

### Options

- `--api-key`: Set the API key for the language model.
- `--prompt "Your prompt"`: Set a custom file prompt for the specified file.
- `--prompt-file "path/to/prompt.txt"`: Use a prompt from a file instead of directly specifying it.
- `--model "model_name"`: Use a specific model for this session (e.g., "gemini-2.0-flash", "gpt-4-turbo").

### Examples

- To edit a text file named `my_book.txt`:
  `uv run -m text_edit_ai.cli my_book.txt`

- To set the API key:
  `uv run -m text_edit_ai.cli --api-key`

- To set a custom file prompt for `my_book.txt`:
  `uv run -m text_edit_ai.cli my_book.txt --prompt "Improve the clarity and conciseness of this text."`

- To use a prompt from a file for `my_book.txt`:
  `uv run -m text_edit_ai.cli my_book.txt --prompt-file "my_detailed_prompt.txt"`

- To use a specific model for the current editing session:
  `uv run -m text_edit_ai.cli my_book.txt --model "gpt-4-turbo"`

## Configuration

The tool stores configurations in `~/.ai_text_editor.cfg`:

- **API Keys**: Securely stores your language model API key
- **Models**: Saves your default model selection
- **Prompts**: File-specific file prompts
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
purple = DF78EF # Used for markup display and section headers
orange = FF9300 # Used for section/file prompt options
```

### Using Prompt Files

For complex or very large prompts, you can store them in separate text files and reference them using the `--prompt-file` option. This is especially useful when:

- Your prompt is too large to type on the command line
- You want to reuse the same detailed prompt across multiple editing sessions
- You need to include formatting or special characters in your prompt

The tool will read the prompt directly from the file each time it's needed, so you can edit the prompt file between sections if needed.

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
   - `file prompt`: Change the file prompt used for all future edits.
   - `markup`: View changes with colorized markup showing additions and deletions.
   - `size`: Change the number of paragraphs per section.
   - `exit`: Exit the program.

4. **Output**: Edited or skipped sections are appended to a new file named `[original_filename]_edited.txt`.

### Contributing

If you'd like to contribute, please fork the repository and open a pull request to the `main` branch.
