import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from google.colab import drive
import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix
import seaborn as sns

drive.mount('/content/drive')

# Exemplo de carregamento de imagem
img = tf.keras.preprocessing.image.load_img(
    r'/content/drive/MyDrive/IA 2025/Redes neurais artificiais/base/test_set/bart/bart1.bmp')

# Pré-processamento
gerador_treinamento = ImageDataGenerator(rescale=1./255, rotation_range=7, horizontal_flip=True, zoom_range=0.2)
base_treinamento = gerador_treinamento.flow_from_directory(
    '/content/drive/MyDrive/IA 2025/Redes neurais artificiais/base/training_set',
    target_size=(64, 64), batch_size=8, class_mode='categorical')

gerador_teste = ImageDataGenerator(rescale=1./255)
base_teste = gerador_teste.flow_from_directory(
    '/content/drive/MyDrive/IA 2025/Redes neurais artificiais/base/test_set',
    target_size=(64, 64), batch_size=8, class_mode='categorical', shuffle=False)

# Definição da CNN
rede_neural = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(32, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(6, activation='relu'),
    Dense(4, activation='relu'),
    Dense(4, activation='relu'),
    Dense(4, activation='relu'),
    Dense(2, activation='softmax')
])

# Compilação
rede_neural.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Treinamento
rede_neural.fit(base_treinamento, epochs=200, validation_data=base_teste)

# Avaliação
previsoes = rede_neural.predict(base_teste)
previsoes2 = np.argmax(previsoes, axis=1)
print("Acurácia:", accuracy_score(base_teste.classes, previsoes2))

# Matriz de confusão
cm = confusion_matrix(base_teste.classes, previsoes2)
sns.heatmap(cm, annot=True)
