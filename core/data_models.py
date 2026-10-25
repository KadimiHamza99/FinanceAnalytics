"""Canonical data structures shared by market-data providers and analyses."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping

import pandas as pd


REQUIRED_PRICE_COLUMNS = ("Open", "High", "Low", "Close", "Volume")


@dataclass(frozen=True)
class MarketData:
    """Normalized market data consumed by the analysis layer."""

    symbol: str
    history: pd.DataFrame
    fundamentals: Mapping[str, Any] = field(default_factory=dict)
    currency: str = ""
    source: str = ""
    fetched_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self):
        symbol = self.symbol.strip().upper()
        if not symbol:
            raise ValueError("Le symbole ne peut pas être vide")
        if not isinstance(self.history, pd.DataFrame):
            raise TypeError("L'historique doit être un DataFrame pandas")

        history = self.history.copy()
        if isinstance(history.columns, pd.MultiIndex):
            history.columns = history.columns.get_level_values(0)
        history.columns = [str(column).title() for column in history.columns]
        missing = [column for column in REQUIRED_PRICE_COLUMNS if column not in history]
        if missing:
            raise ValueError(
                f"Colonnes de prix manquantes pour {symbol}: {', '.join(missing)}"
            )

        history = history.loc[:, list(REQUIRED_PRICE_COLUMNS)].copy()
        history.index = pd.to_datetime(history.index)
        if getattr(history.index, "tz", None) is not None:
            history.index = history.index.tz_localize(None)
        for column in REQUIRED_PRICE_COLUMNS:
            history[column] = pd.to_numeric(history[column], errors="coerce")
        history = history.dropna(subset=["Open", "High", "Low", "Close"])
        history = history[~history.index.duplicated(keep="last")].sort_index()
        if history.empty:
            raise ValueError(f"Aucune séance exploitable pour {symbol}")

        object.__setattr__(self, "symbol", symbol)
        object.__setattr__(self, "history", history)
        object.__setattr__(self, "fundamentals", dict(self.fundamentals))

