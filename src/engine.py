import json
import os

class ModelEngine:

    def __init__(self, config_path="./config/model_config.json"):
        """
        Carica automaticamente il file JSON di configurazione
        all’avvio del motore.
        """
        self.config = self.load_config(config_path)

    def load_config(self, path):
        """Legge e restituisce il file di configurazione JSON."""
        with open(path, "r") as f:
            return json.load(f)

    # ============================================================
    #   TRENDS & HISTORICAL MODULE (Step 4)
    # ============================================================
    def compute_trends(self, match):
        """
        Calcola la componente basata sui trend storici:
        - Over 2.5 trend
        - Over 1.5 HT trend
        - BTTS trend
        - Media gol
        - Volatilità gol
        """

        cfg = self.config["historical_data"]["weights"]

        # Ottieni i valori dal match (default 0 se assenti)
        over25 = match.get("over25_trend", 0)
        over15ht = match.get("over15ht_trend", 0)
        btts = match.get("btts_trend", 0)
        avg_goals = match.get("avg_goals", 0)
        vol = match.get("goals_volatility", 0)

        # Calcolo score pesato
        score = (
            over25 * cfg["over25_trend"] +
            over15ht * cfg["over15ht_trend"] +
            btts * cfg["btts_trend"] +
            avg_goals * cfg["avg_goals"] +
            vol * cfg["goals_volatility"]
        )

        return round(score, 3)

    # ============================================================
    #   FIRST HALF ENGINE (OSS_1T) — PRIORITARIO (Step 3)
    # ============================================================
    def compute_first_half_strength(self, match):
        """
        Calcola la forza offensiva pre-match per il primo tempo (OSS_1T).
        Modulo fondamentale per Over 0.5 HT.
        """

        cfg = self.config["markets"]["over_05_ht"]["weights"]

        # Estrarre i valori dal match (fallback 0)
        trend_o05ht = match.get("trend_o05ht", 0)                 # es: 0.72 = 72%
        xg_first_half = match.get("xg_first_half", 0)             # expected goals 1T
        h2h_first_half_goals = match.get("h2h_first_half_goals", 0)  # media gol 1T negli H2H

        # Calcolo punteggio pesato
        score = (
            trend_o05ht * cfg["trend_o05ht"] +
            xg_first_half * cfg["xg_first_half"] +
            h2h_first_half_goals * cfg["h2h_first_half_goals"]
        )

        return round(score, 3)

    # ============================================================
    #   OFFENSIVE STRENGTH (FULL MATCH) — Step 5
    # ============================================================
    def compute_offensive_strength(self, match):
        """
        Calcola la forza offensiva generale (xG, tiri, dangerous attacks).
        """
        # TODO: implementare nello Step 5
        return 0.0

    # ============================================================
    #   DEFENSIVE LEAK SCORE — Step 6
    # ============================================================
    def compute_defensive_leak(self, match):
        """
        Calcola la propensione a subire gol (xGA, tiri concessi...).
        """
        # TODO: implementare nello Step 6
        return 0.0

    # ============================================================
    #   VOLATILITY (MATCH-UP ENGINE) — Step 7
    # ============================================================
    def compute_volatility(self, match):
        """
        Analizza volatilità del match (H2H, ritmo, variabilità gol).
        """
        # TODO: implementare nello Step 7
        return 0.0

    # ============================================================
    #   MARKET CONFIRMATION (QUOTE) — Step 8
    # ============================================================
    def compute_market_confirmation(self, match):
        """
        Valuta l'effetto dei movimenti quota pre-match (drop, Asian line).
        """
        # TODO: implementare nello Step 8
        return 0.0

    # ============================================================
    #   AI PREDICTION LAYER — Step 9
    # ============================================================
    def compute_ai_prediction(self, match):
        """
        Placeholder per la logica AI.
        Verrà implementato verso la fine.
        """
        # TODO: implementare nello Step 9
        return 0.0

    # ============================================================
    #   TOTAL SCORE (Formula Finale)
    # ============================================================
    def compute_total_score(self, match):
        """
        Combina tutti i moduli secondo i pesi definiti nel JSON.
        È l'output principale del modello.
        """

        cfg = self.config["scoring_formula"]["weights"]

        # calcolo moduli
        oss_1t = self.compute_first_half_strength(match)
        oss = self.compute_offensive_strength(match)
        dls = self.compute_defensive_leak(match)
        vol = self.compute_volatility(match)
        mcs = self.compute_market_confirmation(match)
        ai  = self.compute_ai_prediction(match)

        total = (
            oss_1t * cfg["oss_1t"] +
            oss     * cfg["oss"] +
            dls     * cfg["dls"] +
            vol     * cfg["vol"] +
            mcs     * cfg["mcs"] +
            ai      * cfg["ai"]
        )

        return round(total, 3)
