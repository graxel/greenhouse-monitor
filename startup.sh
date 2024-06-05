#!/usr/bin/env bash

pipenv install

pipenv run python 00_db_setup.py
if [ $? -ne 0 ]; then
    echo "00_db_setup.py failed. Exiting."
    exit 1
fi

pipenv run python 01_update_company_names.py
if [ $? -ne 0 ]; then
    echo "01_update_company_names.py failed. Exiting."
    exit 1
fi

pipenv run python 02_update_job_sites.py
if [ $? -ne 0 ]; then
    echo "02_update_job_sites.py failed. Exiting."
    exit 1
fi

pipenv run python 03_company_crawler.py
if [ $? -ne 0 ]; then
    echo "03_company_crawler.py failed. Exiting."
    exit 1
fi

pipenv run python 04_gather_companies_for_review.py
if [ $? -ne 0 ]; then
    echo "04_gather_companies_for_review.py failed. Exiting."
    exit 1
fi

pipenv run python 05_update_companies_list.py
if [ $? -ne 0 ]; then
    echo "05_update_companies_list.py failed. Exiting."
    exit 1
fi

echo "Initial setup complete. Starting a tmux session."

tmux new-session -d -s fil

tmux split-window -v
tmux select-pane -t 0
tmux split-window -h
tmux select-pane -t 2
tmux split-window -h

tmux select-pane -t 0
tmux send-keys 'pipenv run python 06_scrape_company_page.py' C-m

tmux select-pane -t 2
tmux send-keys 'pipenv run python 07_parse_listings.py' C-m

tmux select-pane -t 1
tmux send-keys 'pipenv run python 08_scrape_job_page.py' C-m

tmux select-pane -t 3
tmux send-keys 'pipenv run python 09_parse_job_page.py' C-m

tmux attach -t fil