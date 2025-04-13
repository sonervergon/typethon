#!/bin/bash

# Get the app directory
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$APP_DIR"

# Set PYTHONPATH to include the app directory
export PYTHONPATH="$APP_DIR"

echo "Formatting Python code..."

# Run isort to organize imports (using pyproject.toml)
echo "Running isort..."
./.venv/bin/isort .

# Run black to format code (using pyproject.toml)
echo "Running black..."
./.venv/bin/black .

echo "✅ Code formatting complete!" 