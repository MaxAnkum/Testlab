# Project Wiki: hello_everywhere.sh

## Overview
This project demonstrates how to write a script that works on almost any computer, regardless of the operating system or shell. The script creates a folder and writes a log message using the simplest commands available in Bash, Zsh, PowerShell, Python, or Windows CMD.

## What is this for?
- To show how you can write scripts that "just work" on Linux, macOS, or Windows.
- To help beginners understand cross-platform scripting basics.

## How does it work?
1. **Checks for PowerShell** (Windows):
   - Uses PowerShell commands to create a folder and log file.
2. **Checks for Bash or Zsh** (Linux/macOS):
   - Uses Bash or Zsh commands to do the same.
3. **Checks for Python:**
   - Uses a tiny Python script if Bash/Zsh/PowerShell aren't available.
4. **Checks for Windows CMD:**
   - Uses basic Windows commands if nothing else is found.
5. **If none of these are available:**
   - Prints an error message and exits.

## How do I run it?
- On Linux/macOS:
  ```sh
  ./hello_everywhere.sh
  # or
  bash hello_everywhere.sh
  ```
- On Windows (with Git Bash, WSL, or PowerShell):
  ```powershell
  bash hello_everywhere.sh
  # or just double-click the file if file associations are set up
  ```

## What does it do?
- Creates a folder called `hello_everywhere_output`.
- Adds a line to `log.txt` in that folder with the current date and time.
- Prints a message showing which shell/language was used.

## Why is this useful?
- You can use this pattern to write scripts that work for everyone, not just people on your OS.
- It helps you learn the basics of scripting in different environments.

## Where to learn more?
- [Bash scripting basics](https://www.gnu.org/software/bash/manual/bash.html)
- [PowerShell scripting basics](https://docs.microsoft.com/en-us/powershell/scripting/overview?view=powershell-7.2)
- [Python scripting basics](https://docs.python.org/3/tutorial/index.html)

---

*This wiki is for beginners. If you get stuck, ask for help or look up the links above!*
