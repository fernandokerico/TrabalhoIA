import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical

# Carrega o dataset
df = pd.read_csv('dataset_rgb.csv')

# Separa features (RGB) e target (classe)
X = df[['R', 'G', 'B']].values
y = df['classe'].values

# Encode as classes para valores numéricos
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)
y_categorical = to_categorical(y_encoded)
np.save('classes.npy', label_encoder.classes_) # Salva os nomes das classes

# Divide os dados em treinamento e teste
X_train, X_test, y_train_categorical, y_test_categorical = train_test_split(X, y_categorical, test_size=0.2, random_state=42)

# Define o modelo da rede neural
model = Sequential([
    Dense(128, activation='relu', input_shape=(3,)),
    Dropout(0.5),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(y_categorical.shape[1], activation='softmax') # Número de neurônios na saída = número de classes
])

# Compila o modelo
model.compile(optimizer=Adam(learning_rate=0.001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

# Treina o modelo
history = model.fit(X_train, y_train_categorical, epochs=50, batch_size=32, validation_data=(X_test, y_test_categorical))

# Avalia o modelo
loss, accuracy = model.evaluate(X_test, y_test_categorical, verbose=0)
print(f'Acurácia do modelo nos dados de teste: {accuracy*100:.2f}%')

# Salva o modelo treinado
model.save('modelo_personagens.h5')

print("Modelo treinado e salvo como 'modelo_personagens.h5'.")