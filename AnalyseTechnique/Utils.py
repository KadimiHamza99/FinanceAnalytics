import yfinance as yf
import pandas as pd
import ta
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import os

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
    def deepSeekPrediction(rsi, macd, ema200, bb_l, bb_h, bb_m, prix_actuel):
        """
        Analyse technique ultra-rapide CPU avec modèle léger (~500Mo).
        """
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM

        print("⚡ Chargement du modèle léger distilgpt2...")

        model_name = "distilgpt2"  # modèle très léger
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)

        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        model.eval()
        print("✅ Modèle chargé instantanément!")

        # Prompt structuré pour guider le modèle
        prompt = (
            f"You are a financial technical analysis assistant.\n"
            f"Indicators:\n"
            f"RSI = {rsi}\n"
            f"MACD = {macd:.3f}\n"
            f"EMA200 = {ema200:.2f}\n"
            f"Bollinger Bands Low = {bb_l:.2f}, Middle = {bb_m:.2f}, High = {bb_h:.2f}\n"
            f"Current Price = {prix_actuel:.2f}\n\n"
            f"Provide a concise technical analysis based on these indicators:\n"
        )

        inputs = tokenizer(prompt, return_tensors="pt")

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=80,
                temperature=0.7,
                do_sample=True,
                top_p=0.9,
                pad_token_id=tokenizer.eos_token_id
            )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Nettoyage du prompt
        if "analysis:" in response.lower():
            response = response.split("analysis:")[-1].strip()

        print("\n📊 Analyse technique générée :")
        print(response)

        return response
