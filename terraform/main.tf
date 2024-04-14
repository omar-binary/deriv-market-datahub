terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.23.0"
    }
  }
}

provider "google" {
  project = var.project_id
  # For simplicity, we are using the default user credentials.
  # credentials = file(var.credentials_file)
  region = var.region
  zone   = var.zone
}

# Artifact Registry
resource "google_artifact_registry_repository" "main" {
  location               = var.region
  repository_id          = var.artifact_registry_repository
  description            = "docker repository"
  format                 = "DOCKER"
  cleanup_policy_dry_run = false
  cleanup_policies {
    id     = "delete-prerelease"
    action = "DELETE"
    condition {
      tag_state  = "ANY"
      older_than = "86400s"
    }
  }
  cleanup_policies {
    id     = "keep-minimum-versions"
    action = "KEEP"
    most_recent_versions {
      keep_count = 2
    }
  }
}

# Dlt staging datalake bucket
resource "google_storage_bucket" "market-data" {
  name                        = var.market_data_bucket
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
}

# BigQuery
resource "google_bigquery_dataset" "staging" {
  dataset_id    = var.bigquery_dataset_id
  friendly_name = var.bigquery_dataset_id
  description   = "staging dataset for first layer of data processing"
  location      = var.location
  labels = {
    env = "default"
  }
  delete_contents_on_destroy = true
}

# Airflow Composer
resource "google_project_service" "composer_api" {
  project            = var.project_id
  service            = "composer.googleapis.com"
  disable_on_destroy = false
}

resource "google_compute_network" "airflow" {
  name                    = "airflow-composer-network"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "airflow" {
  name          = "airflow-composer-subnetwork"
  ip_cidr_range = var.airflow_ip_cidr_range
  region        = var.region
  network       = google_compute_network.airflow.id
}

resource "google_service_account" "airflow" {
  account_id   = var.airflow_service_account
  display_name = "Service Account for Airflow Composer Environment"
}

resource "google_service_account_key" "airflow" {
  service_account_id = google_service_account.airflow.name
  public_key_type    = "TYPE_X509_PEM_FILE"
}

resource "google_project_iam_member" "airflow_composer" {
  project = var.project_id
  role    = "roles/composer.worker"
  member  = "serviceAccount:${google_service_account.airflow.email}"
}

resource "google_project_iam_member" "airflow_logging" {
  project = var.project_id
  role    = "roles/logging.admin"
  member  = "serviceAccount:${google_service_account.airflow.email}"
}

resource "google_project_iam_member" "airflow_storage" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.airflow.email}"
}

resource "google_project_iam_member" "airflow_bigquery" {
  project = var.project_id
  role    = "roles/bigquery.admin"
  member  = "serviceAccount:${google_service_account.airflow.email}"
}

resource "google_project_iam_member" "airflow_artifactregistry" {
  project = var.project_id
  role    = "roles/artifactregistry.admin"
  member  = "serviceAccount:${google_service_account.airflow.email}"
}

resource "google_service_account_iam_member" "airflow_service_agent" {
  service_account_id = google_service_account.airflow.name
  role               = "roles/composer.ServiceAgentV2Ext"
  member             = "serviceAccount:service-${var.project_number}@cloudcomposer-accounts.iam.gserviceaccount.com"
}

resource "google_composer_environment" "airflow" {
  depends_on = [google_service_account_iam_member.airflow_service_agent]
  name       = var.airflow_name
  region     = var.region
  config {
    software_config {
      image_version = "composer-2-airflow-2"
      airflow_config_overrides = {
        # core-dags_are_paused_at_creation = "True",
        scheduler-dag_dir_list_interval = 60
      }

      pypi_packages = {
        apache-airflow-providers-docker = ""
        apache-airflow-providers-google = ""

      }

      env_variables = {
        GCP_PROJECT_ID       = var.project_id
        GCP_REGION           = var.region
        AIRFLOW_PRIVATE_KEY  = google_service_account_key.airflow.private_key
        AIRFLOW_CLIENT_EMAIL = google_service_account.airflow.email
        STAGING_BUCKET_URL   = "gs://${google_storage_bucket.market-data.name}"
        STAGING_BUCKET       = var.market_data_bucket
      }
    }
    workloads_config {
      scheduler {
        cpu        = 0.5
        memory_gb  = 1.875
        storage_gb = 1
        count      = 1
      }
      web_server {
        cpu        = 0.5
        memory_gb  = 1.875
        storage_gb = 1
      }
      worker {
        cpu        = 0.5
        memory_gb  = 1.875
        storage_gb = 1
        min_count  = 1
        max_count  = 3
      }

    }
    environment_size = "ENVIRONMENT_SIZE_SMALL"

    node_config {
      network         = google_compute_network.airflow.id
      subnetwork      = google_compute_subnetwork.airflow.id
      service_account = google_service_account.airflow.name
    }
  }
}

# run local-exec after the resource is created
resource "null_resource" "post-setup" {
  depends_on = [google_composer_environment.airflow, google_bigquery_dataset.staging, google_artifact_registry_repository.main]
  provisioner "local-exec" {
    command = "/bin/bash post-setup.sh 'latest' '${var.artifact_registry_repository}' '${var.project_id}' '${var.region}' '${var.airflow_name}'"
  }
}
