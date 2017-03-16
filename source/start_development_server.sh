#!/usr/bin/env bash
set -e


docker build -t test/nc_assessment .
docker run \
    --env NC_CONFIGURATION=development \
    -p5000:5000 \
    -v$(pwd)/nc_assessment:/nc_assessment \
    test/nc_assessment
