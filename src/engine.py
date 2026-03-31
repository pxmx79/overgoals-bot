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
        Calcola la componente basata sui trend storici.
        """

        cfg = self.config["historical_data"]["weights"]

        over25 = match.get("over25_trend", 0)
        over15ht = match.get("over15ht_trend", 0)
        btts = match.get("btts_trend", 0)
        avg_goals = match.get("avg_goals", 0)
        vol = match.get("goals_volatility", 0)

        score = (
            over25 * cfg["over25_trend"] +
            over15ht * cfg["over15ht_trend"] +
            btts * cfg["btts_trend"] +
            avg_goals * cfg["avg_goals"] +
            vol * cfg["goals_volatility"]
        )

        return round(score, 3)

    # ============================================================
    #   FIRST HALF ENGINE (OSS_1T) — Step 3
    # ============================================================
    def compute_first_half_strength(self, match):
        """
        Calcola la componente del primo tempo (Over 0.5 HT).
        """

        cfg = self.config["markets"]["over_05_ht"]["weights"]

        trend_o05ht = match.get("trend_o05ht", 0)
        xg_first_half = match.get("xg_first_half", 0)
        h2h_first_half_goals = match.get("h2h_first_half_goals", 0)

        score = (
            trend_o05ht * cfg["trend_o05ht"] +
            xg_first_half * cfg["xg_first_half"] +
            h2h_first_half_goals * cfg["h2h_first_half_goals"]
        )

        return round(score, 3)

    # ============================================================
    #   OFFENSIVE STRENGTH (OSS) — Step 5
    # ============================================================
    def compute_offensive_strength(self, match):
        """
        Calcola la forza offensiva generale.
        """

        cfg = self.config["advanced_stats"]["weights"]

        xg_for = match.get("xg_for", 0)
        shots = match.get("shots", 0)
        dangerous_attacks = match.get("dangerous_attacks", 0)
        pace = match.get("pace_factor", 0)
        ppda = match.get("ppda", 0)

        score = (
            xg_for * cfg["xg_for"] +
            shots * cfg["shots"] +
            dangerous_attacks * cfg["dangerous_attacks"] +
            pace * cfg["pace_factor"] +
            ppda * cfg["ppda"]
        )

        return round(score, 3)

    # ============================================================
    #   DEFENSIVE LEAK SCORE (DLS) — Step 6
    # ============================================================
    def compute_defensive_leak(self, match):
        """
        Calcola la vulnerabilità difensiva.
        """

        cfg = self.config["advanced_stats"]["weights"]

        xga = match.get("xg_against", 0)
        shots_conceded = match.get("shots_conceded", 0)
        goals_conceded_avg = match.get("goals_conceded_avg", 0)
        btts_trend = match.get("btts_trend", 0)
        ppda = match.get("ppda", 0)

        score = (
            xga * cfg["xg_against"] +
            shots_conceded * cfg["shots_conceded"] +
            goals_conceded_avg +
            (btts_trend * 0.50) +
            ((1 - ppda) * cfg["ppda"])
        )

        return round(score, 3)

    # ============================================================
    #   VOLATILITY ENGINE — Step 7
    # ============================================================
    def compute_volatility(self, match):
        """
        Calcola la volatilità attesa del match.
        """

        h2h_avg = match.get("h2h_goals_avg", 0)
        pace = match.get("pace_factor", 0)
        vol = match.get("goals_volatility", 0)

        score = (
            h2h_avg * 0.50 +
            pace * 0.30 +
            vol * 0.60
        )

        return round(score, 3)

    # ============================================================
    #   MARKET CONFIRMATION — Step 8
    # ============================================================
    def compute_market_confirmation(self, match):
        """
        Analizza i segnali del mercato:
        - drop percentuale della quota Over 2.5
        - Asian line shift
        - money flow
        """

        cfg = self.config["market_intelligence"]

        drop_percent = match.get("over25_drop_percent", 0)
        asian_shift = match.get("asian_line_shift", 0)
        money_flow = match.get("money_flow_over", 0)

        score = 0.0

        if drop_percent >= cfg["min_over25_drop_percent"]:
            score += drop_percent * cfg["weights"]["odds_drop"]

        score += asian_shift * cfg["weights"]["asian_line_shift"]

        if money_flow >= 0.60:
            score += cfg["weights"]["money_flow"]

        return round(score, 3)

    # ============================================================
    #   AI PREDICTION LAYER — Step 9
    # ============================================================
    def compute_ai_prediction(self, match):
        """
        Mini-modello predittivo che combina:
        - xG for
        - Over25 trend
        - BTTS trend
        - differenza xG
        - volatilità
        """

        xg_for = match.get("xg_for", 0)
        xg_against = match.get("xg_against", 0)
        over25_trend = match.get("over25_trend", 0)
        btts_trend = match.get("btts_trend", 0)
        vol = match.get("goals_volatility", 0)

        score = (
            xg_for * 0.40 +
            over25_trend * 0.25 +
            btts_trend * 0.15 +
            (xg_for - xg_against) * 0.10 +
            vol * 0.10
        )

        return round(score, 3)

    # ============================================================
    #   TOTAL SCORE (Formula Finale)
    # ============================================================
    def compute_total_score(self, match):
        """
        Combina tutti i moduli secondo i pesi nel JSON.
        """

        cfg = self.config["scoring_formula"]["weights"]

        oss_1t = self.compute_first_half_strength(match)
        trends = self.compute_trends(match)
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
