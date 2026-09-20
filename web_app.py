"""Local web dashboard for the FinanceAnalytics analysis service."""

import json
import math
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

import numpy as np
import pandas as pd
import yfinance as yf

from AnalyseFondamentale.FundamentalAnalysis import FundamentalAnalysis
from AnalyseTechnique.TechnicalAnalysis import TechnicalAnalysis
from StockAnalyzer import StockAnalyzer


ROOT = Path(__file__).resolve().parent
DEFAULT_TICKERS = ["CS.PA", "TTE.PA", "SAN.PA"]


ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*m")


def strip_ansi(value):
    """Remove terminal color codes from strings so they can display in HTML/JSON."""
    if value is None:
        return None
    if isinstance(value, str):
        return ANSI_ESCAPE_RE.sub("", value)
    return value


def json_safe(value):
    """Convert pandas/numpy values and non-finite numbers to JSON values."""
    if value is None:
        return value
    if isinstance(value, str):
        return strip_ansi(value)
    if isinstance(value, (bool, int)):
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


def build_fundamental_summary(categories, scores_by_category):
    """Return a short qualitative summary for the web dashboard."""
    if not categories:
        return {"headline": "Aucune donnée fondamentale disponible.", "bullets": []}

    items = []
    for category, rows in categories.items():
        if not rows:
            continue
        score = scores_by_category.get(category, 0) if scores_by_category else 0
        numeric_notes = []
        for row in rows:
            try:
                numeric_notes.append(float(row.get("Note (/10)", 0)))
            except (TypeError, ValueError):
                numeric_notes.append(0.0)
        best = max(rows, key=lambda row: float(row.get("Note (/10)", 0)) if row.get("Note (/10)") is not None else 0.0, default={"Indicateur": "N/A"})
        worst = min(rows, key=lambda row: float(row.get("Note (/10)", 0)) if row.get("Note (/10)") is not None else 10.0, default={"Indicateur": "N/A"})
        items.append({
            "category": category,
            "score": float(score),
            "best": best.get("Indicateur", "N/A"),
            "worst": worst.get("Indicateur", "N/A"),
            "average": sum(numeric_notes) / len(numeric_notes) if numeric_notes else 0.0,
        })

    if not items:
        return {"headline": "Aucune donnée fondamentale disponible.", "bullets": []}

    avg_score = sum(item["score"] for item in items) / len(items)
    if avg_score >= 75:
        headline = "Profil fondamental très solide, avec une qualité globale de l'entreprise favorable."
    elif avg_score >= 60:
        headline = "Profil fondamental correct, mais quelques éléments de vigilance méritent une surveillance."
    elif avg_score >= 50:
        headline = "Profil fondamental moyen : l'équilibre est acceptable, mais la marge de sécurité reste limitée."
    else:
        headline = "Profil fondamental fragile : les fondamentaux restent faibles ou instables."

    strengths = []
    risks = []
    for item in sorted(items, key=lambda entry: entry["score"], reverse=True):
        if item["score"] >= 65:
            strengths.append(f"{item['category']} : {item['best']} est le point fort.")
        elif item["score"] < 50:
            risks.append(f"{item['category']} : {item['worst']} reste le point faible.")

    bullets = []
    for bullet in strengths[:2] + risks[:2]:
        if bullet not in bullets:
            bullets.append(bullet)
    if len(bullets) < 2:
        for item in sorted(items, key=lambda entry: entry["average"], reverse=True)[:2]:
            bullets.append(f"{item['category']} : le signal moyen est {item['average']:.1f}/10.")
    if len(bullets) > 4:
        bullets = bullets[:4]

    return {"headline": headline, "bullets": bullets}


