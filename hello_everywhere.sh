
#!/bin/bash

# Function to create folder and write something using Bash
create_folder_and_log_bash() {
    mkdir -p hello_everywhere_output
    echo "Log created on $(date)" > hello_everywhere_output/log.txt
    echo "Hello from Bash!"
}

# Function to create folder and write something using Python
create_folder_and_log_python() {
    python3 - <<END
import os
import datetime

os.makedirs('hello_everywhere_output', exist_ok=True)
with open('hello_everywhere_output/log.txt', 'w') as f:
    f.write(f"Log created on {datetime.datetime.now()}")
print("Hello from Python!")
END
}

# Check if Bash is available
if command -v bash &> /dev/null
then
    create_folder_and_log_bash
else
    create_folder_and_log_python
fi
