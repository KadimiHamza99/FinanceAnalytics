import yfinance as yf
import pandas as pd
import ta

from core.data_models import MarketData
from data_sources import DataSourceManager

class Utils:
    """Download prices and compute causal indicators for daily data."""

    @staticmethod
    def fetch_market_data(ticker):
        """Return normalized data, trying Yahoo Finance then Stooq."""
        return DataSourceManager().fetch(ticker, period="12mo")

    @staticmethod
    def fetch_data(ticker):
        """Backward-compatible DataFrame view for the analysis engine."""
        market_data = Utils.fetch_market_data(ticker)
        history = market_data.history.copy()
        history.attrs["market_data_source"] = market_data.source
        history.attrs["market_data_symbol"] = market_data.symbol
        return history
        
    @staticmethod
    def _to_series(data, col):
        """Convertit une colonne potentiellement multi-indexée en série simple."""
        if isinstance(data[col], pd.DataFrame):
            return data[col].iloc[:, 0].astype(float)
        return data[col].astype(float)
    
    @staticmethod
    def compute_indicators(data):
        """Ajoute les indicateurs techniques au DataFrame."""
        high, low, close, volume = (
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
        data["EMA50"] = ta.trend.EMAIndicator(close, 50).ema_indicator()
        data["EMA200"] = ta.trend.EMAIndicator(close, 200).ema_indicator()
        data["ADX"] = ta.trend.ADXIndicator(high, low, close, 14).adx()
        data["ATR"] = ta.volatility.AverageTrueRange(high, low, close, 14).average_true_range()
        data["Volume_MA20"] = volume.rolling(20).mean()

        # Les fenêtres incomplètes sont écartées pour éviter tout biais de
        # regard vers l'avenir et garantir des signaux comparables.
        return data.dropna().copy()
