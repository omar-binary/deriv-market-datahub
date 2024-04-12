output "airflow_id" {
  value = google_composer_environment.airflow.id
}
output "airflow_uri" {
  value = google_composer_environment.airflow.config.0.airflow_uri
}
output "dag_gcs_bucket" {
  value = google_composer_environment.airflow.config.0.dag_gcs_prefix
}
output "airflow_service_account" {
  value = google_composer_environment.airflow.config.0.node_config.0.service_account
}
output "airflow_google_service_account" {
  value = google_service_account.airflow.email
}
output "market_data_bucket" {
  value = google_storage_bucket.market-data.url
}
