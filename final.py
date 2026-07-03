from tkinter import messagebox, ttk
import json
import os
import random

# Standard-Startliste (12 Spieler)
DEFAULT_PLAYERS = ["Regina", "Glennn", "Silvia", "Ben", "Frank", "Alex", "Ralf", "Teresa", "Thomas", "Vera", "Julia", "Luca"]
DATA_FILE = "padel_turnier_daten.json"
DEFAULT_MAX_POINTS = 24  # Standardwert, falls nichts gespeichert ist

# PadelCity Farbpalette (mit lila Akzent)
COLOR_NAVY = "#101C33"      # Hauptfarbe / Tiefer Hintergrund
COLOR_TEAL = "#AE0CBB"      # Wunsch-Farbton (Lila/Magenta)
COLOR_DARK = "#1F2E4D"      # Sekundäres Dunkelblau
COLOR_LIGHT = "#F8F9FA"     # Heller App-Hintergrund
COLOR_WHITE = "#FFFFFF"     # Reines Weiß
COLOR_GRAY = "#E5E7EB"      # Sanftes Grau für Boxen
COLOR_TEXT_DARK = "#0F172A" # Gut lesbarer, fast schwarzer Text

# Übersetzungs-Wörterbuch (Localization Dictionary)
LANG_DICT = {
    "de": {
        "menu_title": "Padel City\nAmericano Doppel",
        "menu_info": "Aktuell: {} Spieler ({} Plätze)\nMaximal {} Punkte pro Spiel | Spiele: {}",
        "btn_plan": "Spielplan & Eingabe",
        "btn_rank": "Live-Rangliste",
        "btn_settings": "Spieler & Einstellungen",
        "header_plan": "Spielplan",
        "header_rank": "Live-Rangliste",
        "header_settings": "Konfiguration",
        "lbl_game": "Spiel:",
        "btn_add_game": "+ Spiel",
        "lbl_t1_pts": "T1 Punkte:",
        "btn_save_res": "Ergebnis speichern",
        "rank_col_rank": "Rang",
        "rank_col_player": "Spieler",
        "rank_col_pts": "Punkte",
        "box_players": " Anzahl Spieler ",
        "box_courts": " Anzahl Courts / Plätze ",
        "box_rules": " Spiel-Regeln ",
        "box_lang": " Sprache / Language ",
        "lbl_max_pts": "Max. Punkte pro Match:",
        "box_court_names": " Courts ",
        "box_player_names": " Mitspieler ",
        "btn_save_settings": "Änderungen speichern",
        "btn_reset_tournament": "Turnier komplett zurücksetzen",
        "msg_error_num": "Bitte eine Zahl eingeben!",
        "msg_error_pts_range": "Punkte müssen zwischen 0 und {} liegen!",
        "msg_error_empty_name": "Namen dürfen nicht leer sein!",
        "msg_error_min_players": "Ein Doppel-Turnier benötigt mindestens 4 Spieler!",
        "msg_error_min_courts": "Es muss mindestens 1 Court existieren!",
        "msg_ask_reset": "Möchtest du das Turnier neu starten und alle alten Ergebnisse löschen?",
        "msg_ask_reset_title": "Turnier neu starten?",
        "msg_success_saved": "Spiel {} gespeichert!",
        "msg_success_gen": "Spiel {}: Zufällige Teams generiert!",
        "msg_success_settings": "Einstellungen, Courts und Namen wurden aktualisiert!",
        "msg_success_reset": "Neues Turnier mit {} Courts gestartet!",
        "no_matches": "Keine Spiele in dieser Runde für die\naktuelle Platzeinstellung verfügbar.",
        "msg_error_title": "Fehler",
        "msg_success_title": "Erfolg",
        "msg_warn_title": "Achtung"
    },
    "en": {
        "menu_title": "Padel City\nAmericano Doubles",
        "menu_info": "Current: {} Players ({} Courts)\nMaximum {} Points per Game | Games: {}",
        "btn_plan": "Match Schedule & Input",
        "btn_rank": "Live Leaderboard",
        "btn_settings": "Players & Settings",
        "header_plan": "Match Schedule",
        "header_rank": "Live Leaderboard",
        "header_settings": "Configuration",
        "lbl_game": "Game:",
        "btn_add_game": "+ Game",
        "lbl_t1_pts": "T1 Points:",
        "btn_save_res": "Save Result",
        "rank_col_rank": "Rank",
        "rank_col_player": "Player",
        "rank_col_pts": "Points",
        "box_players": " Number of Players ",
        "box_courts": " Number of Courts ",
        "box_rules": " Game Rules ",
        "box_lang": " Language / Sprache ",
        "lbl_max_pts": "Max. Points per Match:",
        "box_court_names": " Courts ",
        "box_player_names": " Players ",
        "btn_save_settings": "Save Changes",
        "btn_reset_tournament": "Completely Reset Tournament",
        "msg_error_num": "Please enter a valid number!",
        "msg_error_pts_range": "Points must be between 0 and {}!",
        "msg_error_empty_name": "Names cannot be empty!",
        "msg_error_min_players": "A doubles tournament requires at least 4 players!",
        "msg_error_min_courts": "At least 1 court must exist!",
        "msg_ask_reset": "Do you want to restart the tournament and delete all old results?",
        "msg_ask_reset_title": "Restart Tournament?",
        "menu_btn_back": "< Menu",
        "msg_success_saved": "Game {} saved!",
        "msg_success_gen": "Game {}: Random teams generated!",
        "msg_success_settings": "Settings, courts and names have been updated!",
        "msg_success_reset": "New tournament started with {} courts!",
        "no_matches": "No matches available in this round for the\ncurrent court settings.",
        "msg_error_title": "Error",
        "msg_success_title": "Success",
        "msg_warn_title": "Warning"
    }
}

class PadelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Padel City Americano")
        self.root.geometry("420x750")
        self.root.configure(bg=COLOR_LIGHT)
        
        # Interne Variablen initialisieren
        self.total_rounds = 6
        self.extra_matches = []  
        self.manual_court_count = None  
        self.lang = "de"  
        
        # Daten laden oder neu erstellen
        self.load_data()
        self.current_selected_round = 1
        
        # Haupt-Container für den wechselnden Inhalt
        self.main_container = tk.Frame(self.root, bg=COLOR_LIGHT)
        self.main_container.pack(fill="both", expand=True)
        
        # Feste Taskleiste ganz unten platzieren
        self.create_footer()
        
        # Ersten Bildschirm laden
        self.create_menu_screen()

    def t(self, key):
        return LANG_DICT[self.lang].get(key, LANG_DICT["de"].get(key, key))

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    saved = json.load(f)
                    self.player_names = saved.get("names", DEFAULT_PLAYERS.copy())
                    self.players_scores = saved.get("scores", {name: [0]*100 for name in self.player_names})
                    self.inputs = saved.get("inputs", {})
                    self.t2_labels = saved.get("t2_labels", {})
                    self.max_match_points = saved.get("max_points", DEFAULT_MAX_POINTS)
                    self.total_rounds = saved.get("total_rounds", 6)
                    self.extra_matches = saved.get("extra_matches", [])
                    self.manual_court_count = saved.get("manual_court_count", len(self.player_names) // 4)
                    self.lang = saved.get("lang", "de")
                    
                    for name in self.player_names:
                        if name not in self.players_scores:
                            self.players_scores[name] = [0] * 100
                        elif len(self.players_scores[name]) < 100:
                            self.players_scores[name].extend([0] * (100 - len(self.players_scores[name])))
                    
                    default_courts = [f"Platz {i}" for i in range(1, self.manual_court_count + 1)]
                    self.court_names = saved.get("courts", default_courts)
                    
                    if len(self.court_names) != self.manual_court_count:
                        self.court_names = [f"Platz {i}" for i in range(1, self.manual_court_count + 1)]
                    return
            except:
                pass
        
        self.player_names = DEFAULT_PLAYERS.copy()
        self.players_scores = {name: [0]*100 for name in self.player_names}
        self.inputs = {}
        self.t2_labels = {}
        self.max_match_points = DEFAULT_MAX_POINTS
        self.total_rounds = 6
        self.extra_matches = []
        self.manual_court_count = len(self.player_names) // 4
        self.court_names = [f"Platz {i}" for i in range(1, self.manual_court_count + 1)]
        self.lang = "de"

    def save_to_file(self):
        with open(DATA_FILE, "w") as f:
            json.dump({
                "names": self.player_names,
                "scores": self.players_scores,
                "inputs": self.inputs,
                "t2_labels": self.t2_labels,
                "courts": self.court_names,
                "max_points": self.max_match_points,
                "total_rounds": self.total_rounds,
                "extra_matches": self.extra_matches,
                "manual_court_count": self.manual_court_count,
                "lang": self.lang
            }, f)

    def generate_static_matrix(self):
        n = len(self.player_names)
        courts = self.manual_court_count
        matches = []
        
        if n == 12 and courts == 3:
            matrix_12 = [
                {"r": 1, "c": 1, "p": [0, 1, 2, 3]},  {"r": 1, "c": 2, "p": [4, 5, 6, 7]},  {"r": 1, "c": 3, "p": [8, 9, 10, 11]},
                {"r": 2, "c": 1, "p": [0, 4, 8, 1]},  {"r": 2, "c": 2, "p": [2, 5, 9, 6]},  {"r": 2, "c": 3, "p": [3, 7, 10, 11]},
                {"r": 3, "c": 1, "p": [0, 2, 7, 10]}, {"r": 3, "c": 2, "p": [1, 5, 8, 11]}, {"r": 3, "c": 3, "p": [3, 4, 6, 9]},
                {"r": 4, "c": 1, "p": [0, 5, 3, 6]},  {"r": 4, "c": 2, "p": [1, 7, 9, 10]}, {"r": 4, "c": 3, "p": [2, 4, 8, 11]},
                {"r": 5, "c": 1, "p": [0, 9, 2, 11]}, {"r": 5, "c": 2, "p": [1, 4, 6, 10]}, {"r": 5, "c": 3, "p": [3, 5, 7, 8]},
                {"r": 6, "c": 1, "p": [0, 7, 5, 10]}, {"r": 6, "c": 2, "p": [1, 2, 4, 9]},  {"r": 6, "c": 3, "p": [3, 6, 8, 11]}
            ]
            for m in matrix_12:
                matches.append({
                    "runde": m["r"], "platz_idx": m["c"] - 1,
                    "p1": m["p"][0], "p2": m["p"][1], "p3": m["p"][2], "p4": m["p"][3]
                })
        else:
            random.seed(42)
            player_pool = list(range(n))
            for r in range(1, 7):
                round_pool = player_pool.copy()
                if r > 1:
                    random.shuffle(round_pool)
                for c in range(1, courts + 1):
                    if len(round_pool) >= 4:
                        matches.append({
                            "runde": r, "platz_idx": c - 1,
                            "p1": round_pool.pop(0), "p2": round_pool.pop(0),
                            "p3": round_pool.pop(0), "p4": round_pool.pop(0)
                        })
                    else:
                        break
                    
        for em in self.extra_matches:
            matches.append(em)
            
        return matches

    def add_custom_round(self):
        self.total_rounds += 1
        n = len(self.player_names)
        courts = self.manual_court_count
        
        pool = list(range(n))
        random.shuffle(pool)
        
        for c in range(1, courts + 1):
            if len(pool) >= 4:
                match_data = {
                    "runde": self.total_rounds,
                    "platz_idx": c - 1,
                    "p1": pool.pop(0),
                    "p2": pool.pop(0),
                    "p3": pool.pop(0),
                    "p4": pool.pop(0)
                }
                self.extra_matches.append(match_data)
            else:
                break
            
        self.save_to_file()
        
        lbl_game_txt = self.t("lbl_game").replace(":", "")
        self.round_chooser.config(values=[f"{lbl_game_txt} {i}" for i in range(1, self.total_rounds + 1)])
        self.round_chooser.set(f"{lbl_game_txt} {self.total_rounds}")
        self.current_selected_round = self.total_rounds
        self.update_arrow_buttons()
        self.display_matches_for_current_round()
        messagebox.showinfo(self.t("msg_success_title"), self.t("msg_success_gen").format(self.total_rounds))

    def prev_round(self):
        if self.current_selected_round > 1:
            self.current_selected_round -= 1
            lbl_game_txt = self.t("lbl_game").replace(":", "")
            self.round_chooser.set(f"{lbl_game_txt} {self.current_selected_round}")
            self.update_arrow_buttons()
            self.display_matches_for_current_round()

    def next_round(self):
        if self.current_selected_round < self.total_rounds:
            self.current_selected_round += 1
            lbl_game_txt = self.t("lbl_game").replace(":", "")
            self.round_chooser.set(f"{lbl_game_txt} {self.current_selected_round}")
            self.update_arrow_buttons()
            self.display_matches_for_current_round()

    def update_arrow_buttons(self):
        if self.current_selected_round <= 1:
            self.btn_prev.config(state="disabled", bg="#64748B")
        else:
            self.btn_prev.config(state="normal", bg=COLOR_NAVY)

        if self.current_selected_round >= self.total_rounds:
            self.btn_next.config(state="disabled", bg="#64748B")
        else:
            self.btn_next.config(state="normal", bg=COLOR_NAVY)

    def create_footer(self):
        footer = tk.Frame(self.root, bg=COLOR_NAVY, pady=6)
        footer.pack(fill="x", side="bottom")
        
        lbl_location = tk.Label(footer, text="For PadelCity Players\nFürth & Erlangen", font=("Arial", 10, "bold"), fg=COLOR_TEAL, bg=COLOR_NAVY, justify="center")
        lbl_location.pack(anchor="center")
        
        lbl_copyright = tk.Label(footer, text="© Frank Jaworek", font=("Arial", 8, "bold"), fg="#94A3B8", bg=COLOR_NAVY)
        lbl_copyright.pack(anchor="center", pady=(2, 0))

    def clear_main_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def create_menu_screen(self):
        self.clear_main_container()
        
        title = tk.Label(self.main_container, text=self.t("menu_title"), font=("Arial", 22, "bold"), fg=COLOR_NAVY, bg=COLOR_LIGHT, pady=25)
        title.pack()
        
        info_text = self.t("menu_info").format(len(self.player_names), self.manual_court_count, self.max_match_points, self.total_rounds)
        lbl_info = tk.Label(self.main_container, text=info_text, font=("Arial", 11, "italic"), fg="#64748B", bg=COLOR_LIGHT, justify="center")
        lbl_info.pack(pady=(0, 20))
        
        tk.Button(self.main_container, text=self.t("btn_plan"), font=("Arial", 13, "bold"), bg=COLOR_NAVY, fg=COLOR_WHITE, height=2, width=22, bd=0, cursor="hand2", command=self.create_plan_screen).pack(pady=8)
        tk.Button(self.main_container, text=self.t("btn_rank"), font=("Arial", 13, "bold"), bg=COLOR_TEAL, fg=COLOR_WHITE, height=2, width=22, bd=0, cursor="hand2", command=self.create_rank_screen).pack(pady=8)
        tk.Button(self.main_container, text=self.t("btn_settings"), font=("Arial", 13, "bold"), bg="#64748B", fg=COLOR_WHITE, height=2, width=22, bd=0, cursor="hand2", command=self.create_settings_screen).pack(pady=8)

    def create_plan_screen(self):
        self.clear_main_container()
        
        header = tk.Frame(self.main_container, bg=COLOR_NAVY, height=50)
        header.pack(fill="x")
        
        back_txt = "< Menü" if self.lang == "de" else "< Menu"
        tk.Button(header, text=back_txt, bg="#475569", fg=COLOR_WHITE, font=("Arial", 10, "bold"), bd=0, padx=10, command=self.create_menu_screen).pack(side="left", padx=10, pady=10)
        tk.Label(header, text=self.t("header_plan"), fg=COLOR_WHITE, bg=COLOR_NAVY, font=("Arial", 14, "bold")).pack(side="left", padx=15)
        
        filter_frame = tk.Frame(self.main_container, bg=COLOR_LIGHT, pady=10)
        filter_frame.pack(fill="x")
        
        tk.Label(filter_frame, text=self.t("lbl_game"), font=("Arial", 11, "bold"), fg=COLOR_TEXT_DARK, bg=COLOR_LIGHT).pack(side="left", padx=15)
        
        self.btn_prev = tk.Button(filter_frame, text=" < ", font=("Arial", 11, "bold"), bg=COLOR_NAVY, fg=COLOR_WHITE, bd=0, padx=8, command=self.prev_round)
        self.btn_prev.pack(side="left", padx=(5, 5))
        
        lbl_game_txt = self.t("lbl_game").replace(":", "")
        self.round_chooser = ttk.Combobox(filter_frame, values=[f"{lbl_game_txt} {i}" for i in range(1, self.total_rounds + 1)], state="readonly", width=9, font=("Arial", 11))
        self.round_chooser.set(f"{lbl_game_txt} {self.current_selected_round}")
        self.round_chooser.pack(side="left", padx=5)
        self.round_chooser.bind("<<ComboboxSelected>>", self.on_round_changed)
        
        self.btn_next = tk.Button(filter_frame, text=" > ", font=("Arial", 11, "bold"), bg=COLOR_NAVY, fg=COLOR_WHITE, bd=0, padx=8, command=self.next_round)
        self.btn_next.pack(side="left", padx=5)
        
        self.update_arrow_buttons()
        
        btn_add_round = tk.Button(filter_frame, text=self.t("btn_add_game"), font=("Arial", 10, "bold"), bg=COLOR_TEAL, fg=COLOR_WHITE, bd=0, padx=8, pady=3, command=self.add_custom_round)
        btn_add_round.pack(side="right", padx=15)
        
        center_wrapper = tk.Frame(self.main_container, bg=COLOR_LIGHT, padx=10)
        center_wrapper.pack(fill="both", expand=True)
        
        canvas = tk.Canvas(center_wrapper, highlightthickness=0, bg=COLOR_LIGHT)
        scrollbar = ttk.Scrollbar(center_wrapper, orient="vertical", command=canvas.yview)
        self.matches_container = tk.Frame(canvas, bg=COLOR_LIGHT)
        
        self.matches_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.matches_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")
        
        self.display_matches_for_current_round()

    def on_round_changed(self, event):
        self.current_selected_round = int(self.round_chooser.get().split(" ")[1])
        self.update_arrow_buttons()
        self.display_matches_for_current_round()

    def display_matches_for_current_round(self):
        for widget in self.matches_container.winfo_children():
            widget.destroy()
            
        dynamic_matches = self.generate_static_matrix()
        round_matches = [m for m in dynamic_matches if m["runde"] == self.current_selected_round]
        
        if not round_matches:
            tk.Label(self.matches_container, text=self.t("no_matches"), font=("Arial", 11, "italic"), fg="#64748B", bg=COLOR_LIGHT).pack(pady=30)
            return
            
        for m in round_matches:
            r, p_idx = m["runde"], m["platz_idx"]
            p1, p2, p3, p4 = self.player_names[m["p1"]], self.player_names[m["p2"]], self.player_names[m["p3"]], self.player_names[m["p4"]]
            court_title = self.court_names[p_idx] if p_idx < len(self.court_names) else f"Platz {p_idx + 1}"
            
            match_box = tk.LabelFrame(self.matches_container, text=f"  {court_title}  ", font=("Arial", 11, "bold"), fg=COLOR_TEAL, bg=COLOR_WHITE, bd=1, relief="solid", labelanchor="nw", padx=10, pady=8)
            match_box.pack(fill="x", pady=8, ipadx=5, expand=True)
            
            tk.Label(match_box, text=f"{p1} & {p2}  vs.  {p3} & {p4}", font=("Arial", 11, "bold"), fg=COLOR_TEXT_DARK, bg=COLOR_WHITE, justify="center").pack(pady=5, anchor="center")
            
            input_frame = tk.Frame(match_box, bg=COLOR_WHITE)
            input_frame.pack(anchor="center", pady=4)
            
            tk.Label(input_frame, text=self.t("lbl_t1_pts"), font=("Arial", 10), fg="#475569", bg=COLOR_WHITE).pack(side="left", padx=5)
            
            key = f"R{r}_C{p_idx + 1}"
            curr_val = self.inputs.get(key, "")
            
            inp = tk.Entry(input_frame, width=4, font=("Arial", 11, "bold"), justify="center", bd=1, relief="solid", bg=COLOR_LIGHT)
            if curr_val: inp.insert(0, curr_val)
            inp.pack(side="left", padx=5)
            
            t2_val = self.t2_labels.get(key, "-")
            lbl_t2 = tk.Label(input_frame, text=f"T2: {t2_val}", font=("Arial", 10, "bold"), fg=COLOR_NAVY, bg=COLOR_WHITE, width=6, anchor="w")
            lbl_t2.pack(side="left", padx=5)
            
            tk.Button(match_box, text=self.t("btn_save_res"), bg=COLOR_NAVY, fg=COLOR_WHITE, font=("Arial", 10, "bold"), bd=0, height=1,
                      command=lambda entry=inp, label=lbl_t2, round_num=r, court_num=p_idx + 1, names_tuple=(p1, p2, p3, p4): 
                      self.save_match(entry, label, round_num, court_num, names_tuple)).pack(fill="x", pady=4)

    def save_match(self, entry, label, r, c, names):
        val = entry.get().strip()
        if not val.isdigit():
            messagebox.showerror(self.t("msg_error_title"), self.t("msg_error_num"))
            return
        
        s1 = int(val)
        if not (0 <= s1 <= self.max_match_points):
            messagebox.showerror(self.t("msg_error_title"), self.t("msg_error_pts_range").format(self.max_match_points))
            return
            
        s2 = self.max_match_points - s1
        key = f"R{r}_C{c}"
        
        self.inputs[key] = val
        self.t2_labels[key] = str(s2)
        label.config(text=f"T2: {s2}")
        
        r_idx = r - 1
        for name in names:
            if name not in self.players_scores:
                self.players_scores[name] = [0]*100
                
        self.players_scores[names[0]][r_idx] = s1
        self.players_scores[names[1]][r_idx] = s1
        self.players_scores[names[2]][r_idx] = s2
        self.players_scores[names[3]][r_idx] = s2
        
        self.save_to_file()
        messagebox.showinfo(self.t("msg_success_title"), self.t("msg_success_saved").format(r))

    def create_rank_screen(self):
        self.clear_main_container()
        
        header = tk.Frame(self.main_container, bg=COLOR_TEAL, height=50)
        header.pack(fill="x")
        
        back_txt = "< Menü" if self.lang == "de" else "< Menu"
        tk.Button(header, text=back_txt, bg=COLOR_NAVY, fg=COLOR_WHITE, font=("Arial", 10, "bold"), bd=0, padx=10, command=self.create_menu_screen).pack(side="left", padx=10, pady=10)
        tk.Label(header, text=self.t("header_rank"), fg=COLOR_WHITE, bg=COLOR_TEAL, font=("Arial", 14, "bold")).pack(side="left", padx=15)
        
        canvas = tk.Canvas(self.main_container, highlightthickness=0, bg=COLOR_LIGHT)
        scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=canvas.yview)
        table_frame = tk.Frame(canvas, bg=COLOR_LIGHT, padx=10, pady=15)
        
        table_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=table_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")
        
        tk.Label(table_frame, text=self.t("rank_col_rank"), font=("Arial", 11, "bold"), fg=COLOR_NAVY, bg=COLOR_LIGHT, width=5, anchor="center").grid(row=0, column=0, pady=5)
        tk.Label(table_frame, text=self.t("rank_col_player"), font=("Arial", 11, "bold"), fg=COLOR_NAVY, bg=COLOR_LIGHT, width=14, anchor="w").grid(row=0, column=1, pady=5)
        tk.Label(table_frame, text=self.t("rank_col_pts"), font=("Arial", 11, "bold"), fg=COLOR_NAVY, bg=COLOR_LIGHT, width=8, anchor="center").grid(row=0, column=2, pady=5)
        
        tk.Canvas(table_frame, height=1, bg=COLOR_GRAY, bd=0, highlightthickness=0).grid(row=1, column=0, columnspan=3, sticky="we", pady=5)
        
        sorted_players = sorted(self.player_names, key=lambda x: sum(self.players_scores.get(x, [0])), reverse=True)
        
        for idx, player in enumerate(sorted_players, 1):
            total_p = sum(self.players_scores.get(player, [0]))
            bg_row = COLOR_WHITE if idx % 2 == 0 else COLOR_LIGHT
            
            if idx == 1: 
                text_color = "#D4AF37"
                display_name = f" * {player} *"
                rank_str = "1. *"
            elif idx == 2: 
                text_color = "#94A3B8"
                display_name = player
                rank_str = "2."
            elif idx == 3: 
                text_color = "#CD7F32"
                display_name = player
                rank_str = "3."
            else: 
                text_color = COLOR_TEXT_DARK
                display_name = player
                rank_str = f"{idx}."
            
            font_style = ("Arial", 11, "bold") if idx <= 3 else ("Arial", 11)
            
            row_frame = tk.Frame(table_frame, bg=bg_row, pady=2)
            row_frame.grid(row=idx+1, column=0, columnspan=3, sticky="we", pady=1)
            
            tk.Label(row_frame, text=rank_str, font=font_style, fg=text_color, bg=bg_row, width=5, anchor="center").pack(side="left")
            tk.Label(row_frame, text=display_name, font=font_style, fg=text_color, bg=bg_row, width=14, anchor="w").pack(side="left")
            tk.Label(row_frame, text=f"{total_p} P", font=font_style, fg=text_color, bg=bg_row, width=8, anchor="center").pack(side="left")

    def create_settings_screen(self):
        self.clear_main_container()
        
        header = tk.Frame(self.main_container, bg="#475569", height=50)
        header.pack(fill="x")
        
        back_txt = "< Menü" if self.lang == "de" else "< Menu"
        tk.Button(header, text=back_txt, bg=COLOR_NAVY, fg=COLOR_WHITE, font=("Arial", 10, "bold"), bd=0, padx=10, command=self.create_menu_screen).pack(side="left", padx=10, pady=10)
        tk.Label(header, text=self.t("header_settings"), fg=COLOR_WHITE, bg="#475569", font=("Arial", 14, "bold")).pack(side="left", padx=15)
        
        scroll_canvas = tk.Canvas(self.main_container, highlightthickness=0, bg=COLOR_LIGHT)
        scrollbar = ttk.Scrollbar(self.main_container, orient="vertical", command=scroll_canvas.yview)
        
        self.entries_frame = tk.Frame(scroll_canvas, bg=COLOR_LIGHT)
        self.entries_frame.bind("<Configure>", lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all")))
        scroll_canvas.create_window((0, 0), window=self.entries_frame, anchor="nw")
        scroll_canvas.configure(yscrollcommand=scrollbar.set)
        
        scroll_canvas.pack(side="left", fill="both", expand=True, padx=15, pady=5)
        scrollbar.pack(side="right", fill="y")
        
        self.render_configuration_inputs()

    def render_configuration_inputs(self):
        for widget in self.entries_frame.winfo_children():
            widget.destroy()
            
        # 1. Box: Spieleranzahl
        count_frame = tk.LabelFrame(self.entries_frame, text=self.t("box_players"), font=("Arial", 10, "bold"), fg=COLOR_NAVY, bg=COLOR_WHITE, bd=1, relief="solid", padx=8, pady=4)
        count_frame.pack(fill="x", pady=4)
        
        self.lbl_current_count = tk.Label(count_frame, text=f"{len(self.player_names)} " + ("Spieler" if self.lang == "de" else "Players"), font=("Arial", 11, "bold"), fg=COLOR_NAVY, bg=COLOR_WHITE)
        self.lbl_current_count.pack(side="left", padx=5)
        
        tk.Button(count_frame, text="- 4", font=("Arial", 9, "bold"), bg="#EF4444", fg=COLOR_WHITE, bd=0, width=4, command=self.decrease_players).pack(side="right", padx=2)
        tk.Button(count_frame, text="+ 4", font=("Arial", 9, "bold"), bg=COLOR_TEAL, fg=COLOR_WHITE, bd=0, width=4, command=self.increase_players).pack(side="right", padx=2)
        
        # 2. Box: Courtanzahl
        court_count_frame = tk.LabelFrame(self.entries_frame, text=self.t("box_courts"), font=("Arial", 10, "bold"), fg=COLOR_NAVY, bg=COLOR_WHITE, bd=1, relief="solid", padx=8, pady=4)
        court_count_frame.pack(fill="x", pady=4)
        
        self.lbl_court_count = tk.Label(court_count_frame, text=f"{self.manual_court_count} " + ("Courts" if self.lang == "en" else "Plätze"), font=("Arial", 11, "bold"), fg=COLOR_NAVY, bg=COLOR_WHITE)
        self.lbl_court_count.pack(side="left", padx=5)
        
        tk.Button(court_count_frame, text="- 1", font=("Arial", 9, "bold"), bg="#EF4444", fg=COLOR_WHITE, bd=0, width=4, command=self.decrease_courts).pack(side="right", padx=2)
        tk.Button(court_count_frame, text="+ 1", font=("Arial", 9, "bold"), bg=COLOR_TEAL, fg=COLOR_WHITE, bd=0, width=4, command=self.increase_courts).pack(side="right", padx=2)
        
        # 3. Box: Spielregeln (Maximale Punkte)
        points_frame = tk.LabelFrame(self.entries_frame, text=self.t("box_rules"), font=("Arial", 10, "bold"), fg=COLOR_NAVY, bg=COLOR_WHITE, bd=1, relief="solid", padx=8, pady=4)
        points_frame.pack(fill="x", pady=4)
        
        tk.Label(points_frame, text=self.t("lbl_max_pts"), font=("Arial", 9, "bold"), fg=COLOR_TEXT_DARK, bg=COLOR_WHITE).pack(side="left", padx=5)
        self.entry_max_points = tk.Entry(points_frame, width=5, font=("Arial", 10, "bold"), justify="center", bd=1, relief="solid", bg=COLOR_LIGHT)
        self.entry_max_points.insert(0, str(self.max_match_points))
        self.entry_max_points.pack(side="left", padx=5)
        
        # 4. Box: Sprachauswahl
        lang_frame = tk.LabelFrame(self.entries_frame, text=self.t("box_lang"), font=("Arial", 10, "bold"), fg=COLOR_NAVY, bg=COLOR_WHITE, bd=1, relief="solid", padx=8, pady=4)
        lang_frame.pack(fill="x", pady=4)
        
        self.lang_var = tk.StringVar(value=self.lang)
        rb_de = tk.Radiobutton(lang_frame, text="Deutsch", variable=self.lang_var, value="de", bg=COLOR_WHITE, fg=COLOR_TEXT_DARK, font=("Arial", 9, "bold"))
        rb_de.pack(side="left", padx=15)
        rb_en = tk.Radiobutton(lang_frame, text="English", variable=self.lang_var, value="en", bg=COLOR_WHITE, fg=COLOR_TEXT_DARK, font=("Arial", 9, "bold"))
        rb_en.pack(side="left", padx=15)

        # Container für das Zwei-Spalten Raster der Listen
        grid_container = tk.Frame(self.entries_frame, bg=COLOR_LIGHT)
        grid_container.pack(fill="x", pady=4)
        
        # LINKE SPALTE: Courts
        court_box = tk.LabelFrame(grid_container, text=self.t("box_court_names"), font=("Arial", 9, "bold"), fg=COLOR_TEAL, bg=COLOR_WHITE, bd=1, relief="solid", padx=4, pady=4)
        court_box.grid(row=0, column=0, sticky="nsnw", padx=(0, 3))
        
        self.court_entries = []
        for i in range(self.manual_court_count):
            row = tk.Frame(court_box, bg=COLOR_WHITE, pady=1)
            row.pack(fill="x")
            tk.Label(row, text=f"C{i+1}:", font=("Arial", 8, "bold"), fg=COLOR_TEXT_DARK, bg=COLOR_WHITE, width=3, anchor="w").pack(side="left")
            
            entry = tk.Entry(row, font=("Arial", 9), width=10, bd=1, relief="solid", bg=COLOR_LIGHT)
            current_name = self.court_names[i] if i < len(self.court_names) else f"Platz {i+1}"
            entry.insert(0, current_name)
            entry.pack(side="left", padx=2)
            self.court_entries.append(entry)
            
        # RECHTE SPALTE: Spieler
        player_box = tk.LabelFrame(grid_container, text=self.t("box_player_names"), font=("Arial", 9, "bold"), fg=COLOR_NAVY, bg=COLOR_WHITE, bd=1, relief="solid", padx=4, pady=4)
        player_box.grid(row=0, column=1, sticky="nsnw", padx=(3, 0))
        
        self.name_entries = []
        for i in range(len(self.player_names)):
            row = tk.Frame(player_box, bg=COLOR_WHITE, pady=1)
            row.pack(fill="x")
            tk.Label(row, text=f"P{i+1}:", font=("Arial", 8, "bold"), fg=COLOR_TEXT_DARK, bg=COLOR_WHITE, width=3, anchor="w").pack(side="left")
            
            entry = tk.Entry(row, font=("Arial", 9), width=12, bd=1, relief="solid", bg=COLOR_LIGHT)
            entry.insert(0, self.player_names[i])
            entry.pack(side="left", padx=2)
            self.name_entries.append(entry)
            
        # System-Buttons Frame
        btn_frame = tk.Frame(self.entries_frame, bg=COLOR_LIGHT)
        btn_frame.pack(fill="x", pady=10)
        
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        
        btn_save = tk.Button(btn_frame, text=self.t("btn_save_settings"), bg=COLOR_TEAL, fg=COLOR_WHITE, font=("Arial", 8, "bold"), height=2, bd=0, command=self.save_only_settings)
        btn_save.grid(row=0, column=0, sticky="we", padx=(0, 3))
                  
        btn_reset = tk.Button(btn_frame, text=self.t("btn_reset_tournament"), bg="#EF4444", fg=COLOR_WHITE, font=("Arial", 8, "bold"), height=2, bd=0, command=self.save_settings_and_reset)
        btn_reset.grid(row=0, column=1, sticky="we", padx=(3, 0))

    def increase_players(self):
        current_count = len(self.player_names)
        for i in range(1, 5):
            self.player_names.append(f"Spieler {current_count + i}" if self.lang == "de" else f"Player {current_count + i}")
        
        if self.manual_court_count == current_count // 4:
            self.manual_court_count = len(self.player_names) // 4
            self.lbl_court_count.config(text=f"{self.manual_court_count} " + ("Courts" if self.lang == "en" else "Plätze"))
            
        self.lbl_current_count.config(text=f"{len(self.player_names)} " + ("Spieler" if self.lang == "de" else "Players"))
        self.render_configuration_inputs()

    def decrease_players(self):
        if len(self.player_names) <= 4:
            messagebox.showwarning(self.t("msg_warn_title"), self.t("msg_error_min_players"))
            return
        current_count = len(self.player_names)
        self.player_names = self.player_names[:-4]
        
        if self.manual_court_count == current_count // 4:
            self.manual_court_count = max(1, len(self.player_names) // 4)
            self.lbl_court_count.config(text=f"{self.manual_court_count} " + ("Courts" if self.lang == "en" else "Plätze"))
            
        self.lbl_current_count.config(text=f"{len(self.player_names)} " + ("Spieler" if self.lang == "de" else "Players"))
        self.render_configuration_inputs()

    def increase_courts(self):
        self.manual_court_count += 1
        self.court_names.append(f"Platz {self.manual_court_count}" if self.lang == "de" else f"Court {self.manual_court_count}")
        self.lbl_court_count.config(text=f"{self.manual_court_count} " + ("Courts" if self.lang == "en" else "Plätze"))
        self.render_configuration_inputs()

    def decrease_courts(self):
        if self.manual_court_count <= 1:
            messagebox.showwarning(self.t("msg_warn_title"), self.t("msg_error_min_courts"))
            return
        self.manual_court_count -= 1
        self.court_names = self.court_names[:-1]
        self.lbl_court_count.config(text=f"{self.manual_court_count} " + ("Courts" if self.lang == "en" else "Plätze"))
        self.render_configuration_inputs()

    def save_only_settings(self):
        pts_val = self.entry_max_points.get().strip()
        if not pts_val.isdigit() or int(pts_val) <= 0:
            messagebox.showerror(self.t("msg_error_title"), self.t("msg_error_num"))
            return
            
        self.max_match_points = int(pts_val)
        self.lang = self.lang_var.get()  
        
        new_courts = []
        for entry in self.court_entries:
            c_name = entry.get().strip()
            if not c_name: c_name = (f"Platz {len(new_courts)+1}" if self.lang == "de" else f"Court {len(new_courts)+1}")
            new_courts.append(c_name)
        self.court_names = new_courts
            
        new_names = []
        old_names = self.player_names.copy()
        for entry in self.name_entries:
            name = entry.get().strip()
            if not name:
                messagebox.showerror(self.t("msg_error_title"), self.t("msg_error_empty_name"))
                return
            new_names.append(name)
            
        new_scores = {name: [0]*100 for name in new_names}
        for i, old_name in enumerate(old_names):
            if i < len(new_names):
                new_name = new_names[i]
                if old_name in self.players_scores:
                    new_scores[new_name] = self.players_scores[old_name]
                    
        self.player_names = new_names
        self.players_scores = new_scores
        
        self.save_to_file()
        messagebox.showinfo(self.t("msg_success_title"), self.t("msg_success_settings"))
        self.create_menu_screen()

    def save_settings_and_reset(self):
        pts_val = self.entry_max_points.get().strip()
        if not pts_val.isdigit() or int(pts_val) <= 0:
            messagebox.showerror(self.t("msg_error_title"), self.t("msg_error_num"))
            return
            
        if messagebox.askyesno(self.t("msg_ask_reset_title"), self.t("msg_ask_reset")):
            self.max_match_points = int(pts_val)
            self.lang = self.lang_var.get()  
            self.total_rounds = 6
            self.extra_matches = []
            
            new_courts = []
            for entry in self.court_entries:
                c_name = entry.get().strip()
                if not c_name: c_name = (f"Platz {len(new_courts)+1}" if self.lang == "de" else f"Court {len(new_courts)+1}")
                new_courts.append(c_name)
                
            new_names = []
            for entry in self.name_entries:
                name = entry.get().strip()
                if not name:
                    messagebox.showerror(self.t("msg_error_title"), self.t("msg_error_empty_name"))
                    return
                new_names.append(name)
            
            self.court_names = new_courts
            self.player_names = new_names
            self.players_scores = {name: [0]*100 for name in self.player_names}
            self.inputs = {}
            self.t2_labels = {}
            self.current_selected_round = 1
            
            self.save_to_file()
            messagebox.showinfo(self.t("msg_success_title"), self.t("msg_success_reset").format(self.manual_court_count))
            self.create_menu_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = PadelApp(root)
    root.mainloop()
