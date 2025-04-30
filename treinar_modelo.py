import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib

# Carregar os dados
df = pd.read_csv('personagens.csv')

# Separar características e rótulos (usando as colunas R, G, B diretamente)
X = df[['R', 'G', 'B']]
y = df['Classe']

# Codificar os rótulos para valores numéricos
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Criar e treinar o modelo
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Fazer previsões no conjunto de teste
y_pred = modelo.predict(X_test)
print("Acurácia:", accuracy_score(y_test, y_pred))
print("Relatório de Classificação:\n", classification_report(y_test, y_pred, target_names=label_encoder.classes_))

# Salvar o modelo
joblib.dump(modelo, 'modelo_personagens.pkl')
print("Modelo salvo como modelo_personagens.pkl")

# Salvar o LabelEncoder
joblib.dump(label_encoder, 'label_encoder.pkl')
print("LabelEncoder salvo como label_encoder.pkl")