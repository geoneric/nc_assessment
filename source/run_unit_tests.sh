#!/usr/bin/env bash
set -e


docker build -t test/nc_assessment .
docker run --env ENV=TEST -p5000:5000 test/nc_assessment