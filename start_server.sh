#!/bin/sh
uwsgi --socket 0.0.0.0:5000 --protocol=http --uid 1000 --gid 1000 --chdir /home/code/flask_leaderboard -w wsgi:app --enable-threads