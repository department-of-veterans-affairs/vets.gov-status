#!/usr/bin/env bash
set -o errexit
#set -o nounset
# set -x

if [ -z "${INTEGRATION_TEST:-}" ]; then
  echo Running Google Analytics scripts...
  python -m fetch_data
  echo Modifying Last Updated date...
  current_date=$(date "+%B %d, %Y")
  current_time=$(date "+%I:%m %p %Z")
  echo "date: $current_date" > data/last_updated.yml
  echo "time: $current_time" >> data/last_updated.yml
else
  echo Running integration test...
  python -m test.fetch_data_integration_test
fi
