import json
from engine import ModelEngine

# ================================================================
#   FUNZIONE: CARICA I DATI DELLE PARTITE (test dataset)
# ================================================================
def load_match_data(path="./tests/test_input.json"):
    with open(path, "r") as f:
        return json.load(f)

# ================================================================
#   GENERATORE SEGNALI
# ================================================================
def generate_signals():
    engine = ModelEngine()
    matches = load_match_data()

    signals = []

    for match in matches:

        # Calcolo dei moduli
        oss_1t = engine.compute_first_half_strength(match)
        trends = engine.compute_trends(match)
        oss = engine.compute_offensive_strength(match)
        dls = engine.compute_defensive_leak(match)
        vol = engine.compute_volatility(match)
        mcs = engine.compute_market_confirmation(match)
        ai = engine.compute_ai_prediction(match)

        total = engine.compute_total_score(match)

        # ============================================================
        #   APPLICAZIONE DELLE SOGLIE PER I SEGNALI
        # ============================================================

        mkt = match["markets"]

        output = {
            "match": f"{match['home']} – {match['away']}",
            "signals": []
        }

        # -------------------------
        #   Over 0.5 HT
        # -------------------------
        o05 = mkt["over_05_ht"]
        if (
            oss_1t >= o05["score_min"] and
            o05["odds_min"] <= match["odds_o05ht"] <= o05["odds_max"]
        ):
            output["signals"].append(f"🔥 Over 0.5 HT @{match['odds_o05ht']}")

        # -------------------------
        #   Over 1.5 HT
        # -------------------------
        o15 = mkt["over_15_ht"]
        if (
            oss >= o15["oss_min"] and
            vol >= o15["vol_min"] and
            o15["odds_min"] <= match["odds_o15ht"] <= o15["odds_max"]
        ):
            output["signals"].append(f"💥 Over 1.5 HT @{match['odds_o15ht']}")

        # -------------------------
        #   Over 2.5 FT
        # -------------------------
        o25 = mkt["over_25_ft"]
        if (
            total >= o25["total_min"] and
            o25["odds_min"] <= match["odds_o25"] <= o25["odds_max"]
        ):
            output["signals"].append(f"⚽ Over 2.5 FT @{match['odds_o25']}")

        # -------------------------
        #   BTTS
        # -------------------------
        btts_cfg = mkt["btts_ft"]
        if (
            dls >= btts_cfg["dls_min"] and
            oss >= btts_cfg["oss_min"] and
            btts_cfg["odds_min"] <= match["odds_btts"] <= btts_cfg["odds_max"]
        ):
            output["signals"].append(f"🔵 BTTS @{match['odds_btts']}")

        # Aggiungi score totali
        output["details"] = {
            "oss_1t": oss_1t,
            "trends": trends,
            "oss": oss,
            "dls": dls,
            "vol": vol,
            "mcs": mcs,
            "ai": ai,
            "total": total
        }

        signals.append(output)

    return signals


# ================================================================
#   ENTRYPOINT DI TEST
# ================================================================
if __name__ == "__main__":
    signals = generate_signals()
    for s in signals:
        print("\n===============================")
        print(f"🏆  {s['match']}")
        for sig in s["signals"]:
            print(sig)
        print("\n📊 Scores:")
        for k, v in s["details"].items():
            print(f"{k}: {v}")
``
