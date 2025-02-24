## Workflow

1. **Load the file**: The tool reads the specified file and splits it into sections based on double newlines.
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

## Configuration

- **API Key**: Set using the `--api-key` option. The key is stored in a configuration file.
- **System Prompt**: Set using the `--prompt` option. This prompt guides the AI's editing behavior for the specified file.
