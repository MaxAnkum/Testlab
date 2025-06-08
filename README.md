# hello_everywhere.sh

This script is designed to demonstrate how to create a folder and log a message using the most basic scripting languages available on a system, regardless of the shell environment. The goal is to maximize compatibility across different platforms (Linux, macOS, Windows) by using simple Bash or Python code, so that the script can run almost anywhere with minimal requirements.

## How it works
- **Bash function:** If Bash is available, the script creates a folder called `hello_everywhere_output` and writes a log entry with the current date to `log.txt` inside that folder.
- **Python function:** If Bash is not available but Python 3 is, the script does the same using Python code.
- If neither Bash nor Python 3 is available, the script prints an error message and exits.

## Why this approach?
- **Shell differences:** Different operating systems use different default shells (e.g., Bash on Linux/macOS, PowerShell or Command Prompt on Windows). This script checks for the presence of Bash or Python to ensure it can run in as many environments as possible.
- **Minimal dependencies:** By relying only on Bash or Python, the script avoids the need for more complex or platform-specific scripting languages.

## Usage
Run the script in a terminal or shell that supports Bash or Python 3:

```sh
./hello_everywhere.sh
```

Or, on Windows (if Bash or Python is available):

```powershell
bash hello_everywhere.sh
# or
python hello_everywhere.sh
```

## License
See [LICENSE](LICENSE) for details.
