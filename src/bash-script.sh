#!/bin/bash
echo "Mailbox Analysis"
if [ ! -d "inbox" ]; then
    echo "Error: 'inbox' folder does not exist"
    exit 1
fi
file_count=$(find inbox -type f -name "*" 2>/dev/null | wc -l)
echo "Found files: $file_count"
echo "Analysis started"
python3 main.py
exit_code=$?
echo "Analysis finished"
if [ $exit_code -eq 0 ]; then
    echo "Completed successfully"
else
    echo "Error (code: $exit_code)"
fi
exit $exit_code