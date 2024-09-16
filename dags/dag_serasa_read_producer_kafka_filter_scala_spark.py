from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now() - timedelta(days=1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=60),
}

with DAG(
    dag_id='SERASA_READ_PRODUCER_KAFKA_FILTER_SCALA_SPARK',
    default_args=default_args,
    description='Atividade DAG para ingestao de dados no Spark com Scala',
    schedule_interval=None,  # Pode ser ajustado para um cronograma específico
    max_active_runs=1,
    tags=['serasa', 'spark', 'scala']
) as dag:

    spark_submit_task = BashOperator(
    task_id='spark_submit_task',
    bash_command=(
        'spark-submit --master local[*] --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0 '
        '--total-executor-cores 2 --executor-memory 4g --name ConsumeMsgConvetToParquet '
        '/usr/local/airflow/scripts/serasa/scala/stream-taxi-data-consumer_2.12-1.0.0-SNAPSHOT.jar'
    ),
    dag=dag
    )

    # Ordem das tarefas
    spark_submit_task
