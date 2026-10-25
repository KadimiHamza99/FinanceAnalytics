import tempfile
import unittest
from pathlib import Path

from core.analysis_history import AnalysisHistory


class AnalysisHistoryTests(unittest.TestCase):
    def test_snapshots_persist_in_time_order_with_detailed_metrics(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "history.sqlite3"
            history = AnalysisHistory(database)
            history.save(
                {
                    "ticker": "test",
                    "scores": {"global": 60, "fundamental": 65, "technical": 45},
                    "price": 12.5,
                    "fundamental": {"Rentabilité": [{"Indicateur": "ROE", "Valeur": "8 %"}]},
                }
            )
            history.save(
                {
                    "ticker": "TEST",
                    "scores": {"global": 70, "fundamental": 75, "technical": 55},
                    "price": 14.0,
                    "fundamental": {"Rentabilité": [{"Indicateur": "ROE", "Valeur": "9 %"}]},
                }
            )

            reopened_history = AnalysisHistory(database).for_ticker("test")

        self.assertEqual(len(reopened_history), 2)
        self.assertEqual([item["scores"]["global"] for item in reopened_history], [60, 70])
        self.assertEqual(reopened_history[0]["price"], 12.5)
        self.assertEqual(
            reopened_history[1]["fundamental"]["Rentabilité"][0]["Valeur"], "9 %"
        )
        self.assertLessEqual(
            reopened_history[0]["analyzed_at"], reopened_history[1]["analyzed_at"]
        )

    def test_history_limit_keeps_the_most_recent_snapshots(self):
        with tempfile.TemporaryDirectory() as directory:
            history = AnalysisHistory(Path(directory) / "history.sqlite3")
            for score in (10, 20, 30):
                history.save({"ticker": "TEST", "scores": {"global": score}})

            snapshots = history.for_ticker("TEST", limit=2)

        self.assertEqual([item["scores"]["global"] for item in snapshots], [20, 30])

    def test_delete_ticker_removes_only_that_tickers_history(self):
        with tempfile.TemporaryDirectory() as directory:
            history = AnalysisHistory(Path(directory) / "history.sqlite3")
            history.save({"ticker": "TEST", "scores": {"global": 70}})
            history.save({"ticker": "TEST", "scores": {"global": 71}})
            history.save({"ticker": "OTHER", "scores": {"global": 80}})

            deleted = history.delete_ticker(" test ")

            self.assertEqual(deleted, 2)
            self.assertEqual(history.for_ticker("TEST"), [])
            self.assertEqual(len(history.for_ticker("OTHER")), 1)

    def test_delete_ticker_rejects_empty_ticker(self):
        with tempfile.TemporaryDirectory() as directory:
            history = AnalysisHistory(Path(directory) / "history.sqlite3")

            with self.assertRaises(ValueError):
                history.delete_ticker(" ")

    def test_identical_figures_are_not_saved_again(self):
        with tempfile.TemporaryDirectory() as directory:
            history = AnalysisHistory(Path(directory) / "history.sqlite3")
            first = {
                "ticker": "TEST",
                "scores": {"global": 70, "fundamental": 75, "technical": 55},
                "price": 14.0,
                "fundamental": {
                    "Rentabilité": [{"Indicateur": "ROE", "Valeur": "9 %", "Note (/10)": 8}]
                },
                "technical": [{"Indicateur": "RSI", "Valeur": 55.0, "Note (/10)": 6}],
                "performance": {"1M": 2.5},
                "regression": {
                    "slope_per_year": 0.7462426027063089,
                    "r_squared": 0.7209810639820472,
                    "current_vs_line_pct": 81.95364353464159,
                    "residual_std": 4.954196978378732,
                    "current_sigma": 3.825603885805797,
                    "current_leverage": 0.0004293457806503774,
                    "observations": 9315,
                },
                "interpretation": "Lecture initiale",
            }
            repeated = {
                **first,
                "interpretation": "Lecture actualisée",
                "regression": {
                    "slope_per_year": 0.7462426038531729,
                    "r_squared": 0.720981066271902,
                    "current_vs_line_pct": 81.95364330640396,
                    "residual_std": 4.954196957796196,
                    "current_sigma": 3.8256038958440963,
                    "current_leverage": 0.0004293457806503774,
                    "observations": 9315,
                    "end_date": "2026-10-03",
                },
            }

            self.assertTrue(history.save_if_changed(first))
            self.assertFalse(history.save_if_changed(repeated))
            snapshots = history.for_ticker("TEST")

        self.assertEqual(len(snapshots), 1)
        self.assertEqual(snapshots[0]["interpretation"], "Lecture initiale")

    def test_changes_below_display_precision_do_not_create_snapshots(self):
        with tempfile.TemporaryDirectory() as directory:
            history = AnalysisHistory(Path(directory) / "history.sqlite3")
            first = {
                "ticker": "TEST",
                "scores": {"global": 65.4403, "fundamental": 71.7204},
                "price": 42.06999969482422,
                "performance": {"1M": -5.757167853860176},
                "regression": {
                    "years": 36.106776180698155,
                    "slope_per_year": 0.7462426027063089,
                    "r_squared": 0.7209810639820472,
                    "current_vs_line_pct": 81.95364353464159,
                    "current_sigma": 3.825603885805797,
                    "observations": 9315,
                },
            }
            same_display = {
                **first,
                "scores": {"global": 65.4403, "fundamental": 71.7204},
                "price": 42.06999969482422,
                "performance": {"1M": -5.757167853860176},
                "regression": {
                    "years": 36.106776180698155,
                    "slope_per_year": 0.7462426038531729,
                    "r_squared": 0.720981066271902,
                    "current_vs_line_pct": 81.95364330640396,
                    "current_sigma": 3.8256038958440963,
                    "observations": 9315,
                },
            }

            self.assertTrue(history.save_if_changed(first))
            self.assertFalse(history.save_if_changed(same_display))
            self.assertEqual(len(history.for_ticker("TEST")), 1)

    def test_existing_duplicate_snapshots_are_collapsed_when_reading(self):
        with tempfile.TemporaryDirectory() as directory:
            history = AnalysisHistory(Path(directory) / "history.sqlite3")
            first = {
                "ticker": "TEST",
                "scores": {"global": 65.4403},
                "price": 42.06999969482422,
                "regression": {"slope_per_year": 0.7462426027063089},
            }
            repeated = {
                **first,
                "regression": {"slope_per_year": 0.7462426038531729},
            }
            history.save(first)
            history.save(repeated)

            snapshots = history.for_ticker("TEST")

        self.assertEqual(len(snapshots), 1)
        self.assertEqual(snapshots[0]["regression"]["slope_per_year"], 0.7462426038531729)

    def test_changed_analysis_figures_are_saved(self):
        with tempfile.TemporaryDirectory() as directory:
            history = AnalysisHistory(Path(directory) / "history.sqlite3")
            first = {
                "ticker": "TEST",
                "scores": {"global": 70},
                "price": 14.0,
                "fundamental": {"Rentabilité": [{"Indicateur": "ROE", "Valeur": "9 %"}]},
            }
            changed = {
                **first,
                "price": 14.1,
                "fundamental": {"Rentabilité": [{"Indicateur": "ROE", "Valeur": "9.1 %"}]},
            }

            self.assertTrue(history.save_if_changed(first))
            self.assertTrue(history.save_if_changed(changed))
            self.assertEqual(len(history.for_ticker("TEST")), 2)

    def test_empty_ticker_and_invalid_limit_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            history = AnalysisHistory(Path(directory) / "history.sqlite3")

            with self.assertRaises(ValueError):
                history.for_ticker("")
            with self.assertRaises(ValueError):
                history.for_ticker("TEST", limit=0)
            with self.assertRaises(ValueError):
                history.save({"ticker": " "})


if __name__ == "__main__":
    unittest.main()
