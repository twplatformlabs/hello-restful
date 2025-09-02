#!/usr/bin/env bash
set -eo pipefail

env=$1
tag=$2

echo "deploy hello-restful:$tag to demo-$env"
helm upgrade hello-restful charts/hello-restful \
      --install --atomic --timeout 120s \
      --namespace "demo-$env" \
      --values "charts/hello-restful/values.yaml" \
      --values "charts/hello-restful/values-$env.yaml" \
      --set image.tag="$tag"


# helm template hello-restful charts/hello-restful \
#       --namespace "demo-$env" \
#       --values "charts/hello-restful/values.yaml" \
#       --values "charts/hello-restful/values-dev.yaml" \
#       --set image.tag="$tag"