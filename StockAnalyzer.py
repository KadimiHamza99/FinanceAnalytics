from colorama import Fore, Style, Back
from SendNotification import SendNotification

class StockAnalyzer:
    def __init__(self, tickers):
        self.tickers = tickers
        from Formatter import Formatter
        from TablePrinter import TablePrinter
        self.f = Formatter()
        self.p = TablePrinter()

    
    def score_final(self, sf, st, sn):
        score = 0.45 * sf + 0.35 * st + 0.20 * sn
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

        for ticker in self.tickers:
            print(Style.BRIGHT + Fore.WHITE + "\n" + "="*80)
            print(f"--- 📊 Analyse détaillée de {ticker} ---")
            print("="*80 + Style.RESET_ALL)

            sf, st = 0, 0  # Scores par défaut
            df_f, df_t, reco = None, None, "N/A"

            # === FONDAMENTALE ===
            try:
                fa = FundamentalAnalysis(ticker)
                df_f, sf, company_name, market_cap = fa.run()
                df_f["Note (/10)"] = df_f["Note (/10)"].apply(f.colorize_score)
                print(Fore.CYAN + "\n=== 🔍 ANALYSE FONDAMENTALE ===" + Style.RESET_ALL)
                p.afficher_table(
                    df_f,
                    ["Indicateur", "Valeur", "Note (/10)", "Poids (%)", "Interprétation"],
                    center_cols=["Valeur", "Note (/10)", "Poids (%)"]
                )
                print(f"\nScore fondamental : {f.colorize_percent_score(sf)}")
            except Exception as e:
                print(Fore.RED + f"⚠️ Erreur lors de l'analyse fondamentale de {ticker} : {e}" + Style.RESET_ALL)
                print("→ Passage à l'analyse technique...\n")
                sf = 0  # Score neutre si erreur

            print("-"*80)

            # === TECHNIQUE ===
            try:
                ta = TechnicalAnalysis(ticker)
                df_t, st, reco, llm_reco = ta.run()

                if df_t is None or df_t.empty:
                    print(Fore.RED + "❌ Données techniques non disponibles." + Style.RESET_ALL)
                else:
                    df_t["Note (/10)"] = df_t["Note (/10)"].apply(f.colorize_score)
                    print(Fore.MAGENTA + "\n=== 📈 ANALYSE TECHNIQUE ===" + Style.RESET_ALL)
                    p.afficher_table(
                        df_t,
                        ["Indicateur", "Valeur", "Note (/10)", "Poids (%)", "Interprétation"],
                        center_cols=["Valeur", "Note (/10)", "Poids (%)"]
                    )
                    print(f"\nScore technique : {f.colorize_percent_score(st)}")
                    print(f"Recommandation : {reco}")
            except Exception as e:
                print(Fore.RED + f"⚠️ Erreur lors de l'analyse technique de {ticker} : {e}" + Style.RESET_ALL)
                st = 0
                reco = "Non disponible"

            print("="*80)

            # === ACTUALITÉS ===
            try:
                from AnalyseDActualite.NewsAnalysis import NewsAnalysis
                na = NewsAnalysis(ticker)
                df_n, sn = na.run(company_name)

                print(Fore.YELLOW + "\n=== 🗞️ ANALYSE DES ACTUALITÉS ===" + Style.RESET_ALL)
                if df_n:
                    print(f"Score actualités : {f.colorize_percent_score(sn)}")
                    print(df_n["Interprétation"])
                else:
                    print("Aucune actualité récente trouvée.")
            except Exception as e:
                print(Fore.RED + f"⚠️ Erreur lors de l'analyse des actualités : {e}" + Style.RESET_ALL)
                sn = 50  # neutre


            # === SCORE GLOBAL ===
            try:
                sg, txt = self.score_final(sf, st, sn)
                print(Style.BRIGHT + Fore.WHITE + Back.BLUE +
                    f"   🧮 SCORE GLOBAL PONDÉRÉ : {f.colorize_percent_score(sg)}   " +
                    Style.RESET_ALL)
                print(f"Interprétation finale : {txt}")
            except Exception as e:
                print(Fore.RED + f"⚠️ Erreur lors du calcul du score global : {e}" + Style.RESET_ALL)
                sg = 0

            print("="*80)

            if ((sf > 75) and (st > 50)) or (sg > 70) and (market_cap > 1_500_000_000):
                message = (
                    f"🚀 {company_name} ({ticker}) — {llm_reco}\n\n"
                    f"📊 Score Technique : {st}/100\n"
                    f"✅ Score Fondamental : {sf}/100\n\n"
                )

                SendNotification.send(message)

