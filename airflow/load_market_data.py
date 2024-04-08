import base64

from datetime import datetime, timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.operators import bash
from airflow.operators.empty import EmptyOperator
from airflow.providers.docker.operators.docker import DockerOperator


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
    dag_id='load_market_data',
    catchup=True,
    default_args=default_args,
    start_date=datetime.datetime(2024, 4, 1),
    # schedule_interval=datetime.timedelta(days=1),
    schedule='@daily',
    max_active_runs=1,
    dagrun_timeout=timedelta(minutes=120),
):

    # Print the dag_run id from the Airflow logs
    print_dag_run_conf = bash.BashOperator(
        task_id='print_dag_run_conf',
        bash_command='echo {{ dag_run.id }}',
    )

    EmptyOperator(task_id='task')

    t1 = DockerOperator(
        task_id='load_market_data',
        image='us-central1-docker.pkg.dev/vital-scout-418612/main/market_data_loader:latest',
        docker_conn_id='gcr',  # setup connection in Airflow UI
        api_version='auto',
        auto_remove=True,
        tty=True,
        do_xcom_push=False,
        force_pull=True,
        mount_tmp_dir=False,
        private_environment={
            'DESTINATION__FILESYSTEM__CREDENTIALS__PROJECT_ID': Variable.get('PROJECT_ID'),
            'DESTINATION__FILESYSTEM__CREDENTIALS__PRIVATE_KEY': base64.b64decode(Variable.get('AIRFLOW_PRIVATE_KEY')),
            'DESTINATION__FILESYSTEM__CREDENTIALS__CLIENT_EMAIL': Variable.get('AIRFLOW_CLIENT_EMAIL'),
            'DESTINATION__FILESYSTEM__BUCKET_URL': Variable.get('STAGING_BUCKET_URL'),
        },
        command="""/bin/bash -c 'poetry run python3 importer.py \
            --resource_name symbols""",
        docker_url='unix://var/run/docker.sock',
    )
