import base64
import json
import os

from datetime import datetime, timedelta

from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator


default_args = {
    'owner': 'Composer',
    'depends_on_past': True,
    'start_date': datetime(2024, 4, 1),
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=1),
}

symbols_list = ['R_50', 'OTC_NDX', 'OTC_DJI', 'cryBTCUSD']

with DAG(
    dag_id='load_market_ticks_history_data',
    catchup=True,
    default_args=default_args,
    start_date=datetime(2024, 4, 1),
    # schedule_interval=timedelta(days=1),
    schedule='@daily',
    max_active_runs=1,
    dagrun_timeout=timedelta(minutes=120),
):
    for symbol in symbols_list:
        extract_ticks_history = KubernetesPodOperator(
            namespace='composer-user-workloads',
            image=f'{os.environ["GCP_REGION"]}-docker.pkg.dev/{os.environ["GCP_PROJECT_ID"]}/main/market_data_loader:latest',
            cmds=['poetry', 'run', 'python3', 'importer.py'],
            arguments=[
                '--resource_name',
                'ticks_history',
                '--symbol',
                symbol,
                '--start',
                '{{ prev_execution_date.int_timestamp }}',
                '--end',
                '{{ execution_date.int_timestamp }}',
            ],
            name=f'pod-extract-{symbol}-ticks-history',
            task_id=f'pod-extract-{symbol}-ticks-history',
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
            task_id=f"gcs_to_bigquery_{symbol}",
            bucket=os.environ['STAGING_BUCKET'],
            source_objects=['market_data/ticks_history/*.parquet'],
            destination_project_dataset_table='staging.ticks_history',
            # schema_fields=schema_fields,
            source_format='PARQUET',
            write_disposition='WRITE_TRUNCATE',
            external_table=True,
            autodetect=True,
        )

        extract_ticks_history >> load_bq_from_data_lake
