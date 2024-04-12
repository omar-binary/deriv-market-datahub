#!/bin/bash
set -e

TAG="${1:-latest}"
REPOSITORY="${2:-main}"
GCP_PROJECT="${3}"
GCP_REGION="${4:-us-central1}"
COMPOSER_NAME="${5}"

# change to root dicrectory
cd ..

# Setup Artifact Registry
gcloud auth configure-docker $GCP_REGION-docker.pkg.dev

# build and push docker image
./build_and_push.sh $TAG $REPOSITORY $GCP_PROJECT $GCP_REGION

# Setup Cloud Composer Dags
gcloud composer environments storage dags import \
--environment $COMPOSER_NAME  --location $GCP_REGION \
--source airflow/load_market_static_data.py && echo 'load_market_static_data loaded'

gcloud composer environments storage dags import \
--environment $COMPOSER_NAME  --location $GCP_REGION \
--source airflow/load_market_ticks_history_data.py && echo 'load_market_ticks_history_data loaded'

gcloud composer environments storage dags import \
--environment $COMPOSER_NAME  --location $GCP_REGION \
--source airflow/load_market_candles_history_data.py && echo 'load_market_candles_history_data loaded'
