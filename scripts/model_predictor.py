import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

print("📥 Chargement du fichier CSV...")
df = pd.read_csv("job_descriptions_clean.csv")

print("🧽 Nettoyage des données (suppression des lignes vides)...")
df = df.dropna(subset=["clean_description", "Job Title"])

print(f"📊 Nombre de lignes après nettoyage : {len(df)}")

print("🧾 Préparation des features et des labels...")
X = df["clean_description"]
y = df["Job Title"]

print("✏️ Vectorisation TF-IDF (max_features=1000)...")
vectorizer = TfidfVectorizer(max_features=1000)
X_vec = vectorizer.fit_transform(X)

print("✂️ Séparation des données en train/test...")
X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, stratify=y)

print(f"✅ Données d'entraînement : {X_train.shape[0]} lignes")
print(f"✅ Données de test : {X_test.shape[0]} lignes")

print("🧠 Entraînement du modèle LogisticRegression...")
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

print("🔍 Prédiction sur les données de test...")
y_pred = model.predict(X_test)

print("📊 Rapport de classification :")
print(classification_report(y_test, y_pred))

print("✅ Modèle entraîné et évalué avec succès.")
