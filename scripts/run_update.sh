#! /usr/bin/env bash

# Get to git repo root directory from the directory of this script
cd $(dirname $0)/..

# Get the latest version locally
git checkout master
git pull

# Create branch for the update using data to differentiate
git checkout -b "$(date -I)-ga-data"

export DATA_DIR="${PWD}/_data"

# Create a virtual environment to run our script in to prevent any package version conflicts
scripts/updates.sh

# Push our changes up to github and clean up local branch
git add .
git commit -m "$(date -I) automated GA data pull"
git push -u origin HEAD
git checkout master
git branch -d "$(date -I)-ga-data"

GH_TOKEN=$( git config --get github.token )

# Open the pull request and store its number
ISSUE="$(curl -H "Authorization: token $GH_TOKEN" \
     --data "{
              \"title\": \"$(date -I) automated GA data pull\",
              \"body\": \"Daily GA data pull\",
              \"head\": \"$(date -I)-ga-data\",
              \"base\": \"master\"
            }" \
     https://api.github.com/repos/department-of-veterans-affairs/vets.gov-status/pulls \
     2> /dev/null | grep \"number\": | sed 's/^\W*number\W*\([0-9][0-9]*\)\W*/\1/')"

# Assign the pull request so its easier to find
curl -H "Authorization: token $GH_TOKEN" \
    --data "{
             \"assignee\": \"$(git config --get github.username)\"
           }" \
    -X PATCH \
    https://api.github.com/repos/department-of-veterans-affairs/vets.gov-status/issues/$ISSUE
