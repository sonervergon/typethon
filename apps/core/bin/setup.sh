#!/bin/bash

# Get the app directory
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$APP_DIR"

echo "Setting up Core API environment..."
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
deactivate

echo "Core API environment has been set up successfully!"
echo "To use the virtual environment, run: cd $(basename $APP_DIR) && source venv/bin/activate" 