"""Formatting helpers used by the console reports.

The analysis layer keeps numeric values numeric.  This module is the only
place responsible for turning them into display strings or ANSI-coloured
values.
"""

import pandas as pd
from colorama import Fore, Style


class Formatter:
    """Format values consistently for the terminal output."""

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
    def colorize_score(score):
        """Colour a score expressed on a scale from 0 to 10."""
        if score >= 8:
            return Fore.GREEN + f"{score}/10" + Style.RESET_ALL
        if score >= 6:
            return Fore.YELLOW + f"{score}/10" + Style.RESET_ALL
        if score >= 4:
            return Fore.LIGHTYELLOW_EX + f"{score}/10" + Style.RESET_ALL
        else:
            return Fore.RED + f"{score}/10" + Style.RESET_ALL

    @staticmethod
    def colorize_percent_score(score):
        """Colour a score expressed on a scale from 0 to 100."""
        if score >= 80:
            return Fore.GREEN + f"{score:.2f}/100" + Style.RESET_ALL
        if score >= 65:
            return Fore.CYAN + f"{score:.2f}/100" + Style.RESET_ALL
        if score >= 50:
            return Fore.YELLOW + f"{score:.2f}/100" + Style.RESET_ALL
        else:
            return Fore.RED + f"{score:.2f}/100" + Style.RESET_ALL
