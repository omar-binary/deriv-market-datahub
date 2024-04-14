#!/bin/bash
set -e

TAG="${1:-latest}"
REPOSITORY="${2:-main}"
GCP_PROJECT="${3}"
GCP_REGION="${4:-us-central1}"

# data ingestion image
docker build -t $GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$REPOSITORY/market_data_loader:$TAG .

docker push $GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$REPOSITORY/market_data_loader:$TAG

# dbt image
docker build -t $GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$REPOSITORY/dbt_builder:$TAG ./dbt

docker push $GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$REPOSITORY/dbt_builder:$TAG