def build_technical_summary(technical_rows, recommendation=None):
    """Return a short qualitative summary for technical reading."""
    if not technical_rows:
        return {"headline": "Analyse technique indisponible.", "bullets": []}

    notes = []
    for row in technical_rows:
        try:
            notes.append(float(row.get("Note (/10)", 0)))
        except (TypeError, ValueError):
            pass

    if not notes:
        return {"headline": "Analyse technique non exploitable.", "bullets": ["Aucun signal technique fiable n'a été calculé."]}

    avg_note = sum(notes) / len(notes)
    best = max(technical_rows, key=lambda row: float(row.get("Note (/10)", 0)) if row.get("Note (/10)") is not None else 0.0)
    worst = min(technical_rows, key=lambda row: float(row.get("Note (/10)", 0)) if row.get("Note (/10)") is not None else 10.0)

    if avg_note >= 7:
        headline = "Tendance technique favorable : le momentum et la structure du prix sont alignés."
    elif avg_note >= 5:
        headline = "Structure technique acceptable, mais la confirmation reste nécessaire avant une entrée."
    elif avg_note >= 4:
        headline = "Technique fragile : quelques signes positifs existent, mais le risque de rebond incomplet demeure."
    else:
        headline = "Technique défavorable : le marché reste sous pression et l'entrée est peu crédible."

    bullets = []
    if best:
        bullets.append(f"Point fort : {best.get('Indicateur', 'N/A')} affiche une lecture de {best.get('Note (/10)', 'N/A')}/10.")
    if worst:
        bullets.append(f"Point de vigilance : {worst.get('Indicateur', 'N/A')} est le plus faible avec {worst.get('Note (/10)', 'N/A')}/10.")

    if recommendation:
        bullets.append(f"Conclusion : {recommendation}")

    if len(bullets) > 4:
        bullets = bullets[:4]

    return {"headline": headline, "bullets": bullets}


def get_ticker_performance(symbol):
    """Return price performance for several horizons when available."""
    try:
        history = yf.Ticker(symbol).history(period="1y", auto_adjust=True)
    except Exception:
        return {"1M": None, "3M": None, "1Y": None}
    if history is None or history.empty:
        return {"1M": None, "3M": None, "1Y": None}

    series = history["Close"].dropna()
    if series.empty:
        return {"1M": None, "3M": None, "1Y": None}

    tz = series.index.tz

    def pct_change_for(days):
        try:
            now = pd.Timestamp.now(tz=tz) if tz is not None else pd.Timestamp.now()
            cutoff = now - pd.Timedelta(days=days)
            window = series[series.index >= cutoff]
            if window.empty or len(window) < 2:
                return None
            start = window.iloc[0]
            end = window.iloc[-1]
            if pd.isna(start) or start in (None, 0):
                return None
            return float(((end - start) / start) * 100)
        except Exception:
            return None

    return {
        "1M": pct_change_for(30),
        "3M": pct_change_for(90),
        "1Y": pct_change_for(365),
    }


