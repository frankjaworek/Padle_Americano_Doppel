import streamlit as st
import json
import os
import random

# --- Konfiguration ---
DATA_FILE = "padel_turnier_daten.json"
DEFAULT_PLAYERS = ["Regina", "Glennn", "Silvia", "Ben", "Frank", "Alex", "Ralf", "Teresa", "Thomas", "Vera", "Julia", "Luca"]

# --- Hilfsfunktionen für Daten ---
def init_state():
    if 'data' not in st.session_state:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                st.session_state.data = json.load(f)
        else:
            st.session_state.data = {
                "names": DEFAULT_PLAYERS.copy(),
                "scores": {name: [0]*100 for name in DEFAULT_PLAYERS},
                "inputs": {},
                "t2_labels": {},
                "max_points": 24,
                "total_rounds": 6,
                "manual_court_count": 3,
                "extra_matches": []
            }
        st.session_state.current_round = 1

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.data, f)

init_state()

# --- Logik: Matrix Generierung ---
def generate_matches():
    n = len(st.session_state.data["names"])
    courts = st.session_state.data["manual_court_count"]
    matches = []
    # Hier fügst du deine generate_static_matrix Logik ein:
    # (Ich habe hier einen Platzhalter für die 12-Spieler-Matrix gelassen)
    random.seed(42)
    # ... Logik wie in deinem Original ...
    return matches

# --- UI Screens ---
def screen_menu():
    st.title("Padel City Americano")
    st.write(f"Aktuell: {len(st.session_state.data['names'])} Spieler")
    if st.button("Spielplan & Eingabe"): st.session_state.page = "plan"; st.rerun()
    if st.button("Rangliste"): st.session_state.page = "rank"; st.rerun()
    if st.button("Einstellungen"): st.session_state.page = "settings"; st.rerun()

def screen_plan():
    st.header("Spielplan")
    if st.button("Zurück"): st.session_state.page = "menu"; st.rerun()
    
    round_sel = st.number_input("Spiel:", 1, st.session_state.data["total_rounds"], st.session_state.current_round)
    
    # Beispiel für die Spiel-Boxen
    st.subheader(f"Runde {round_sel}")
    # Hier Iteration über matches und st.text_input für Punkte, wie im Original
    pts = st.text_input("T1 Punkte:")
    if st.button("Ergebnis speichern"):
        # Speichere die Punkte in st.session_state.data["inputs"]
        save_data()
        st.success("Gespeichert!")

def screen_rank():
    st.header("Live-Rangliste")
    if st.button("Zurück"): st.session_state.page = "menu"; st.rerun()
    # Hier die Tabellen-Logik aus deinem Original (sorted_players)
    st.write("Rangliste wird hier angezeigt...")

def screen_settings():
    st.header("Konfiguration")
    if st.button("Zurück"): st.session_state.page = "menu"; st.rerun()
    # Hier die Inputs aus deiner render_configuration_inputs Funktion
    if st.button("Turnier zurücksetzen"):
        # Logik zum Resetten
        save_data()
        st.rerun()

# --- Router ---
if 'page' not in st.session_state: st.session_state.page = "menu"

if st.session_state.page == "menu": screen_menu()
elif st.session_state.page == "plan": screen_plan()
elif st.session_state.page == "rank": screen_rank()
elif st.session_state.page == "settings": screen_settings()
