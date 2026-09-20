"""Shared formatting, table rendering, reporting, and notification text."""

import pandas as pd
from colorama import Back, Fore, Style
from tabulate import tabulate


class Presentation:
    """Single presentation service used by the CLI and analysis modules."""

    MAGENTA = Fore.MAGENTA
    RED = Fore.RED
    CATEGORY_EMOJIS = {
        "Rentabilité": "💰",
        "Liquidité": "💧",
        "Solvabilité": "🏦",
        "Valorisation": "📈",
        "Risque & Marché": "⚡",
    }

    @staticmethod
    def colorize(text, color=Fore.WHITE, bright=False):
        """Apply one consistent ANSI style to a display string."""
        emphasis = Style.BRIGHT if bright else ""
        return f"{emphasis}{color}{text}{Style.RESET_ALL}"

    @staticmethod
    def format_number(value, decimals=2, suffix=""):
        """Format a numeric value or return ``N/A`` when unavailable."""
        if value is None or pd.isna(value):
            return "N/A"
        try:
            return f"{float(value):.{decimals}f}{suffix}"
        except (TypeError, ValueError):
            return str(value)

    @staticmethod
    def format_ratio(value, suffix=""):
        """Format a ratio consistently."""
        return Presentation.format_number(value, suffix=suffix)

    @staticmethod
    def format_pourcentage(value):
        """Format a ratio as a percentage, accepting ``0.12`` or ``12``."""
        if value is None or pd.isna(value):
            return "N/A"
        try:
            return f"{value * 100:.2f}%" if abs(value) < 1 else f"{value:.2f}%"
        except (TypeError, ValueError):
            return str(value)

    @staticmethod
    def format_money(value):
        """Format a monetary value using readable million/billion units."""
        if value is None or pd.isna(value):
            return "N/A"
        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            return str(value)

        if abs(numeric_value) >= 1e9:
            return f"{numeric_value / 1e9:.2f} B"
        if abs(numeric_value) >= 1e6:
            return f"{numeric_value / 1e6:.2f} M"
        return f"{numeric_value:,.2f}"

    @staticmethod
    def format_billions(value, currency=""):
        """Format a market capitalization in billions."""
        if value is None or pd.isna(value):
            return "N/A"
        try:
            return f"{float(value) / 1e9:.2f} Milliard {currency}".strip()
        except (TypeError, ValueError):
            return str(value)

    @staticmethod
    def colorize_score(score):
        """Colour a score expressed on a scale from 0 to 10."""
        if score >= 8:
            color = Fore.GREEN
        elif score >= 6:
            color = Fore.YELLOW
        elif score >= 4:
            color = Fore.LIGHTYELLOW_EX
        else:
            color = Fore.RED
        return Presentation.colorize(f"{score}/10", color)

    @staticmethod
    def colorize_percent_score(score):
        """Colour a score expressed on a scale from 0 to 100."""
        if score >= 80:
            color = Fore.GREEN
        elif score >= 65:
            color = Fore.CYAN
        elif score >= 50:
            color = Fore.YELLOW
        else:
            color = Fore.RED
        return Presentation.colorize(f"{score:.2f}/100", color)

    @staticmethod
    def format_score(score, scale=100):
        """Format a score while preserving an unavailable state."""
        return f"{score:.2f}/{scale}" if score is not None else "N/A"

    @staticmethod
    def format_price(price, currency=""):
        """Format a price and optional currency."""
        return "N/A" if price is None else f"{price:.2f} {currency}".strip()

    @staticmethod
    def global_interpretation(score):
        """Return the coloured interpretation associated with a global score."""
        if score >= 80:
            return Presentation.colorize(
                "💚 Excellent profil global — Opportunité d'achat (FAIBLE RISQUE)",
                Fore.GREEN,
                bright=True,
            )
        if score >= 65:
            return Presentation.colorize(
                "💙 Bon profil — Potentiel intéressant (RISQUE MODÉRÉ)",
                Fore.CYAN,
                bright=True,
            )
        if score >= 50:
            return Presentation.colorize(
                "🟠 Profil moyen — À surveiller (RISQUE NORMAL)", Fore.YELLOW
            )
        return Presentation.colorize(
            "🔴 Profil faible — Risque élevé (ÉVITER)", Fore.RED, bright=True
        )

    @staticmethod
    def afficher_table(df, colonnes, center_cols=None):
        """Render a dataframe as a consistent terminal table."""
        center_cols = center_cols or []
        table = []
        for _, row in df[colonnes].iterrows():
            values = []
            for column in colonnes:
                value = str(row[column])
                values.append(value.center(20) if column in center_cols else value)
            table.append(values)
        print(tabulate(table, headers=colonnes, tablefmt="fancy_grid", stralign="center"))

    @staticmethod
    def print_fundamental_report(
        data_by_category, scores_by_category, score, formatter, table_printer
    ):
        """Print the fundamental analysis grouped by category."""
        print(Presentation.colorize("\n=== 🔍 ANALYSE FONDAMENTALE ===", Fore.CYAN))
        for category, indicators in data_by_category.items():
            if not indicators:
                continue
            dataframe = pd.DataFrame(indicators)
            dataframe["Note (/10)"] = dataframe["Note (/10)"].apply(
                formatter.colorize_score
            )
            emoji = Presentation.CATEGORY_EMOJIS.get(category, "📊")
            print(Presentation.colorize(f"\n{emoji} {category.upper()}", Fore.YELLOW))
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

        print(Presentation.colorize(f"\n{'=' * 80}", Fore.GREEN))
        print(
            Presentation.colorize(
                f"Score fondamental global : {formatter.colorize_percent_score(score)}",
                Fore.GREEN,
            )
        )
        print(Presentation.colorize("=" * 80, Fore.GREEN))

    @staticmethod
    def print_technical_report(dataframe, score, recommendation, formatter, table_printer):
        """Print technical indicators and their recommendation."""
        if dataframe is None or dataframe.empty:
            print(Presentation.colorize("❌ Données techniques non disponibles.", Fore.RED))
            return False
        dataframe["Note (/10)"] = dataframe["Note (/10)"].apply(
            formatter.colorize_score
        )
        print(Presentation.colorize("\n=== 📈 ANALYSE TECHNIQUE ===", Fore.MAGENTA))
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
        """Return notification-relevant Fibonacci data."""
        analysis = fibonacci.get("analysis", {}) if fibonacci else {}
        return analysis.get("targets", []), analysis.get("score")

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
        """Build a notification channel and message, or return ``None``."""
        targets, fibonacci_score = Presentation.extract_fibonacci_summary(fibonacci)
        price_text = Presentation.format_price(price, currency)
        fundamental_text = Presentation.format_score(fundamental_score)
        technical_text = Presentation.format_score(technical_score)
        fibonacci_text = Presentation.format_score(fibonacci_score, scale=10)

        if ticker in portfolio:
            targets_text = "\n".join(
                f"Vendre à {target['level']:.2f} EUR → "
                f"{target['gain_potential']:.2f}%"
                for target in targets
            ) or "Niveaux Fibonacci indisponibles"
            return "portfolio", (
                f"📢 {company_name} ({ticker}) — Prix actuel {price_text}\n\n"
                f"📊 Score Technique : {technical_text}\n"
                f"🔗 Score Fibonacci : {fibonacci_text}\n"
                f"✅ Score Fondamental : {fundamental_text}\n\n"
                "🔗 Fibonacci Analysis :\n"
                f"{targets_text}"
            )

        if fundamental_score is None or technical_score is None:
            return None
        if fundamental_score > 70 and technical_score > 60:
            return "high", (
                f"🌟 {company_name} ({ticker}) — {price_text} — "
                "Opportunité d'achat à considérer\n\n"
                f"📊 Score Technique : {technical_text}\n"
                f"🔗 Score Fibonacci : {fibonacci_text}\n"
                f"✅ Score Fondamental : {fundamental_text}\n"
            )
        if fundamental_score > 70 and technical_score > 40:
            potential = targets[-1].get("gain_potential") if targets else None
            potential_text = f"{potential:.2f}%" if potential is not None else "N/A"
            return "normal", (
                f"🚀 {company_name} ({ticker}) — {price_text}\n\n"
                f"📊 Score Technique : {technical_text}\n"
                f"🔗 Score Fibonacci : {fibonacci_text}\n"
                f"🔗 Potential : {potential_text}\n"
                f"✅ Score Fondamental : {fundamental_text}\n"
            )
        return None

    @staticmethod
    def print_global_score(score, interpretation, formatter):
        """Print the combined score or its unavailable-state explanation."""
        if score is None:
            print(
                Presentation.colorize(
                    "⚠️ Score global indisponible : analyse fondamentale ou technique absente.",
                    Fore.YELLOW,
                )
            )
            return
        banner = f"   🧮 SCORE GLOBAL PONDÉRÉ : {formatter.colorize_percent_score(score)}   "
        print(Style.BRIGHT + Fore.WHITE + Back.BLUE + banner + Style.RESET_ALL)
        print(f"Interprétation finale : {interpretation}")

    @staticmethod
    def format_fibonacci_info(fib_data):
        """Build the human-readable Fibonacci report."""
        if not fib_data.get("valid", True):
            return (
                "\n⚠️ FIBONACCI NON APPLICABLE\n"
                f"{fib_data['analysis']['interpretation']}\n"
            )

        analysis = fib_data["analysis"]
        current = fib_data["current_price"]
        trend_emoji = {"haussier": "📈", "baissier": "📉", "neutre": "➡️"}
        lines = [
            "\n" + "=" * 60,
            "📊 ANALYSE TECHNIQUE INTÉGRÉE (63 séances)",
            "=" * 60,
            f"\n📍 Prix actuel : {current:.2f}€",
            f"{trend_emoji.get(fib_data['trend'], '📊')} Tendance : {fib_data['trend'].upper()}",
            f"📈 Plus haut (63 séances) : {fib_data['high']:.2f}€",
            f"📉 Plus bas (63 séances) : {fib_data['low']:.2f}€",
            f"📏 Range : {fib_data['range']:.2f}€ ({fib_data['range'] / current * 100:.1f}%)",
            "\n\n🎯 NIVEAUX DE RETRACEMENT FIBONACCI :",
        ]
        for name, level in fib_data["levels"].items():
            distance = abs(level - current) / fib_data["range"] * 100
            marker = " ← 🎯 PRIX ACTUEL ICI" if distance < 2 else ""
            lines.append(f"  {name:15} : {level:.2f}€{marker}")

        if fib_data["trend"] == "haussier":
            lines.append("\n\n🚀 EXTENSIONS FIBONACCI (Objectifs haussiers) :")
            for name, level in fib_data["extensions"].items():
                gain = (level - current) / current * 100
                lines.append(f"  {name:15} : {level:.2f}€ (+{gain:.1f}%)")

        lines.extend(["\n\n" + "-" * 60, "💡 RECOMMANDATIONS DE TRADING :", "-" * 60])
        if analysis["support"]:
            distance = (current - analysis["support"]) / analysis["support"] * 100
            lines.append(
                f"🛡️  Support proche : {analysis['support']:.2f}€ "
                f"({analysis['support_name']}) [-{distance:.1f}%]"
            )
        if analysis["resistance"]:
            distance = (analysis["resistance"] - current) / current * 100
            lines.append(
                f"⚔️  Résistance proche : {analysis['resistance']:.2f}€ "
                f"({analysis['resistance_name']}) [+{distance:.1f}%]"
            )

        entry_low, entry_high = analysis["entry_zone"]
        if entry_low <= current <= entry_high:
            status = " ✓ (DANS LA ZONE)"
        elif current < entry_low:
            status = f" (attendre {(entry_low - current) / current * 100:.1f}% de hausse)"
        else:
            status = f" (attendre {(current - entry_high) / current * 100:.1f}% de baisse)"
        lines.append(
            f"\n\n✅ Zone d'entrée recommandée : {entry_low:.2f}€ - {entry_high:.2f}€{status}"
        )

        stop_distance = abs(current - analysis["stop_loss"]) / current * 100
        direction = "au-dessus" if analysis["stop_loss"] > current else "en dessous"
        lines.append(
            f"🛑 Stop Loss recommandé : {analysis['stop_loss']:.2f}€ "
            f"({stop_distance:.1f}% {direction})"
        )
        if analysis["targets"]:
            lines.append("\n\n🎯 Objectifs de sortie :")
            for index, target in enumerate(analysis["targets"], 1):
                sign = "+" if target["gain_potential"] > 0 else ""
                lines.append(
                    f"   Objectif {index} : {target['level']:.2f}€ ({target['name']})"
                    f" | {target['type']} | Potentiel: {sign}{target['gain_potential']:.1f}%"
                )

        risk_reward = analysis["risk_reward"]
        if risk_reward and risk_reward["ratio"] > 0:
            ratio = risk_reward["ratio"]
            quality = (
                " ✅ Excellent" if ratio >= 2 else
                " ✓ Bon" if ratio >= 1.5 else
                " ~ Acceptable" if ratio >= 1 else
                " ⚠️ Défavorable"
            )
            lines.extend([
                f"\n\n⚖️  Ratio Risque/Récompense : 1:{ratio:.2f}{quality}",
                f"   💸 Risque : {risk_reward['risk']:.2f}€ | "
                f"💰 Récompense : {risk_reward['reward']:.2f}€",
            ])
        lines.extend([
            f"\n\n📝 {analysis['interpretation']}",
            f"⭐ Score Fibonacci : {analysis['score']:.1f}/10",
            "\n" + "=" * 60 + "\n",
        ])
        return "\n".join(lines)
