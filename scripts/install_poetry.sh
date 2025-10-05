#!/bin/bash

# Install Poetry for Python environment management in the monorepo
# Usage: ./install_poetry.sh

set -e

echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found. Please install Python3 first."
    exit 1
fi

echo "Installing Poetry..."
curl -sSL https://install.python-poetry.org | python3 -

echo "Adding Poetry to PATH..."
export PATH="$HOME/.local/bin:$PATH"

echo "Configuring Poetry..."
poetry config virtualenvs.in-project true
poetry config virtualenvs.create true

echo "Poetry installed successfully. Use 'poetry init' in project directories to set up environments."
