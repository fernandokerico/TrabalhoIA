from PIL import Image
import os
import numpy as np
import pandas as pd

def carregar_imagens(diretorio_base, tamanho=(64, 64)):
    caracteristicas = []
    rotulos = []
    for classe in os.listdir(diretorio_base):
        caminho_classe = os.path.join(diretorio_base, classe)
        if not os.path.isdir(caminho_classe):
            continue
        for arquivo in os.listdir(caminho_classe):
            caminho_arquivo = os.path.join(caminho_classe, arquivo)
            try:
                imagem = Image.open(caminho_arquivo).convert('RGB')
                imagem = imagem.resize(tamanho)
                array_imagem = np.array(imagem)
                media_r = np.mean(array_imagem[:, :, 0])
                media_g = np.mean(array_imagem[:, :, 1])
                media_b = np.mean(array_imagem[:, :, 2])
                caracteristicas.append([media_r, media_g, media_b])
                rotulos.append(classe)
            except Exception as e:
                print(f"Erro ao processar {caminho_arquivo}: {e}")
    return caracteristicas, rotulos

def criar_dataframe(caracteristicas, rotulos):
    df = pd.DataFrame(caracteristicas, columns=['R', 'G', 'B'])
    df['Classe'] = rotulos
    return df

def salvar_csv(df, caminho_csv):
    df.to_csv(caminho_csv, index=False)
    print(f"CSV salvo com sucesso em: {caminho_csv}")
