#!/bin/bash
# Wrapper script to run the idea processor

# Change to repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import openai" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r scripts/idea_processor/requirements.txt
fi

# Run the processor
python3 -m scripts.idea_processor.cli "$@"
