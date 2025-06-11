# 🤖 Projet NLP – Analyse de Descriptions de Métiers

Ce projet NLP (Natural Language Processing) a été développé dans le cadre d’un module de formation pour automatiser l’analyse de descriptions de postes et faciliter l’interaction avec les données métiers via un chatbot.

---

## 🎯 Objectifs
- Nettoyer et vectoriser un corpus de descriptions de postes.
- Extraire les missions et compétences des métiers.
- Permettre à un utilisateur d’interroger les données via un chatbot.
- Déployer une API pour centraliser les requêtes.
- Prédire une estimation de salaire à l’aide du Machine Learning.

---

## ⚙️ Technologies utilisées
- Python
- FastAPI
- SQLite
- scikit-learn
- pandas / numpy / nltk
- Streamlit (ou terminal) pour le chatbot
- Git + GitHub

---

## 📁 Structure du projet

```
projet_NLP/
├── api_metiers/            # API FastAPI avec routes et base de données
│   ├── main.py             # Fichier principal de l'API
│   └── db.py               # Gestion de la base SQLite
│
├── chatbot/                # Scripts de chatbot (terminal et web)
│   ├── chatbot_essai.py
│   ├── chatbot_web.py
│   └── chatbootnv.py
│
├── preprocessing/          # Fonctions de nettoyage et préparation
│   └── clean_text.py
│
├── scripts/                # Traitements NLP et machine learning
│   ├── apply_preprocessing.py
│   ├── model_predictor.py
│   ├── vectorize_texts.py
│   └── vectors_csv_to_parquet.py
│
├── parquet_chunks/         # Données transformées en chunks parquet
│
├── job_descriptions_clean.csv   # Dataset nettoyé (peut être ignoré si gitignore actif)
├── questions.db                 # Base SQLite pour les questions utilisateur
├── tfidf_vectors.csv            # Fichier de représentation vectorielle
├── Etapes_Projet_NLP.pptx       # Présentation du projet
├── consignes projet1.png        # Instructions du projet
├── liens.txt / Liens de l.docx  # Références et liens API/dataset
└── README.md                    # Description du projet (ce fichier)
```

projet_NLP/
│
├── api_metiers/           # API FastAPI (routes métiers + BDD)
├── chatbot/               # Scripts chatbot terminal et web
├── preprocessing/         # Scripts de nettoyage
├── scripts/               # Vectorisation, ML, prédictions
├── job_descriptions.csv   # Dataset (ignoré si .gitignore actif)
├── questions.db           # Base SQLite pour sauvegarde
└── ...
```

---

## ▶️ Lancer le projet

### 1. Lancer l'API FastAPI
```bash
uvicorn api_metiers.main:app --reload
```
Accès à la doc Swagger : http://127.0.0.1:8000/docs

### 2. Lancer le chatbot (exemples)

#### En terminal :
```bash
python3 chatbot/chatbootnv.py
```

#### En Web (Streamlit) :
```bash
streamlit run chatbot/chatbot_web.py
```

---

## ✨ Résultats
- API fonctionnelle exposant des métiers + prédictions.
- Chatbot capable de répondre aux questions sur les métiers (Compétences, missions, salaires).
- Pipeline complet du traitement de texte à la prédiction.

---

## 📌 Auteure
**Ossama Louridi** 
**Manel Zerguit** 
