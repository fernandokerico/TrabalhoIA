import pandas as pd
from scipy.io import arff
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf

# Carregar o conjunto de dados CIFAR-10 no formato ARFF (localmente)
data, meta = arff.loadarff('arff/dataset_31_credit-g.arff')  # Caminho para o arquivo ARFF

# Converter os dados para DataFrame do pandas
df = pd.DataFrame(data)

# Exibir as primeiras linhas para verificar os dados
print(df.head())

# Se os rótulos estiverem em bytes, converta-os para string
df['classe'] = df['classe'].apply(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)

# Agora, vamos separar as variáveis (X - imagens) e os rótulos (y - classes)
X = np.array(df.drop(columns=['classe']))  # Remover a coluna de rótulos (se houver)
y = np.array(df['classe'])  # Aqui deve estar o rótulo da classe

# Verifique o formato de X e y antes de seguir
print(f'Formato de X: {X.shape}, Formato de y: {y.shape}')

# Dividir os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Certifique-se de que os dados estão na forma correta (como imagens para CNN)
X_train = X_train.reshape(-1, 32, 32, 3)  # Ajuste para 32x32 imagens com 3 canais (RGB)
X_test = X_test.reshape(-1, 32, 32, 3)

# Normalizar as imagens para valores entre 0 e 1
X_train = X_train.astype('float32') / 255
X_test = X_test.astype('float32') / 255

# Criar o modelo de rede neural (CNN)
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')  # 10 classes para CIFAR-10
])

# Compilar o modelo
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# Treinar o modelo
model.fit(X_train, y_train, epochs=10)

# Avaliar o modelo
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f'Acurácia no teste: {test_acc}')
