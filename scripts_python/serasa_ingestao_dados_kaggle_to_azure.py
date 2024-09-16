from azure.storage.blob import BlobClient
from pathlib import Path
import json, os, zipfile

# Variáveis de apoio
api_user_kaggle = {
    "username": "marcusantoniotg", 
    "key": "bb852bcfb02a9a30042e1864786503ec"
}

cadeia_conexao = 'DefaultEndpointsProtocol=https;AccountName=stgaccount1368363;AccountKey=jMSH7MrQZ9UJbvBFA92oQbQFyh25YY5iyfu09AjSU1KDGgcH19CMjV8O0GUG8PemNi2Lg1cXayyG+AStXi+0QQ==;EndpointSuffix=core.windows.net'

# Configurar credenciais do Kaggle
kaggle_path = Path('/root/.kaggle')
os.makedirs(kaggle_path, exist_ok=True)

with open(kaggle_path / 'kaggle.json', 'w') as handle:
    json.dump(api_user_kaggle, handle)

# Definir permissões corretas para o arquivo da chave de API
os.chmod(kaggle_path / 'kaggle.json', 0o600)

# Baixar os dados da competição usando Kaggle API
os.system('kaggle competitions download -c new-york-city-taxi-fare-prediction')

# Descompactar o arquivo baixado
with zipfile.ZipFile('new-york-city-taxi-fare-prediction.zip', 'r') as zip_ref:
    zip_ref.extractall("new-york-city-taxi-fare-prediction")

# Carregar arquivos no Azure Storage Blob
for arquivo in os.listdir("new-york-city-taxi-fare-prediction"):
    arquivo_blob = f'raw/new-york-city-taxi-fare-prediction/{arquivo}'
    blob = BlobClient.from_connection_string(
        conn_str=cadeia_conexao, 
        container_name="datalake-1368363", 
        blob_name=arquivo_blob
    )
    with open(f"new-york-city-taxi-fare-prediction/{arquivo}", "rb") as data:
        blob.upload_blob(data, overwrite=True)
        print(f"file {data} copiado para azure")

