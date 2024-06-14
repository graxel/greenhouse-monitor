#!/usr/bin/env bash

echo "Checking if all dependencies are installed:"

python -V
if [ $? -ne 0 ]; then
    echo "Python not found."
    exit 1
fi

pipenv --version
if [ $? -ne 0 ]; then
    echo "Pipenv not found. Install it with sudo apt install pipenv."
    exit 1
fi

tmux -V
if [ $? -ne 0 ]; then
    echo "tmux not found. Try running apt install tmux to install it."
    exit 1
fi

chmod +x ./setup.sh
chmod +x ./run_scrapers.sh