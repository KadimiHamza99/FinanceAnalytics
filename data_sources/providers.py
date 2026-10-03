"""Adapters that translate external market-data APIs to ``MarketData``."""

import io
import os

import pandas as pd
import requests
import yfinance as yf

from core.data_models import MarketData


class YahooFinanceProvider:
    name = "Yahoo Finance via yfinance"

    def fetch(self, symbol, period="12mo"):
        ticker = yf.Ticker(symbol)
        history = yf.download(
            symbol,
            period=period,
            interval="1d",
            auto_adjust=True,
            progress=False,
        )
        if history is None or history.empty:
            raise ValueError("Yahoo Finance n'a renvoyé aucune séance")
        try:
            fundamentals = ticker.info or {}
        except Exception:
            fundamentals = {}
        return MarketData(
            symbol=symbol,
            history=history,
            fundamentals=fundamentals,
            currency=fundamentals.get("currency", ""),
            source=self.name,
        )


class StooqProvider:
    """Public CSV adapter used as a key-free historical-price fallback."""

    name = "Stooq"
    url = "https://stooq.com/q/d/l/"

    def fetch(self, symbol, period="12mo"):
        response = requests.get(
            self.url,
            params={"s": symbol.lower(), "i": "d"},
            timeout=15,
        )
        response.raise_for_status()
        history = pd.read_csv(io.StringIO(response.text))
        if history.empty or "Date" not in history:
            raise ValueError("Stooq n'a renvoyé aucune séance")
        history = history.rename(columns={"Date": "date"}).set_index("date")
        history.index = pd.to_datetime(history.index)
        return MarketData(
            symbol=symbol,
            history=history,
            source=self.name,
        )


class AlphaVantageProvider:
    """Daily OHLCV adapter for Alpha Vantage's free API."""

    name = "Alpha Vantage"
    url = "https://www.alphavantage.co/query"

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("ALPHAVANTAGE_API_KEY", "").strip()

    def fetch(self, symbol, period="12mo"):
        if not self.api_key:
            raise ValueError("ALPHAVANTAGE_API_KEY n'est pas configurée")

        response = requests.get(
            self.url,
            params={
                "function": "TIME_SERIES_DAILY",
                "symbol": symbol,
                "outputsize": "compact",
                "apikey": self.api_key,
            },
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
        if "Note" in payload or "Information" in payload:
            raise RuntimeError(payload.get("Note") or payload["Information"])
        raw_series = payload.get("Time Series (Daily)")
        if not raw_series:
            raise ValueError(
                payload.get("Error Message", "Alpha Vantage n'a renvoyé aucune séance")
            )

        history = pd.DataFrame.from_dict(raw_series, orient="index")
        history.index = pd.to_datetime(history.index)
        history = history.rename(
            columns={
                "1. open": "Open",
                "2. high": "High",
                "3. low": "Low",
                "4. close": "Close",
                "5. volume": "Volume",
            }
        )
        return MarketData(
            symbol=symbol,
            history=history,
            currency="",
            source=self.name,
        )
