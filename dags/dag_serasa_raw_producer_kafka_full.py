from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now() - timedelta(days=1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=60),
}

dag = DAG(
    dag_id= 'SERASA_RAW_FILE_PRODUCER_KAFKA_FULL',
    default_args=default_args,
    description='Atividade DAG para ingestao de dados no Kafka',
    #schedule_interval='* * * * *',
    schedule_interval=None,
    max_active_runs=1,
    tags=['serasa','kafka']
)

carregar_dados_camada_raw = BashOperator(
    task_id='get_raw_file_writing_producer_kafka',
    bash_command='python3 /usr/local/airflow/scripts/serasa/serasa_send_raw_file_to_producer_kafka_full.py',
    dag=dag,
)

carregar_dados_camada_raw