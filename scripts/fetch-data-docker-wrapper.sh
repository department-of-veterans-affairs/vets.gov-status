#!/usr/bin/env bash
set -o errexit
set -o nounset
# set -x

# Build the image for testing
docker build -t dashboard-fetch-img .

current_time=$(date "+%Y.%m.%d-%H.%M.%S")
container_name=dashboard-fetch-container-${current_time}

echo "Fetching data via docker image"
if [ -n "${CI:-}" ]; then
  docker run --name ${container_name} --tmpfs /var/tmp --env GA_SERVICEACCOUNT --env CI --env INTEGRATION_TEST dashboard-fetch-img
else
  # We want to override GA_SERVICE account credentials location if not running in CI
  export GA_SERVICEACCOUNT_FILE="local_credentials/ga-serviceaccount.json"
  docker run --name ${container_name} --tmpfs /var/tmp --env GA_SERVICEACCOUNT_FILE --env FORESEE_CREDENTIALS --env INTEGRATION_TEST dashboard-fetch-img
fi

docker cp ${container_name}:/application/data/. ../src/_data
docker rm ${container_name}
echo "Done fetching data"
