from confluent_kafka import Producer
from azure.storage.blob import BlobServiceClient
import csv, json

# Conexão ao contêiner Azure Data Lake
blob_service_client = BlobServiceClient.from_connection_string('DefaultEndpointsProtocol=https;AccountName=stgaccount1368363;AccountKey=jMSH7MrQZ9UJbvBFA92oQbQFyh25YY5iyfu09AjSU1KDGgcH19CMjV8O0GUG8PemNi2Lg1cXayyG+AStXi+0QQ==;EndpointSuffix=core.windows.net')
container_name = 'datalake-1368363'
blob_name = 'raw/new-york-city-taxi-fare-prediction/train.csv'  # Nome do arquivo que você quer ler

# Download do arquivo do Data Lake
container_client = blob_service_client.get_container_client(container_name)
blob_client = container_client.get_blob_client(blob_name)

# Fazer download do arquivo
with open("train.csv", "wb") as my_blob:
    blob_data = blob_client.download_blob()
    my_blob.write(blob_data.readall())

# Kafka Producer Configuration
producer_conf = {
    'bootstrap.servers': '10.0.0.4:9092',  # Ou IP da máquina virtual no Azure
    'client.id': 'data-lake-producer'
}
producer = Producer(producer_conf)

# Função para transformar cada linha do CSV em uma string JSON
def format_message(row):
    message = {
        'key': row['key'],
        'pickup_datetime': row['pickup_datetime'],
        'pickup_longitude': float(row['pickup_longitude']),
        'pickup_latitude': float(row['pickup_latitude']),
        'dropoff_longitude': float(row['dropoff_longitude']),
        'dropoff_latitude': float(row['dropoff_latitude']),
        'passenger_count': int(row['passenger_count']),
        'fare_amount': float(row['fare_amount']) if 'fare_amount' in row else None
    }
    return json.dumps(message)

error_count = 0

# Enviar dados linha por linha para o Kafka
with open("train.csv", "r") as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        try:
            message = format_message(row)  # Formatar a linha como JSON
            producer.produce('topic_new_york_taxis', key=row['key'], value=message)
        except Exception as e:
            # Contabilizando erros
            error_count += 1
            print(f"Erro na linha {csvreader.line_num}: {e}")
        finally:
            producer.flush()

print(f"Dados do arquivo train.csv enviados para o Kafka com sucesso!")
print(f"Número total de linhas com erro: {error_count}")