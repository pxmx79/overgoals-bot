import json
import os

class ModelEngine:

    def __init__(self, config_path="./config/model_config.json"):
        self.config = self.load_config(config_path)

    def load_config(self, path):
        with open(path, "r") as f:
            return json.load(f)

    # -------------------------------
    #   TRENDS & HISTORICAL MODULE
    # -------------------------------
    def compute_trends(self, match):
        # TODO: implementare logica
        return 0.0

    # -------------------------------
    #   FIRST HALF ENGINE (0.5 HT)
    # -------------------------------
    def compute_first_half_strength(self, match):
        # TODO: implementare logica
        return 0.0

    # -------------------------------
    #   OFFENSIVE STRENGTH (FULL)
    # -------------------------------
    def compute_offensive_strength(self, match):
        # TODO: implementare logica
        return 0.0

    # -------------------------------
    #   DEFENSIVE LEAK SCORE
    # -------------------------------
    def compute_defensive_leak(self, match):
        # TODO: implementare logica
        return 0.0

    # -------------------------------
    #   VOLATILITY (MATCH-UP ENGINE)
    # -------------------------------
    def compute_volatility(self, match):
        # TODO: implementare logica
        return 0.0

    # -------------------------------
    #   MARKET CONFIRMATION (QUOTE)
    # -------------------------------
    def compute_market_confirmation(self, match):
        # TODO: implementare logica
        return 0.0

    # -------------------------------
    #   AI PREDICTION LAYER
    # -------------------------------
    def compute_ai_prediction(self, match):
        # TODO: implementare logica
        return 0.0

    # -------------------------------
    #   CALCOLO FINALE (TOTAL SCORE)
    # -------------------------------
    def compute_total_score(self, match):
        cfg = self.config["scoring_formula"]["weights"]

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
``
