#!/bin/bash
set -e

TAG="${1:-latest}"
REPOSITORY="${2:-main}"
GCP_PROJECT="${3}"
GCP_REGION="${4:-us-central1}"

docker build -t $GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$REPOSITORY/market_data_loader:$TAG .
docker push $GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$REPOSITORY/market_data_loader:$TAG
