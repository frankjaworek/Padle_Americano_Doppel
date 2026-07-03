import streamlit as st
import json
import os
import random

# --- Konfiguration & Daten ---
DATA_FILE = "padel_turnier_daten.json"
DEFAULT_PLAYERS = ["Regina", "Glennn", "Silvia", "Ben", "Frank", "Alex", "Ralf", "Teresa", "Thomas", "Vera", "Julia", "Luca"]

def init_session_state():
    if 'data' not in st.session_state:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                st.session_state.data = json.load(f)
        else:
            st.session_state.data = {
                "names": DEFAULT_PLAYERS.copy(),
                "scores": {name: [0]*100 for name in DEFAULT_PLAYERS},
                "max_points": 24,
                "total_rounds": 6,
                "manual_court_count": len(DEFAULT_PLAYERS) // 4
            }

init_session_state()

# --- Seiten-Navigation ---
st.sidebar.title("Padel City")
page = st.sidebar.radio("Navigation", ["Menü", "Spielplan", "Rangliste", "Einstellungen"])

# --- Menü-Seite ---
if page == "Menü":
    st.title("Padel City Americano")
    st.write(f"Spieler: {len(st.session_state.data['names'])} | Runden: {st.session_state.data['total_rounds']}")
    if st.button("Spielplan & Eingabe"):
        st.session_state.page = "plan"
        st.rerun()

# --- Spielplan-Seite ---
elif page == "Spielplan":
    st.header("Spielplan")
    round_sel = st.selectbox("Runde:", range(1, st.session_state.data["total_rounds"] + 1))
    
    # Beispiel für eine Spiel-Eingabe
    st.write(f"Spiele für Runde {round_sel}")
    with st.form("match_form"):
        p1_pts = st.number_input("T1 Punkte:", min_value=0, max_value=st.session_state.data["max_points"])
        if st.form_submit_button("Ergebnis speichern"):
            st.success("Ergebnis gespeichert!")
            # Hier müsste die Logik zum Schreiben in st.session_state.data["scores"] stehen

# --- Rangliste-Seite ---
elif page == "Rangliste":
    st.header("Live-Rangliste")
    ranking = sorted(st.session_state.data["names"], 
                     key=lambda x: sum(st.session_state.data["scores"].get(x, [0])), reverse=True)
    for i, player in enumerate(ranking, 1):
        score = sum(st.session_state.data["scores"].get(player, [0]))
        st.write(f"{i}. {player} - {score} Punkte")

# --- Einstellungsseite ---
elif page == "Einstellungen":
    st.header("Konfiguration")
    max_pts = st.number_input("Max. Punkte pro Match:", value=st.session_state.data["max_points"])
    if st.button("Speichern"):
        st.session_state.data["max_points"] = max_pts
        with open(DATA_FILE, "w") as f:
            json.dump(st.session_state.data, f)
        st.success("Einstellungen gespeichert!")
