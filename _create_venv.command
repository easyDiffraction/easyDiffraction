#!/bin/sh
clear

CURRENT_DIR="$(dirname "$0")"
VENV_DIR=$CURRENT_DIR/.python-venv

echo "*** create virtual environment: $VENV_DIR"
python3.7 -m venv $VENV_DIR

read -p "Press any key to exit..."
exit 0
