"""Helpers for presenting and notifying stock analysis results."""

import pandas as pd
from colorama import Back, Fore, Style


class StockAnalysisUtils:
    """Keep report formatting and notification payloads out of the orchestrator."""

    CATEGORY_EMOJIS = {
        "Rentabilité": "💰",
        "Liquidité": "💧",
        "Solvabilité": "🏦",
        "Valorisation": "📈",
        "Risque & Marché": "⚡",
    }

    @staticmethod
    def print_fundamental_report(
        data_by_category, scores_by_category, score, formatter, table_printer
    ):
        """Print the fundamental analysis grouped by financial category."""
        print(Fore.CYAN + "\n=== 🔍 ANALYSE FONDAMENTALE ===" + Style.RESET_ALL)

        for category, indicators in data_by_category.items():
            if not indicators:
                continue

            dataframe = pd.DataFrame(indicators)
            dataframe["Note (/10)"] = dataframe["Note (/10)"].apply(
                formatter.colorize_score
            )
            emoji = StockAnalysisUtils.CATEGORY_EMOJIS.get(category, "📊")

            print(f"\n{Fore.YELLOW}{emoji} {category.upper()}{Style.RESET_ALL}")
            print(
                "Score catégorie : "
                f"{formatter.colorize_percent_score(scores_by_category[category])}"
            )
            table_printer.afficher_table(
                dataframe,
                [
                    "Indicateur",
                    "Valeur",
                    "Note (/10)",
                    "Poids (%)",
                    "Interprétation",
                    "Définition",
                ],
                center_cols=["Valeur", "Note (/10)", "Poids (%)"],
            )

        print(f"\n{Fore.GREEN}{'=' * 80}{Style.RESET_ALL}")
        print(
            f"{Fore.GREEN}Score fondamental global : "
            f"{formatter.colorize_percent_score(score)}{Style.RESET_ALL}"
        )
        print(f"{Fore.GREEN}{'=' * 80}{Style.RESET_ALL}")

    @staticmethod
    def print_technical_report(dataframe, score, recommendation, formatter, table_printer):
        """Print the technical indicators and their recommendation."""
        if dataframe is None or dataframe.empty:
            print(Fore.RED + "❌ Données techniques non disponibles." + Style.RESET_ALL)
            return False

        dataframe["Note (/10)"] = dataframe["Note (/10)"].apply(
            formatter.colorize_score
        )
        print(Fore.MAGENTA + "\n=== 📈 ANALYSE TECHNIQUE ===" + Style.RESET_ALL)
        table_printer.afficher_table(
            dataframe,
            ["Indicateur", "Valeur", "Note (/10)", "Poids (%)", "Interprétation"],
            center_cols=["Valeur", "Note (/10)", "Poids (%)"],
        )
        print(f"\nScore technique : {formatter.colorize_percent_score(score)}")
        print(f"Recommandation : {recommendation}")
        return True

    @staticmethod
    def extract_fibonacci_summary(fibonacci):
        """Return the small Fibonacci subset required by notifications."""
        analysis = fibonacci.get("analysis", {}) if fibonacci else {}
        return (
            analysis.get("targets", []),
            analysis.get("score"),
        )

    @staticmethod
    def format_score(score):
        """Format a score while preserving an explicit unavailable state."""
        return f"{score:.2f}/100" if score is not None else "N/A"

    @staticmethod
    def format_price(price, currency):
        """Format the latest price for a notification."""
        return f"{price:.2f} {currency}".strip() if price is not None else "N/A"

    @staticmethod
    def build_notification(
        ticker,
        company_name,
        price,
        currency,
        fundamental_score,
        technical_score,
        fibonacci,
        portfolio,
    ):
        """Build the notification channel and message, or return ``None``."""
        targets, fibonacci_score = StockAnalysisUtils.extract_fibonacci_summary(
            fibonacci
        )
        price_text = StockAnalysisUtils.format_price(price, currency)
        fundamental_text = StockAnalysisUtils.format_score(fundamental_score)
        technical_text = StockAnalysisUtils.format_score(technical_score)
        fibonacci_text = (
            f"{fibonacci_score:.2f}/10" if fibonacci_score is not None else "N/A"
        )

        if ticker in portfolio:
            targets_text = "\n".join(
                f"Vendre à {target['level']:.2f} EUR → "
                f"{target['gain_potential']:.2f}%"
                for target in targets
            ) or "Niveaux Fibonacci indisponibles"
            message = (
                f"📢 {company_name} ({ticker}) — Prix actuel {price_text}\n\n"
                f"📊 Score Technique : {technical_text}\n"
                f"🔗 Score Fibonacci : {fibonacci_text}\n"
                f"✅ Score Fondamental : {fundamental_text}\n\n"
                "🔗 Fibonacci Analysis :\n"
                f"{targets_text}"
            )
            return "portfolio", message

        if fundamental_score is not None and technical_score is not None:
            if fundamental_score > 70 and technical_score > 60:
                message = (
                    f"🌟 {company_name} ({ticker}) — {price_text} — "
                    "Opportunité d'achat à considérer\n\n"
                    f"📊 Score Technique : {technical_text}\n"
                    f"🔗 Score Fibonacci : {fibonacci_text}\n"
                    f"✅ Score Fondamental : {fundamental_text}\n"
                )
                return "high", message

            if fundamental_score > 70 and technical_score > 40:
                potential = targets[-1].get("gain_potential") if targets else None
                potential_text = f"{potential:.2f}%" if potential is not None else "N/A"
                message = (
                    f"🚀 {company_name} ({ticker}) — {price_text}\n\n"
                    f"📊 Score Technique : {technical_text}\n"
                    f"🔗 Score Fibonacci : {fibonacci_text}\n"
                    f"🔗 Potential : {potential_text}\n"
                    f"✅ Score Fondamental : {fundamental_text}\n"
                )
                return "normal", message

        return None

    @staticmethod
    def print_global_score(score, interpretation, formatter):
        """Print the combined score or its unavailable-state explanation."""
        if score is None:
            print(
                Fore.YELLOW
                + "⚠️ Score global indisponible : analyse fondamentale ou technique absente."
                + Style.RESET_ALL
            )
            return

        print(
            Style.BRIGHT
            + Fore.WHITE
            + Back.BLUE
            + f"   🧮 SCORE GLOBAL PONDÉRÉ : {formatter.colorize_percent_score(score)}   "
            + Style.RESET_ALL
        )
        print(f"Interprétation finale : {interpretation}")
