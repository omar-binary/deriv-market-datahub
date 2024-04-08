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
  ip_cidr_range = "10.2.0.0/16"
  region        = var.region
  network       = google_compute_network.airflow.id
}

resource "google_service_account" "airflow" {
  account_id   = "airflow-composer-sa"
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

resource "google_service_account_iam_member" "airflow_service_agent" {
  service_account_id = google_service_account.airflow.name
  role               = "roles/composer.ServiceAgentV2Ext"
  member             = "serviceAccount:service-${var.project_number}@cloudcomposer-accounts.iam.gserviceaccount.com"
}

resource "google_composer_environment" "airflow" {
  name   = "airflow-composer-env"
  region = var.region
  config {
    software_config {
      image_version = "composer-2-airflow-2"
      airflow_config_overrides = {
        core-dags_are_paused_at_creation = "True"
      }

      pypi_packages = {
      }

      env_variables = {
        PROJECT_ID           = var.project_id
        AIRFLOW_PRIVATE_KEY  = google_service_account_key.airflow.private_key
        AIRFLOW_CLIENT_EMAIL = google_service_account.airflow.email
        STAGING_BUCKET_URL   = "gs://${google_storage_bucket.market-data.name}"
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


# Dlt loader
resource "google_service_account" "dlt" {
  account_id   = "dlt-loader"
  display_name = "Service Account for DLT to load data into GCP"
}

resource "google_project_iam_member" "dlt_bigquery" {
  project = var.project_id
  role    = "roles/bigquery.admin"
  member  = "serviceAccount:${google_service_account.dlt.email}"
}

resource "google_project_iam_member" "dlt_storage" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.dlt.email}"
}

resource "google_storage_bucket" "market-data" {
  name                        = "staging-market-datahub"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
}

# Artifact Registry
resource "google_artifact_registry_repository" "main" {
  location               = "us-central1"
  repository_id          = "main"
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
