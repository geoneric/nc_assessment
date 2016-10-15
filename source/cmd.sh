#!/usr/bin/env bash
set -e


if [ "$ENV" = "DEVELOPMENT" ]; then
    exec python run_server.py
elif [ "$ENV" = "TEST" ]; then
    exec python test.py
else
    exec uwsgi uwsgi.ini
fi
