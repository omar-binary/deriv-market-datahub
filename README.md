# deriv-market-datahub

- [deriv-market-datahub](#deriv-market-datahub)
  - [Problem description](#problem-description)
  - [Solution](#solution)
  - [Prerequisites](#prerequisites)
  - [Architecture](#architecture)
  - [Setup](#setup)
    - [Terraform](#terraform)
    - [Composer Note](#composer-note)
  - [Cleanup](#cleanup)

## Problem description

We would like to analyze the market data for indices and track daily market changes.

We will leverage the [Deriv API](https://api.deriv.com/) to retrieve the necessary market data. The Deriv API provides a way to fetch market data for indices and various other assets. Refer to the API documentation [here](https://api.deriv.com/api-explorer) for more details.

Data of Interest:

- Dimensions: **Symbol**, **Country**, **Asset**
- **Closing tick** Our primary interest is capturing closing tick data for a select group of actively traded symbols, which will be stored in BigQuery.
- **Daily candle** data for the past 30 days for each symbol.

## Solution

- The plan is to extract market data, store it in BigQuery for further analysis, and create a dashboard in Data Studio.
- To start, we will create a data pipeline that fetches the last tick for some active symbols and stores them in [GCS](https://cloud.google.com/storage?hl=en) (which will act as our data lake). We also plan to store the historical data for the last 30 days for each symbol, then load it into our data warehouse, BigQuery.
- This data pipeline will be created using Google Cloud Composer, a fully managed workflow orchestration service that empowers you to author, schedule, and monitor pipelines that span across clouds and on-premises data centers.
- Next, we'll model our data using [dbt](https://www.getdbt.com/), a command-line tool that allows data analysts and engineers to effectively transform data in their warehouses.
- Finally, we will create a dashboard in Data Studio to visualize the data.
- **Check the dashboard [here](https://lookerstudio.google.com/u/0/reporting/f8385142-a03e-4f74-8bad-37ddc1cf4cc1/page/tEnnC)** 📈📊.


## Prerequisites

A Google Cloud Platform account. If you do not have a [GCP account](https://console.cloud.google.com/cloud-resource-manager), create one now from [here](https://console.cloud.google.com/projectcreate).

- The [gcloud CLI](https://cloud.google.com/sdk/docs/install) installed locally.
- [Terraform](https://developer.hashicorp.com/terraform/install) 0.15.3+ installed locally.
- [Docker](https://www.docker.com/products/docker-desktop/) installed locally.

## Architecture

[Check the full architecture here](Architecture.md)

## Setup

### Terraform

- run: `gcloud auth application-default login`
- Display the project IDs for your Google Cloud projects: `gcloud projects list`
- Using the applicable project ID from the previous step, set the default project to the one in which you want to enable the API: `gcloud config set project YOUR_PROJECT_ID`
- Display the project Number for your Google Cloud projects: `gcloud projects describe YOUR_PROJECT_ID`
- Open `terraform/terraform.tfvars` in your text editor, and paste in the configuration below. Be sure to replace <PROJECT_ID> with your project's ID, and <PROJECT_NUMBER> project with your project's Number then save the file.

- Open `terraform/variables.tf` in your text editor, replace <market_data_bucket> default value with your selected name then save the file. (as bucket names should be unique across all GCP projects)

- Enable Compute Engine API: `gcloud services enable compute.googleapis.com`
- Enable the Cloud Composer API: `gcloud services enable composer.googleapis.com`

- Go to the `terraform` directory: `cd terraform`
- Run `terraform init` to initialize the Terraform configuration.
- Run `terraform plan` to view the resources that Terraform will create.
- Run `terraform apply -auto-approve` to create the resources.
- Run `terraform show` to view the resources that Terraform created.

### Composer Note

Due to Quotas limit on the size of environments and amount of workers, you may need to run the dags in batches by enabling them one by one.
Avoid running all the dags at once, as it may exceed the worker quota limit and cause the worker environment to fail.

## Cleanup

- Once done run `terraform destroy` to delete the resources.
- Make sure to delete any remaining disks, as they are not automatically deleted by Terraform. [here](https://console.cloud.google.com/compute/disks)
- Make sure to delete the Bucket created by Terraform. [here](https://console.cloud.google.com/storage/browser)
