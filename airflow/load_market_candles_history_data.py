import base64
import json
import os

from datetime import datetime, timedelta

from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator


default_args = {
    'owner': 'Composer',
    'depends_on_past': True,
    'start_date': datetime(2024, 4, 1),
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=10),
}

symbols_list = ['R_50', 'OTC_NDX', 'OTC_DJI', 'cryBTCUSD']

with DAG(
    dag_id='load_market_candles_history_data',
    catchup=True,
    default_args=default_args,
    start_date=datetime(2024, 4, 1),
    # schedule_interval=timedelta(days=1),
    schedule='@daily',
    max_active_runs=1,
    dagrun_timeout=timedelta(minutes=120),
):
    for symbol in symbols_list:
        extract_candles_history = KubernetesPodOperator(
            namespace='composer-user-workloads',
            image='us-central1-docker.pkg.dev/vital-scout-418612/main/market_data_loader:latest',
            cmds=['poetry', 'run', 'python3', 'importer.py'],
            arguments=[
                '--resource_name',
                'candles_history',
                '--symbol',
                symbol,
                '--start',
                '{{ prev_execution_date.int_timestamp }}',
                '--end',
                '{{ execution_date.int_timestamp }}',
            ],
            name=f'pod-extract-{symbol}-candles-history',
            task_id=f'pod-extract-{symbol}-candles-history',
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
