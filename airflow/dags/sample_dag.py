import pendulum
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator

with DAG(
    dag_id="sample_dag",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
):

    def hello():
        print("hello Airflow")


    PythonOperator(task_id="hello", python_callable=hello)
