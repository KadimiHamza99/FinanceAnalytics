"""Local web dashboard for the FinanceAnalytics analysis service."""

import json
import math
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd

from AnalyseFondamentale.FundamentalAnalysis import FundamentalAnalysis
from AnalyseTechnique.TechnicalAnalysis import TechnicalAnalysis
from StockAnalyzer import StockAnalyzer


ROOT = Path(__file__).resolve().parent
DEFAULT_TICKERS = ["CS.PA", "TTE.PA", "SAN.PA"]


def json_safe(value):
    """Convert pandas/numpy values and non-finite numbers to JSON values."""
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, pd.Series):
        return json_safe(value.to_dict())
    if isinstance(value, pd.DataFrame):
        return json_safe(value.to_dict(orient="records"))
    try:
        return json_safe(value.item())
    except (AttributeError, ValueError):
        return str(value)


def analyze_ticker(ticker):
    """Run both existing services and return presentation-ready data."""
    symbol = ticker.strip().upper()
    if not symbol:
        raise ValueError("Le ticker ne peut pas être vide.")

    fundamental = FundamentalAnalysis(symbol)
    (
        categories,
        _,
        fundamental_score,
        company_name,
        market_cap,
        category_scores,
    ) = fundamental.run()
    technical_df, technical_score, recommendation, price, fibonacci = (
        TechnicalAnalysis(symbol).run()
    )

    global_score = None
    interpretation = None
    if fundamental_score is not None and technical_score is not None:
        global_score, interpretation = StockAnalyzer.score_final(
            fundamental_score, technical_score
        )

    analysis = fibonacci.get("analysis", {}) if fibonacci else {}
    return {
        "ticker": symbol,
        "company": company_name or symbol,
        "sector": fundamental.sector,
        "currency": fundamental.info.get("currency", ""),
        "market_cap": market_cap,
        "price": price,
        "scores": {
            "fundamental": fundamental_score,
            "technical": technical_score,
            "global": global_score,
            "categories": category_scores,
        },
        "interpretation": interpretation,
        "recommendation": recommendation,
        "fundamental": categories,
        "technical": technical_df.to_dict(orient="records")
        if technical_df is not None
        else [],
        "fibonacci": {
            "valid": fibonacci.get("valid", False) if fibonacci else False,
            "trend": fibonacci.get("trend") if fibonacci else None,
            "levels": fibonacci.get("levels", {}) if fibonacci else {},
            "analysis": analysis,
        },
    }


class DashboardHandler(BaseHTTPRequestHandler):
    """Serve the dashboard and its local JSON API."""

    def _send_json(self, payload, status=200):
        body = json.dumps(json_safe(payload), ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if urlparse(self.path).path != "/":
            self.send_error(404)
            return
        dashboard = (ROOT / "dashboard.html").read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(dashboard)))
        self.end_headers()
        self.wfile.write(dashboard)

    def do_POST(self):
        if urlparse(self.path).path != "/api/analyze":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length))
            tickers = payload.get("tickers", [])
            if not isinstance(tickers, list):
                raise ValueError("Le champ tickers doit être une liste.")
            tickers = list(dict.fromkeys(str(item) for item in tickers))[:10]
            if not tickers:
                raise ValueError("Ajoutez au moins un ticker.")
            results = []
            errors = []
            for ticker in tickers:
                try:
                    results.append(analyze_ticker(ticker))
                except Exception as error:
                    errors.append({"ticker": ticker, "message": str(error)})
            self._send_json({"results": results, "errors": errors})
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            self._send_json({"error": str(error)}, status=400)

    def log_message(self, format_string, *args):
        return


def main():
    """Start the local dashboard server."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            pass
    host = os.getenv("FINANCE_ANALYTICS_HOST", "127.0.0.1")
    port = int(os.getenv("FINANCE_ANALYTICS_PORT", "8765"))
    server = ThreadingHTTPServer((host, port), DashboardHandler)
    print(f"Dashboard FinanceAnalytics : http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nArrêt du dashboard.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
