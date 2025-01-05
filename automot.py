import os
import datetime
import requests

# Configurações do Meta
META_GRAPH_API_URL = 'https://graph.facebook.com/v13.0/{page_id}/media'
ACCESS_TOKEN = 'token_de_acesso_aqui'

# Função para fazer o upload de um post
def upload_post(filename, post_date):
    with open(filename, 'rb') as file:
        files = {'source': file}
        data = {
            'caption': '',
            'scheduled_publish_time': post_date.timestamp(),
            'published': False,
            'access_token': ACCESS_TOKEN
        }
        response = requests.post(META_GRAPH_API_URL.format(page_id='sua_pagina_id'), files=files, data=data)
        
        if response.status_code == 200:
            print(f'Successfully uploaded {filename}')
        else:
            print(f'Failed to upload {filename}. Status code: {response.status_code} - {response.json()}')

# Diretório com os posts
directory = 'caminho_para_sua_pasta'

# Percorre todos os arquivos na pasta
for filename in os.listdir(directory):
    if filename.endswith('.png') or filename.endswith('.jpg'):
        # Extrai o dia do nome do arquivo
        try:
            day = int(filename.split('_')[0])
        except ValueError:
            print(f'Nome de arquivo inválido: {filename}')
            continue

        # Configura a data de postagem para o dia especificado no nome do arquivo às 7 horas da manhã
        now = datetime.datetime.now()
        post_date = datetime.datetime(now.year, now.month, day, 7, 0, 0)
        
        # Chama a função para fazer o upload
        upload_post(os.path.join(directory, filename), post_date)

print("All posts processed.")