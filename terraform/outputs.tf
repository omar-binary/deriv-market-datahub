output "airflow_id" {
  value = google_composer_environment.airflow.id
}

output "airflow_uri" {
  value = google_composer_environment.airflow.config.0.airflow_uri
}

output "dag_gcs_prefix" {
  value = google_composer_environment.airflow.config.0.dag_gcs_prefix
}

output "environment_size" {
  value = google_composer_environment.airflow.config.0.environment_size
}

output "node_count" {
  value = google_composer_environment.airflow.config.0.node_count
}

output "python_version" {
  value = google_composer_environment.airflow.config.0.software_config.0.python_version
}

output "scheduler_count" {
  value = google_composer_environment.airflow.config.0.software_config.0.scheduler_count
}
