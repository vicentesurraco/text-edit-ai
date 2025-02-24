# AI Text Editor

A command-line tool for editing text with the assistance of AI, using language models to suggest improvements or changes to text sections.

## Installation

1. Clone the repository:
   Run `git clone https://github.com/yourusername/text-edit-ai.git` and then `cd text-edit-ai`.

2. Install the required dependencies:
   Run `uv sync --lockfile uv.lock`.

   **Note:** Ensure you have Python 3.8 or higher installed, and `uv` installed globally.

## Usage

Run the tool with the following command:
`python main.py [file] [options]`

### Options

- `--api-key`: Set the API key for the language model.
- `--prompt "Your prompt"`: Set a custom system prompt for the specified file.

### Examples

- To edit a text file named `my_book.txt`:
  `python main.py my_book.txt`

- To set the API key:
  `python main.py --api-key`

- To set a custom system prompt for `my_book.txt`:
  `python main.py my_book.txt --prompt "Improve the clarity and conciseness of this text."`

## Workflow

1. **Process the file**: Pass the file path as a positional argument; the tool splits it into sections based on double newlines.
2. **Process sections**: For each section, the user is prompted to:
   - `continue`: Use AI to suggest edits.
   - `skip`: Keep the section as is.
   - `size`: Change the number of paragraphs per section.
   - `exit`: Stop the editing process.
3. **AI suggestions**: If `continue` is chosen, the AI provides an edited version of the section. The user can then:
   - `accept`: Save the AI's suggestion.
   - `skip`: Keep the original section.
   - `edit`: Provide a new prompt for the AI to re-edit the section.
   - `size`: Change the section size.
   - `exit`: Stop the process.
4. **Output**: Edited or skipped sections are appended to a new file named `[original_filename]_edited.txt`.
