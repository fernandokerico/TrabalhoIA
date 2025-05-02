import os
import numpy as np
import pandas as pd
import joblib
from PIL import Image
from flask import Flask, request, render_template, jsonify
import json
import subprocess
from datetime import datetime
import shutil  # Importe o módulo shutil para operações de arquivo

app = Flask(__name__)  # Instancia o Flask **antes** de usar @app.route


# Configuração para a pasta principal de dados de treinamento
DATA_FOLDER = 'data'
app.config['DATA_FOLDER'] = DATA_FOLDER
os.makedirs(DATA_FOLDER, exist_ok=True)

# Configuração para a pasta de uploads temporários (análise)
UPLOAD_FOLDER = '.'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Caminhos dos arquivos para o modelo .pkl (análise)
MODELO_CAMINHO_PKL = 'modelo_personagens.pkl'
LABEL_ENCODER_CAMINHO_PKL = 'label_encoder.pkl'
CSV_CAMINHO = 'personagens.csv'

# Caminhos dos arquivos para o modelo .h5 (treinamento)
MODELO_CAMINHO_H5 = 'modelo_personagens.h5'
CLASSES_CAMINHO_NPY = 'classes.npy'

# Carregar o modelo treinado .pkl para análise
modelo_pkl = None
try:
    modelo_pkl = joblib.load(MODELO_CAMINHO_PKL)
    print('Modelo .pkl carregado com sucesso para análise!')
except Exception as e:
    print(f"Erro ao carregar o modelo .pkl: {e}")

# Carregar o LabelEncoder para análise
label_encoder_pkl = None
try:
    label_encoder_pkl = joblib.load(LABEL_ENCODER_CAMINHO_PKL)
    print('Label Encoder carregado com sucesso para análise!')
except FileNotFoundError:
    label_encoder_pkl = None
    print(f"Erro: Arquivo {LABEL_ENCODER_CAMINHO_PKL} não encontrado.")
except Exception as e:
    label_encoder_pkl = None
    print(f"Erro ao carregar o Label Encoder para análise: {e}")

# Carregar os nomes das classes para análise (se label_encoder.pkl não existir)
classes_analise = None
inverse_label_encoder_pkl = None
if label_encoder_pkl is None:
    try:
        dataset = pd.read_csv(CSV_CAMINHO)
        if 'Classe' in dataset.columns:
            classes_analise = dataset['Classe'].unique()
            label_encoder_pkl = {classe: i for i, classe in enumerate(classes_analise)}
            inverse_label_encoder_pkl = {i: classe for classe, i in enumerate(label_encoder_pkl.items())}
            print('Classes carregadas do CSV para análise!')
        else:
            print(f"Erro: Coluna 'Classe' não encontrada em {CSV_CAMINHO}.")
    except FileNotFoundError:
        print(f"Erro: Arquivo {CSV_CAMINHO} não encontrado para carregar classes.")
    except Exception as e:
        print(f"Erro ao carregar classes do CSV: {e}")
else:
    inverse_label_encoder_pkl = {i: classe for i, classe in enumerate(label_encoder_pkl.classes_)} if hasattr(
        label_encoder_pkl, 'classes_') else None


# Função para extrair características (RGB médio) de uma imagem para análise
def extrair_caracteristicas(imagem_path):
    try:
        imagem = Image.open(imagem_path).convert('RGB')
        pixels = np.array(imagem).reshape(-1, 3)
        media_rgb = np.mean(pixels, axis=0)
        return media_rgb.reshape(1, -1)
    except Exception as e:
        print(f"Erro ao extrair características da imagem: {e}")
        return None


