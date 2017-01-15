#!/usr/bin/env bash
set -e


docker build -t test/nc_assessment .
docker run -p9090:9090 test/nc_assessment
