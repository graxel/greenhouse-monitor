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

echo "All dependencies are installed."

echo "Creating virtual environment and installing Python packages:"
pipenv install
echo "Done."

echo "Creating database and updating companies table:"

pipenv run python 00_db_setup.py
if [ $? -ne 0 ]; then
    echo "00_db_setup.py failed. Exiting."
    exit 1
fi
 
pipenv run python 05_update_companies_list.py
if [ $? -ne 0 ]; then
    echo "05_update_companies_list.py failed. Exiting."
    exit 1
fi
echo "Done."