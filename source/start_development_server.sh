#!/usr/bin/env bash
set -e


docker build -t test/assessment .
docker run --env ENV=DEVELOPMENT -p5000:5000 -v$(pwd)/assessment:/assessment test/assessment
