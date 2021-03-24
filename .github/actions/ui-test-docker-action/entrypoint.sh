#!/usr/bin/env bash
set -e

cd github/workspace

make yarn-install
make ci-ui-test