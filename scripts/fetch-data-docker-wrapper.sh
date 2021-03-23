#!/usr/bin/env bash
set -o errexit
set -o nounset
# set -x

# Build the image for testing
docker build -t dashboard-fetch-img .

current_time=$(date "+%Y.%m.%d-%H.%M.%S")
container_name=dashboard-fetch-container-${current_time}

echo "Fetching data via docker image"
if [ -z "${CI:-}" ]; then
  source local_credentials/.secrets
fi

docker run --name ${container_name} \
  --env GA_SERVICEACCOUNT \
  --env FORESEE_CREDENTIALS \
  --env INTEGRATION_TEST \
  dashboard-fetch-img

docker cp ${container_name}:/application/data/. ../src/_data
docker rm ${container_name}
echo "Done fetching data"
