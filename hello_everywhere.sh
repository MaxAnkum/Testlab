#!/bin/bash

# Cross-platform script: works in Bash, PowerShell, or CMD
# Creates hello_everywhere_output/log.txt with a timestamped message

# Detect PowerShell
if command -v pwsh &> /dev/null || command -v powershell &> /dev/null; then
    if command -v pwsh &> /dev/null; then
        pwsh -Command "New-Item -ItemType Directory -Force -Path hello_everywhere_output; Add-Content -Path hello_everywhere_output/log.txt -Value ('Log created on ' + (Get-Date)); Write-Host 'Hello from PowerShell!'"
    else
        powershell -Command "New-Item -ItemType Directory -Force -Path hello_everywhere_output; Add-Content -Path hello_everywhere_output/log.txt -Value ('Log created on ' + (Get-Date)); Write-Host 'Hello from PowerShell!'"
    fi
    exit 0
fi

# Detect Bash/sh (macOS uses Bash or Zsh by default)
if command -v bash &> /dev/null || command -v sh &> /dev/null || command -v zsh &> /dev/null; then
    if command -v zsh &> /dev/null; then
        zsh -c 'mkdir -p hello_everywhere_output && echo "Log created on $(date)" >> hello_everywhere_output/log.txt && echo "Hello from Zsh!"'
    else
        mkdir -p hello_everywhere_output
        echo "Log created on $(date)" >> hello_everywhere_output/log.txt
        echo "Hello from Bash!"
    fi
    exit 0
fi

# Detect Python
if command -v python3 &> /dev/null || command -v python &> /dev/null; then
    if command -v python3 &> /dev/null; then
        python3 - <<END
import os, datetime
os.makedirs('hello_everywhere_output', exist_ok=True)
with open('hello_everywhere_output/log.txt', 'a') as f:
    f.write(f"Log created on {datetime.datetime.now()}\n")
print('Hello from Python!')
END
    else
        python - <<END
import os, datetime
os.makedirs('hello_everywhere_output', exist_ok=True)
with open('hello_everywhere_output/log.txt', 'a') as f:
    f.write("Log created on {}\n".format(datetime.datetime.now()))
print('Hello from Python!')
END
    fi
    exit 0
fi

# Detect Windows CMD
if [ "$COMSPEC" != "" ]; then
    mkdir hello_everywhere_output 2>nul
    echo Log created on %date% %time% >> hello_everywhere_output\log.txt
    echo Hello from CMD!
    exit 0
fi

echo "No supported shell or language found. Exiting."
exit 1
