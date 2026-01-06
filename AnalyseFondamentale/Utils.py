from colorama import Fore

class Utils:
    """
    Classe utilitaire contenant les poids sectoriels
    et d'autres méthodes d'aide générales.
    """

    @staticmethod
    def get_sector_weights(sector: str):
        """
        Retourne les poids des indicateurs selon le secteur d'activité.
        Chaque secteur totalise 100 points.
        """

        sector_weights = {
            'Technology': {
                # Rentabilité (35) - Priorité : marges et croissance
                'ROE': 7, 'ROA': 4, 'Marge nette': 7, 'Marge opérationnelle': 6, 'Croissance bénéfices': 6, 'FCF Yield': 5,
                # Liquidité (7)
                'Current Ratio': 2, 'Quick Ratio': 2, 'Operating Cash Flow': 3,
                # Solvabilité (10)
                'Dette/Equity': 3, 'Dette/EBITDA': 3, 'Dette/Actifs': 2, 'Valeur comptable': 2,
                # Valorisation (33) - Priorité : Forward PE et PEG
                'Forward P/E': 9, 'Trailing PE': 3, 'Price to Book': 3, 'PEG Ratio': 8, 'Dividend Yield': 3, 'Payout ratio': 7,
                # Risque & Marché (15)
                'Beta': 4, 'Position 52W': 6, 'Avis Analystes': 5
            },  # total = 100

            'Healthcare': {
                # Rentabilité (37) - Priorité : marges élevées pour R&D
                'ROE': 7, 'ROA': 5, 'Marge nette': 9, 'Marge opérationnelle': 7, 'Croissance bénéfices': 5, 'FCF Yield': 4,
                # Liquidité (10)
                'Current Ratio': 4, 'Quick Ratio': 3, 'Operating Cash Flow': 3,
                # Solvabilité (13)
                'Dette/Equity': 5, 'Dette/EBITDA': 4, 'Dette/Actifs': 2, 'Valeur comptable': 2,
                # Valorisation (26)
                'Forward P/E': 7, 'Trailing PE': 4, 'Price to Book': 3, 'PEG Ratio': 5, 'Dividend Yield': 3, 'Payout ratio': 4,
                # Risque & Marché (14)
                'Beta': 3, 'Position 52W': 6, 'Avis Analystes': 5
            },  # total = 100

            'Financial Services': {
                # Rentabilité (33) - Priorité : ROE et ROA dominants
                'ROE': 15, 'ROA': 8, 'Marge nette': 5, 'Marge opérationnelle': 5,
                # Liquidité (4)
                'Current Ratio': 2, 'Quick Ratio': 2,
                # Solvabilité (15)
                'Dette/Equity': 5, 'Dette/EBITDA': 4, 'Dette/Actifs': 3, 'Valeur comptable': 3,
                # Valorisation (38) - Priorité : P/B et dividendes
                'Price to Book': 14, 'Dividend Yield': 9, 'Payout ratio': 6, 'Forward P/E': 4, 'Trailing PE': 3, 'PEG Ratio': 2,
                # Risque & Marché (10)
                'Beta': 3, 'Position 52W': 3, 'Avis Analystes': 4
            },  # total = 100

            'Energy': {
                # Rentabilité (24) - Équilibré entre marges et cash
                'ROE': 4, 'ROA': 3, 'Marge nette': 4, 'Marge opérationnelle': 5, 'Marge brute': 5, 'FCF Yield': 3,
                # Liquidité (14) - Important pour cycles
                'Current Ratio': 6, 'Quick Ratio': 3, 'Operating Cash Flow': 5,
                # Solvabilité (22) - Critique secteur capitalistique
                'Dette/Equity': 7, 'Dette/EBITDA': 6, 'Dette/Actifs': 5, 'Valeur comptable': 4,
                # Valorisation (28) - Dividendes clés
                'Dividend Yield': 8, 'Forward P/E': 5, 'Trailing PE': 4, 'Price to Book': 3, 'Payout ratio': 4, 'PEG Ratio': 4,
                # Risque & Marché (12)
                'Beta': 4, 'Position 52W': 4, 'Avis Analystes': 4
            },  # total = 100

            'Consumer Cyclical': {
                # Rentabilité (32)
                'ROE': 7, 'ROA': 5, 'Marge nette': 8, 'Marge opérationnelle': 6, 'Croissance bénéfices': 4, 'FCF Yield': 2,
                # Liquidité (12)
                'Current Ratio': 5, 'Quick Ratio': 3, 'Operating Cash Flow': 4,
                # Solvabilité (13)
                'Dette/Equity': 5, 'Dette/EBITDA': 4, 'Dette/Actifs': 2, 'Valeur comptable': 2,
                # Valorisation (25)
                'Forward P/E': 8, 'Trailing PE': 4, 'Price to Book': 3, 'PEG Ratio': 4, 'Dividend Yield': 3, 'Payout ratio': 3,
                # Risque & Marché (18) - Sentiment important
                'Beta': 5, 'Position 52W': 7, 'Avis Analystes': 6
            },  # total = 100

            'Consumer Defensive': {
                # Rentabilité (31) - Marges critiques
                'ROE': 6, 'ROA': 5, 'Marge nette': 10, 'Marge opérationnelle': 6, 'FCF Yield': 4,
                # Liquidité (10)
                'Current Ratio': 5, 'Quick Ratio': 3, 'Operating Cash Flow': 2,
                # Solvabilité (14)
                'Dette/Equity': 5, 'Dette/EBITDA': 4, 'Dette/Actifs': 3, 'Valeur comptable': 2,
                # Valorisation (35) - Dividendes prioritaires
                'Dividend Yield': 12, 'Payout ratio': 6, 'Forward P/E': 5, 'Trailing PE': 4, 'Price to Book': 3, 'PEG Ratio': 5,
                # Risque & Marché (10)
                'Beta': 3, 'Position 52W': 3, 'Avis Analystes': 4
            },  # total = 100

            'Communication Services': {
                # Rentabilité (34)
                'ROE': 7, 'ROA': 7, 'Marge nette': 8, 'Marge opérationnelle': 6, 'Croissance bénéfices': 3, 'FCF Yield': 3,
                # Liquidité (8)
                'Current Ratio': 3, 'Quick Ratio': 3, 'Operating Cash Flow': 2,
                # Solvabilité (13)
                'Dette/Equity': 5, 'Dette/EBITDA': 4, 'Dette/Actifs': 2, 'Valeur comptable': 2,
                # Valorisation (30)
                'Forward P/E': 7, 'Trailing PE': 4, 'Price to Book': 5, 'PEG Ratio': 6, 'Dividend Yield': 4, 'Payout ratio': 4,
                # Risque & Marché (15)
                'Beta': 4, 'Position 52W': 6, 'Avis Analystes': 5
            },  # total = 100

            'Industrials': {
                # Rentabilité (30)
                'ROE': 7, 'ROA': 5, 'Marge nette': 7, 'Marge opérationnelle': 6, 'Croissance bénéfices': 3, 'FCF Yield': 2,
                # Liquidité (12)
                'Current Ratio': 5, 'Quick Ratio': 3, 'Operating Cash Flow': 4,
                # Solvabilité (15) - Dette importante
                'Dette/Equity': 6, 'Dette/EBITDA': 5, 'Dette/Actifs': 2, 'Valeur comptable': 2,
                # Valorisation (28)
                'Forward P/E': 7, 'Trailing PE': 5, 'Price to Book': 4, 'Dividend Yield': 4, 'Payout ratio': 3, 'PEG Ratio': 5,
                # Risque & Marché (15)
                'Beta': 4, 'Position 52W': 6, 'Avis Analystes': 5
            },  # total = 100

            'Real Estate': {
                # Rentabilité (17)
                'ROE': 4, 'ROA': 3, 'Marge nette': 4, 'Marge opérationnelle': 4, 'FCF Yield': 2,
                # Liquidité (9)
                'Current Ratio': 4, 'Quick Ratio': 2, 'Operating Cash Flow': 3,
                # Solvabilité (24) - Critique immobilier
                'Dette/Equity': 8, 'Dette/EBITDA': 7, 'Dette/Actifs': 5, 'Valeur comptable': 4,
                # Valorisation (42) - P/B et dividendes dominants
                'Price to Book': 15, 'Dividend Yield': 13, 'Payout ratio': 5, 'Forward P/E': 4, 'Trailing PE': 3, 'PEG Ratio': 2,
                # Risque & Marché (8)
                'Beta': 3, 'Position 52W': 3, 'Avis Analystes': 2
            },  # total = 100

            'Utilities': {
                # Rentabilité (21)
                'ROE': 5, 'ROA': 4, 'Marge nette': 5, 'Marge opérationnelle': 5, 'FCF Yield': 2,
                # Liquidité (8)
                'Current Ratio': 4, 'Quick Ratio': 2, 'Operating Cash Flow': 2,
                # Solvabilité (26) - Dette structurelle élevée
                'Dette/Equity': 9, 'Dette/EBITDA': 8, 'Dette/Actifs': 5, 'Valeur comptable': 4,
                # Valorisation (37) - Dividendes critiques
                'Dividend Yield': 14, 'Payout ratio': 5, 'Price to Book': 6, 'Forward P/E': 5, 'Trailing PE': 4, 'PEG Ratio': 3,
                # Risque & Marché (8)
                'Beta': 3, 'Position 52W': 3, 'Avis Analystes': 2
            },  # total = 100

            'Basic Materials': {
                # Rentabilité (28)
                'ROE': 6, 'ROA': 5, 'Marge nette': 6, 'Marge opérationnelle': 6, 'Croissance bénéfices': 3, 'FCF Yield': 2,
                # Liquidité (12)
                'Current Ratio': 5, 'Quick Ratio': 3, 'Operating Cash Flow': 4,
                # Solvabilité (17)
                'Dette/Equity': 6, 'Dette/EBITDA': 5, 'Dette/Actifs': 4, 'Valeur comptable': 2,
                # Valorisation (28)
                'Forward P/E': 6, 'Trailing PE': 5, 'Price to Book': 5, 'Dividend Yield': 5, 'PEG Ratio': 4, 'Payout ratio': 3,
                # Risque & Marché (15)
                'Beta': 5, 'Position 52W': 6, 'Avis Analystes': 4
            },  # total = 100

            'Général': {
                # Rentabilité (30)
                'ROE': 7, 'ROA': 5, 'Marge nette': 7, 'Marge opérationnelle': 5, 'Croissance bénéfices': 4, 'FCF Yield': 2,
                # Liquidité (10)
                'Current Ratio': 4, 'Quick Ratio': 3, 'Operating Cash Flow': 3,
                # Solvabilité (14)
                'Dette/Equity': 5, 'Dette/EBITDA': 5, 'Dette/Actifs': 2, 'Valeur comptable': 2,
                # Valorisation (31)
                'Forward P/E': 6, 'Trailing PE': 4, 'Price to Book': 5, 'Dividend Yield': 5, 'Payout ratio': 3, 'PEG Ratio': 5, 'FCF Yield': 3,
                # Risque & Marché (15)
                'Beta': 4, 'Position 52W': 6, 'Avis Analystes': 5
            }  # total = 100
        }


        for sector_key in sector_weights:
            if sector_key.lower() in str(sector).lower():
                return sector_weights[sector_key]

        return sector_weights['Général']


    @staticmethod
    def print_company_info(info: dict, ticker_symbol: str):
        """
        Affiche les informations générales d'une entreprise à partir des données yfinance
        """
        company_name = info.get("shortName") or info.get("longName") or ticker_symbol
        country = info.get("country", "N/A")
        industry = info.get("industry", "N/A")
        sector = info.get("sector", "N/A")
        market_cap = info.get("marketCap", None)
        currency = info.get("currency", "N/A")

        # Conversion en milliards
        if market_cap:
            market_cap_display = f"{market_cap / 1e9:.2f} Milliard {currency}"
        else:
            market_cap_display = "N/A"

        print(Fore.MAGENTA + "==================== INFOS ENTREPRISE ====================" + Fore.RESET)
        print(f"Nom : {company_name}")
        print(f"Ticker : {ticker_symbol}")
        print(f"Pays : {country}")
        print(f"Secteur : {sector}")
        print(f"Industrie : {industry}")
        print(f"Capitalisation boursière : {market_cap_display}")
        print(Fore.MAGENTA + "==========================================================" + Fore.RESET)

    @staticmethod
    def print_yfinance_brut_data(info: dict):
        """
        Affiche les informations générales d'une entreprise à partir des données yfinance
        """

        print(Fore.RED + "==================== BRUT DATA ====================" + Fore.RED)
        print(info)
        print(Fore.RED + "==========================================================" + Fore.RED)



    @staticmethod
    def add_indicator(data: list, weights: dict, nom: str, val, note, interp, defn, petite_def):
        """
        Ajoute un indicateur au tableau d'analyse pondéré, 
        uniquement si le poids du secteur est > 0.
        """
        poids = weights.get(nom, 0)
        if poids > 0:
            data.append({
                "Indicateur": nom,
                "Valeur": val,
                "Note (/10)": note,
                "Poids (%)": poids,
                "Interprétation": interp,
                "Définition": defn,
                "Petite Définition": petite_def
            })


    @staticmethod
    def _get_sector_group(sector: str) -> str:
        """Identifie le groupe de secteur pour l'interprétation"""
        sector_lower = str(sector).lower()
        if any(s in sector_lower for s in ["tech", "information technology"]):
            return "Technology"
        elif any(s in sector_lower for s in ["health", "pharma", "bio", "medical"]):
            return "Healthcare"
        elif any(s in sector_lower for s in ["financial", "bank", "insurance", "finance"]):
            return "Financial Services"
        elif any(s in sector_lower for s in ["energy", "oil", "gas", "utilities"]):
            return "Energy"
        elif any(s in sector_lower for s in ["cyclical", "discretionary"]):
            return "Consumer Cyclical"
        elif any(s in sector_lower for s in ["defensive", "staples"]):
            return "Consumer Defensive"
        elif any(s in sector_lower for s in ["communication", "media", "telecom"]):
            return "Communication Services"
        elif any(s in sector_lower for s in ["industrial", "construction", "manufacturing"]):
            return "Industrials"
        elif any(s in sector_lower for s in ["real estate", "reit"]):
            return "Real Estate"
        else:
            return "General"