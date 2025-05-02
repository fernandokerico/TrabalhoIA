import os
import pandas as pd
import cv2

# Caminho para a pasta onde estão as imagens organizadas por personagem
data_dir = 'data'

# Lista para guardar os dados
dados = []

# Percorre cada subpasta (cada personagem)
for personagem in os.listdir(data_dir):
    personagem_path = os.path.join(data_dir, personagem)
    
    # Verifica se é uma pasta
    if os.path.isdir(personagem_path):
        # Percorre cada imagem da pasta
        for imagem_nome in os.listdir(personagem_path):
            imagem_path = os.path.join(personagem_path, imagem_nome)
            
            # Lê a imagem
            imagem = cv2.imread(imagem_path)
            
            if imagem is not None:
                # Calcula a média dos valores de cor (em ordem BGR)
                media_cor = imagem.mean(axis=(0, 1))  # média para cada canal (B, G, R)
                B, G, R = media_cor
                
                # Salva os dados (invertendo para R, G, B)
                dados.append({
                    'R': int(R),
                    'G': int(G),
                    'B': int(B),
                    'classe': personagem
                })

# Cria o DataFrame
df = pd.DataFrame(dados)

# Salva o CSV
df.to_csv('dataset_rgb.csv', index=False)

print("Dataset RGB criado com sucesso como 'dataset_rgb.csv'.")
