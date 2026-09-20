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
from web_app import get_regression_analysis


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

    def test_regression_uses_full_history_and_reports_fit_quality(self):
        index = pd.date_range("2010-01-01", periods=600, freq="B")
        close = pd.Series(50 + np.arange(len(index)) * 0.2, index=index)
        history = pd.DataFrame({"Close": close})

        with patch("web_app.yf.Ticker") as ticker:
            ticker.return_value.history.return_value = history
            regression = get_regression_analysis("TEST")

        self.assertTrue(regression["valid"])
        self.assertEqual(regression["source"], "Yahoo Finance via yfinance")
        self.assertEqual(regression["observations"], 600)
        self.assertIsNone(regression["error"])
        self.assertGreater(regression["years"], 2)
        self.assertAlmostEqual(regression["slope_per_year"], 50.4, places=1)
        self.assertGreater(regression["r_squared"], 0.99)
        self.assertAlmostEqual(regression["current_sigma"], 0, places=10)
        self.assertAlmostEqual(regression["residual_std"], 0, places=10)
        self.assertGreater(regression["current_leverage"], 0)
        ticker.return_value.history.assert_called_once_with(
            period="max", auto_adjust=True
        )

    def test_regression_exposes_yfinance_failure_reason(self):
        with patch("web_app.yf.Ticker") as ticker:
            ticker.return_value.history.return_value = pd.DataFrame()
            regression = get_regression_analysis("UNKNOWN")

        self.assertFalse(regression["valid"])
        self.assertIn("aucune séance", regression["error"])

    def test_regression_sigma_is_standardized_for_the_last_point(self):
        index = pd.date_range("2020-01-01", periods=40, freq="B")
        x = np.arange(len(index), dtype=float)
        values = 10 + 0.5 * x + np.sin(x) * 0.3
        history = pd.DataFrame({"Close": values}, index=index)

        with patch("web_app.yf.Ticker") as ticker:
            ticker.return_value.history.return_value = history
            regression = get_regression_analysis("TEST")

        slope, intercept = np.polyfit(x, values, 1)
        residuals = values - (slope * x + intercept)
        s = np.sqrt(np.sum(residuals**2) / (len(values) - 2))
        leverage = 1 / len(values) + (x[-1] - x.mean()) ** 2 / np.sum((x - x.mean()) ** 2)
        expected = residuals[-1] / (s * np.sqrt(1 - leverage))
        self.assertAlmostEqual(regression["current_sigma"], expected, places=10)


class NotificationReliabilityTests(unittest.TestCase):
    def test_notification_failure_does_not_raise(self):
        with patch("SendNotification.requests.post", side_effect=requests.Timeout("timeout")):
            self.assertFalse(SendNotification.send("message"))


if __name__ == "__main__":
    unittest.main()
