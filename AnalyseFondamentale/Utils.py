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
                'ROE': 12, 'ROA': 6, 'Forward P/E': 12,
                'Trailing PE': 5, 'FCF Yield': 20, 'Marge nette': 10,
                'Beta': 5, 'Dette/Equity': 6, 'Avis Analystes': 13, 'Position 52W': 11
            },  # total = 100
            # Justif: FCF + ROE + Forward P/E prioritaires (croissance & cash), analystes & momentum influents.

            'Healthcare': {
                'ROE': 10, 'ROA': 6, 'Forward P/E': 9,
                'Trailing PE': 6, 'FCF Yield': 18, 'Marge nette': 14,
                'Beta': 4, 'Dette/Equity': 8, 'Avis Analystes': 10, 'Position 52W': 15
            },  # total = 100
            # Ajustement: +5 FCF (R&D & besoin de cash) +5 Position52W (momentum et news cliniques peuvent changer les cours).
            # Justif: marges & FCF pour financer R&D; momentum/analystes influent fortement sur annonces.

            'Financial Services': {
                'ROE': 22, 'ROA': 10, 'Price to Book': 20, 'Dividend Yield': 10,
                'Payout ratio': 10, 'Dette/Equity': 7, 'Avis Analystes': 7,
                'Beta': 4, 'Forward P/E': 6, 'Trailing PE': 4
            },  # total = 100
            # Justif: ROE & P/B dominants pour banques/assurances; dividendes & payout importants; bilan/levier surveillés.

            'Energy': {
                'ROE': 8, 'ROA': 3, 'FCF Yield': 20, 'Dividend Yield': 14,
                'Payout ratio': 6, 'Trailing PE': 5, 'Forward P/E': 6,
                'Beta': 5, 'Dette/Equity': 13, 'Current Ratio': 7,
                'Position 52W': 6, 'Avis Analystes': 7
            },  # total = 100
            # Justif: FCF crucial (capex), dette & dividende clefs, valorisation cyclique moins structurante.

            'Consumer Cyclical': {
                'ROE': 9, 'ROA': 6, 'Forward P/E': 11,
                'Trailing PE': 6, 'FCF Yield': 13, 'Marge nette': 11,
                'Beta': 5, 'Dette/Equity': 6, 'Current Ratio': 7,
                'Position 52W': 12, 'Avis Analystes': 14
            },  # total = 100
            # Ajustement: +3 Position52W, +4 Avis Analystes, +3 FCF → reflète plus l'importance du sentiment & du cash.
            # Justif: secteur cyclique → sentiment/analystes & momentum sont des signaux avancés; FCF utile pour résistance.

            'Consumer Defensive': {
                'ROE': 8, 'ROA': 7, 'Marge nette': 16, 'Dividend Yield': 15,
                'Payout ratio': 10, 'FCF Yield': 10, 'Trailing PE': 6,
                'Beta': 4, 'Dette/Equity': 7, 'Current Ratio': 7,
                'Position 52W': 5, 'Avis Analystes': 5
            },  # total = 100
            # Justif: stabilité, marges et dividendes prioritaires; faible sensibilité au beta/momentum.

            'Communication Services': {
                'ROE': 10, 'ROA': 10, 'Forward P/E': 10,
                'Trailing PE': 5, 'FCF Yield': 14, 'Marge nette': 12,
                'Beta': 5, 'Avis Analystes': 12, 'Position 52W': 10,
                'Dette/Equity': 6, 'Price to Book': 6
            },  # total = 100
            # Ajustement: +4 Position52W, +3 PriceToBook, +3 ROA → pour corriger la somme et mieux représenter les télécoms vs streaming.
            # Justif: mix croissance/stabilité; FCF & analystes essentiels; ROA/PriceToBook légèrement plus importants localement.

            'Industrials': {
                'ROE': 9, 'ROA': 7, 'Marge nette': 10, 'FCF Yield': 11,
                'Trailing PE': 6, 'Forward P/E': 8,
                'Dividend Yield': 7, 'Payout ratio': 5, 'Beta': 5,
                'Dette/Equity': 9, 'Current Ratio': 8,
                'Avis Analystes': 7, 'Position 52W': 8
            },  # total = 100
            # Ajustement: +3 Position52W, +2 FCF, +1 Dividend Yield → pour atteindre 100 et mieux capter le momentum cyclique.
            # Justif: dette & cash-flow importants; momentum/position 52W signale reprise / contraction cyclique.

            'Real Estate': {
                'ROE': 7, 'ROA': 4, 'FCF Yield': 12, 'Dividend Yield': 15,
                'Payout ratio': 10, 'Price to Book': 18, 'Trailing PE': 4,
                'Beta': 5, 'Dette/Equity': 12, 'Current Ratio': 5,
                'Position 52W': 4, 'Avis Analystes': 4
            },  # total = 100
            # Justif: P/B & rendement locatif dominent; dette & FCF critiques; faible dépendance au court terme.

            'Général': {
                'ROE': 9, 'ROA': 7, 'Forward P/E': 7,
                'Trailing PE': 5, 'Price to Book': 6, 'Marge nette': 9,
                'FCF Yield': 10, 'Dette/Equity': 8, 'Current Ratio': 6,
                'Beta': 5, 'Avis Analystes': 10, 'Dividend Yield': 5,
                'Payout ratio': 3, 'Position 52W': 10
            }  # total = 100
            # Justif: profil neutre, équilibre entre rentabilité, valorisation et perception marché.
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