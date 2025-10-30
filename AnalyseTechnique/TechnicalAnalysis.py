import pandas as pd
import numpy as np
from AnalyseTechnique.IndicatorEvaluator import IndicatorEvaluator
from AnalyseTechnique.Utils import Utils


class TechnicalAnalysis:
    """Analyse technique des points d’entrée avec évaluation pondérée."""

    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol
        self.evaluator = IndicatorEvaluator()

    def run(self):
        try:
            data = Utils.fetch_data(self.ticker_symbol)
            data = Utils.compute_indicators(data)
        except Exception as e:
            return pd.DataFrame(), 0, f"❌ {e}"

        last = data.iloc[-1]
        ev = self.evaluator
        results = []

        # --- Conversion explicite en float ---
        rsi = float(last["RSI"].iloc[0])
        stoch_k = float(last["STOCH_K"].iloc[0])
        stoch_d = float(last["STOCH_D"].iloc[0])
        close = float(last["Close"].iloc[0])
        bb_l = float(last["BB_L"].iloc[0])
        bb_m = float(last["BB_M"].iloc[0])
        bb_h = float(last["BB_H"].iloc[0])
        macd_val = float(last["MACD"].iloc[0])
        signal_val = float(last["Signal"].iloc[0])
        obv = float(last["OBV"].iloc[0])
        ema200 = float(last["EMA200"].iloc[0])
        adx = float(last["ADX"].iloc[0])

        # print("\n=== Dernières valeurs techniques pour", self.ticker_symbol, "===")
        # print(f"RSI (14)           : {rsi:.2f}")
        # print(f"Stochastique K/D   : {stoch_k:.2f} / {stoch_d:.2f}")
        # print(f"Close              : {close:.2f}")
        # print(f"Bollinger Bands    : L={bb_l:.2f}, M={bb_m:.2f}, H={bb_h:.2f}")
        # print(f"MACD / Signal      : {macd_val:.4f} / {signal_val:.4f}")
        # print(f"OBV                : {obv:.2f}")
        # print(f"EMA200             : {ema200:.2f}")
        # print(f"ADX (14)           : {adx:.2f}")
        # print("============================================\n")

        # Évaluations
        results.append(self._make_row("RSI (14)", rsi, *ev.evaluate_rsi(rsi), ev.weights["RSI"]))
        results.append(self._make_row("Stochastique K/D", f"{stoch_k:.2f}/{stoch_d:.2f}",
                                    *ev.evaluate_stoch(stoch_k, stoch_d), ev.weights["Stochastique"]))
        results.append(self._make_row("Bandes de Bollinger", close,
                                    *ev.evaluate_bollinger(close, bb_l, bb_m, bb_h), ev.weights["Bollinger"]))
        results.append(self._make_row("MACD", macd_val,
                                    *ev.evaluate_macd(macd_val, signal_val), ev.weights["MACD"]))
        results.append(self._make_row("OBV", obv,
                                    *ev.evaluate_obv(data["OBV"].iloc[-5:].mean(), data["OBV"].iloc[-20:-5].mean()), ev.weights["OBV"]))
        results.append(self._make_row("Décote vs EMA200", f"{(close - ema200) / ema200 * 100:.2f}%",
                                    *ev.evaluate_ema200(close, ema200), ev.weights["EMA200"]))
        results.append(self._make_row("ADX (14)", adx,
                                    *ev.evaluate_adx(adx), ev.weights["ADX"]))

        df = pd.DataFrame(results)
        df["Score pondéré"] = df["Note (/10)"] * df["Poids (%)"] / 10
        score_total = df["Score pondéré"].sum()

        reco = IndicatorEvaluator._global_interpretation(df, score_total)

        # print(Utils.askMistralTechnicalAnalysis(rsi, macd_val, ema200, bb_l, bb_m, bb_h, stoch_k, stoch_d, obv, adx, close))
        print(f"Prix Actuel en bourse : {close}")
        return df, score_total, reco

    def _make_row(self, name, value, note, interp, weight):
        return {
            "Indicateur": name,
            "Valeur": f"{value:.2f}" if isinstance(value, (int, float, np.floating)) else str(value),
            "Note (/10)": note,
            "Poids (%)": weight,
            "Interprétation": interp,
        }