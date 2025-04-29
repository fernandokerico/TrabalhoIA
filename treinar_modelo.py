import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib  # para salvar o modelo

# Carregar os dados
df = pd.read_csv('personagens.csv')

# Separar características e rótulos
X = df[['R', 'G', 'B']]
y = df['Classe']

# Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Criar e treinar o modelo
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_train, y_train)

# Avaliar o modelo
y_pred = modelo.predict(X_test)
print("Acurácia:", accuracy_score(y_test, y_pred))
print("Relatório de Classificação:\n", classification_report(y_test, y_pred))

# Salvar o modelo
joblib.dump(modelo, 'modelo_personagens.pkl')
print("Modelo salvo como modelo_personagens.pkl")
