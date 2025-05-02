import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Pré-processamento (normalizar pixel para 0-1)
gerador = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2  # 80% treino, 20% validação automaticamente
)

# Base de treinamento
base_treinamento = gerador.flow_from_directory(
    'data',
    target_size=(64, 64),
    batch_size=8,
    class_mode='categorical',
    subset='training',
    shuffle=True
)

# Base de validação
teste = gerador.flow_from_directory(
    'data',
    target_size=(64, 64),
    batch_size=8,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

# Definição da CNN
rede_neural = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(32, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(2, activation='softmax')
])

# Compilacao
rede_neural.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Treinamento
rede_neural.fit(base_treinamento, epochs=20, validation_data=teste)

# Avaliacao
previsoes = rede_neural.predict(teste)
previsoes_classes = np.argmax(previsoes, axis=1)

print("Acurácia:", accuracy_score(teste.classes, previsoes_classes))

# Matriz de confusao
cm = confusion_matrix(teste.classes, previsoes_classes)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Previsto')
plt.ylabel('Real')
plt.show()
