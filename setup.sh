#!/bin/bash

## Setup script for debian based systems 
echo "Updating system and installing dependencies..."
sudo apt update
sudo apt install git python3 python3-pip python3-venv tmux -y

echo "Installing uv..."
curl -LsSf https://astral.sh/uv/install.sh | sh

source $HOME/.cargo/env

echo "Cloning repository..."
git clone https://github.com/feljost/slope-finder-backend.git
cd slope-finder-backend

echo "Creating virtual environment..."
uv venv
source .venv/bin/activate

echo "Installing project dependencies..."
uv pip install -e .

# 8. Create a placeholder .env file (Optional)
# You can edit this file later with: nano .env
if [ ! -f .env ]; then
    echo "Creating empty .env file..."
    touch .env
    echo "# Add your env vars here (e.g. DB_URL=...)" >> .env
fi

echo "Starting Uvicorn..."
uvicorn slope_finder_backend.api.main:app --host 0.0.0.0 --port 8000 --env-file .env