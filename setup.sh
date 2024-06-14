#!/usr/bin/env bash

pipenv install

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