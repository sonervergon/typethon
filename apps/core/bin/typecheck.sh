#!/bin/bash

# Get the app directory
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$APP_DIR"

# Set PYTHONPATH to include the app directory
export PYTHONPATH="$APP_DIR"

echo "Running type checking..."

# Run mypy
echo "Running mypy..."
./.venv/bin/mypy . --exclude .venv --exclude venv --exclude __pycache__ --exclude .pytest_cache

# Return success/failure status
if [ $? -eq 0 ]; then
  echo "✅ Type checking passed!"
  exit 0
else
  echo "❌ Type checking failed."
  exit 1
fi 