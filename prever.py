import joblib
import numpy as np
from PIL import Image
import os

# Função para extrair média de cores
def extrair_media_rgb(caminho_imagem):
    imagem = Image.open(caminho_imagem).convert('RGB')
    imagem = imagem.resize((100, 100))  # opcional: padroniza o tamanho
    np_imagem = np.array(imagem)
    media_rgb = np.mean(np_imagem.reshape(-1, 3), axis=0)
    return media_rgb

# Carrega o modelo treinado
modelo = joblib.load('modelo_personagens.pkl')

# Caminho da imagem a ser testada
caminho_imagem = 'teste.jpg'  # você pode mudar isso

if not os.path.exists(caminho_imagem):
    print(f"Imagem '{caminho_imagem}' não encontrada!")
else:
    media_rgb = extrair_media_rgb(caminho_imagem).reshape(1, -1)
    previsao = modelo.predict(media_rgb)
    print(f"Previsão: {previsao[0]}")
