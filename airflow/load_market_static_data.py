import base64
import json
import os

from datetime import datetime, timedelta

from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator


default_args = {
    'owner': 'Composer',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 1),
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=1),
}

dimensions_dictionary = {
    'symbols': [],
    'assets': [],
    'assets__value': [],
    'assets__value__list': [],
    'countries': [],
    'countries__tin_format': [],
}

with DAG(
    dag_id='load_market_static_data',
    catchup=False,
    default_args=default_args,
    start_date=datetime(2024, 4, 1),
    schedule='@daily',
    max_active_runs=1,
    dagrun_timeout=timedelta(minutes=120),
):
    for dimension, schema_fields in dimensions_dictionary.items():
        if '__' not in dimension:
            extract_dimension = KubernetesPodOperator(
                namespace='composer-user-workloads',
                image='us-central1-docker.pkg.dev/vital-scout-418612/main/market_data_loader:latest',
                cmds=['poetry', 'run', 'python3', 'importer.py'],
                arguments=['--resource_name', dimension],
                name=f'pod-extract-{dimension}',
                task_id=f'pod-extract-{dimension}',
                config_file='/home/airflow/composer_kube_config',
                env_vars={
                    'DESTINATION__FILESYSTEM__CREDENTIALS__PROJECT_ID': os.environ['GCP_PROJECT_ID'],
                    'DESTINATION__FILESYSTEM__CREDENTIALS__PRIVATE_KEY': json.loads(
                        base64.b64decode(os.environ['AIRFLOW_PRIVATE_KEY']).decode('utf-8'),
                    )['private_key'],
                    'DESTINATION__FILESYSTEM__CREDENTIALS__CLIENT_EMAIL': os.environ['AIRFLOW_CLIENT_EMAIL'],
                    'DESTINATION__FILESYSTEM__BUCKET_URL': os.environ['STAGING_BUCKET_URL'],
                },
                get_logs=True,
            )

        load_bq_from_data_lake = GCSToBigQueryOperator(
            task_id=f"gcs_to_bigquery_{dimension}",
            bucket='staging-market-datahub',
            source_objects=[f"market_data/{dimension}/*.parquet"],
            destination_project_dataset_table=f"staging.{dimension}",
            # schema_fields=schema_fields,
            source_format='PARQUET',
            write_disposition='WRITE_TRUNCATE',
            external_table=True,
            autodetect=True,
        )

        extract_dimension >> load_bq_from_data_lake
