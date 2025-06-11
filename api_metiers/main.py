from fastapi import FastAPI, Depends, HTTPException
import json
from pathlib import Path
import pandas as pd
import glob
from difflib import get_close_matches

# 🔁 Étape 7 : gestion DB
from api_metiers.db import Question, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

# 🔁 Paramètres
CHUNK_SIZE = 100000
PARQUET_DIR = "parquet_chunks"

# 🔁 Session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔹 Charger les données du fichier JSON
json_path = Path("api_metiers/metiers_40_complet.json")
with json_path.open(encoding="utf-8") as f:
    metiers = json.load(f)

# 🔸 Route : infos métier
@app.get("/metier/{nom_metier}")
def get_metier(nom_metier: str):
    nom = nom_metier.strip().lower()
    all_keys = list(metiers.keys())
    all_keys_lower = [k.lower().strip() for k in all_keys]

    # Cherche correspondance exacte
    for i, key_lower in enumerate(all_keys_lower):
        if key_lower == nom:
            key = all_keys[i]
            return {
                "metier": key,
                "missions": metiers[key]["missions"],
                "competences": metiers[key]["competences"],
                "salaire_moyen": metiers[key].get("salaire_moyen", "Non renseigné")
            }

    # 🔍 Recherche approximative
    match = get_close_matches(nom, all_keys_lower, n=1, cutoff=0.7)
    if match:
        index = all_keys_lower.index(match[0])
        key = all_keys[index]
        return {
            "metier": key,
            "missions": metiers[key]["missions"],
            "competences": metiers[key]["competences"],
            "salaire_moyen": metiers[key].get("salaire_moyen", "Non renseigné"),
            "correction": f"Suggestion automatique pour '{nom_metier}'"
        }

    return {"message": f"Le métier '{nom_metier}' n’a pas été trouvé."}

# 🔸 Route : vecteur TF-IDF d'une ligne globale
@app.get("/vector/{index}")
def get_vector(index: int):
    part_num = index // CHUNK_SIZE + 1
    local_index = index % CHUNK_SIZE
    file_path = f"{PARQUET_DIR}/tfidf_vectors_part_{part_num}.parquet"

    if not Path(file_path).exists():
        return {"error": f"Fichier {file_path} introuvable."}

    df = pd.read_parquet(file_path)

    if local_index >= len(df):
        return {"error": f"Index {local_index} hors limites dans {file_path}"}

    return df.iloc[local_index].to_dict()

# 🔸 Route : top lignes où le mot a le score TF-IDF le plus élevé
@app.get("/mot/{mot}")
def top_lignes_pour_mot(mot: str, top_n: int = 5):
    results = []
    parquet_files = sorted(glob.glob(f"{PARQUET_DIR}/tfidf_vectors_part_*.parquet"))

    for part_num, file_path in enumerate(parquet_files, start=1):
        df = pd.read_parquet(file_path)

        if mot not in df.columns:
            continue

        top_indices = df[mot].nlargest(top_n)
        for local_index, score in top_indices.items():
            global_index = (part_num - 1) * CHUNK_SIZE + local_index
            results.append({
                "global_index": global_index,
                "score": round(score, 4),
                "chunk": part_num,
                "local_index": local_index
            })

    if not results:
        return {"message": f"Aucune ligne trouvée pour le mot '{mot}'."}

    results = sorted(results, key=lambda x: x["score"], reverse=True)[:top_n]

    return {
        "mot": mot,
        "top_resultats": results
    }

# 🔸 Route : retrouver le texte original d’un métier via son index global
@app.get("/texte/{index}")
def get_clean_description(index: int):
    try:
        df = pd.read_csv("job_descriptions_clean.csv", usecols=["clean_description"])
    except FileNotFoundError:
        return {"error": "Fichier job_descriptions_clean.csv introuvable."}
    except Exception as e:
        return {"error": f"Erreur lors du chargement du fichier : {str(e)}"}

    if index < 0 or index >= len(df):
        return {"error": f"Index {index} hors limites (max = {len(df)-1})"}

    return {
        "index": index,
        "description": df.iloc[index]["clean_description"]
    }

# ✅ Étape 7 : API BDD

@app.post("/save_question")
def save_question(texte: str, reponse: str, type_info: str, db: Session = Depends(get_db)):
    q = Question(texte=texte, reponse=reponse, type_info=type_info)
    db.add(q)
    db.commit()
    db.refresh(q)
    return {"message": "✅ Question enregistrée", "id": q.id}

@app.get("/list_questions")
def list_questions(db: Session = Depends(get_db)):
    return db.query(Question).all()

@app.delete("/delete_question/{id}")
def delete_question(id: int, db: Session = Depends(get_db)):
    q = db.query(Question).filter(Question.id == id).first()
    if not q:
        raise HTTPException(status_code=404, detail="Question introuvable")
    db.delete(q)
    db.commit()
    return {"message": f"❌ Question {id} supprimée"}
