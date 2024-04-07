import datetime

from airflow import DAG
from airflow.operators import bash
from airflow.operators.empty import EmptyOperator


# If you are running Airflow in more than one time zone
# see https://airflow.apache.org/docs/apache-airflow/stable/timezone.html
# for best practices
YESTERDAY = datetime.datetime.now() - datetime.timedelta(days=1)

default_args = {
    'owner': 'Composer',
    'depends_on_past': False,
    'email': [''],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': datetime.timedelta(minutes=5),
    'start_date': YESTERDAY,
}

with DAG(
    dag_id='load_market_data',
    catchup=False,
    default_args=default_args,
    start_date=datetime.datetime(2024, 4, 1),
    # schedule_interval=datetime.timedelta(days=1),
    schedule='@daily',
):

    # Print the dag_run id from the Airflow logs
    print_dag_run_conf = bash.BashOperator(
        task_id='print_dag_run_conf',
        bash_command='echo {{ dag_run.id }}',
    )

    EmptyOperator(task_id='task')
