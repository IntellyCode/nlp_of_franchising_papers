#!/bin/zsh

# Define the path to your virtual environment
VENV_PATH="./.venv"

# Define the Python file you want to run
PYTHON_FILE="main.py"

# Check if the virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment not found. Please create it first."
    exit 1
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# Check if the Python file exists
if [ ! -f "$PYTHON_FILE" ]; then
    echo "Python file '$PYTHON_FILE' not found."
    exit 1
fi

# Run the Python file
echo "Running Python file: $PYTHON_FILE"
python "$PYTHON_FILE"

