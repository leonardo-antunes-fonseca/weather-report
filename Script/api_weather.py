import pandas as pd
import requests
from datetime import datetime
from pandas_gbq import to_gbq
from google.cloud import bigquery
from concurrent.futures import ThreadPoolExecutor
import os

os.environ['GOOGLE_APLICATION_CREDENTIALS'] = 'SUAS_CREDENCIAIS'

url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"

response = requests.get(url)

if response.status_code == 200:
    result = response.json()  
    
    dados_extraidos = []

    for municipio in result:
            dados_extraidos.append({
                'ID': municipio['id'],
                'Nome': municipio['nome'],
                'Microrregião': municipio['microrregiao']['nome'],
                'Mesorregião': municipio['microrregiao']['mesorregiao']['nome'],
                'UF': municipio['microrregiao']['mesorregiao']['UF']['sigla'],
                'Estado': municipio['microrregiao']['mesorregiao']['UF']['nome'],
                'Região': municipio['microrregiao']['mesorregiao']['UF']['regiao']['nome'],
                'Região Imediata': municipio['regiao-imediata']['nome'],
                'Região Intermediária': municipio['regiao-imediata']['regiao-intermediaria']['nome']
            })

    df = pd.DataFrame(dados_extraidos)

df['Pais'] = 'Brasil'

list_muninicipios = df['Nome'].tolist()

list_municipios_sp = df[df['Estado'] == 'São Paulo']['Nome'].tolist()
def obter_clima(cidade):
    url = "https://api.openweathermap.org/data/2.5/weather"
    # Adicione sua chave de API 
    params = {"q": cidade, "appid": "SUA_API_KEY", "units": "standard"}
    
    response = requests.get(url, params=params)

    if response.status_code == 200:
        clima = response.json()
        return {
            'nome': clima.get('name', ''),
            'temperatura': clima['main'].get('temp'),
            'min_temperatura': clima['main'].get('temp_min'),
            'max_temperatura': clima['main'].get('temp_max'),
            'sensacao_termica': clima['main'].get('feels_like'),
            'umidade': clima['main'].get('humidity'),
            'velocidade_vento': clima['wind'].get('speed'),
            'nascer_do_sol': datetime.utcfromtimestamp(clima['sys'].get('sunrise', 0)).strftime('%Y-%m-%d %H:%M:%S'),
            'por_do_sol': datetime.utcfromtimestamp(clima['sys'].get('sunset', 0)).strftime('%Y-%m-%d %H:%M:%S'),
            'date': datetime.utcfromtimestamp(clima.get('dt', 0)).strftime('%Y-%m-%d %H:%M:%S')
        }
    return None  

with ThreadPoolExecutor() as executor:
    dados_clima = list(executor.map(obter_clima, list_muninicipios))

dados_clima = [dado for dado in dados_clima if dado is not None]

df_clima = pd.DataFrame(dados_clima)

projeto_id = "SEU_PROJETO"
dataset_id = "SEU_DATASET"
tabela_id = "DimBrazilIbge"


tabela_destino = f"{dataset_id}.{tabela_id}"
to_gbq(df, tabela_destino, project_id=projeto_id, if_exists='replace')

projeto_id = "SEU_PROJETO"
dataset_id = "SEU_DATASET"
tabela_id = "FactBrazilTemp"


tabela_destino = f"{dataset_id}.{tabela_id}"
to_gbq(df_clima, tabela_destino, project_id=projeto_id, if_exists='replace')