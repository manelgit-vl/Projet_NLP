import pandas as pd
import os

csv_path = "../tfidf_vectors.csv"
output_dir = "../parquet_chunks"
chunk_size = 100000

# Créer un dossier pour stocker les fichiers par lot
os.makedirs(output_dir, exist_ok=True)

print("📦 Conversion CSV → Parquet en plusieurs fichiers...")

for i, chunk in enumerate(pd.read_csv(csv_path, chunksize=chunk_size)):
    file_path = os.path.join(output_dir, f"tfidf_vectors_part_{i+1}.parquet")
    print(f"💾 Sauvegarde : {file_path}")
    chunk.to_parquet(file_path, index=False, engine='pyarrow')

print("✅ Tous les fichiers parquet individuels sont créés.")
