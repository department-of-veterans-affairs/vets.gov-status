#!/usr/bin/env bash

# Create a virtual environment to run our script in to prevent any package version conflicts
python3 -m venv update_data

# move our scripts over into the venv
cp -r scripts/* update_data/

cd update_data

# Install requirements
bin/pip3 install wheel
bin/pip3 install -r requirements.txt

export PROMETHEUS_API_SITE=http://prometheus-prod.vetsgov-internal:9090/prometheus/api/v1
export PROMETHEUS_API_UTILITY=http://prometheus-utility.vetsgov-internal:9090/prometheus/api/v1

bin/python3 update_from_prometheus.py

mv *.yml ../_data

cd ..

# Clean up venv so git doesn't pick it up
rm -rf update_data
