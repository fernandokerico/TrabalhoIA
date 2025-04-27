# Importação das bibliotecas
import numpy as np
import tensorflow as tf
from PIL import Image
import os
from sklearn.preprocessing import LabelEncoder
import pandas as pd

# Função para extrair características da nova imagem
def extrair_caracteristicas(imagem_path):
    imagem = Image.open(imagem_path).convert('RGB')
    pixels = np.array(imagem).reshape(-1, 3)  # "achata" para uma lista de pixels
    media_rgb = np.mean(pixels, axis=0)  # calcula a média de R, G e B
    return media_rgb

# Caminhos dos arquivos
MODELO_CAMINHO = 'modelo_rgb.h5'
CSV_CAMINHO = 'dados_imagens.csv'

# Carregar o modelo treinado
modelo = tf.keras.models.load_model(MODELO_CAMINHO)
print('Modelo carregado com sucesso!')

# Recarregar o LabelEncoder
dataset = pd.read_csv(CSV_CAMINHO)
label_encoder = LabelEncoder()
label_encoder.fit(dataset['Classe'])

# Perguntar o caminho da imagem nova
imagem_nova = input('Digite o caminho da nova imagem para classificar: ')

if not os.path.exists(imagem_nova):
    print('Arquivo de imagem não encontrado. Verifique o caminho informado.')
    exit()

# Extrair características da nova imagem
caracteristicas = extrair_caracteristicas(imagem_nova)
caracteristicas = caracteristicas.reshape(1, -1)  # deixar no formato certo pro modelo

# Fazer a previsão
previsao = modelo.predict(caracteristicas)
classe_predita = np.argmax(previsao)

# Mostrar o resultado
classe_final = label_encoder.inverse_transform([classe_predita])[0]
print(f'A imagem foi classificada como: {classe_final}')
