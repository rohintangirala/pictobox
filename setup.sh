#!/bin/bash

if ! command -v python3 &>/dev/null; then
    echo "Please install Python 3. Aborting..."
    exit 1
fi

if ! command -v pip &>/dev/null; then
    echo "Please install pip. Aborting..."
    exit 1
fi

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "'requirements.txt' not found. Aborting..."
    exit 1
fi

chmod +x pictobox.py

echo -e "\nPictobox setup complete."
