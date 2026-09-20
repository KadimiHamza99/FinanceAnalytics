"""Application-level orchestration for stock analyses."""

from AnalyseFondamentale.FundamentalAnalysis import FundamentalAnalysis
from AnalyseTechnique.TechnicalAnalysis import TechnicalAnalysis
from core.presentation import Presentation
from SendNotification import SendNotification


class StockAnalyzer:
    """Coordinate analysis services without owning presentation details."""

    SCORE_WEIGHTS = {"fundamental": 0.75, "technical": 0.25}
    PORTFOLIO = frozenset({"CS.PA", "TTE.PA", "NOV.F", "SAN.PA", "AI.PA"})

    def __init__(self, tickers):
        """Create an analyzer, removing empty and duplicate ticker symbols."""
        self.tickers = tuple(
            dict.fromkeys(ticker.strip() for ticker in tickers if ticker.strip())
        )
        self.presentation = Presentation()
        self.formatter = self.presentation
        self.table_printer = self.presentation

    @classmethod
    def score_final(cls, fundamental_score, technical_score):
        """Combine both analyses with the documented 75/25 weighting."""
        score = (
            cls.SCORE_WEIGHTS["fundamental"] * fundamental_score
            + cls.SCORE_WEIGHTS["technical"] * technical_score
        )
        return score, Presentation.global_interpretation(score)

    def _run_fundamental_analysis(self, ticker):
        """Run fundamental analysis without printing its detailed data."""
        try:
            analysis = FundamentalAnalysis(ticker)
            (
                _,
                _,
                score,
                company_name,
                _,
                _,
            ) = analysis.run()
            return score, company_name, analysis.info.get("currency", "")
        except Exception as error:
            print(f"⚠️ Erreur lors de l'analyse fondamentale de {ticker} : {error}")
            return None, ticker, ""

    def _run_technical_analysis(self, ticker):
        """Run technical analysis without printing its detailed data."""
        try:
            dataframe, score, recommendation, price, fibonacci = TechnicalAnalysis(
                ticker
            ).run()
            return (
                (score, recommendation, price, fibonacci)
                if dataframe is not None and not dataframe.empty
                else (None, "Non disponible", None, None)
            )
        except Exception as error:
            print(f"⚠️ Erreur lors de l'analyse technique de {ticker} : {error}")
            return None, "Non disponible", None, None

    def _send_notification(
        self, ticker, company_name, price, currency, fundamental_score, technical_score, fibonacci
    ):
        """Send an alert when the configured portfolio rules are met."""
        notification = self.presentation.build_notification(
            ticker,
            company_name,
            price,
            currency,
            fundamental_score,
            technical_score,
            fibonacci,
            self.PORTFOLIO,
        )
        if notification:
            channel, message = notification
            SendNotification.send(message, canal=channel)

    def run(self):
        """Run every requested ticker with concise progress messages."""
        for ticker in self.tickers:
            print(f"🔎 Analyse de {ticker}...")

            fundamental_score, company_name, currency = self._run_fundamental_analysis(
                ticker
            )
            technical_score, _, price, fibonacci = self._run_technical_analysis(ticker)

            self._send_notification(
                ticker,
                company_name,
                price,
                currency,
                fundamental_score,
                technical_score,
                fibonacci,
            )
            print(f"✅ Analyse de {ticker} terminée.")
