import yfinance as yf
import pandas as pd
import numpy as np
import ta
from colorama import Fore, Style


class TechnicalAnalysis:
    """
    Classe d'analyse technique orientée détection de points d’entrée (sous-évaluation technique).
    Fournit un score global et une interprétation claire basée sur plusieurs indicateurs.
    """

    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol

    def _to_series(self, data, col):
        """Convertit une colonne potentiellement multi-indexée en série simple."""
        if isinstance(data[col], pd.DataFrame):
            return data[col].iloc[:, 0].astype(float)
        else:
            return data[col].astype(float)

    def run(self):
        """Exécute l’analyse technique et renvoie le DataFrame, le score total et la recommandation."""
        try:
            data = yf.download(self.ticker_symbol, period="1y", interval="1d", auto_adjust=True, progress=False)
        except Exception as e:
            return pd.DataFrame(), 0, f"❌ Erreur de téléchargement des données : {e}"

        if data.empty:
            return pd.DataFrame(), 0, "❌ Données historiques non disponibles"

        # --- Normalisation des colonnes ---
        open_ = self._to_series(data, "Open")
        high = self._to_series(data, "High")
        low = self._to_series(data, "Low")
        close = self._to_series(data, "Close")
        volume = self._to_series(data, "Volume")

        # === Indicateurs principaux ===
        data["RSI"] = ta.momentum.RSIIndicator(close, 14).rsi()
        stoch = ta.momentum.StochasticOscillator(high=high, low=low, close=close, window=14, smooth_window=3)
        data["STOCH_K"], data["STOCH_D"] = stoch.stoch(), stoch.stoch_signal()
        macd = ta.trend.MACD(close)
        data["MACD"], data["Signal"] = macd.macd(), macd.macd_signal()
        data["OBV"] = ta.volume.OnBalanceVolumeIndicator(close, volume).on_balance_volume()
        bb = ta.volatility.BollingerBands(close, window=20, window_dev=2)
        data["BB_H"], data["BB_L"], data["BB_M"] = bb.bollinger_hband(), bb.bollinger_lband(), bb.bollinger_mavg()
        data["EMA200"] = ta.trend.EMAIndicator(close, 200).ema_indicator()
        data["ADX"] = ta.trend.ADXIndicator(high, low, close, window=14).adx()
        data["CCI"] = ta.trend.CCIIndicator(high, low, close, window=20).cci()

        data = data.dropna()
        if len(data) < 50:
            return pd.DataFrame(), 0, "❌ Données techniques insuffisantes"

        data = data.bfill().ffill()
        last = data.iloc[-1:]

        results = []

        # === RSI (survente = potentiel d’entrée fort) ===
        rsi = float(last["RSI"].iloc[0])
        if rsi < 25:
            note, interp = 10, "RSI très bas (<25) → Zone de capitulation : point d’entrée fort 🚀"
        elif rsi < 35:
            note, interp = 8, "RSI bas (<35) → Sous-évaluation probable : bonne opportunité"
        elif rsi < 45:
            note, interp = 6, "RSI modéré → marché encore fragile, surveiller un rebond"
        else:
            note, interp = 3, "RSI élevé → aucun signe de sous-évaluation"
        results.append({
            "Indicateur": "RSI (14)",
            "Valeur": f"{rsi:.2f}",
            "Note (/10)": note,
            "Poids (%)": 20,
            "Interprétation": interp
        })

        # === Stochastique ===
        stoch_k = float(last["STOCH_K"].iloc[0])
        stoch_d = float(last["STOCH_D"].iloc[0])
        if stoch_k < 20 and stoch_k > stoch_d:
            note, interp = 9, "Croisement haussier en zone survendue → signal d’entrée imminent"
        elif stoch_k < 20:
            note, interp = 8, "Zone de survente profonde → accumulation possible"
        elif 20 <= stoch_k <= 40:
            note, interp = 6, "Zone basse mais sans signal fort"
        else:
            note, interp = 3, "Zone neutre ou surachetée → pas de timing d’entrée"
        results.append({
            "Indicateur": "Stochastique K/D",
            "Valeur": f"{stoch_k:.2f}/{stoch_d:.2f}",
            "Note (/10)": note,
            "Poids (%)": 15,
            "Interprétation": interp
        })

        # === Bandes de Bollinger ===
        close_price = float(last["Close"].iloc[0])
        bb_low = float(last["BB_L"].iloc[0])
        bb_mid = float(last["BB_M"].iloc[0])
        bb_high = float(last["BB_H"].iloc[0])

        if close_price <= bb_low:
            note, interp = 10, "Prix sous la bande basse → excès de vente, excellent point d’entrée"
        elif close_price < (bb_mid - (bb_high - bb_low) * 0.2):
            note, interp = 8, "Prix dans le bas du canal → opportunité intéressante"
        elif close_price < bb_mid:
            note, interp = 6, "Prix légèrement sous la moyenne → possible rebond"
        else:
            note, interp = 3, "Prix proche du haut du canal → peu de marge"
        results.append({
            "Indicateur": "Bandes de Bollinger",
            "Valeur": f"{close_price:.2f}",
            "Note (/10)": note,
            "Poids (%)": 15,
            "Interprétation": interp
        })

        # === MACD ===
        macd_val = float(last["MACD"].iloc[0])
        signal_val = float(last["Signal"].iloc[0])
        if macd_val > signal_val and macd_val < 0:
            note, interp = 9, "Croisement haussier sous zéro → momentum en reprise"
        elif macd_val < 0:
            note, interp = 6, "MACD négatif → sous-évaluation possible mais signal non confirmé"
        else:
            note, interp = 4, "MACD positif → potentiel déjà exploité"
        results.append({
            "Indicateur": "MACD",
            "Valeur": f"{macd_val:.2f}",
            "Note (/10)": note,
            "Poids (%)": 15,
            "Interprétation": interp
        })

        # === OBV ===
        obv_recent = data["OBV"].iloc[-5:].mean()
        obv_prev = data["OBV"].iloc[-20:-5].mean()
        if obv_recent > obv_prev:
            note, interp = 8, "Hausse des volumes en zone basse → accumulation silencieuse"
        else:
            note, interp = 5, "Volumes neutres → pas de signal fort"
        results.append({
            "Indicateur": "OBV",
            "Valeur": f"{obv_recent:.2f}",
            "Note (/10)": note,
            "Poids (%)": 10,
            "Interprétation": interp
        })

        # === Distance au EMA200 ===
        ema200 = float(last["EMA200"].iloc[0])
        discount = (close_price - ema200) / ema200 * 100
        if discount < -10:
            note, interp = 9, f"Prix {abs(discount):.1f}% sous EMA200 → décote forte, point d’entrée probable"
        elif discount < -5:
            note, interp = 7, f"Prix {abs(discount):.1f}% sous EMA200 → sous-évaluation modérée"
        elif discount < 0:
            note, interp = 5, f"Prix légèrement sous EMA200 → neutre"
        else:
            note, interp = 3, f"Prix au-dessus de l’EMA200 → peu d’intérêt"
        results.append({
            "Indicateur": "Décote vs EMA200",
            "Valeur": f"{discount:.2f}%",
            "Note (/10)": note,
            "Poids (%)": 10,
            "Interprétation": interp
        })

        # === ADX ===
        adx = float(last["ADX"].iloc[0])
        if adx < 20:
            note, interp = 8, "Faible tendance → possible retournement ou accumulation"
        elif 20 <= adx <= 40:
            note, interp = 6, "Tendance modérée → marché équilibré"
        else:
            note, interp = 3, "Tendance forte → momentum déjà exploité"
        results.append({
            "Indicateur": "ADX (14)",
            "Valeur": f"{adx:.2f}",
            "Note (/10)": note,
            "Poids (%)": 8,
            "Interprétation": interp
        })

        # === CCI ===
        cci = float(last["CCI"].iloc[0])
        if cci < -100:
            note, interp = 9, "CCI < -100 → signal de survente fort"
        elif -100 <= cci <= 100:
            note, interp = 6, "CCI neutre → aucun signal clair"
        else:
            note, interp = 3, "CCI > 100 → surachat probable"
        results.append({
            "Indicateur": "CCI (20)",
            "Valeur": f"{cci:.2f}",
            "Note (/10)": note,
            "Poids (%)": 7,
            "Interprétation": interp
        })

        # === Score global ===
        df = pd.DataFrame(results)
        df["Score pondéré"] = df["Note (/10)"] * df["Poids (%)"] / 10
        score_total = df["Score pondéré"].sum()

        # === Interprétation globale ===
        if score_total >= 80:
            reco = Fore.GREEN + "🟢 Forte sous-évaluation : point d’entrée optimal"
        elif score_total >= 65:
            reco = Fore.CYAN + "🔵 Sous-évaluation modérée : surveiller un signal de rebond"
        elif score_total >= 50:
            reco = Fore.YELLOW + "🟠 Valeur équilibrée : pas d’entrée claire"
        else:
            reco = Fore.RED + "🔴 Aucun signe de sous-évaluation"

        return df, score_total, reco + Style.RESET_ALL
