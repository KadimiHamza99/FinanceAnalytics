"""Provider selection and controlled fallback for market data."""

import os

import requests

from .providers import AlphaVantageProvider, StooqProvider, YahooFinanceProvider


class DataSourceManager:
    """Fetch canonical data using a configured provider and optional fallback."""

    PROVIDERS = {
        "yahoo": YahooFinanceProvider,
        "yfinance": YahooFinanceProvider,
        "alpha": AlphaVantageProvider,
        "alphavantage": AlphaVantageProvider,
        "stooq": StooqProvider,
    }

    def __init__(self, providers=None):
        self.providers = providers or (
            YahooFinanceProvider(),
            AlphaVantageProvider(),
            StooqProvider(),
        )

    def fetch(self, symbol, period="12mo"):
        requested = os.getenv("FINANCE_DATA_SOURCE", "auto").strip().lower()
        if requested != "auto":
            provider_class = self.PROVIDERS.get(requested)
            if provider_class is None:
                raise ValueError(
                    f"Source inconnue '{requested}'. Choisissez auto, yahoo, alpha ou stooq."
                )
            providers = (provider_class(),)
        else:
            providers = self.providers

        errors = []
        for provider in providers:
            try:
                return provider.fetch(symbol, period=period)
            except (
                ValueError,
                TypeError,
                OSError,
                RuntimeError,
                requests.RequestException,
            ) as error:
                errors.append(f"{provider.name}: {error}")
        raise RuntimeError(
            f"Impossible de récupérer les données de {symbol}. " + " | ".join(errors)
        )

    def compare(self, symbol, period="12mo"):
        """Compare the latest common OHLCV values from Yahoo and Alpha Vantage."""
        yahoo = YahooFinanceProvider().fetch(symbol, period=period)
        alpha = AlphaVantageProvider().fetch(symbol, period=period)
        common_dates = yahoo.history.index.intersection(alpha.history.index)
        if common_dates.empty:
            raise ValueError(f"Aucune date commune entre les sources pour {symbol}")

        date = common_dates[-1]
        yahoo_close = float(yahoo.history.loc[date, "Close"])
        alpha_close = float(alpha.history.loc[date, "Close"])
        difference = abs(yahoo_close - alpha_close)
        reference = max(abs(yahoo_close), abs(alpha_close))
        return {
            "symbol": yahoo.symbol,
            "date": date.date().isoformat(),
            "yahoo_close": yahoo_close,
            "alpha_vantage_close": alpha_close,
            "difference": difference,
            "difference_pct": (difference / reference * 100) if reference else 0.0,
            "reliable": difference / reference <= 0.01 if reference else False,
        }
