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
    'retry_delay': timedelta(minutes=1),
}
# TODO: update it to be triggered from the other dag
with DAG(
    dag_id='dbt_create_model',
    catchup=False,
    default_args=default_args,
    start_date=datetime(2024, 4, 1),
    schedule=None,  # Triggered by load dag
    max_active_runs=1,
    dagrun_timeout=timedelta(minutes=120),
):
    dbt_run = KubernetesPodOperator(
        namespace='composer-user-workloads',
        image=f'{os.environ["GCP_REGION"]}-docker.pkg.dev/{os.environ["GCP_PROJECT_ID"]}/main/dbt_builder:latest',
        cmds=['dbt', 'run'],
        # arguments=['--resource_name', dimension],
        name='dbt_test',
        task_id='dbt_test',
        config_file='/home/airflow/composer_kube_config',
        env_vars={
            'BIGQUERY_TYPE': json.loads(base64.b64decode(os.environ['AIRFLOW_PRIVATE_KEY']).decode('utf-8'))['type'],
            'GCP_PROJECT_ID': os.environ['GCP_PROJECT_ID'],
            'BIGQUERY_PRIVATE_KEY_ID': json.loads(base64.b64decode(os.environ['AIRFLOW_PRIVATE_KEY']).decode('utf-8'))[
                'private_key_id'
            ],
            'BIGQUERY_PRIVATE_KEY': json.loads(base64.b64decode(os.environ['AIRFLOW_PRIVATE_KEY']).decode('utf-8'))[
                'private_key'
            ],
            'BIGQUERY_CLIENT_EMAIL': json.loads(base64.b64decode(os.environ['AIRFLOW_PRIVATE_KEY']).decode('utf-8'))[
                'client_email'
            ],
            'BIGQUERY_CLIENT_ID': json.loads(base64.b64decode(os.environ['AIRFLOW_PRIVATE_KEY']).decode('utf-8'))[
                'client_id'
            ],
            'BIGQUERY_AUTH_URI': json.loads(base64.b64decode(os.environ['AIRFLOW_PRIVATE_KEY']).decode('utf-8'))[
                'auth_uri'
            ],
            'BIGQUERY_TOKEN_URI': json.loads(base64.b64decode(os.environ['AIRFLOW_PRIVATE_KEY']).decode('utf-8'))[
                'token_uri'
            ],
            'BIGQUERY_AUTH_PROVIDER_X509_CERT_URL': json.loads(
                base64.b64decode(os.environ['AIRFLOW_PRIVATE_KEY']).decode('utf-8'),
            )['auth_provider_x509_cert_url'],
            'BIGQUERY_CLIENT_X509_CERT_URL': json.loads(
                base64.b64decode(os.environ['AIRFLOW_PRIVATE_KEY']).decode('utf-8'),
            )['client_x509_cert_url'],
        },
        get_logs=True,
    )
