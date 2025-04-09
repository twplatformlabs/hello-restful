#!/usr/bin/env bash
set -eo pipefail

env=$1
tag=$2
url="https://twplatformlabs.org/v1/hello/healthz"

if [[ "$env" != "prod" ]];  then
  url="https://$env.twplatformlabs.org/v1/hello/healthz"
else
  url="https://api.twplatformlabs.org/v1/hello/healthz"
fi

echo "test $url for version=$tag"
reponse=$(curl "$url")
version=$(echo "$reponse" | jq -r .version)
echo "reported version $version"

if [[ "$version" != "$tag" ]]; then
    echo "error: healthz not ok"
    exit 1
fi
