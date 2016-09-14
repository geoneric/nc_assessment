#!/usr/bin/env bash
set -e


if [ "$ENV" = "DEVELOPMENT" ]; then
    exec python run_server.py
else
    exec uwsgi uwsgi.ini
fi
