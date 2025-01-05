import os
import datetime
import requests

# Configurações do Meta
INSTAGRAM_GRAPH_API_URL = 'https://graph.facebook.com/v13.0/{ig_user_id}/media'
INSTAGRAM_PUBLISH_URL = 'https://graph.facebook.com/v13.0/{ig_user_id}/media_publish'
ACCESS_TOKEN = 'token_de_acesso_aqui'
IG_USER_ID = 'seu_usuario_instagram_id'

# Função para criar um container de mídia (para feed)
def create_media_container(image_path, caption):
    files = {'image_url': (None, image_path)}  # URL remota da imagem
    data = {
        'caption': caption,
        'access_token': ACCESS_TOKEN,
    }
    response = requests.post(INSTAGRAM_GRAPH_API_URL.format(ig_user_id=IG_USER_ID), data=data, files=files)
    return response.json()

# Função para publicar o container de mídia
def publish_media(media_id):
    data = {
        'creation_id': media_id,
        'access_token': ACCESS_TOKEN
    }
    response = requests.post(INSTAGRAM_PUBLISH_URL.format(ig_user_id=IG_USER_ID), data=data)
    return response.json()

# Diretório com os posts
directory = 'caminho_para_sua_pasta'

# Percorre todos os arquivos na pasta
for filename in os.listdir(directory):
    if filename.endswith('.png') or filename.endswith('.jpg'):
        try:
            # Extrai o dia do nome do arquivo
            day = int(filename.split('_')[0])
        except ValueError:
            print(f'Nome de arquivo inválido: {filename}')
            continue

        # Configura a data de postagem para o dia especificado no nome do arquivo às 7 horas da manhã
        now = datetime.datetime.now()
        post_date = datetime.datetime(now.year, now.month, day, 7, 0, 0)
        if post_date < now:
            print(f"Data já passada para {filename}, ignorando...")
            continue

        # Cria o container de mídia
        caption = f'Story programado para {post_date.strftime("%d/%m/%Y %H:%M")}'
        response = create_media_container(os.path.join(directory, filename), caption)
        
        if 'id' in response:
            media_id = response['id']
            publish_response = publish_media(media_id)
            print(f"Publicado como feed para {filename}: {publish_response}")
        else:
            print(f"Erro ao criar container para {filename}: {response}")

print("Processamento concluído.")
