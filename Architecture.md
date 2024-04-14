# Architecture

- [Architecture](#architecture)
  - [Tools and Technologies](#tools-and-technologies)
  - [Architecture](#architecture-1)
  - [Demo](#demo)
    - [Terraform](#terraform)
    - [Artifacts Registry (Docker Image)](#artifacts-registry-docker-image)
    - [Airflow (Google Cloud Composer)](#airflow-google-cloud-composer)
    - [Data Lake](#data-lake)
    - [Google BigQuery (BQ)](#google-bigquery-bq)
    - [Google Looker Studio](#google-looker-studio)

## Tools and Technologies

1- Cloud Services

- Google Cloud Platform (GCP)
- Terraform (IaC)
- `local-exec` provisioner (for running local scripts to fully automate the setup)

2- Data Extraction and Ingestion:

- WebSocket API
- Deriv API
- Artifacts Registry (Docker Image)
- DLT (Data Load Tool)

3- Data Lake:

- Google Cloud Storage (GCS)

4- Data Warehousing:

- Google BigQuery (BQ)

5- Data Transformations and Processing:

- Airflow (Google Cloud Composer)

6- Orchestration and Automation:

- Airflow (Google Cloud Composer)
- KubernetesPodOperator
- GCSToBigQueryOperator

7- Dashboard and Visualization:

- Google Looker Studio
- Check the dashboard [here](https://lookerstudio.google.com/u/0/reporting/f8385142-a03e-4f74-8bad-37ddc1cf4cc1/page/tEnnC).

## Architecture

TODO: add Architecture diagram

## Demo

### Terraform

![terraform_run](images/terraform_run.png)
![terraform_local_run](images/terraform_local_run.png)

### Artifacts Registry (Docker Image)

![artifacts_registry](images/artifacts_registry.png)

### Airflow (Google Cloud Composer)

![airflow_composer](images/airflow_dags.png)
![dag_dependencies](images/dag_dependencies.png)
![historical_dag_example](images/historical_dag_example.png)
![static_dag_example](images/static_dag_example.png)
![historical_ticks_dag_example](images/historical_ticks_dag_example.png)

### Data Lake

![staging_bucket](images/staging_bucket.png)

### Google BigQuery (BQ)

![BQ_tables](images/BQ_tables.png)

### Google Looker Studio

Check the dashboard [here](https://lookerstudio.google.com/u/0/reporting/f8385142-a03e-4f74-8bad-37ddc1cf4cc1/page/tEnnC).
