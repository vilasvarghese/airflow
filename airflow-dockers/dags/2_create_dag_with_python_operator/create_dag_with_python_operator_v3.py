from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'vilas',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


def greet(age, ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    print(f"Hello World! My name is {first_name} {last_name}, "
          f"and I am {age} years old!")


def get_name(ti):
    ti.xcom_push(key='first_name', value='Vilas')
    ti.xcom_push(key='last_name', value='Varghese')


with DAG(
    default_args=default_args,
    dag_id='our_dag_with_python_operator_v03',
    description='Our first dag using python operator',
    start_date=datetime(2024, 5, 5),
    schedule_interval='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        op_kwargs={'age': 47}
    )

    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name
    )

    task2 >> task1