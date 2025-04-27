# Importação das bibliotecas necessárias
import os
from utils.processamento import carregar_imagens, criar_dataframe, salvar_csv

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

# Definir caminhos
DIRETORIO_IMAGENS = 'data'  # onde estão suas pastas de imagens
ARQUIVO_CSV = 'dados_imagens.csv'  # onde vamos salvar os dados

# ======== PROCESSAMENTO DAS IMAGENS ========

# Carregar imagens e extrair características
caracteristicas, rotulos = carregar_imagens(DIRETORIO_IMAGENS)

# Criar um DataFrame com os dados
df = criar_dataframe(caracteristicas, rotulos)

# Salvar o DataFrame em CSV
salvar_csv(df, ARQUIVO_CSV)

# ======== TREINAMENTO DA REDE NEURAL ========

# Carregar os dados
dataset = pd.read_csv(ARQUIVO_CSV)

# Separar características (X) e rótulos (y)
X = dataset[['R', 'G', 'B']].values
y = dataset['Classe'].values

# Converter rótulos de texto para números
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Dividir os dados em treino e teste
X_treinamento, X_teste, y_treinamento, y_teste = train_test_split(X, y, test_size=0.2, random_state=42)

# Construir a rede neural
rede_neural = tf.keras.models.Sequential()
rede_neural.add(tf.keras.layers.Dense(units=8, activation='relu', input_shape=(3,)))
rede_neural.add(tf.keras.layers.Dense(units=8, activation='relu'))
rede_neural.add(tf.keras.layers.Dense(units=len(np.unique(y)), activation='softmax'))

# Compilar a rede
rede_neural.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Treinar a rede
historico = rede_neural.fit(X_treinamento, y_treinamento, epochs=100, validation_split=0.1)

# ======== AVALIAÇÃO DO MODELO ========

# Avaliar no conjunto de teste
loss, accuracy = rede_neural.evaluate(X_teste, y_teste)
print(f'Acurácia no teste: {accuracy*100:.2f}%')

# ======== SALVAR O MODELO TREINADO ========

# Salvar modelo treinado
rede_neural.save('modelo_rgb.h5')
print('Modelo salvo como modelo_rgb.h5')

# ======== GRÁFICO DE DESEMPENHO ========

plt.plot(historico.history['accuracy'], label='Acurácia Treinamento')
plt.plot(historico.history['val_accuracy'], label='Acurácia Validação')
plt.legend()
plt.title('Evolução da Acurácia')
plt.xlabel('Épocas')
plt.ylabel('Acurácia')
plt.show()
