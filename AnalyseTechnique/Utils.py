import yfinance as yf
import pandas as pd
import ta
import subprocess
from OllamaSession import OllamaSession

class Utils:

    @staticmethod
    def fetch_data(ticker):
        try:
            data = yf.download(
                ticker,
                period="12mo",
                interval="1d",
                auto_adjust=True,
                progress=False
            )

            if data.empty:
                raise ValueError("Données historiques non disponibles")

            return data

        except Exception as e:
            raise RuntimeError(f"Erreur de téléchargement : {e}")
        
    @staticmethod
    def _to_series(data, col):
        """Convertit une colonne potentiellement multi-indexée en série simple."""
        if isinstance(data[col], pd.DataFrame):
            return data[col].iloc[:, 0].astype(float)
        return data[col].astype(float)
    
    @staticmethod
    def compute_indicators(data):
        """Ajoute les indicateurs techniques au DataFrame."""
        open_, high, low, close, volume = (
            Utils._to_series(data, "Open"),
            Utils._to_series(data, "High"),
            Utils._to_series(data, "Low"),
            Utils._to_series(data, "Close"),
            Utils._to_series(data, "Volume"),
        )

        data["RSI"] = ta.momentum.RSIIndicator(close, 14).rsi()
        stoch = ta.momentum.StochasticOscillator(high, low, close, 14, 3)
        data["STOCH_K"], data["STOCH_D"] = stoch.stoch(), stoch.stoch_signal()
        macd = ta.trend.MACD(close)
        data["MACD"], data["Signal"] = macd.macd(), macd.macd_signal()
        data["OBV"] = ta.volume.OnBalanceVolumeIndicator(close, volume).on_balance_volume()
        bb = ta.volatility.BollingerBands(close, 20, 2)
        data["BB_H"], data["BB_L"], data["BB_M"] = bb.bollinger_hband(), bb.bollinger_lband(), bb.bollinger_mavg()
        data["EMA200"] = ta.trend.EMAIndicator(close, 200).ema_indicator()
        data["ADX"] = ta.trend.ADXIndicator(high, low, close, 14).adx()

        return data.dropna().bfill().ffill()
    


    @staticmethod
    def askMistralTechnicalAnalysis(rsi, macd, ema200, bb_l, bb_h, bb_m, stoch_k, stoch_d, obv, adx, prix_actuel):

        # Prompt structuré pour guider le modèle
        prompt = f"""<s>[INST] Tu es un analyste boursier expert en stratégie long terme.

            Indicateurs techniques :
            - RSI: {rsi:.2f}
            - OBV: {obv:.2f}
            - ADX: {adx:.2f}
            - STOCH K/D: {stoch_k:.2f}/{stoch_d:.2f}
            - MACD: {macd:.3f}
            - EMA200: {ema200:.2f}
            - Bollinger: {bb_l:.2f} | {bb_m:.2f} | {bb_h:.2f}
            - Prix: {prix_actuel:.2f}

            Analyse sévére et objective pour position longue, proposes moi des points d'entrée au niveau des supports calculés.
            Réponse UNIQUEMENT dans ce format :

            Conclusion : [phrase unique] \n
            Point d'entrée recommandé : [prix ou plage] [/INST]
        """

        # OllamaSession.ask("gemma2:2b",prompt)
        # OllamaSession.ask("mistral:7b",prompt)
        return OllamaSession.ask_http("mistral:7b",prompt)