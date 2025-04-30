import os
import numpy as np
import pandas as pd
import joblib  # Para carregar o modelo .pkl
from PIL import Image
from flask import Flask, request, render_template
import json

app = Flask(__name__)

# Configuração para a pasta de uploads (agora será a raiz)
UPLOAD_FOLDER = '.'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Caminhos dos arquivos
MODELO_CAMINHO = 'modelo_personagens.pkl'
CSV_CAMINHO = 'personagens.csv'

# Carregar o modelo treinado
try:
    modelo = joblib.load(MODELO_CAMINHO)
    print('Modelo carregado com sucesso!')
except Exception as e:
    print(f"Erro ao carregar o modelo: {e}")
    modelo = None

# Carregar o LabelEncoder
try:
    dataset = pd.read_csv(CSV_CAMINHO)
    label_encoder = joblib.load('label_encoder.pkl') # Se você salvou o LabelEncoder separadamente
    if 'Classe' in dataset.columns:
        label_encoder.fit(dataset['Classe']) # Garante que o encoder tenha as classes (útil se não salvo separado)
    print('Label Encoder carregado com sucesso!')
except FileNotFoundError:
    label_encoder = None
    print(f"Erro: Arquivo {CSV_CAMINHO} ou label_encoder.pkl não encontrado.")
except Exception as e:
    label_encoder = None
    print(f"Erro ao carregar o Label Encoder: {e}")

# Função para extrair características (RGB médio) de uma imagem
def extrair_caracteristicas(imagem_path):
    try:
        imagem = Image.open(imagem_path).convert('RGB')
        pixels = np.array(imagem).reshape(-1, 3)  # "Achata" para uma lista de pixels
        media_rgb = np.mean(pixels, axis=0)  # Calcula a média de R, G e B
        return media_rgb.reshape(1, -1)  # Retorna no formato esperado pelo modelo
    except Exception as e:
        print(f"Erro ao extrair características da imagem: {e}")
        return None

# Rota principal para o formulário
@app.route('/')
def index():
    return render_template('index.html')

# Rota para processar os dados do formulário
@app.route('/processar', methods=['POST'])
def processar_dados():
    if modelo is None or label_encoder is None:
        return json.dumps({'erro': 'Modelo ou Label Encoder não carregados'}), 500

    imagens = request.files.getlist('images[]')
    resultados = []

    for imagem in imagens:
        if imagem and imagem.filename != '':
            caminho_imagem_temp = os.path.join(app.config['UPLOAD_FOLDER'], imagem.filename)
            try:
                imagem.save(caminho_imagem_temp)
                caracteristicas = extrair_caracteristicas(caminho_imagem_temp)
                if caracteristicas is not None:
                    previsao = modelo.predict(caracteristicas)
                    classe_predita_num = previsao[0]
                    classe_final = label_encoder.inverse_transform([classe_predita_num])[0]
                    resultados.append({'filename': imagem.filename, 'classe': classe_final})
                else:
                    resultados.append({'filename': imagem.filename, 'classe': 'Erro ao processar a imagem'})
            except Exception as e:
                print(f"Erro ao processar a imagem {imagem.filename}: {e}")
                resultados.append({'filename': imagem.filename, 'classe': f'Erro no processamento: {e}'})
            finally:
                if os.path.exists(caminho_imagem_temp):
                    os.remove(caminho_imagem_temp)
        elif imagem.filename == '':
            resultados.append({'filename': 'Arquivo vazio', 'classe': 'Nenhum arquivo selecionado'})

    return json.dumps({'resultados': resultados})

# Rota para exibir os resultados
@app.route('/resultado')
def resultado():
    return render_template('resultado.html')

if __name__ == '__main__':
    app.run(debug=True)