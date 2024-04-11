# deriv-market-datahub

## Prerequisites

A Google Cloud Platform account. If you do not have a [GCP account](https://console.cloud.google.com/cloud-resource-manager), create one now from [here](https://console.cloud.google.com/projectcreate).

- The gcloud CLI installed locally.
- Terraform 0.15.3+ installed locally.
- Docker installed locally.

## Setup

### Terraform

- run: `gcloud auth application-default login`
- Display the project IDs for your Google Cloud projects: `gcloud projects list`
- Using the applicable project ID from the previous step, set the default project to the one in which you want to enable the API: `gcloud config set project YOUR_PROJECT_ID`
- Display the project Number for your Google Cloud projects: `gcloud projects describe YOUR_PROJECT_ID`
- Open `terraform.tfvars` in your text editor, and paste in the configuration below. Be sure to replace <PROJECT_ID> with your project's ID, and <PROJECT_NUMBER> project with your project's Number then save the file.

- Enable Compute Engine API: `gcloud services enable compute.googleapis.com`
- Enable the Cloud Composer API: `gcloud services enable composer.googleapis.com`

- Go to the `terraform` directory: `cd terraform`
- Run `terraform init` to initialize the Terraform configuration.
- Run `terraform plan` to view the resources that Terraform will create.
- Run `terraform apply` to create the resources.
- Run `terraform show` to view the resources that Terraform created.

### Artifact Registry

```bash
$ gcloud auth configure-docker us-central1-docker.pkg.dev
# $ ./build_and_push.sh $TAG $REPOSITORY $PROJECT_ID $REGION
$ ./build_and_push.sh "latest" "main" "vital-scout-418612" "us-central1"
# docker pull us-central1-docker.pkg.dev/vital-scout-418612/main/market_data_loader:latest
```

### Airflow

- Upload the DAG to the Composer environment using the following command:

```bash
$ gcloud composer environments storage dags import \
--environment airflow-composer-env  --location us-central1 \
--source airflow/load_market_static_data.py

$ gcloud composer environments storage dags import \
--environment airflow-composer-env  --location us-central1 \
--source airflow/load_market_ticks_history_data.py

$ gcloud composer environments storage dags import \
--environment airflow-composer-env  --location us-central1 \
--source airflow/load_market_candles_history_data.py
```

## BQ

```sql
CREATE EXTERNAL TABLE `vital-scout-418612.staging.tick_ty3`
(
  style STRING,
  ticks_history STRING,
  price STRING,
  time NUMERIC,
  pip_size NUMERIC,
  _dlt_load_id STRING,
  _dlt_id STRING
)
OPTIONS(
  format="PARQUET",
  uris=["gs://staging-market-datahub/market_data/ticks_history/*"]
);
```

## Cleanup

- Once done run `terraform destroy` to delete the resources.
- Make sure to delete any remaining disks, as they are not automatically deleted by Terraform. [here](https://console.cloud.google.com/compute/disks)
- Make sure to delete Bucket created by Terraform. [here](https://console.cloud.google.com/storage/browser)
