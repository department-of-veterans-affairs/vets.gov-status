#!/usr/bin/env bash

# Note - not doing a `set -e` because we don't want the script to exit without displaying test failures

export PYTHONWARNINGS="ignore::DeprecationWarning:numpy"

command="python -m pytest --cov \
  --cov-report term --cov-report html"

echo "$command"
eval "$command"

echo
echo Flake8 comments:
flake8 --max-line-length=120 scripts