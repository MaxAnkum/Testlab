
#!/bin/bash

# Function to create folder and write something using Bash language in powershell (which should be standard for powershell)
create_folder_and_log_bash() {
    mkdir -p hello_everywhere_output
    echo "Log created on $(date)" > hello_everywhere_output/log.txt
    echo "Hello from Bash!"
}

# Function to create folder and write something using Python 
# Check if Python is available before using it
create_folder_and_log_python() {
    python3 - <<END
import os
import datetime

os.makedirs('hello_everywhere_output', exist_ok=True)
with open('hello_everywhere_output/log.txt', 'a') as f:
    f.write(f"Log created on {datetime.datetime.now()}\n")
# Removed redundant print statement
END
}

# Check if Bash is available
if command -v bash &> /dev/null
then
    create_folder_and_log_bash
elif command -v python3 &> /dev/null
then
    create_folder_and_log_python
else
    echo "Neither Bash nor Python3 is available on this system."
    exit 1
fi
else
    echo "Neither Bash nor Python is available. Exiting."
    exit 1
fi
