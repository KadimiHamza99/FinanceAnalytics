from colorama import Fore, Style, Back
from SendNotification import SendNotification
import pandas as pd
# from AnalyseDActualite.NewsAnalysis import NewsAnalysis

class StockAnalyzer:
    def __init__(self, tickers):
        self.tickers = tickers
        from Formatter import Formatter
        from TablePrinter import TablePrinter
        self.f = Formatter()
        self.p = TablePrinter()
        self.portfolio = {"CS.PA", "TTE.PA", "NOV.F", "SAN.PA", "AI.PA"}

    
    def score_final(self, sf, st):
        score = 0.75 * sf + 0.25 * st
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

            sf, st = None, None
            df_f, df_t, reco = None, None, "N/A"
            company_name = ticker
            currency = ""
            llm_reco, fibo = None, None

            # === FONDAMENTALE ===
            try:
                fa = FundamentalAnalysis(ticker)
                data_by_category, df_f, sf, company_name, market_cap, scores_by_category = fa.run()
                currency = fa.info.get("currency", "")
                
                print(Fore.CYAN + "\n=== 🔍 ANALYSE FONDAMENTALE ===" + Style.RESET_ALL)
                
                # Affichage par catégorie
                for category, data in data_by_category.items():
                    if data:  # Afficher seulement si la catégorie contient des données
                        df_cat = pd.DataFrame(data)
                        df_cat["Note (/10)"] = df_cat["Note (/10)"].apply(f.colorize_score)
                        
                        # Emoji selon la catégorie
                        emoji_map = {
                            "Rentabilité": "💰",
                            "Liquidité": "💧",
                            "Solvabilité": "🏦",
                            "Valorisation": "📈",
                            "Risque & Marché": "⚡"
                        }
                        emoji = emoji_map.get(category, "📊")
                        
                        print(f"\n{Fore.YELLOW}{emoji} {category.upper()}{Style.RESET_ALL}")
                        print(f"Score catégorie : {f.colorize_percent_score(scores_by_category[category])}")
                        
                        p.afficher_table(
                            df_cat,
                            ["Indicateur", "Valeur", "Note (/10)", "Poids (%)", "Interprétation", "Définition"],
                            center_cols=["Valeur", "Note (/10)", "Poids (%)"]
                        )
                
                print(f"\n{Fore.GREEN}{'='*80}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}Score fondamental global : {f.colorize_percent_score(sf)}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}{'='*80}{Style.RESET_ALL}")
                
            except Exception as e:
                print(Fore.RED + f"⚠️ Erreur lors de l'analyse fondamentale de {ticker} : {e}" + Style.RESET_ALL)
                print("→ Passage à l'analyse technique...\n")
                sf = None

            print("-"*80)

            # === TECHNIQUE ===
            try:
                ta = TechnicalAnalysis(ticker)
                df_t, st, reco, llm_reco, fibo = ta.run()

                if df_t is None or df_t.empty:
                    print(Fore.RED + "❌ Données techniques non disponibles." + Style.RESET_ALL)
                    st = None
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
                st = None
                reco = "Non disponible"

            print("="*80)

            # === ACTUALITÉS ===
            ##CODE POUR ANALYSE DES ACTUALITÉS À AJOUTER ICI##
            # newsAnalysis = NewsAnalysis(ticker)
            # news_interpretation, score = newsAnalysis.run(company_name)
            # print(Fore.YELLOW + "\n=== 📰 ANALYSE DES ACTUALITÉS RÉCENTES ===" + Style.RESET_ALL)
            # print(f"Score des actualités : {f.colorize_percent_score(news_interpretation['Score'])}")
            # print(f"Interprétation des actualités : {news_interpretation['Interprétation']}")

            # === SCORE GLOBAL ===
            if sf is None or st is None:
                sg = None
                print(
                    Fore.YELLOW
                    + "⚠️ Score global indisponible : analyse fondamentale ou technique absente."
                    + Style.RESET_ALL
                )
            else:
                try:
                    sg, txt = self.score_final(sf, st)
                    print(Style.BRIGHT + Fore.WHITE + Back.BLUE +
                        f"   🧮 SCORE GLOBAL PONDÉRÉ : {f.colorize_percent_score(sg)}   " +
                        Style.RESET_ALL)
                    print(f"Interprétation finale : {txt}")
                except Exception as e:
                    print(Fore.RED + f"⚠️ Erreur lors du calcul du score global : {e}" + Style.RESET_ALL)
                    sg = None

            print("="*80)

            price_str = f"{llm_reco:.2f} {currency}".strip() if llm_reco is not None else "N/A"
            fibo_analysis = fibo.get("analysis", {}) if fibo else {}
            fibo_targets = fibo_analysis.get("targets", [])
            fibo_score = fibo_analysis.get("score")
            fibo_score_str = f"{fibo_score:.2f}/10" if fibo_score is not None else "N/A"
            fundamental_score = f"{sf:.2f}/100" if sf is not None else "N/A"
            technical_score = f"{st:.2f}/100" if st is not None else "N/A"

            if ticker in self.portfolio:
                print(
                    Style.BRIGHT + Fore.WHITE + Back.GREEN +
                    f"   📢 Objectif de sortie : {ticker}   " +
                    Style.RESET_ALL
                )

                fibo_targets_text = "\n".join(
                    f"Vendre à {item['level']:.2f} EUR → {item['gain_potential']:.2f}%"
                    for item in fibo_targets
                ) or "Niveaux Fibonacci indisponibles"

                message = (
                    f"📢 {company_name} ({ticker}) — Prix actuel {price_str}\n\n"
                    f"📊 Score Technique : {technical_score}\n"
                    f"🔗 Score Fibonacci : {fibo_score_str}\n"
                    f"✅ Score Fondamental : {fundamental_score}\n\n"
                    "🔗 Fibonacci Analysis :\n"
                    f"{fibo_targets_text}"
                )

                SendNotification.send(message, canal="portfolio")

            elif sf is not None and st is not None and sf > 70 and st > 60:
                message = (
                    f"🌟 {company_name} ({ticker}) — {price_str} — Opportunité d'achat à considérer\n\n"
                    f"📊 Score Technique : {technical_score}\n"
                    f"🔗 Score Fibonacci : {fibo_score_str}\n"
                    f"✅ Score Fondamental : {fundamental_score}\n"
                )
                SendNotification.send(message, canal="high")

            elif sf is not None and st is not None and sf > 70 and st > 40:
                potential = fibo_targets[-1].get("gain_potential") if fibo_targets else None
                potential_str = f"{potential:.2f}%" if potential is not None else "N/A"
                message = (
                    f"🚀 {company_name} ({ticker}) — {price_str}\n\n"
                    f"📊 Score Technique : {technical_score}\n"
                    f"🔗 Score Fibonacci : {fibo_score_str}\n"
                    f"🔗 Potential : {potential_str}\n"
                    f"✅ Score Fondamental : {fundamental_score}\n"
                )
                SendNotification.send(message, canal="normal")
