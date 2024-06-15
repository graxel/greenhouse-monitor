#!/usr/bin/env bash


tmux has-session -t fil 2>/dev/null

if [ $? -ne 0 ]; then
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
fi

tmux attach -t fil