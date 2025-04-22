#!/bin/bash

# Run mypy
echo "Running mypy..."
uv run mypy . --exclude .venv --exclude venv --exclude __pycache__ --exclude .pytest_cache

# Return success/failure status
if [ $? -eq 0 ]; then
  echo "✅ Type checking passed!"
  exit 0
else
  echo "❌ Type checking failed."
  exit 1
fi 