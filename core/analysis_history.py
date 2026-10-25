"""SQLite persistence for successive stock-analysis snapshots."""

import json
import math
import numbers
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


class AnalysisHistory:
    """Store and retrieve complete analysis snapshots, ordered by run time."""

    def __init__(self, database_path):
        self.database_path = Path(database_path)

    @contextmanager
    def _connection(self):
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.database_path, timeout=10)
        connection.row_factory = sqlite3.Row
        try:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS analysis_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT NOT NULL,
                    analyzed_at TEXT NOT NULL,
                    global_score REAL,
                    fundamental_score REAL,
                    technical_score REAL,
                    price REAL,
                    snapshot_json TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_analysis_history_ticker_id
                ON analysis_history (ticker, id)
                """
            )
            yield connection
            connection.commit()
        finally:
            connection.close()

    def save(self, snapshot):
        """Persist one successful analysis without discarding its detailed metrics."""
        with self._connection() as connection:
            self._insert(connection, snapshot)

    def save_if_changed(self, snapshot):
        """Save an analysis only if its numerical figures differ from the latest."""
        ticker = self._ticker(snapshot)
        figures = self._figures(snapshot)

        with self._connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            previous = connection.execute(
                """
                SELECT snapshot_json
                FROM analysis_history
                WHERE ticker = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (ticker,),
            ).fetchone()
            if previous is not None:
                previous_snapshot = json.loads(previous["snapshot_json"])
                if figures == self._figures(previous_snapshot):
                    return False

            self._insert(connection, snapshot, ticker=ticker)
            return True

    def delete_ticker(self, ticker):
        """Delete all saved analysis snapshots for one ticker."""
        if not isinstance(ticker, str) or not ticker.strip():
            raise ValueError("Le ticker doit être une chaîne non vide.")
        symbol = ticker.strip().upper()
        with self._connection() as connection:
            cursor = connection.execute(
                "DELETE FROM analysis_history WHERE ticker = ?",
                (symbol,),
            )
            return cursor.rowcount

    def for_ticker(self, ticker, limit=100):
        """Return the latest snapshots for a ticker in chronological order."""
        if not isinstance(ticker, str):
            raise ValueError("Le ticker doit être une chaîne non vide.")
        symbol = ticker.strip().upper()
        if not symbol:
            raise ValueError("Le ticker ne peut pas être vide.")
        if not isinstance(limit, int) or limit < 1:
            raise ValueError("La limite doit être un entier positif.")

        with self._connection() as connection:
            rows = connection.execute(
                """
                SELECT id, analyzed_at, snapshot_json
                FROM analysis_history
                WHERE ticker = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (symbol, limit),
            ).fetchall()

        snapshots = []
        for row in reversed(rows):
            snapshot = json.loads(row["snapshot_json"])
            snapshot["analysis_id"] = row["id"]
            snapshot["analyzed_at"] = row["analyzed_at"]
            if snapshots and self._figures(snapshots[-1]) == self._figures(snapshot):
                snapshots[-1] = snapshot
            else:
                snapshots.append(snapshot)
        return snapshots

    @staticmethod
    def _ticker(snapshot):
        ticker = snapshot.get("ticker")
        if not isinstance(ticker, str) or not ticker.strip():
            raise ValueError("Le ticker doit être une chaîne non vide.")
        return ticker.strip().upper()

    @staticmethod
    def _numeric_tree(value):
        """Round displayed numerical details to their visible precision."""
        if isinstance(value, bool) or value is None:
            return None
        if isinstance(value, numbers.Real):
            numeric_value = float(value)
            return round(numeric_value, 2) if math.isfinite(numeric_value) else None
        if isinstance(value, dict):
            numeric_items = {}
            for key, item in value.items():
                numeric = AnalysisHistory._numeric_tree(item)
                if numeric is not None:
                    numeric_items[key] = numeric
            return numeric_items or None
        if isinstance(value, (list, tuple)):
            numeric_items = []
            for item in value:
                numeric = AnalysisHistory._numeric_tree(item)
                if numeric is not None:
                    numeric_items.append(numeric)
            return numeric_items or None
        return None

    @classmethod
    def _figures(cls, snapshot):
        scores = snapshot.get("scores") or {}
        fundamental = snapshot.get("fundamental") or {}
        technical = snapshot.get("technical") or []

        def metric_rows(rows):
            normalized_rows = []
            for row in rows:
                metric = {
                    field: row[field]
                    for field in ("Indicateur", "Valeur")
                    if field in row
                }
                if "Valeur" in metric and isinstance(metric["Valeur"], numbers.Real):
                    metric["Valeur"] = round(float(metric["Valeur"]), 2)
                if "Note (/10)" in row:
                    note = cls._numeric_tree(row["Note (/10)"])
                    metric["Note (/10)"] = round(note, 1) if note is not None else None
                normalized_rows.append(metric)
            return normalized_rows

        normalized_scores = {}
        for key, value in scores.items():
            numeric = cls._numeric_tree(value)
            if key in {"global", "fundamental", "technical"} and numeric is not None:
                numeric = round(numeric, 1)
            normalized_scores[key] = numeric

        return {
            "currency": snapshot.get("currency"),
            "scores": normalized_scores,
            "price": cls._numeric_tree(snapshot.get("price")),
            "market_cap": cls._numeric_tree(snapshot.get("market_cap")),
            "fundamental": {
                category: metric_rows(rows)
                for category, rows in fundamental.items()
            },
            "technical": metric_rows(technical),
            "performance": {
                key: round(value, 1)
                for key, raw_value in (snapshot.get("performance") or {}).items()
                if (value := cls._numeric_tree(raw_value)) is not None
            },
            "fibonacci": cls._numeric_tree(snapshot.get("fibonacci")),
            "regression": cls._regression_figures(snapshot.get("regression") or {}),
        }

    @classmethod
    def _regression_figures(cls, regression):
        displayed_precision = {
            "years": 1,
            "slope_per_year": 2,
            "r_squared": 3,
            "current_vs_line_pct": 1,
            "current_sigma": 2,
            "observations": 0,
        }
        figures = {}
        for field, digits in displayed_precision.items():
            value = cls._numeric_tree(regression.get(field))
            if value is not None:
                figures[field] = round(value, digits)
        return figures

    @staticmethod
    def _insert(connection, snapshot, ticker=None):
        ticker = ticker or AnalysisHistory._ticker(snapshot)
        scores = snapshot.get("scores") or {}
        payload = json.dumps(snapshot, ensure_ascii=False, allow_nan=False)
        analyzed_at = datetime.now(timezone.utc).isoformat(timespec="microseconds")
        connection.execute(
            """
            INSERT INTO analysis_history (
                ticker, analyzed_at, global_score, fundamental_score,
                technical_score, price, snapshot_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ticker,
                analyzed_at,
                scores.get("global"),
                scores.get("fundamental"),
                scores.get("technical"),
                snapshot.get("price"),
                payload,
            ),
        )
