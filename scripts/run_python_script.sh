#!/usr/bin/env bash

# Create a virtual environment to run our script in to prevent any package version conflicts
python3 -m venv update_data

# move our scripts over into the venv
cp -r scripts/* update_data/

cd update_data

# Install requirements
bin/pip3 install wheel
bin/pip3 install -r requirements.txt

bin/python3 update_data.py
bin/python3 update_vcl_clicks.py
bin/python3 update_filtered_views.py
bin/python3 weekly_account_rollup.py
mv *.csv ../_data

cd ..

# Clean up venv so git doesn't pick it up
rm -rf update_data
