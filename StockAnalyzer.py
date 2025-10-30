from colorama import Fore, Style, Back

class StockAnalyzer:
    def __init__(self, tickers):
        self.tickers = tickers
        from Formatter import Formatter
        from TablePrinter import TablePrinter
        self.f = Formatter()
        self.p = TablePrinter()

    def score_final(self, fond, tech):
        f = self.f
        score = fond * 0.7 + tech * 0.3
        if score >= 80:
            txt = Fore.GREEN + Style.BRIGHT + "💚 Excellent profil global — Opportunité d'achat (FAIBLE RISQUE)"
        elif score >= 65:
            txt = Fore.CYAN + Style.BRIGHT + "💙 Bon profil — Potentiel intéressant (RISQUE MODÉRÉ)"
        elif score >= 50:
            txt = Fore.YELLOW + "🟠 Profil moyen — À surveiller (RISQUE NORMAL)"
        else:
            txt = Fore.RED + Style.BRIGHT + "🔴 Profil faible — Risque élevé (ÉVITER)"
        return score, txt

    def run(self):
        f, p = self.f, self.p
        from AnalyseFondamentale.FundamentalAnalysis import FundamentalAnalysis
        from AnalyseTechnique.TechnicalAnalysis import TechnicalAnalysis

        watch_list_tickers = []

        for ticker in self.tickers:
            print(Style.BRIGHT + Fore.WHITE + "\n" + "="*80)
            print(f"--- 📊 Analyse détaillée de {ticker} ---")
            print("="*80 + Style.RESET_ALL)

            # === FONDAMENTALE ===
            fa = FundamentalAnalysis(ticker)
            df_f, sf = fa.run()
            df_f["Note (/10)"] = df_f["Note (/10)"].apply(f.colorize_score)
            print(Fore.CYAN + "\n=== 🔍 ANALYSE FONDAMENTALE ===" + Style.RESET_ALL)
            p.afficher_table(df_f, ["Indicateur", "Valeur", "Note (/10)", "Poids (%)", "Interprétation", "Petite Définition"],
                            center_cols=["Valeur", "Note (/10)", "Poids (%)"])
            print(f"\nScore fondamental : {f.colorize_percent_score(sf)}")
            print("-"*80)

            # === TECHNIQUE ===
            ta = TechnicalAnalysis(ticker)
            df_t, st, reco = ta.run()
            if df_t.empty:
                print(Fore.RED + "❌ Données techniques non disponibles." + Style.RESET_ALL)
                continue
            df_t["Note (/10)"] = df_t["Note (/10)"].apply(f.colorize_score)
            print(Fore.MAGENTA + "\n=== 📈 ANALYSE TECHNIQUE ===" + Style.RESET_ALL)
            p.afficher_table(df_t, ["Indicateur", "Valeur", "Note (/10)", "Poids (%)", "Interprétation"],
                            center_cols=["Valeur", "Note (/10)", "Poids (%)"])
            print(f"\nScore technique : {f.colorize_percent_score(st)}")
            print(f"Recommandation : {reco}")
            print("="*80)

            # === SCORE GLOBAL ===
            sg, txt = self.score_final(sf, st)
            print(Style.BRIGHT + Fore.WHITE + Back.BLUE +
                f"   🧮 SCORE GLOBAL PONDÉRÉ : {f.colorize_percent_score(sg)}   " +
                Style.RESET_ALL)
            print(f"Interprétation finale : {txt}")
            print("="*80)

            if(sg > 65) :
                watch_list_tickers.append(ticker)
        return watch_list_tickers

