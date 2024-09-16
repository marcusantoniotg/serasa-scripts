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
    dag_id= 'SERASA_GET_DATASET_KAGGLE_SEND_AZURE',
    default_args=default_args,
    description='Atividade DAG para ingestao de dados do KAGGLE para AZURE',
    #schedule_interval='* * * * *',
    schedule_interval=None,
    max_active_runs=1,
    tags=['serasa','kafka']
)

carregar_dados_camada_raw = BashOperator(
    task_id='get_dataset_kaggle_send_azure',
    bash_command='python3 /usr/local/airflow/scripts/serasa/serasa_ingestao_dados_kaggle_to_azure.py',
    dag=dag,
)

carregar_dados_camada_raw