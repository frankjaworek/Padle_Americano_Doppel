import streamlit as st
import pandas as pd
import json
import os

# Datei-Konfiguration
DATA_FILE = "turnier_daten.json"

# App-Titel
st.set_page_config(page_title="Padel City Americano", layout="centered")
st.title("🎾 Padel City Americano")

# Daten initialisieren
if not os.path.exists(DATA_FILE):
    # Hier werden die Daten aus deiner Excel-Struktur initialisiert
    data = {
        "scores": {player: 0 for player in ["Regina", "Glennn", "Silvia", "Ben", "Frank", "Alex", "Ralf", "Teresa", "Thomas", "Vera", "Julia", "Luca"]},
        "matches": []
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()

# Tabs für Navigation
tab1, tab2, tab3 = st.tabs(["Spielplan", "Rangliste", "Einstellungen"])

with tab1:
    st.subheader("Spielplan & Ergebnisse")
    # Beispiel für eine Spiel-Eingabe (du kannst dies dynamisch erweitern)
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.write("Regina & Glennn vs. Silvia & Ben")
    with col2:
        t1_pts = st.number_input("Punkte T1", 0, 24, key="m1")
    with col3:
        st.write(f"T2: {24 - t1_pts}")

with tab2:
    st.subheader("Live-Rangliste")
    df_rank = pd.DataFrame.from_dict(data["scores"], orient="index", columns=["Punkte"])
    st.table(df_rank.sort_values(by="Punkte", ascending=False))

with tab3:
    st.subheader("Turnier-Einstellungen")
    if st.button("Turnier zurücksetzen"):
        # Logik zum Reset
        st.warning("Alles gelöscht!")