def get_regression_analysis(symbol):
    """Analyse la tendance linéaire du cours sur tout l'historique disponible."""
    invalid = {
        "valid": False,
        "source": "Yahoo Finance via yfinance",
        "observations": 0,
        "years": None,
        "start_date": None,
        "end_date": None,
        "slope_per_year": None,
        "r_squared": None,
        "current_vs_line_pct": None,
        "residual_std": None,
        "current_leverage": None,
        "current_sigma": None,
        "trend": None,
        "error": "Historique maximal indisponible.",
        "interpretation": "Droite de régression indisponible.",
    }
    try:
        history = yf.Ticker(symbol).history(period="max", auto_adjust=True)
        if history is None or history.empty:
            invalid["error"] = "yfinance n'a renvoyé aucune séance pour ce ticker."
            return invalid

        close = history["Close"]
        if isinstance(close, pd.DataFrame):
            close = close.iloc[:, 0]
        close = pd.to_numeric(close, errors="coerce").dropna()
        if len(close) < 30:
            invalid["error"] = (
                f"Historique insuffisant ({len(close)} séance(s), minimum 30)."
            )
            return invalid

        dates = pd.DatetimeIndex(close.index)
        values = close.to_numpy(dtype=float)
        valid_rows = np.isfinite(values) & (values > 0) & ~dates.isna()
        dates = dates[valid_rows]
        values = values[valid_rows]
        if len(values) < 30:
            invalid["error"] = "Pas assez de cours de clôture valides."
            return invalid

        x = np.arange(len(values), dtype=float)
        slope, intercept = np.polyfit(x, values, 1)
        fitted = slope * x + intercept
        residuals = values - fitted
        degrees_of_freedom = len(values) - 2
        residual_std = float(
            np.sqrt(np.sum(residuals**2) / degrees_of_freedom)
        )
        total_variation = float(np.sum((values - values.mean()) ** 2))
        r_squared = (
            1.0 - float(np.sum(residuals**2)) / total_variation
            if total_variation > 0
            else 1.0
        )
        current_vs_line_pct = float((values[-1] - fitted[-1]) / fitted[-1] * 100)
        x_mean = float(x.mean())
        sum_x2 = float(np.sum((x - x_mean) ** 2))
        current_leverage = (
            1.0 / len(values)
            + ((x[-1] - x_mean) ** 2 / sum_x2 if sum_x2 > 0 else 0.0)
        )
        residual_scale = residual_std * np.sqrt(max(0.0, 1.0 - current_leverage))
        current_sigma = float(residuals[-1] / residual_scale) if residual_scale > 0 else 0.0
        years = float((dates[-1] - dates[0]).days / 365.25)
        slope_per_year = float(slope * 252)
    except Exception as error:
        invalid["error"] = f"Erreur yfinance/régression : {error}"
        return invalid

    if slope_per_year > 0:
        trend = "haussière"
    elif slope_per_year < 0:
        trend = "baissière"
    else:
        trend = "neutre"

    return {
        "valid": True,
        "source": "Yahoo Finance via yfinance",
        "observations": len(values),
        "years": max(years, 0.0),
        "start_date": dates[0].date().isoformat(),
        "end_date": dates[-1].date().isoformat(),
        "slope_per_year": slope_per_year,
        "r_squared": max(0.0, min(1.0, r_squared)),
        "current_vs_line_pct": current_vs_line_pct,
        "residual_std": residual_std,
        "current_leverage": current_leverage,
        "current_sigma": current_sigma,
        "trend": trend,
        "error": None,
        "interpretation": (
            f"Tendance {trend} sur {max(years, 0.0):.1f} an(s), "
            f"avec une pente de {slope_per_year:.2f} par an. "
            f"La droite explique {max(0.0, min(1.0, r_squared)):.0%} "
            f"de la variation du cours. Le dernier cours est à "
            f"{current_sigma:+.2f} sigma standardisé de la droite."
        ),
    }


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
    fundamental_summary = build_fundamental_summary(categories, category_scores)
    technical_df, technical_score, recommendation, price, fibonacci = (
        TechnicalAnalysis(symbol).run()
    )
    technical_summary = build_technical_summary(
        technical_df.to_dict(orient="records") if technical_df is not None else [],
        recommendation,
    )

    global_score = None
    interpretation = None
    if fundamental_score is not None and technical_score is not None:
        global_score, interpretation = StockAnalyzer.score_final(
            fundamental_score, technical_score
        )

    analysis = fibonacci.get("analysis", {}) if fibonacci else {}
    recommendation = strip_ansi(recommendation)
    interpretation = strip_ansi(interpretation)
    if analysis:
        analysis["interpretation"] = strip_ansi(analysis.get("interpretation"))

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
        "fundamental_summary": fundamental_summary,
        "technical_summary": technical_summary,
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
        "performance": get_ticker_performance(symbol),
        "regression": get_regression_analysis(symbol),
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
            print(f"🔎 Analyse web lancée : {', '.join(tickers)}")
            results = []
            errors = []
            for ticker in tickers:
                try:
                    results.append(analyze_ticker(ticker))
                except Exception as error:
                    errors.append({"ticker": ticker, "message": str(error)})
            print(
                f"✅ Analyse web terminée : {len(results)} résultat(s), "
                f"{len(errors)} erreur(s)"
            )
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
