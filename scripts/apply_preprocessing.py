import pandas as pd
import sys
import os
from tqdm import tqdm

# Initialiser tqdm
tqdm.pandas()

# Ajouter le dossier parent au path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
sys.path.insert(0, PROJECT_DIR)

from preprocessing.clean_text import clean_text, tokenize, lemmatize

# Pipeline de prétraitement
def preprocess_pipeline(text):
    if pd.isna(text):
        return ""
    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    lemmas = lemmatize(tokens)
    return " ".join(lemmas)

# Paramètres
input_path = "../job_descriptions.csv"
output_path = "../job_descriptions_clean.csv"
chunk_size = 10000  # Nombre de lignes par lot
batch_num = 0

# Supprimer ancien fichier de sortie s'il existe
if os.path.exists(output_path):
    os.remove(output_path)

# Traitement par lot
for chunk in pd.read_csv(input_path, chunksize=chunk_size):
    print(f"🔁 Traitement du lot {batch_num + 1}")
    chunk["clean_description"] = chunk["Job Description"].progress_apply(preprocess_pipeline)
    
    # Mode 'w' pour le premier lot, puis 'a' pour append
    mode = 'w' if batch_num == 0 else 'a'
    header = (batch_num == 0)
    chunk.to_csv(output_path, mode=mode, header=header, index=False)

    batch_num += 1

print(f"✅ Traitement terminé en {batch_num} lots. Résultat : {output_path}")
