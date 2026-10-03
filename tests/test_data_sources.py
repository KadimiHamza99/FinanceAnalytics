import unittest
from unittest.mock import patch

import pandas as pd

from core.data_models import MarketData
from data_sources.service import DataSourceManager
from data_sources.providers import AlphaVantageProvider


def price_history():
    columns = pd.MultiIndex.from_product(
        [["Open", "High", "Low", "Close", "Volume"], ["TEST"]]
    )
    return pd.DataFrame(
        [[10, 11, 9, 10.5, 1000]],
        columns=columns,
        index=["2026-01-02"],
    )


class DataSourceTests(unittest.TestCase):
    def test_alpha_vantage_parses_daily_response(self):
        response = {
            "Time Series (Daily)": {
                "2026-01-02": {
                    "1. open": "10",
                    "2. high": "11",
                    "3. low": "9",
                    "4. close": "10.5",
                    "5. volume": "1000",
                }
            }
        }
        with patch("data_sources.providers.requests.get") as get:
            get.return_value.json.return_value = response
            get.return_value.raise_for_status.return_value = None
            data = AlphaVantageProvider(api_key="test").fetch("TEST")

        self.assertEqual(data.source, "Alpha Vantage")
        self.assertEqual(float(data.history.iloc[0]["Close"]), 10.5)

    def test_market_data_normalizes_multi_index_and_metadata(self):
        data = MarketData("test", price_history(), source="fixture")

        self.assertEqual(data.symbol, "TEST")
        self.assertEqual(list(data.history.columns), ["Open", "High", "Low", "Close", "Volume"])
        self.assertEqual(data.source, "fixture")
        self.assertEqual(data.history.index[0], pd.Timestamp("2026-01-02"))

    def test_manager_falls_back_to_second_provider(self):
        class FailingProvider:
            name = "primary"

            def fetch(self, symbol, period):
                raise RuntimeError("unavailable")

        class WorkingProvider:
            name = "secondary"

            def fetch(self, symbol, period):
                return MarketData(symbol, price_history(), source=self.name)

        with patch.dict("os.environ", {"FINANCE_DATA_SOURCE": "auto"}):
            data = DataSourceManager(
                providers=(FailingProvider(), WorkingProvider())
            ).fetch("TEST")

        self.assertEqual(data.source, "secondary")


if __name__ == "__main__":
    unittest.main()
