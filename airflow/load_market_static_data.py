import base64
import json
import os

from datetime import datetime, timedelta

from airflow import DAG
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator


default_args = {
    'owner': 'Composer',
    'depends_on_past': False,
    'start_date': datetime(2024, 4, 1),
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 5,
    'retry_delay': timedelta(minutes=10),
}

with DAG(
    dag_id='load_market_static_data',
    catchup=False,
    default_args=default_args,
    start_date=datetime(2024, 4, 1),
    # schedule_interval=timedelta(days=1),
    schedule='@daily',
    max_active_runs=1,
    dagrun_timeout=timedelta(minutes=120),
):

    extract_symbols = KubernetesPodOperator(
        namespace='composer-user-workloads',
        image='us-central1-docker.pkg.dev/vital-scout-418612/main/market_data_loader:latest',
        cmds=['poetry', 'run', 'python3', 'importer.py'],
        arguments=['--resource_name', 'symbols'],
        name='pod-extract-symbols',
        task_id='pod-extract-symbols',
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

    extract_assets = KubernetesPodOperator(
        namespace='composer-user-workloads',
        image='us-central1-docker.pkg.dev/vital-scout-418612/main/market_data_loader:latest',
        cmds=['poetry', 'run', 'python3', 'importer.py'],
        arguments=['--resource_name', 'assets'],
        name='pod-extract-assets',
        task_id='pod-extract-assets',
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

    extract_countries = KubernetesPodOperator(
        namespace='composer-user-workloads',
        image='us-central1-docker.pkg.dev/vital-scout-418612/main/market_data_loader:latest',
        cmds=['poetry', 'run', 'python3', 'importer.py'],
        arguments=['--resource_name', 'countries'],
        name='pod-extract-countries',
        task_id='pod-extract-countries',
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
