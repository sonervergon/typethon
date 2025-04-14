#!/bin/bash

# Get the app directory
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$APP_DIR"

echo "Setting up Core API environment..."

# Check Python version
PYTHON_VERSION=$(python --version 2>&1)
echo "Using Python: $PYTHON_VERSION"

# Remove existing venv if present
if [ -d ".venv" ]; then
  echo "Removing existing venv directory..."
  rm -rf .venv
fi

# Create a new .venv directory
echo "Creating Python virtual environment in .venv..."
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

echo "Core API environment has been set up successfully!"
echo "To use the virtual environment, run: cd $(basename $APP_DIR) && source .venv/bin/activate" 