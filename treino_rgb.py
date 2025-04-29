import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Carrega CSV
dados = pd.read_csv('dataset_rgb.csv')

# Separa dados e rótulos
X = dados[['R', 'G', 'B']].values
y = dados['classe'].values

# Codifica as classes para 0, 1, ...
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Divide treino/teste
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.2)

# Modelo MLP simples
modelo = tf.keras.models.Sequential()
modelo.add(tf.keras.layers.Dense(units=8, activation='relu', input_shape=(3,)))
modelo.add(tf.keras.layers.Dense(units=6, activation='relu'))
modelo.add(tf.keras.layers.Dense(units=4, activation='relu'))
modelo.add(tf.keras.layers.Dense(units=len(set(y)), activation='softmax'))

modelo.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
modelo.summary()

modelo.fit(X_treino, y_treino, epochs=100, validation_split=0.1)

# Avaliação
loss, acc = modelo.evaluate(X_teste, y_teste)
print(f"Acurácia: {acc:.2f}")
