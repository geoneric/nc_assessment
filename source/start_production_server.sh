#!/usr/bin/env bash
set -e


docker build -t test/assessment .
docker run -p9090:9090 test/assessment
