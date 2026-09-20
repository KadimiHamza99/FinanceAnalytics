import io
import math
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import numpy as np
import pandas as pd
import requests

from AnalyseFondamentale.FundamentalAnalysis import FundamentalAnalysis
from AnalyseFondamentale.IndicatorInterpreter import IndicatorInterpreter
from AnalyseFondamentale.Utils import Utils as FundamentalUtils
from AnalyseTechnique.TechnicalAnalysis import TechnicalAnalysis
from AnalyseTechnique.Utils import Utils as TechnicalUtils
from core.presentation import Presentation
from SendNotification import SendNotification


class FundamentalReliabilityTests(unittest.TestCase):
    def test_sector_weights_are_complete_and_utilities_are_distinct(self):
        sectors = (
            "Technology", "Healthcare", "Financial Services", "Energy",
            "Consumer Cyclical", "Consumer Defensive", "Communication Services",
            "Industrials", "Real Estate", "Utilities", "Basic Materials", "Général",
        )

        for sector in sectors:
            self.assertEqual(sum(FundamentalUtils.get_sector_weights(sector).values()), 100)

        self.assertEqual(FundamentalUtils._get_sector_group("Utilities"), "Utilities")

    def test_nan_and_zero_financial_values_are_handled_without_corrupting_score(self):
        analysis = FundamentalAnalysis.__new__(FundamentalAnalysis)
        analysis.ticker_symbol = "TEST"
        analysis.info = {
            "shortName": "Test Utilities",
            "sector": "Utilities",
            "currency": "USD",
            "returnOnEquity": float("nan"),
            "returnOnAssets": 0.04,
            "profitMargins": 0.10,
            "operatingMargins": 0.12,
            "freeCashflow": 0,
            "marketCap": 1_000_000,
            "currentRatio": 0,
            "quickRatio": 0,
            "operatingCashflow": 0,
            "totalCurrentLiabilities": 100,
            "debtToEquity": 0,
            "totalDebt": 0,
            "ebitda": 100,
            "totalAssets": 1_000,
            "totalStockholderEquity": 0,
            "forwardPE": 15,
            "trailingPE": 20,
            "priceToBook": 2,
            "trailingPegRatio": 1.2,
            "dividendYield": 0.03,
            "payoutRatio": 0.5,
            "beta": 0,
            "recommendationMean": 2.5,
            "numberOfAnalystOpinions": 10,
        }
        analysis.formatter = Presentation()
        analysis.sector = "Utilities"
        analysis.interpreter = IndicatorInterpreter()

        _, dataframe, score, *_ = analysis.run()
        rows = dataframe.set_index("Indicateur")

        self.assertEqual(rows.loc["ROE", "Note (/10)"], 4)
        self.assertEqual(rows.loc["FCF Yield", "Valeur"], "0.00%")
        self.assertEqual(rows.loc["Dette/EBITDA", "Valeur"], "0.00x")
        self.assertEqual(rows.loc["Dividend Yield", "Valeur"], "3.00%")
        self.assertTrue(math.isfinite(score))


class TechnicalReliabilityTests(unittest.TestCase):
    def test_technical_score_stays_on_a_100_point_scale(self):
        index = pd.date_range("2025-01-01", periods=260, freq="B")
        close = pd.Series(np.linspace(100, 140, len(index)), index=index)
        data = pd.DataFrame(
            {
                "Open": close - 0.5,
                "High": close + 1,
                "Low": close - 1,
                "Close": close,
                "Volume": 1_000_000,
            },
            index=index,
        )

        with patch.object(TechnicalUtils, "fetch_data", return_value=data):
            with redirect_stdout(io.StringIO()):
                dataframe, score, recommendation, price, fibonacci = TechnicalAnalysis("TEST").run()

        self.assertFalse(dataframe.empty)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        self.assertIsInstance(recommendation, str)
        self.assertGreater(price, 0)
        self.assertIsInstance(fibonacci, dict)


class NotificationReliabilityTests(unittest.TestCase):
    def test_notification_failure_does_not_raise(self):
        with patch("SendNotification.requests.post", side_effect=requests.Timeout("timeout")):
            self.assertFalse(SendNotification.send("message"))


if __name__ == "__main__":
    unittest.main()
