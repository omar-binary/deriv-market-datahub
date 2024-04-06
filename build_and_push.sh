#!/bin/bash
set -e

TAG="${1:-latest}"
docker build -t gcr.io/GCP_PROJECT/IMAGE:$TAG .
docker push gcr.io/GCP_PROJECT/IMAGE:$TAG
