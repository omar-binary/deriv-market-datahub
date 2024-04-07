# deriv-market-datahub

## Prerequisites

A Google Cloud Platform account. If you do not have a [GCP account](https://console.cloud.google.com/cloud-resource-manager), create one now from [here](https://console.cloud.google.com/projectcreate).

- The gcloud CLI installed locally.
- Terraform 0.15.3+ installed locally.

## Setup

- run: `gcloud auth application-default login`
- Display the project IDs for your Google Cloud projects: `gcloud projects list`
- Using the applicable project ID from the previous step, set the default project to the one in which you want to enable the API: `gcloud config set project YOUR_PROJECT_ID`
- Display the project Number for your Google Cloud projects: `gcloud projects describe YOUR_PROJECT_ID`
- Open `terraform.tfvars` in your text editor, and paste in the configuration below. Be sure to replace <PROJECT_ID> with your project's ID, and <PROJECT_NUMBER> project with your project's Number then save the file.

- Enable Compute Engine API: `gcloud services enable compute.googleapis.com`
- Enable the Cloud Composer API: `gcloud services enable composer.googleapis.com`

- Run `terraform init` to initialize the Terraform configuration.
- Run `terraform plan` to view the resources that Terraform will create.
- Run `terraform apply` to create the resources.
- Run `terraform show` to view the resources that Terraform created.

- Once done run `terraform destroy` to delete the resources.



## Plan


filter on "market": "indices",

- active symbols and their last quote in a day
- get historical last 30 days quotes for a symbol -> store in table
- daily job to get yesterday last tick for all active symbols

- load data to GCS
- terraform GCS + service account + key
- terraform cloud composer
- dag to load data from GCS to BQ

- Call deriv API to load data into GCS [done]
- Spin up airflow using terraform
- Call this extraction from airflow
- Load data into BQ using airflow operator
- Create BQ schema
- Use DBT to create a model on top of BQ table
- Create a dashboard in data studio
