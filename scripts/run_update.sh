#! /usr/bin/env bash

# Create branch for the update using data to differentiate
git checkout -b "$(date -I)-ga-data"

# Create a virtual environment to run our script in to prevent any package version conflicts
scripts/run_python_script.sh

# Push our changes up to github and clean up local branch
git add .
git commit -m "$(date -I) automated GA data pull"
#git push -u origin HEAD
git checkout master
git branch -D "$(date -I)-ga-data"
