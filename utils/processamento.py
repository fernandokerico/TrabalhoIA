# Importação das bibliotecas necessárias
import os
import numpy as np
import pandas as pd
from PIL import Image

def carregar_imagens(diretorio_base, tamanho=(64, 64)):
    """
    Lê todas as imagens em subpastas do diretório base.
    Cada subpasta é considerada uma classe.
    
    Args:
        diretorio_base (str): caminho para a pasta 'data/'.
        tamanho (tuple): redimensiona imagens para esse tamanho (largura, altura).
        
    Returns:
        lista de características das imagens, lista de rótulos (classes)
    """
    caracteristicas = []  # aqui vamos guardar os dados de cada imagem
    rotulos = []          # aqui vamos guardar o nome da classe de cada imagem

    # Percorrer todas as subpastas (cada subpasta é uma classe)
    for classe in os.listdir(diretorio_base):
        caminho_classe = os.path.join(diretorio_base, classe)
        
        # Garantir que seja uma pasta
        if not os.path.isdir(caminho_classe):
            continue
        
        # Agora percorremos cada imagem da subpasta
        for arquivo in os.listdir(caminho_classe):
            caminho_arquivo = os.path.join(caminho_classe, arquivo)
            try:
                # Abrir a imagem
                imagem = Image.open(caminho_arquivo).convert('RGB')
                imagem = imagem.resize(tamanho)  # Redimensionar para padrão

                # Converter para array NumPy
                array_imagem = np.array(imagem)

                # Extrair características - média de R, G e B
                media_r = np.mean(array_imagem[:, :, 0])
                media_g = np.mean(array_imagem[:, :, 1])
                media_b = np.mean(array_imagem[:, :, 2])

                # Salvar os dados
                caracteristicas.append([media_r, media_g, media_b])
                rotulos.append(classe)

            except Exception as e:
                print(f"Erro ao processar {caminho_arquivo}: {e}")

    return caracteristicas, rotulos

def criar_dataframe(caracteristicas, rotulos):
    """
    Recebe listas de características e rótulos, e cria um DataFrame do Pandas.
    
    Args:
        caracteristicas (list): lista com médias de RGB.
        rotulos (list): lista com nomes das classes.
        
    Returns:
        pd.DataFrame: DataFrame com colunas R, G, B e Classe.
    """
    df = pd.DataFrame(caracteristicas, columns=['R', 'G', 'B'])
    df['Classe'] = rotulos
    return df

def salvar_csv(df, caminho_csv):
    """
    Salva o DataFrame em um arquivo CSV.
    
    Args:
        df (pd.DataFrame): DataFrame a ser salvo.
        caminho_csv (str): caminho do arquivo CSV.
    """
    df.to_csv(caminho_csv, index=False)
    print(f"Arquivo CSV salvo em: {caminho_csv}")
