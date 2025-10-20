class Formatter:
    @staticmethod
    def format_pourcentage(val):
        import pandas as pd
        if val is None or pd.isna(val):
            return "N/A"
        try:
            return f"{val*100:.2f}%" if abs(val) < 1 else f"{val:.2f}%"
        except:
            return str(val)

    @staticmethod
    def format_money(val):
        import pandas as pd
        if val is None or pd.isna(val):
            return "N/A"
        try:
            v = float(val)
            if abs(v) >= 1e9:
                return f"{v/1e9:.2f} B"
            elif abs(v) >= 1e6:
                return f"{v/1e6:.2f} M"
            else:
                return f"{v:,.2f}"
        except:
            return str(val)

    @staticmethod
    def colorize_score(score):
        from colorama import Fore, Style
        if score >= 8:
            return Fore.GREEN + f"{score}/10" + Style.RESET_ALL
        elif score >= 6:
            return Fore.YELLOW + f"{score}/10" + Style.RESET_ALL
        elif score >= 4:
            return Fore.LIGHTYELLOW_EX + f"{score}/10" + Style.RESET_ALL
        else:
            return Fore.RED + f"{score}/10" + Style.RESET_ALL

    @staticmethod
    def colorize_percent_score(score):
        from colorama import Fore, Style
        if score >= 80:
            return Fore.GREEN + f"{score:.2f}/100" + Style.RESET_ALL
        elif score >= 65:
            return Fore.CYAN + f"{score:.2f}/100" + Style.RESET_ALL
        elif score >= 50:
            return Fore.YELLOW + f"{score:.2f}/100" + Style.RESET_ALL
        else:
            return Fore.RED + f"{score:.2f}/100" + Style.RESET_ALL
