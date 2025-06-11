import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.title("🤖 Chatbot - Informations sur les postes")

st.markdown("Pose une question du type : `quelles sont les compétences du data analyst`, `missions du développeur`, `salaire pour data engineer`, etc.")

question = st.text_input("❓ Ta question :")

if st.button("Envoyer") and question:
    with st.spinner("🔄 Recherche en cours..."):

        question_lower = question.lower()

        if any(word in question_lower for word in ["compétence", "compétences"]):
            objectif = "competences"
        elif "mission" in question_lower:
            objectif = "missions"
        elif any(word in question_lower for word in ["salaire", "rémunération"]):
            objectif = "salaire"
        else:
            st.warning("❗ Je n’ai pas compris ta question. Essaie avec 'compétences', 'missions' ou 'salaire'.")
            st.stop()

        for separateur in ["du", "de", "d'", "pour"]:
            if separateur in question_lower:
                metier = question_lower.split(separateur)[-1].strip()
                break
        else:
            st.warning("❗ Précise un métier après 'du', 'de', ou 'pour'")
            st.stop()

        response = requests.get(f"{API_BASE}/metier/{metier}")
        if response.status_code != 200:
            st.error(f"❌ Erreur {response.status_code}")
            st.stop()

        data = response.json()
        metier_final = data.get("metier", metier)

        if "correction" in data:
            st.info(f"🔁 {data['correction']}")

        # Définir la réponse selon le type demandé
        if objectif == "competences" and "competences" in data:
            st.success(f"✅ Les compétences pour **{metier_final}** sont :")
            reponse_formatee = ""
            for comp in data["competences"]:
                st.markdown(f"- {comp}")
                reponse_formatee += f"- {comp}\n"

        elif objectif == "missions" and "missions" in data:
            st.success(f"📋 Les missions de **{metier_final}** sont :")
            reponse_formatee = ""
            for mission in data["missions"]:
                st.markdown(f"- {mission}")
                reponse_formatee += f"- {mission}\n"

        elif objectif == "salaire" and "salaire_moyen" in data:
            st.success(f"💰 Le salaire moyen pour **{metier_final}** est :")
            st.markdown(f"**{data['salaire_moyen']}**")
            reponse_formatee = str(data['salaire_moyen'])

        else:
            st.warning(f"Aucune information '{objectif}' trouvée pour {metier_final}.")
            reponse_formatee = "Aucune information trouvée."

        # Enregistrement en base de données
        params = {
            "texte": question,
            "reponse": reponse_formatee,
            "type_info": objectif
        }
        save_resp = requests.post(f"{API_BASE}/save_question", params=params)
        if save_resp.status_code == 200:
            st.success("📌 Question enregistrée dans la base de données.")
        else:
            st.warning("⚠️ Échec de l'enregistrement de la question.")
