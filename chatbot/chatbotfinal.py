import streamlit as st
import requests

# Configuration
API_BASE = "http://127.0.0.1:8000"
st.set_page_config(page_title="Assistant Emploi", page_icon="💼", layout="centered")

# Header
st.markdown("<h1 style='text-align: center;'>💼 Assistant Emploi - Métiers & Compétences</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Découvre les missions, compétences ou le salaire moyen d’un métier.</p>", unsafe_allow_html=True)

# Exemples
with st.expander("💡 Exemples de questions"):
    st.markdown("- compétences pour data analyst")
    st.markdown("- missions du développeur")
    st.markdown("- salaire pour chef de projet")

# Saisie
question = st.text_input("❓ Ta question", placeholder="ex: compétences pour data engineer")

if st.button("🔍 Rechercher") and question:
    with st.spinner("Recherche en cours..."):
        question_lower = question.lower()

        # Objectif
        if "compétence" in question_lower:
            objectif = "competences"
        elif "mission" in question_lower:
            objectif = "missions"
        elif "salaire" in question_lower:
            objectif = "salaire"
        else:
            st.warning("❗ Utilise 'compétences', 'missions' ou 'salaire'.")
            st.stop()

        # Extraction du métier
        for sep in ["du", "de", "d'", "pour"]:
            if sep in question_lower:
                metier = question_lower.split(sep)[-1].strip()
                break
        else:
            st.warning("❗ Précise un métier après 'de', 'du' ou 'pour'.")
            st.stop()

        # Appel API
        try:
            response = requests.get(f"{API_BASE}/metier/{metier}")
            data = response.json()
        except Exception:
            st.error("❌ Erreur lors de l'appel à l'API.")
            st.stop()

        metier_final = data.get("metier", metier)
        if "correction" in data:
            st.info(f"🔁 Suggestion automatique : **{metier_final}**")

        # Réponse affichée
        if objectif == "competences" and "competences" in data:
            st.success(f"🎓 Compétences pour **{metier_final}**")
            for c in data["competences"]:
                st.markdown(f"- {c}")
            reponse = "\n".join(data["competences"])

        elif objectif == "missions" and "missions" in data:
            st.success(f"📋 Missions de **{metier_final}**")
            for m in data["missions"]:
                st.markdown(f"- {m}")
            reponse = "\n".join(data["missions"])

        elif objectif == "salaire" and "salaire_moyen" in data:
            st.success(f"💰 Salaire moyen pour **{metier_final}**")
            st.markdown(f"**{data['salaire_moyen']}**")
            reponse = data["salaire_moyen"]
        else:
            st.warning(f"❌ Aucune information '{objectif}' pour **{metier_final}**.")
            reponse = "Aucune info."

        # Enregistrement API
        save = requests.post(f"{API_BASE}/save_question", params={
            "texte": question,
            "reponse": reponse,
            "type_info": objectif
        })

        if save.status_code == 200:
            st.success("✅ Question enregistrée dans la base.")
        else:
            st.warning("⚠️ Problème d’enregistrement.")
