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
    return media_rgb.reshape(1, -1) # Garante a forma correta para o predict

# Carrega o modelo treinado
modelo = joblib.load('modelo_personagens.pkl')

# Carrega o LabelEncoder
label_encoder = joblib.load('label_encoder.pkl')

# Caminho da imagem a ser testada
caminho_imagem = 'teste.jpg'  # você pode mudar isso

if not os.path.exists(caminho_imagem):
    print(f"Imagem '{caminho_imagem}' não encontrada!")
else:
    media_rgb = extrair_media_rgb(caminho_imagem)
    previsao_numerica = modelo.predict(media_rgb)
    nome_da_classe = label_encoder.inverse_transform(previsao_numerica)
    print(f"Previsão Numérica: {previsao_numerica[0]}")
    print(f"Nome da Classe Prevista: {nome_da_classe[0]}")