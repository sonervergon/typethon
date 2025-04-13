#!/bin/bash

# Get the app directory
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$APP_DIR"

# Set PYTHONPATH to include the app directory
export PYTHONPATH="$APP_DIR"

echo "Running linters..."

# Run flake8
echo "Running flake8..."
./.venv/bin/flake8 .

# Return success if linting succeeded
if [ $? -eq 0 ]; then
  echo "✅ Linting passed!"
  exit 0
else
  echo "❌ Linting failed."
  exit 1
fi 