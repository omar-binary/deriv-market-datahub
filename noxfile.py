import os

from shutil import rmtree

import nox


@nox.session(python=['3.8'])
@nox.parametrize('python', ['3.8'])
@nox.parametrize('airflow', ['2.2.2'])
@nox.parametrize(
    'airflow_extra',
    ['amazon,async,datadog,docker,google,password,postgres,redis,samba,sftp,ssh,statsd,slack'],
)
def tests(session, python, airflow, airflow_extra):
    # Clean environment
    rmtree('airflow_data', ignore_errors=True)

    env = {
        'AIRFLOW_HOME': os.getcwdb().decode('utf-8') + '/airflow_data',
        'AIRFLOW__CORE__DAGS_FOLDER': 'airflow/dags',
        'AIRFLOW__CORE__LOAD_EXAMPLES': 'False',
        'AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS': 'False',
        'AIRFLOW__OPERATORS__ALLOW_ILLEGAL_ARGUMENTS': 'True',
    }

    args = session.posargs or [
        '-m',
        'unittest',
        'discover',
        '-s',
        'airflow/tests',
        '-p',
        '*_test*.py',
        '-t',
        'airflow',
        '-v',
    ]
    # Prerequisites packages
    session.install('psycopg2-binary')
    session.install('GitPython')

    # Airflow setup
    session.install(
        f'apache-airflow=={airflow}',
        '--constraint',
        f'https://raw.githubusercontent.com/apache/airflow/constraints-{airflow}/constraints-{python}.txt',
        env=env,
    )

    session.install('apache-airflow-providers-amazon')
    session.install('apache-airflow-providers-datadog')
    session.install('apache-airflow-providers-docker')
    session.install('apache-airflow-providers-google')
    session.install('apache-airflow-providers-postgres')
    session.install('apache-airflow-providers-redis')
    session.install('apache-airflow-providers-samba')
    session.install('apache-airflow-providers-sftp')
    session.install('apache-airflow-providers-ssh')
    session.install('apache-airflow-providers-datadog')
    session.install('apache-airflow-providers-slack')

    session.run('airflow', 'db', 'upgrade', env=env)
    session.run('airflow', 'variables', 'import', 'airflow/tests/airflow_test_variables.json', env=env)
    # Run unittest
    session.run(' python3 ', *args, env=env)
