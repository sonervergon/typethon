#!/bin/bash
cd "$(dirname "$0")"
export PYTHONPATH=$PWD
./venv/bin/python main.py
