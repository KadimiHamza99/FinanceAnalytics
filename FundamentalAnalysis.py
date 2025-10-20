import yfinance as yf
import pandas as pd
from colorama import Fore
from Formatter import Formatter 
import warnings
warnings.filterwarnings('ignore')

# Définition de la classe Formatter pour que le code soit fonctionnel même sans le fichier Formatter.py
class Formatter:
    def format_pourcentage(self, value):
        if value is not None:
            return f"{value * 100:.2f}%"
        return "N/A"

class FundamentalAnalysis:
    """
    Classe réalisant une analyse fondamentale complète sur un ticker boursier.
    Calcule différents indicateurs avec des poids adaptés au secteur d'activité.
    """

    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol
        self.ticker = yf.Ticker(ticker_symbol)
        self.info = self.ticker.info
        self.formatter = Formatter()
        self.sector = self.info.get('sector', 'Général')
        
    def get_sector_weights(self):
        """
        Retourne les poids des indicateurs selon le secteur d'activité
        """
        sector_weights = {
            'Technology': {
                'ROE': 11, 'ROA': 6, 'Croissance attendue': 12, 'Forward P/E': 9,
                'Trailing PE': 4, 'FCF Yield': 16, 'Marge nette': 9,
                'Beta': 6, 'Dette/Equity': 6, 'Avis Analystes': 8, 'Position 52W': 6,
                'Price to Book': 7
            },  # Total: 100
            'Healthcare': {
                'ROE': 8, 'ROA': 7, 'Croissance attendue': 10, 'Forward P/E': 8,
                'Trailing PE': 5, 'FCF Yield': 14, 'Marge nette': 14,
                'Beta': 5, 'Dette/Equity': 8, 'Avis Analystes': 10, 'Position 52W': 3, 
                'Price to Book': 8
            },  # Total: 100
            'Financial Services': {
                'ROE': 21, 'ROA': 11, 'Price to Book': 22,
                'Forward P/E': 5, 'Trailing PE': 4, 'Dette/Equity': 11, 'FCF Yield': 4,
                'Beta': 6, 'Avis Analystes': 10, 'Position 52W': 6
            },  # Total: 100
            'Energy': {
                'ROE': 9, 'ROA': 3, 'FCF Yield': 20, 'Dividend Yield': 14,
                'Payout ratio': 7, 'Trailing PE': 4, 'Forward P/E': 6,
                'Beta': 6, 'Dette/Equity': 12, 'Current Ratio': 6, 'Position 52W': 5, 
                'Avis Analystes': 8
            },  # Total: 100
            'Consumer Cyclical': {
                'ROE': 9, 'ROA': 6, 'Croissance attendue': 10, 'Forward P/E': 6,
                'Trailing PE': 4, 'FCF Yield': 12, 'Marge nette': 13,
                'Beta': 6, 'Dette/Equity': 6, 'Current Ratio': 8, 'Position 52W': 8, 
                'Avis Analystes': 10
            },  # Total: 100
            'Consumer Defensive': {
                'ROE': 9, 'ROA': 8, 'Marge nette': 15, 'Dividend Yield': 12,
                'Payout ratio': 5, 'FCF Yield': 11, 'Trailing PE': 7,
                'Beta': 3, 'Dette/Equity': 7, 'Current Ratio': 8, 'Position 52W': 5, 
                'Avis Analystes': 10
            },  # Total: 100
            'Communication Services': {
                'ROE': 8, 'ROA': 6, 'Croissance attendue': 12, 'Forward P/E': 8,
                'Trailing PE': 5, 'FCF Yield': 15, 'Marge nette': 12,
                'Beta': 9, 'Avis Analystes': 10, 'Position 52W': 5, 'Dette/Equity': 5, 
                'Price to Book': 5
            },  # Total: 100
            'Industrials': {
                'ROE': 9, 'ROA': 9, 'Marge nette': 11, 'FCF Yield': 11,
                'Croissance attendue': 8, 'Trailing PE': 7,
                'Beta': 6, 'Dette/Equity': 8, 'Current Ratio': 8, 'Avis Analystes': 10, 
                'Position 52W': 4, 'Price to Book': 9
            },  # Total: 100
            'Real Estate': {
                'ROE': 7, 'ROA': 5, 'FCF Yield': 14, 'Dividend Yield': 11,
                'Payout ratio': 5, 'Price to Book': 18, 'Trailing PE': 3,
                'Beta': 6, 'Dette/Equity': 11, 'Current Ratio': 5, 'Position 52W': 5,
                'Avis Analystes': 10
            },  # Total: 100
            'Général': {
                'ROE': 10, 'ROA': 8, 'Croissance attendue': 8, 'Forward P/E': 5,
                'Trailing PE': 5, 'Price to Book': 5, 'Marge nette': 9,
                'FCF Yield': 9, 'Dette/Equity': 8, 'Current Ratio': 5,
                'Beta': 5, 'Avis Analystes': 10, 'Dividend Yield': 4, 'Payout ratio': 2, 
                'Position 52W': 7
            }   # Total: 100
        }

        
        # Trouve le secteur correspondant ou utilise 'Général'
        for sector_key in sector_weights:
            if sector_key.lower() in str(self.sector).lower():
                return sector_weights[sector_key]
        
        return sector_weights['Général']

    def run(self):
        info = self.info
        f = self.formatter
        data = []
        
        # # AJOUT DU PRINT POUR AFFICHER TOUTES LES DONNÉES BRUTES
        # print(Fore.CYAN + "=========================================================")
        # print(Fore.CYAN + f"🚨 DONNÉES BRUTES DE YFINANCE POUR {self.ticker_symbol} 🚨")
        # print(Fore.CYAN + "=========================================================" + Fore.RESET)
        # # print(self.info)
        # print(Fore.CYAN + "=========================================================" + Fore.RESET)
        # # FIN DE L'AJOUT

        # === NOUVELLE SECTION : Infos générales de l'entreprise ===
        company_name = info.get("shortName") or info.get("longName") or self.ticker_symbol
        country = info.get("country", "N/A")
        industry = info.get("industry", "N/A")
        sector = info.get("sector", "N/A")
        market_cap = info.get("marketCap", "N/A")
        currency = info.get("currency", "N/A")
        # Conversion en milliards si disponible
        if market_cap is not None:
            market_cap_display = f"{market_cap / 1e9:.2f}M {currency}"
        else:
            market_cap_display = "N/A"
        print(Fore.MAGENTA + "==================== INFOS ENTREPRISE ====================" + Fore.RESET)
        print(f"Nom : {company_name}")
        print(f"Ticker : {self.ticker_symbol}")
        print(f"Pays : {country}")
        print(f"Secteur : {sector}")
        print(f"Industrie : {industry}")
        print(f"Capitalisation boursière : {market_cap_display}")
        print(Fore.MAGENTA + "==========================================================" + Fore.RESET)
        
        # Récupère les poids selon le secteur
        weights = self.get_sector_weights()
        print(f"🔍 Analyse pour le secteur: {self.sector}")

        def add(nom, val, note, interp, defn, petite_def):
            # Utilise le poids du secteur ou 0 si l'indicateur n'est pas utilisé
            poids = weights.get(nom, 0)
            if poids > 0:  # N'ajoute que les indicateurs avec poids > 0
                data.append({
                    "Indicateur": nom,
                    "Valeur": val,
                    "Note (/10)": note,
                    "Poids (%)": poids,
                    "Interprétation": interp,
                    "Définition": defn,
                    "Petite Définition": petite_def
                })

        # === ROE ===
        roe = info.get("returnOnEquity")
        if roe:
            if roe > 0.20: note, interp = 9, "Excellente rentabilité"
            elif roe > 0.12: note, interp = 7, "Bonne rentabilité"
            elif roe > 0.07: note, interp = 5, "Rentabilité moyenne"
            else: note, interp = 3, "Rentabilité faible"
        else:
            note, interp = 5, "Données indisponibles"
        add("ROE", f.format_pourcentage(roe), note, interp, 
            "Return on Equity - Mesure combien de profit une entreprise génère pour chaque euro investi par les actionnaires",
            "Rentabilité des capitaux propres")

        # === ROA ===
        roa = info.get("returnOnAssets")
        if roa:
            if roa > 0.08: note, interp = 9, "Excellente utilisation des actifs"
            elif roa > 0.05: note, interp = 7, "Bonne utilisation des actifs"
            elif roa > 0.02: note, interp = 5, "Utilisation moyenne"
            else: note, interp = 3, "Faible utilisation des actifs"
        else:
            note, interp = 5, "Données indisponibles"
        add("ROA", f.format_pourcentage(roa), note, interp, 
    "Return on Assets - Indique l'efficacité de l'entreprise à utiliser ses actifs pour générer du profit",
    "Rentabilité par rapport aux actifs")

        # === Forward P/E ===
        forward_pe = info.get("forwardPE")

        if forward_pe is not None:
            if forward_pe < 10:
                note, interp = 9, "Très attractif 🚀"
            elif forward_pe < 15:
                note, interp = 7, "Attractif ✅"
            elif forward_pe < 25:
                note, interp = 5, "Moyen 📊"
            elif forward_pe < 35:
                note, interp = 3, "Élevé ⚠️"
            else:
                note, interp = 1, "Très élevé 🚨"
            add(
                "Forward P/E",
                f"{forward_pe:.1f}x",
                note,
                interp,
                "Ratio cours/bénéfices anticipé pour l'année suivante",
                "Valorisation future anticipée de l'action"
            )
        else:
            note, interp = 5, "Données indisponibles"
            add(
                "Forward P/E",
                "N/A",
                note,
                interp,
                "Ratio cours/bénéfices anticipé pour l'année suivante",
                "Valorisation future anticipée de l'action"
            )

        # === Croissance attendue (Forward PE) ===
        pe = info.get("trailingPE")
        forward_pe = info.get("forwardPE")
        ratio = None
        if pe and forward_pe:
            try:
                ratio = 1 - forward_pe / pe
                if ratio > 0.15: note, interp = 9, "Croissance forte attendue 🚀"
                elif ratio > 0.05: note, interp = 7, "Croissance modérée 👍"
                elif ratio < -0.05: note, interp = 3, "Baisse probable 📉"
                else: note, interp = 5, "Stabilité attendue 😐"
            except (TypeError, ZeroDivisionError):
                note, interp = 3, "Calcul impossible"
        else:
            note, interp = 5, "Données insuffisantes"
        add("Croissance attendue", f.format_pourcentage(ratio), note, interp,
    "Différence entre le PER actuel et le PER prévisionnel, reflétant les attentes de croissance future des bénéfices",
    "Prévision de croissance")
        
        # === NOUVEL INDICATEUR: Trailing PE ===
        trailing_pe = info.get("trailingPE")
        if trailing_pe is not None:
            # Évaluation différente selon le secteur pour plus de précision
            if self.sector in ['Technology', 'Healthcare']:
                # Secteurs à croissance élevée - PER plus élevé accepté
                if trailing_pe < 25: note, interp = 9, "Très attractif pour le secteur 🚀"
                elif trailing_pe < 35: note, interp = 7, "Correct pour le secteur ✅"
                elif trailing_pe < 50: note, interp = 5, "Élevé mais justifiable 📊"
                elif trailing_pe < 70: note, interp = 3, "Très élevé ⚠️"
                else: note, interp = 1, "Excessif 🚨"
            elif self.sector in ['Financial Services', 'Energy', 'Utilities']:
                # Secteurs value - PER bas attendu
                if trailing_pe < 10: note, interp = 9, "Excellent rapport 💎"
                elif trailing_pe < 15: note, interp = 7, "Bon rapport ✅"
                elif trailing_pe < 20: note, interp = 5, "Dans la moyenne 📊"
                elif trailing_pe < 25: note, interp = 3, "Élevé pour le secteur ⚠️"
                else: note, interp = 1, "Très élevé 🚨"
            else:
                # Secteurs généraux
                if trailing_pe < 12: note, interp = 9, "Très attractif 💎"
                elif trailing_pe < 18: note, interp = 7, "Attractif ✅"
                elif trailing_pe < 25: note, interp = 5, "Valorisation correcte 📊"
                elif trailing_pe < 35: note, interp = 3, "Élevé ⚠️"
                else: note, interp = 1, "Très élevé 🚨"
        else:
            note, interp = 5, "Données indisponibles"
        add("Trailing PE", f"{trailing_pe:.2f}" if trailing_pe else "N/A", note, interp,
            "Price to Earnings Ratio basé sur les bénéfices des 12 derniers mois - Mesure la valorisation actuelle par rapport aux performances passées",
            "PER sur 12 mois")

        # === NOUVEL INDICATEUR: Beta ===
        beta = info.get("beta")
        if beta is not None:
            if beta < 0.8: 
                note, interp = 8, "Faible volatilité (moins risqué) 🛡️"
            elif beta < 1.2: 
                note, interp = 6, "Volatilité similaire au marché 📊"
            elif beta < 1.5: 
                note, interp = 4, "Volatilité élevée (plus risqué) ⚠️"
            else: 
                note, interp = 2, "Très haute volatilité (très risqué) 🚨"
        else:
            note, interp = 5, "Données indisponibles"
        add("Beta", f"{beta:.2f}" if beta else "N/A", note, interp,
            "Beta - Mesure la volatilité de l'action par rapport au marché (indice de référence S&P 500). "
            "Un beta de 1 signifie une volatilité égale au marché, <1 moins volatile, >1 plus volatile",
            "Volatilité par rapport au marché")

        # === Price to Book === (Principalement pour banques et immobilier)
        pb = info.get("priceToBook")
        if pb:
            if pb < 1: note, interp = 9, "Sous la valeur comptable 💎"
            elif pb < 1.5: note, interp = 7, "Bon rapport ✅"
            elif pb < 3: note, interp = 5, "Valorisation standard 📊"
            elif pb < 5: note, interp = 3, "Élevé ⚠️"
            else: note, interp = 1, "Très élevé 🚨"
        else:
            note, interp = 5, "Données indisponibles"
        add("Price to Book", f"{pb:.2f}" if pb else "N/A", note, interp, 
    "Price to Book Ratio - Compare la valeur de marché de l'entreprise à sa valeur comptable",
    "Prix vs valeur comptable")

        # === Dette / Equity ===
        debt = info.get("debtToEquity")
        if debt is not None:
            if debt < 40: note, interp = 9, "Faible endettement 🛡️"
            elif debt < 100: note, interp = 6, "Endettement raisonnable 🙂"
            elif debt < 150: note, interp = 4, "Endettement élevé 😟"
            else: note, interp = 2, "Très endettée 🛑"
        else:
            note, interp = 2, "Données indisponibles"
        add("Dette/Equity", f"{debt:.2f}" if debt else "N/A", note, interp, 
    "Debt to Equity Ratio - Mesure le niveau d'endettement par rapport aux capitaux propres",
    "Niveau d'endettement")

        # === Current Ratio === (Principalement pour industrie et consommation)
        current_ratio = info.get("currentRatio")
        if current_ratio:
            if current_ratio > 2: note, interp = 9, "Excellente liquidité 🚀"
            elif current_ratio > 1.5: note, interp = 7, "Bonne liquidité ✅"
            elif current_ratio > 1: note, interp = 5, "Liquidité acceptable 📊"
            else: note, interp = 3, "Problème de liquidité ⚠️"
        else:
            note, interp = 5, "Données indisponibles"
        add("Current Ratio", f"{current_ratio:.2f}" if current_ratio else "N/A", note, interp, 
    "Ratio de liquidité générale - Capacité de l'entreprise à rembourser ses dettes à court terme avec ses actifs à court terme",
    "Liquidité à court terme")

        # === Marge nette ===
        marg = info.get("profitMargins")
        if marg:
            if marg > 0.15: note, interp = 9, "Marge élevée ✨"
            elif marg > 0.08: note, interp = 6, "Marge correcte 👍"
            elif marg > 0.05: note, interp = 4, "Marge faible 🤏"
            else: note, interp = 2, "Marge très faible 😥"
        else:
            note, interp = 5, "Données indisponibles"
        add("Marge nette", f.format_pourcentage(marg), note, interp, 
    "Profit Margin - Pourcentage du chiffre d'affaires qui reste en bénéfice net après toutes les dépenses",
    "Profit sur les ventes")

        # === Free Cash Flow Yield === (Supprime FCF Margin - redondant)
        fcf = info.get("freeCashflow")
        market_cap = info.get("marketCap")
        if fcf and market_cap and market_cap > 0:
            fcf_yield = fcf / market_cap
            if fcf_yield > 0.08: note, interp = 9, "Très bon rendement cash 🔥"
            elif fcf_yield > 0.05: note, interp = 7, "Bon rendement cash ✅"
            elif fcf_yield > 0.03: note, interp = 5, "Rendement cash correct 📊"
            else: note, interp = 3, "Faible rendement cash ⚠️"
            add("FCF Yield", f.format_pourcentage(fcf_yield), note, interp, 
    "Free Cash Flow Yield - Rendement du flux de trésorerie libre par rapport à la capitalisation boursière, indicateur de cash disponible",
    "Rendement du cash disponible")

        # === Avis des Analystes ===
        try:
            rec_mean = info.get("recommendationMean")
            num_analysts = info.get("numberOfAnalystOpinions", 0)

            if rec_mean is not None:
                # Base sur la note moyenne
                if rec_mean <= 1.5:
                    note, base_interp = 9, "Achat fort 🚀"
                elif rec_mean <= 2.5:
                    note, base_interp = 7, "Achat ✅"
                elif rec_mean <= 3.5:
                    note, base_interp = 5, "Neutre 📊"
                elif rec_mean <= 4.5:
                    note, base_interp = 3, "Vente ⚠️"
                else:
                    note, base_interp = 1, "Vente forte 🚨"

                # Ajustement selon le nombre d'analystes
                if num_analysts < 3:
                    note = max(1, note - 2)  # réduire la note si très peu d'analystes
                    interp = f"{base_interp} ⚠️ Peu d'avis ({num_analysts})"
                elif num_analysts < 6:
                    note = max(1, note - 1)
                    interp = f"{base_interp} ⚠️ Avis limités ({num_analysts})"
                else:
                    interp = f"{base_interp} ({num_analysts} analystes)"

                grade_str = f"{rec_mean:.1f}/5"
                add(
                    "Avis Analystes",
                    grade_str,
                    note,
                    interp,
                    "Note moyenne des recommandations des analystes",
                    "Note moyenne des experts"
                )
            else:
                note, interp = 5, "Données indisponibles"
                add(
                    "Avis Analystes",
                    "N/A",
                    note,
                    interp,
                    "Recommandation des analystes",
                    "Recommandation des experts"
                )
        except Exception as e:
            note, interp = 3, "Erreur de récupération"
            add(
                "Avis Analystes",
                "N/A",
                note,
                interp,
                "Recommandation des analystes",
                "Recommandation des experts"
            )



        # === Dividend Yield === (Principalement pour valeur et revenu)
        div = info.get("dividendYield")
        if div:
            if div/100 > 0.06: note, interp = 6, "Rendement élevé (attention soutenabilité)"
            elif div/100 > 0.03: note, interp = 8, "Bon rendement 💰"
            elif div/100 > 0.01: note, interp = 5, "Rendement modeste"
            else: note, interp = 3, "Rendement faible"
        else:
            note, interp = 3, "Pas de dividende 🚫"
        add("Dividend Yield", div, note, interp, 
    "Rendement du dividende - Dividende annuel divisé par le prix de l'action, montre le revenu généré par l'investissement",
    "Rendement annuel du dividende")

        # === Payout Ratio === (Pour entreprises avec dividendes)
        payout = info.get("payoutRatio")
        if payout is not None:
            if 0.3 <= payout <= 0.6: note, interp = 9, "Distribution équilibrée ✅"
            elif payout <= 0.9: note, interp = 6, "Distribution élevée ⬆️"
            elif payout > 1: note, interp = 2, "Non soutenable 🚨"
            else: note, interp = 4, "Distribution trop faible ⬇️"
        else:
            note, interp = 5, "Données indisponibles"
        add("Payout ratio", f.format_pourcentage(payout), note, interp, 
    "Pourcentage des bénéfices distribués aux actionnaires sous forme de dividendes, indique la soutenabilité des paiements",
    "Part des bénéfices distribuée")

        # === Position 52 semaines ===
        current_price = info.get("regularMarketPrice")
        low_52w = info.get("fiftyTwoWeekLow")
        high_52w = info.get("fiftyTwoWeekHigh")
        if current_price and low_52w and high_52w and high_52w != low_52w:
            position = (current_price - low_52w) / (high_52w - low_52w) * 100
            if position < 20: note, interp = 9, "🟢 Très proche du plus bas annuel"
            elif position < 40: note, interp = 7, "🙂 Bas (bon prix)"
            elif position < 60: note, interp = 5, "🤔 Milieu du range"
            elif position < 80: note, interp = 3, "🔴 Haut (cher)"
            else: note, interp = 2, "⚠️ Proche du plus haut"
            add("Position 52W", f"{position:.2f}%", note, interp, 
    "Position du prix actuel par rapport aux plus haut et plus bas sur 52 semaines, indique si l'action est chère ou bon marché",
    "Cours par rapport au range annuel")

        # === Score global ===
        df = pd.DataFrame(data)
        df["Score pondéré"] = df["Note (/10)"] * df["Poids (%)"] / 10
        score_total = df["Score pondéré"].sum()

        return df, score_total