# Rota para o upload das imagens de treinamento
@app.route('/upload_treinamento', methods=['POST'])
def upload_treinamento():
    if 'images[]' not in request.files:
        return jsonify({'error': 'Nenhum arquivo de imagem enviado'}), 400

    files = request.files.getlist('images[]')
    classes = request.form.getlist('classes[]')  # Recebe a lista de classes do formulário

    if not files or not classes or len(files) != len(classes):
        return jsonify({'error': 'Número de arquivos e classes não corresponde'}), 400

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_paths = []
    for i, file in enumerate(files):
        if file and file.filename != '':
            filename = file.filename
            class_name = classes[i].lower().replace(' ',
                                                  '_')  # Usa o nome da classe fornecido pelo usuário e formata
            print(f"Nome da classe: {class_name}")  # Adicione esta linha para debug
            # Cria o diretório para a classe se não existir
            if class_name == 'cascao':  # Verifica se a classe é 'cascao'
                class_path = os.path.join(app.config['DATA_FOLDER'], timestamp,
                                          class_name)  # Inclui o timestamp na criação do caminho
                print(f"Caminho da pasta: {class_path}")  # Adicione esta linha para debug
                try:
                    if not os.path.exists(class_path):
                        os.makedirs(class_path)
                        print(f"Pasta criada: {class_path}")  # Nova linha de debug
                    else:
                        print(f"Pasta já existia: {class_path}")  # pasta já existia
                except Exception as e:
                    print(f"Erro ao criar pasta: {e}")
                    return jsonify({'error': f'Erro ao criar pasta: {e}'}), 500

                file_path = os.path.join(class_path, filename)
                try:
                    file.save(file_path)
                    print(f"Arquivo salvo em: {file_path}")
                    file_paths.append(
                        os.path.join(timestamp, class_name, filename))  # Adiciona o caminho do arquivo à lista
                except Exception as e:
                    print(f"Erro ao salvar o arquivo {filename}: {e}")
                    return jsonify({'error': f'Erro ao salvar o arquivo {filename}: {e}'}), 500
            else:
                return jsonify({
                    'error': f'Classe {class_name} não é "cascao". Apenas a classe "cascao" é permitida.'
                }), 400

    # Retorna os caminhos dos arquivos para serem usados no treinamento
    return jsonify({
        'message': 'Imagens de treinamento enviadas e salvas com sucesso!',
        'file_paths': file_paths
    }), 200


# Rota principal para o formulário
@app.route('/')
def index():
    return render_template('index.html')


# Rota para processar os dados do formulário (análise)
@app.route('/processar', methods=['POST'])
def processar_dados():
    if modelo_pkl is None or label_encoder_pkl is None or inverse_label_encoder_pkl is None:
        return json.dumps({'erro': 'Modelo ou Label Encoder não carregados corretamente para análise'}), 500

    imagens = request.files.getlist('images[]')
    resultados = []

    for imagem in imagens:
        if imagem and imagem.filename != '':
            caminho_imagem_temp = os.path.join(app.config['UPLOAD_FOLDER'], imagem.filename)
            try:
                imagem.save(caminho_imagem_temp)
                caracteristicas = extrair_caracteristicas(caminho_imagem_temp)
                if caracteristicas is not None:
                    previsao = modelo_pkl.predict(caracteristicas)
                    classe_predita_num = previsao[0]
                    classe_final = inverse_label_encoder_pkl[classe_predita_num]
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


# Rota para iniciar o treinamento com pastas
@app.route('/iniciar_treinamento_com_pastas', methods=['POST'])
def iniciar_treinamento_com_pastas():
    script_path_treinar_modelo = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'treino_rgb.py')
    script_path_gerar_dataset = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gerar_dataset_rgb.py')

    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({'error': 'Erro: Dados enviados não são um dicionário'}), 400

    file_paths = data.get('file_paths', [])  # Obtém a lista de caminhos dos arquivos

    try:
        print("Iniciando geração do dataset...")
        # Passa os caminhos dos arquivos como argumento para o script gerar_dataset_rgb.py
        process_dataset = subprocess.run(['python', script_path_gerar_dataset, '--image_paths', ','.join(file_paths)],
                                         capture_output=True, text=True, check=True)
        print("Geração do dataset concluída.")
        print("Saída do script de geração:", process_dataset.stdout)
        if process_dataset.stderr:
            print("Erros do script de geração:", process_dataset.stderr)

        print("Iniciando treinamento do modelo...")
        process_treinamento = subprocess.run(['python', script_path_treinar_modelo], capture_output=True, text=True,
                                            check=True)
        print("Treinamento do modelo concluído.")
        print("Saída do script de treinamento:", process_treinamento.stdout)
        if process_treinamento.stderr:
            print("Erros do script de treinamento:", process_treinamento.stderr)

        return jsonify({'message': 'Treinamento concluído com sucesso!'})

    except subprocess.CalledProcessError as e:
        error_message = f"Erro ao executar script: {e}"
        if e.stdout:
            error_message += f"\nStdout: {e.stdout}"
        if e.stderr:
            error_message += f"\nStderr: {e.stderr}"
        print(error_message)
        return jsonify({'error': error_message}), 500  # Retorna erro 500
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return jsonify({'error': f"Erro inesperado: {e}"}), 500  # Retorna erro 500


# Rota para exibir os resultados
@app.route('/resultado')
def resultado():
    return render_template('resultado.html')


if __name__ == '__main__':
    app.run(debug=True)
