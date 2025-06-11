import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from tqdm import tqdm
import os

input_path = "job_descriptions_clean.csv"
output_path = "../tfidf_vectors.csv"
chunk_size = 90000

# 🔁 Étape 1 – Apprentissage du vocabulaire
print("📌 Étape 1 : Construction du vocabulaire TF-IDF...")
vectorizer = TfidfVectorizer(max_features=1000)

texts_for_fit = []

for chunk in pd.read_csv(input_path, chunksize=chunk_size):
    texts_for_fit.extend(chunk["clean_description"].fillna("").astype(str).tolist())

vectorizer.fit(texts_for_fit)
print("✅ Vocabulaire appris.")

# 🔁 Étape 2 – Vectorisation et export par lot
print("📌 Étape 2 : Vectorisation des lots...")

if os.path.exists(output_path):
    os.remove(output_path)

batch_num = 0

for chunk in pd.read_csv(input_path, chunksize=chunk_size):
    print(f"🔁 Lot {batch_num + 1}")
    texts = chunk["clean_description"].fillna("").astype(str).tolist()
    tfidf_matrix = vectorizer.transform(texts)
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())
    tfidf_df.to_csv(output_path, mode='a', header=(batch_num == 0), index=False)
    batch_num += 1

print(f"✅ Vectorisation complète en {batch_num} lots. Résultat : {output_path}")
