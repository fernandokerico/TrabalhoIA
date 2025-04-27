import openml
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from utils.processamento import carregar_imagens, criar_dataframe, salvar_csv
import os

# Função para carregar o modelo treinado
def carregar_modelo(modelo_caminho):
    try:
        modelo = tf.keras.models.load_model(modelo_caminho)
        print('Modelo carregado com sucesso!')
        return modelo
    except Exception as e:
        print(f"Erro ao carregar o modelo: {e}")
        return None

# Função para classificar uma nova imagem
def classificar_imagem(imagem_path, modelo, label_encoder):
    caracteristicas = extrair_caracteristicas(imagem_path)
    caracteristicas = caracteristicas.reshape(1, -1)  # Deixe no formato certo pro modelo
    previsao = modelo.predict(caracteristicas)
    classe_predita = np.argmax(previsao)
    classe_final = label_encoder.inverse_transform([classe_predita])[0]
    return classe_final

# Função para extrair características (RGB médio) de uma imagem
def extrair_caracteristicas(imagem_path):
    from PIL import Image
    imagem = Image.open(imagem_path).convert('RGB')
    pixels = np.array(imagem).reshape(-1, 3)  # "Achata" para uma lista de pixels
    media_rgb = np.mean(pixels, axis=0)  # Calcula a média de R, G e B
    return media_rgb

# Baixar o conjunto de dados do OpenML (CIFAR-10)
def baixar_dados_openml():
    dataset = openml.datasets.get_dataset(45104)  # CIFAR-10 Dataset ID
    X, y, _, _ = dataset.get_data(target=dataset.default_target_attribute)
    return X, y

# Caminhos dos arquivos
MODELO_CAMINHO = 'modelo_rgb.h5'
CSV_CAMINHO = 'dados_imagens.csv'

# Carregar o modelo treinado
modelo = carregar_modelo(MODELO_CAMINHO)
if modelo is None:
    exit()  # Se o modelo não for carregado, o programa deve parar.

# Recarregar o LabelEncoder
dataset = pd.read_csv(CSV_CAMINHO)
label_encoder = LabelEncoder()
label_encoder.fit(dataset['Classe'])

# Baixar dados do OpenML
X, y = baixar_dados_openml()
print("Dados do OpenML carregados com sucesso.")

# Classificar uma nova imagem (exemplo de uso)
imagem_nova = input('Digite o caminho da nova imagem para classificar: ')
if not os.path.exists(imagem_nova):
    print('Arquivo de imagem não encontrado. Verifique o caminho informado.')
    exit()

classe_final = classificar_imagem(imagem_nova, modelo, label_encoder)
print(f'A imagem foi classificada como: {classe_final}')
