import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.title("🔍 Test API Métiers (DEBUG)")

metier = st.text_input("Nom du métier :")

if st.button("Rechercher") and metier:
    url = f"{API_BASE}/metier/{metier}"
    st.write(f"URL appelée : {url}")

    try:
        response = requests.get(url)
        st.write("Statut HTTP :", response.status_code)
        st.subheader("📦 Contenu brut")
        st.json(response.json())
    except Exception as e:
        st.error(f"Erreur de requête : {e}")
