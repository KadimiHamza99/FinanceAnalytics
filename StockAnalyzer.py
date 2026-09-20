"""Application-level orchestration for stock analyses."""

from colorama import Fore, Style

from AnalyseFondamentale.FundamentalAnalysis import FundamentalAnalysis
from AnalyseTechnique.TechnicalAnalysis import TechnicalAnalysis
from Formatter import Formatter
from SendNotification import SendNotification
from StockAnalysisUtils import StockAnalysisUtils
from TablePrinter import TablePrinter


class StockAnalyzer:
    """Coordinate analysis services without owning presentation details."""

    SCORE_WEIGHTS = {"fundamental": 0.75, "technical": 0.25}
    PORTFOLIO = frozenset({"CS.PA", "TTE.PA", "NOV.F", "SAN.PA", "AI.PA"})

    def __init__(self, tickers):
        """Create an analyzer, removing empty and duplicate ticker symbols."""
        self.tickers = tuple(
            dict.fromkeys(ticker.strip() for ticker in tickers if ticker.strip())
        )
        self.formatter = Formatter()
        self.table_printer = TablePrinter()

    @classmethod
    def score_final(cls, fundamental_score, technical_score):
        """Combine both analyses with the documented 75/25 weighting."""
        score = (
            cls.SCORE_WEIGHTS["fundamental"] * fundamental_score
            + cls.SCORE_WEIGHTS["technical"] * technical_score
        )
        if score >= 80:
            interpretation = (
                Fore.GREEN
                + Style.BRIGHT
                + "💚 Excellent profil global — Opportunité d'achat (FAIBLE RISQUE)"
            )
        elif score >= 65:
            interpretation = (
                Fore.CYAN
                + Style.BRIGHT
                + "💙 Bon profil — Potentiel intéressant (RISQUE MODÉRÉ)"
            )
        elif score >= 50:
            interpretation = Fore.YELLOW + "🟠 Profil moyen — À surveiller (RISQUE NORMAL)"
        else:
            interpretation = (
                Fore.RED
                + Style.BRIGHT
                + "🔴 Profil faible — Risque élevé (ÉVITER)"
            )
        return score, interpretation

    def _run_fundamental_analysis(self, ticker):
        """Run and display the fundamental analysis for one ticker."""
        try:
            analysis = FundamentalAnalysis(ticker)
            (
                data_by_category,
                _,
                score,
                company_name,
                _,
                scores_by_category,
            ) = analysis.run()
            StockAnalysisUtils.print_fundamental_report(
                data_by_category,
                scores_by_category,
                score,
                self.formatter,
                self.table_printer,
            )
            return score, company_name, analysis.info.get("currency", "")
        except Exception as error:
            print(
                Fore.RED
                + f"⚠️ Erreur lors de l'analyse fondamentale de {ticker} : {error}"
                + Style.RESET_ALL
            )
            print("→ Passage à l'analyse technique...\n")
            return None, ticker, ""

    def _run_technical_analysis(self, ticker):
        """Run and display the technical analysis for one ticker."""
        try:
            dataframe, score, recommendation, price, fibonacci = TechnicalAnalysis(
                ticker
            ).run()
            available = StockAnalysisUtils.print_technical_report(
                dataframe,
                score,
                recommendation,
                self.formatter,
                self.table_printer,
            )
            return (
                (score, recommendation, price, fibonacci)
                if available
                else (None, "Non disponible", None, None)
            )
        except Exception as error:
            print(
                Fore.RED
                + f"⚠️ Erreur lors de l'analyse technique de {ticker} : {error}"
                + Style.RESET_ALL
            )
            return None, "Non disponible", None, None

    def _send_notification(
        self, ticker, company_name, price, currency, fundamental_score, technical_score, fibonacci
    ):
        """Send an alert when the configured portfolio rules are met."""
        notification = StockAnalysisUtils.build_notification(
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
        """Run and print every requested ticker analysis."""
        for ticker in self.tickers:
            print(Style.BRIGHT + Fore.WHITE + "\n" + "=" * 80)
            print(f"--- 📊 Analyse détaillée de {ticker} ---")
            print("=" * 80 + Style.RESET_ALL)

            fundamental_score, company_name, currency = self._run_fundamental_analysis(
                ticker
            )
            print("-" * 80)
            technical_score, _, price, fibonacci = self._run_technical_analysis(ticker)
            print("=" * 80)

            global_score = None
            interpretation = None
            if fundamental_score is not None and technical_score is not None:
                try:
                    global_score, interpretation = self.score_final(
                        fundamental_score, technical_score
                    )
                except (TypeError, ValueError) as error:
                    print(
                        Fore.RED
                        + f"⚠️ Erreur lors du calcul du score global : {error}"
                        + Style.RESET_ALL
                    )
            StockAnalysisUtils.print_global_score(
                global_score, interpretation, self.formatter
            )
            print("=" * 80)
            self._send_notification(
                ticker,
                company_name,
                price,
                currency,
                fundamental_score,
                technical_score,
                fibonacci,
            )
