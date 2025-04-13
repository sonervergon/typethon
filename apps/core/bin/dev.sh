#!/bin/bash

# Get the app directory
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$APP_DIR"

# Set PYTHONPATH to include the current directory
export PYTHONPATH=$APP_DIR

# Run the application
./.venv/bin/python main.py 