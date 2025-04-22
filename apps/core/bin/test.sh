#!/bin/bash

# Get the app directory
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$APP_DIR"

# Set PYTHONPATH to include the app directory
export PYTHONPATH="$APP_DIR"

# Debug output to show PATH and PYTHONPATH
echo "Running tests with PYTHONPATH=$PYTHONPATH"

# Run pytest with uv instead of direct Python call
uv run pytest "$@" 