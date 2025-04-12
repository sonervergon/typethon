#!/bin/bash

# Initialize Python environments for all Python services in the monorepo

# Core API service
echo "Setting up Core API environment..."
cd apps/core
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
deactivate
cd ../..

echo "All Python environments have been initialized!" 