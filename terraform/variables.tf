variable "project_id" {}

variable "project_number" {}

# variable "credentials_file" {}

variable "location" {
  default = "US"
}
variable "region" {
  default = "us-central1"
}

variable "zone" {
  default = "us-central1-c"
}

variable "market_data_bucket" {
  default     = "staging-market-datahub-01" # make sure to change this, to avoid conflicts
  description = "Data Lake bucket of market data"
}

variable "artifact_registry_repository" {
  default = "main"
}

variable "airflow_name" {
  default = "airflow-composer"
}
variable "airflow_service_account" {
  default = "airflow-composer-sa"
}

variable "airflow_ip_cidr_range" {
  default = "10.2.0.0/16"
}

variable "bigquery_dataset_id" {
  default = "staging"
}
