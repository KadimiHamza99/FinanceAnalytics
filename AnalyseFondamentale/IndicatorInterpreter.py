from AnalyseFondamentale.Utils import Utils

class IndicatorInterpreter:
    """
    Classe dédiée à l'interprétation des indicateurs fondamentaux par secteur.
    Fournit pour chaque indicateur :
    - une note sur 10
    - une interprétation qualitative spécifique au secteur
    """

    # --- Rentabilité ---
    @staticmethod
    def interpret_roe(roe, sector="General"):
        if roe is None:
            return 4, "Données indisponibles"
        
        sector_group = Utils._get_sector_group(sector)

        # --- Technology ---
        if sector_group == "Technology":
            if roe > 0.25: return 10, "ROE exceptionnel pour la tech - création de valeur majeure 💎"
            elif roe > 0.18: return 9, "Excellente rentabilité tech - largement au-dessus du coût du capital 🚀"
            elif roe > 0.13: return 8, "Bonne rentabilité pour le secteur ✅"
            elif roe > 0.09: return 7, "Rentabilité correcte 👍"
            elif roe > 0.05: return 6, "Rentabilité faible - création de valeur limitée ⚠️"
            elif roe > 0: return 4, "Rentabilité très faible - préoccupant 🔴"
            return 2, "Rentabilité négative - destruction de valeur 🚨"

        # --- Financial Services ---
        elif sector_group == "Financial Services":
            if roe > 0.18: return 10, "ROE exceptionnel pour le secteur financier 💎"
            elif roe > 0.14: return 9, "Excellente rentabilité bancaire 🚀"
            elif roe > 0.10: return 8, "Bonne rentabilité financière ✅"
            elif roe > 0.07: return 7, "Rentabilité correcte pour une banque 👍"
            elif roe > 0.04: return 6, "Rentabilité faible 📊"
            elif roe > 0: return 4, "Rentabilité très faible 🔴"
            return 1, "Rentabilité négative - critique 🚨"

        # --- Healthcare ---
        elif sector_group == "Healthcare":
            if roe > 0.20: return 10, "ROE exceptionnel pour la santé 💎"
            elif roe > 0.15: return 9, "Excellente rentabilité pharma 🚀"
            elif roe > 0.11: return 8, "Bonne rentabilité santé ✅"
            elif roe > 0.07: return 7, "Rentabilité correcte 👍"
            elif roe > 0.04: return 6, "Rentabilité faible 📊"
            elif roe > 0: return 4, "Rentabilité très faible 🔴"
            return 2, "Rentabilité négative - R&D non rentable 🚨"

        # --- Energy ---
        elif sector_group == "Energy":
            if roe > 0.18: return 10, "ROE exceptionnel pour l'énergie 💎"
            elif roe > 0.14: return 9, "Excellente rentabilité énergie 🚀"
            elif roe > 0.10: return 8, "Bonne rentabilité ✅"
            elif roe > 0.06: return 7, "Rentabilité correcte 👍"
            elif roe > 0.03: return 6, "Rentabilité faible ⚠️"
            elif roe > 0: return 4, "Rentabilité très faible 🔴"
            return 2, "Rentabilité négative - cycle bas ou inefficacités 🚨"

        # --- General / autres secteurs ---
        else:
            if roe > 0.25: return 10, "Exceptionnel - création de valeur majeure 💎"
            elif roe > 0.20: return 9, "Excellente rentabilité 🚀"
            elif roe > 0.15: return 8, "Très bonne rentabilité ✅"
            elif roe > 0.12: return 7, "Bonne rentabilité 👍"
            elif roe > 0.08: return 6, "Rentabilité correcte 📊"
            elif roe > 0.05: return 5, "Rentabilité moyenne 😐"
            elif roe > 0.02: return 4, "Rentabilité faible ⬇️"
            elif roe > 0: return 3, "Rentabilité très faible ⚠️"
            return 1, "Rentabilité négative - destruction de valeur 🔴"

    @staticmethod
    def interpret_roa(roa, sector="General"):
        if roa is None:
            return 4, "Données indisponibles"
        
        sector_group = Utils._get_sector_group(sector)

        # --- Financial Services ---
        if sector_group == "Financial Services":
            if roa > 0.015: return 10, "ROA exceptionnel pour une banque 💎"
            elif roa > 0.012: return 9, "Excellente utilisation des actifs 🚀"
            elif roa > 0.009: return 8, "Bonne efficacité bancaire ✅"
            elif roa > 0.006: return 7, "Efficacité correcte 👍"
            elif roa > 0.004: return 6, "Efficacité moyenne 📊"
            elif roa > 0.002: return 5, "Efficacité faible ⚠️"
            elif roa > 0: return 4, "Efficacité très faible 🔴"
            return 2, "ROA négatif - problème sérieux 🚨"

        # --- Technology ---
        elif sector_group == "Technology":
            if roa > 0.15: return 10, "Utilisation exceptionnelle des actifs tech 💎"
            elif roa > 0.11: return 9, "Excellente efficacité tech 🚀"
            elif roa > 0.08: return 8, "Bonne utilisation des actifs ✅"
            elif roa > 0.05: return 7, "Efficacité correcte 👍"
            elif roa > 0.03: return 6, "Efficacité moyenne 📊"
            elif roa > 0.01: return 5, "Efficacité faible ⚠️"
            elif roa > 0: return 4, "Efficacité très faible 🔴"
            return 2, "Efficacité négative - actifs mal utilisés 🚨"

        # --- Healthcare ---
        elif sector_group == "Healthcare":
            if roa > 0.12: return 10, "ROA exceptionnel pour la santé 💎"
            elif roa > 0.09: return 9, "Excellente efficacité R&D 🚀"
            elif roa > 0.07: return 8, "Bonne utilisation des actifs ✅"
            elif roa > 0.05: return 7, "Efficacité correcte 👍"
            elif roa > 0.03: return 6, "Efficacité moyenne 📊"
            elif roa > 0.01: return 5, "Efficacité faible ⚠️"
            elif roa > 0: return 4, "Efficacité très faible 🔴"
            return 2, "ROA négatif - mauvaise allocation 🚨"

        # --- Energy ---
        elif sector_group == "Energy":
            if roa > 0.13: return 10, "ROA exceptionnel pour l'énergie 💎"
            elif roa > 0.10: return 9, "Excellente utilisation des actifs 🚀"
            elif roa > 0.07: return 8, "Bonne efficacité ✅"
            elif roa > 0.05: return 7, "Efficacité correcte 👍"
            elif roa > 0.03: return 6, "Efficacité moyenne 📊"
            elif roa > 0.01: return 5, "Efficacité faible ⚠️"
            elif roa > 0: return 4, "Efficacité très faible 🔴"
            return 2, "ROA négatif - inefficacités majeures 🚨"

        # --- General / autres secteurs ---
        else:
            if roa > 0.15: return 10, "Utilisation des actifs exceptionnelle 💎"
            elif roa > 0.12: return 9, "Excellente efficacité 🚀"
            elif roa > 0.09: return 8, "Très bonne utilisation ✅"
            elif roa > 0.06: return 7, "Bonne efficacité 👍"
            elif roa > 0.04: return 6, "Utilisation correcte 📊"
            elif roa > 0.02: return 5, "Utilisation moyenne 😐"
            elif roa > 0.01: return 4, "Utilisation faible ⬇️"
            elif roa > 0: return 3, "Utilisation très faible ⚠️"
            return 1, "Utilisation négative - destruction de valeur 🔴"


    # --- Valorisation ---
    @staticmethod
    def interpret_forward_pe(forward_pe, sector="General"):
        if forward_pe is None:
            return 4, "Données indisponibles"
        
        sector_group = Utils._get_sector_group(sector)

        # --- Technology & Healthcare ---
        if sector_group in ["Technology", "Healthcare"]:
            if forward_pe < 12: return 10, "Exceptionnellement attractif pour la croissance 💎"
            elif forward_pe < 18: return 9, "Très attractif 🚀"
            elif forward_pe < 25: return 8, "Attractif pour le secteur ✅"
            elif forward_pe < 35: return 7, "Correct pour une entreprise de croissance 👍"
            elif forward_pe < 45: return 6, "Légèrement élevé 📊"
            elif forward_pe < 60: return 5, "Élevé mais justifiable 😐"
            elif forward_pe < 80: return 4, "Très élevé ⚠️"
            elif forward_pe < 120: return 3, "Excessif 🔴"
            return 1, "Bullesque 💀"

        # --- Financial Services, Energy, Real Estate ---
        elif sector_group in ["Financial Services", "Energy", "Real Estate"]:
            if forward_pe < 5: return 10, "Exceptionnellement attractif 💎"
            elif forward_pe < 7: return 9, "Très attractif 🚀"
            elif forward_pe < 10: return 8, "Attractif ✅"
            elif forward_pe < 13: return 7, "Correct 👍"
            elif forward_pe < 18: return 6, "Légèrement élevé 📊"
            elif forward_pe < 22: return 5, "Élevé pour le secteur 😐"
            elif forward_pe < 30: return 4, "Très élevé ⚠️"
            elif forward_pe < 45: return 3, "Excessif 🔴"
            return 1, "Extrêmement excessif 💀"

        # --- General / autres secteurs ---
        else:
            if forward_pe < 7: return 10, "Exceptionnellement attractif 💎"
            elif forward_pe < 10: return 9, "Très attractif 🚀"
            elif forward_pe < 14: return 8, "Attractif ✅"
            elif forward_pe < 18: return 7, "Légèrement attractif 👍"
            elif forward_pe < 22: return 6, "Correct 📊"
            elif forward_pe < 28: return 5, "Légèrement élevé 😐"
            elif forward_pe < 35: return 4, "Élevé ⚠️"
            elif forward_pe < 45: return 3, "Très élevé 🚨"
            elif forward_pe < 60: return 2, "Excessif 🔴"
            return 1, "Extrêmement excessif 💀"

    @staticmethod
    def interpret_trailing_pe(trailing_pe, sector="General"):
        if trailing_pe is None:
            return 4, "Données indisponibles"
            
        sector_group = Utils._get_sector_group(sector)

        # --- Technology & Healthcare ---
        if sector_group in ["Technology", "Healthcare"]:
            if trailing_pe < 15: return 10, "Exceptionnel pour le secteur 💎"
            elif trailing_pe < 20: return 9, "Très attractif 🚀"
            elif trailing_pe < 28: return 8, "Attractif ✅"
            elif trailing_pe < 36: return 7, "Correct 👍"
            elif trailing_pe < 46: return 6, "Légèrement élevé 📊"
            elif trailing_pe < 60: return 5, "Élevé 😐"
            elif trailing_pe < 75: return 4, "Très élevé ⚠️"
            elif trailing_pe < 100: return 3, "Excessif 🔴"
            else: return 1, "Extrêmement excessif 💀"

        # --- Financial Services, Energy, Real Estate ---
        elif sector_group in ["Financial Services", "Energy", "Real Estate"]:
            if trailing_pe < 5: return 10, "Exceptionnel 💎"
            elif trailing_pe < 8: return 9, "Très attractif 🚀"
            elif trailing_pe < 12: return 8, "Attractif ✅"
            elif trailing_pe < 16: return 7, "Correct 👍"
            elif trailing_pe < 20: return 6, "Légèrement élevé 📊"
            elif trailing_pe < 26: return 5, "Élevé 😐"
            elif trailing_pe < 34: return 4, "Très élevé ⚠️"
            elif trailing_pe < 45: return 3, "Excessif 🔴"
            else: return 1, "Extrêmement excessif 💀"

        # --- General / autres secteurs ---
        else:
            if trailing_pe < 7: return 10, "Exceptionnel 💎"
            elif trailing_pe < 11: return 9, "Très attractif 🚀"
            elif trailing_pe < 15: return 8, "Attractif ✅"
            elif trailing_pe < 20: return 7, "Correct 👍"
            elif trailing_pe < 25: return 6, "Légèrement élevé 📊"
            elif trailing_pe < 32: return 5, "Élevé 😐"
            elif trailing_pe < 42: return 4, "Très élevé ⚠️"
            elif trailing_pe < 55: return 3, "Excessif 🔴"
            else: return 1, "Extrêmement excessif 💀"


    @staticmethod
    def interpret_price_to_book(pb, sector="General"):
        if pb is None:
            return 4, "Données indisponibles"
        
        sector_group = Utils._get_sector_group(sector)

        # --- Financial Services & Real Estate ---
        if sector_group in ["Financial Services", "Real Estate"]:
            if pb < 0.4: return 10, "Très sous-évalué pour le secteur 💎"
            elif pb < 0.7: return 9, "Sous-évalué 🚀"
            elif pb < 0.95: return 8, "Légèrement sous-évalué ✅"
            elif pb < 1.2: return 7, "Correct pour une banque/REIT 👍"
            elif pb < 1.6: return 6, "Légèrement élevé 📊"
            elif pb < 2.2: return 5, "Élevé 😐"
            elif pb < 3.0: return 4, "Très élevé ⚠️"
            elif pb < 4.0: return 3, "Excessif 🔴"
            else: return 1, "Extrêmement excessif 💀"

        # --- Technology ---
        elif sector_group == "Technology":
            if pb < 1.5: return 10, "Exceptionnel pour la tech 💎"
            elif pb < 3.0: return 9, "Très attractif 🚀"
            elif pb < 5.0: return 8, "Attractif ✅"
            elif pb < 8.0: return 7, "Correct pour la croissance 👍"
            elif pb < 12.0: return 6, "Légèrement élevé 📊"
            elif pb < 18.0: return 5, "Élevé 😐"
            elif pb < 25.0: return 4, "Très élevé ⚠️"
            elif pb < 35.0: return 3, "Excessif 🔴"
            else: return 1, "Bullesque 💀"

        # --- General / autres secteurs ---
        else:
            if pb < 0.6: return 10, "Très sous-évalué 💎"
            elif pb < 0.9: return 9, "Sous-évalué 🚀"
            elif pb < 1.2: return 8, "Légèrement sous-évalué ✅"
            elif pb < 1.6: return 7, "Bon rapport 👍"
            elif pb < 2.2: return 6, "Correct 📊"
            elif pb < 3.0: return 5, "Légèrement élevé 😐"
            elif pb < 4.0: return 4, "Élevé ⚠️"
            elif pb < 6.0: return 3, "Très élevé 🔴"
            elif pb < 10.0: return 2, "Excessif 💀"
            else: return 1, "Extrêmement excessif 🎯"


    # --- Risque / Solidité financière ---
    @staticmethod
    def interpret_beta(beta, sector="General"):
        if beta is None:
            return 4, "Données indisponibles"
            
        sector_group = Utils._get_sector_group(sector)
        # --- Technology & Consumer Cyclical ---
        if sector_group in ["Technology", "Consumer Cyclical"]:
            if beta < 0.6: return 10, "Très défensif pour le secteur tech/cyclique 🛡️"
            elif beta < 0.85: return 9, "Défensif ✅"
            elif beta < 1.1: return 8, "Volatilité modérée 👍"
            elif beta < 1.3: return 7, "Typique du secteur 📊"
            elif beta < 1.6: return 6, "Volatilité élevée 😐"
            elif beta < 1.9: return 5, "Très volatile ⚠️"
            elif beta < 2.3: return 4, "Extrêmement volatile 🔴"
            else: return 2, "Spéculatif 💀"

        # --- Consumer Defensive & Utilities ---
        elif sector_group in ["Consumer Defensive", "Utilities"]:
            if beta < 0.3: return 10, "Très défensif 💎"
            elif beta < 0.6: return 9, "Défensif 🛡️"
            elif beta < 0.85: return 8, "Légèrement défensif ✅"
            elif beta < 1.05: return 7, "Neutre 👍"
            elif beta < 1.25: return 6, "Légèrement volatil 📊"
            elif beta < 1.6: return 5, "Volatilité élevée 😐"
            elif beta < 2.0: return 4, "Très volatile ⚠️"
            else: return 3, "Extrêmement volatile 🔴"

        # --- General / autres secteurs ---
        else:
            if beta < 0.4: return 10, "Très faible volatilité 🛡️"
            elif beta < 0.7: return 9, "Faible volatilité ✅"
            elif beta < 0.9: return 8, "Légèrement défensif 👍"
            elif beta < 1.1: return 7, "Similaire au marché 📊"
            elif beta < 1.3: return 6, "Légèrement volatil 😐"
            elif beta < 1.6: return 5, "Volatilité élevée ⚠️"
            elif beta < 2.0: return 4, "Très volatile 🔴"
            elif beta < 2.5: return 3, "Extrêmement volatile 💀"
            else: return 1, "Spéculatif extrême 🎰"


    @staticmethod
    def interpret_debt_to_equity(debt, sector="General"):
        if debt is None:
            return 3, "Données indisponibles"
        
        sector_group = Utils._get_sector_group(sector)

        if sector_group in ["Financial Services", "Real Estate"]:
            if debt < 100: return 10, "Endettement très faible 💎"
            elif debt < 200: return 9, "Endettement faible 🚀"
            elif debt < 350: return 8, "Endettement modéré ✅"
            elif debt < 550: return 7, "Acceptable 👍"
            elif debt < 800: return 6, "Légèrement élevé 📊"
            elif debt < 1100: return 5, "Élevé 😐"
            elif debt < 1500: return 4, "Très endetté ⚠️"
            elif debt < 2000: return 3, "Endettement excessif 🔴"
            else: return 2, "Critique 💀"

        elif sector_group == "Utilities":
            if debt < 40: return 10, "Très faible endettement 💎"
            elif debt < 80: return 9, "Endettement faible 🚀"
            elif debt < 130: return 8, "Endettement modéré ✅"
            elif debt < 200: return 7, "Acceptable 👍"
            elif debt < 280: return 6, "Élevé 📊"
            elif debt < 400: return 5, "Très endetté 😐"
            elif debt < 600: return 4, "Endettement excessif ⚠️"
            else: return 3, "Critique 🔴"

        elif sector_group == "Technology":
            if debt < 5: return 10, "Endettement quasi nul 💎"
            elif debt < 15: return 9, "Endettement faible 🚀"
            elif debt < 30: return 8, "Endettement modéré ✅"
            elif debt < 60: return 7, "Acceptable 👍"
            elif debt < 100: return 6, "Élevé 📊"
            elif debt < 150: return 5, "Très endetté 😐"
            elif debt < 220: return 4, "Endettement excessif ⚠️"
            else: return 3, "Critique 🔴"

        else:  # General / autres secteurs
            if debt < 10: return 10, "Endettement très faible 💎"
            elif debt < 25: return 9, "Endettement faible 🚀"
            elif debt < 50: return 8, "Endettement modéré ✅"
            elif debt < 80: return 7, "Acceptable 👍"
            elif debt < 120: return 6, "Moyen 📊"
            elif debt < 180: return 5, "Élevé 😐"
            elif debt < 250: return 4, "Très endetté ⚠️"
            elif debt < 350: return 3, "Endettement excessif 🔴"
            else: return 2, "Critique 💀"


    @staticmethod
    def interpret_current_ratio(cr, sector="General"):
        if cr is None:
            return 4, "Données indisponibles"
        
        sector_group = Utils._get_sector_group(sector)

        if sector_group == "Financial Services":
            if cr > 1.5: return 10, "Très forte liquidité 💎"
            elif cr > 1.2: return 9, "Forte liquidité 🚀"
            elif cr > 1.0: return 8, "Bonne liquidité ✅"
            elif cr > 0.8: return 7, "Correcte 👍"
            elif cr > 0.6: return 6, "Acceptable 📊"
            elif cr > 0.4: return 5, "Faible 😐"
            elif cr > 0.3: return 4, "Problème ⚠️"
            else: return 3, "Critique 🔴"

        elif sector_group in ["Technology", "Healthcare"]:
            if cr > 4.0: return 10, "Liquidité très forte 💎"
            elif cr > 3.0: return 9, "Excellente 🚀"
            elif cr > 2.0: return 8, "Bonne ✅"
            elif cr > 1.5: return 7, "Correcte 👍"
            elif cr > 1.2: return 6, "Acceptable 📊"
            elif cr > 1.0: return 5, "Faible 😐"
            elif cr > 0.8: return 4, "Problème ⚠️"
            else: return 3, "Critique 🔴"

        else:
            if cr > 3.5: return 10, "Très forte liquidité 💎"
            elif cr > 2.5: return 9, "Excellente 🚀"
            elif cr > 1.8: return 8, "Bonne ✅"
            elif cr > 1.5: return 7, "Correcte 👍"
            elif cr > 1.2: return 6, "Acceptable 📊"
            elif cr > 1.0: return 5, "Faible 😐"
            elif cr > 0.8: return 4, "Problème ⚠️"
            elif cr > 0.6: return 3, "Grave problème 💀"
            else: return 2, "Situation critique 🚨"


    # --- Rentabilité / marges ---
    @staticmethod
    def interpret_profit_margin(marg, sector="General"):
        if marg is None:
            return 4, "Données indisponibles"
        
        sector_group = Utils._get_sector_group(sector)

        if sector_group == "Technology":
            if marg > 0.30: return 10, "Marge exceptionnelle 💎"
            elif marg > 0.22: return 9, "Très bonne marge 🚀"
            elif marg > 0.15: return 8, "Bonne marge logicielle ✅"
            elif marg > 0.10: return 7, "Acceptable 👍"
            elif marg > 0.05: return 6, "Marge faible ⚠️"
            elif marg > 0.02: return 4, "Marge très faible 🔴"
            return 1, "Pertes - modèle non rentable 🚨"

        elif sector_group == "Healthcare":
            if marg > 0.25: return 10, "Marge exceptionnelle pharma 💎"
            elif marg > 0.18: return 9, "Excellente marge 🚀"
            elif marg > 0.12: return 8, "Bonne marge ✅"
            elif marg > 0.08: return 7, "Correcte 👍"
            elif marg > 0.04: return 6, "Marge faible ⚠️"
            elif marg > 0.01: return 4, "Marge très faible 🔴"
            return 1, "Pertes - R&D non amortie 🚨"

        elif sector_group in ["Financial Services", "Energy"]:
            if marg > 0.35: return 10, "Marge exceptionnelle 💎"
            elif marg > 0.25: return 9, "Excellente marge 🚀"
            elif marg > 0.18: return 8, "Très bonne marge ✅"
            elif marg > 0.12: return 7, "Bonne marge 👍"
            elif marg > 0.07: return 6, "Marge correcte 📊"
            elif marg > 0.03: return 4, "Marge faible ⚠️"
            return 1, "Pertes 🚨"

        else:  # General et autres secteurs
            if marg > 0.30: return 10, "Marge exceptionnelle 💎"
            elif marg > 0.22: return 9, "Très bonne marge 🚀"
            elif marg > 0.15: return 8, "Bonne marge ✅"
            elif marg > 0.10: return 7, "Correcte 👍"
            elif marg > 0.06: return 6, "Marge moyenne ⚠️"
            elif marg > 0.03: return 4, "Marge faible 🔴"
            elif marg > 0: return 3, "Marge très faible 💀"
            return 1, "Pertes 🚨"


    @staticmethod
    def interpret_fcf_yield(fcf_yield, sector="General"):
        if fcf_yield is None:
            return 4, "Données indisponibles"

        sector_group = Utils._get_sector_group(sector)

        if sector_group in ["Technology", "Healthcare"]:
            if fcf_yield > 0.10: return 10, "Rendement exceptionnel 💎"
            elif fcf_yield > 0.07: return 9, "Très bon rendement 🚀"
            elif fcf_yield > 0.05: return 8, "Bon rendement ✅"
            elif fcf_yield > 0.03: return 6, "Correct 👍"
            elif fcf_yield > 0.02: return 5, "Rendement faible ⚠️"
            elif fcf_yield > 0.01: return 4, "Très faible 🔴"
            return 1, "Cash-flow négatif 🚨"

        elif sector_group == "Energy":
            if fcf_yield > 0.15: return 10, "Rendement exceptionnel 💎"
            elif fcf_yield > 0.10: return 9, "Très bon rendement 🚀"
            elif fcf_yield > 0.07: return 8, "Bon rendement ✅"
            elif fcf_yield > 0.04: return 6, "Correct 👍"
            elif fcf_yield > 0.02: return 4, "Rendement faible ⚠️"
            return 1, "Cash-flow négatif 🚨"

        else:  # General et autres secteurs
            if fcf_yield > 0.12: return 10, "Rendement exceptionnel 💎"
            elif fcf_yield > 0.08: return 9, "Très bon rendement 🚀"
            elif fcf_yield > 0.06: return 8, "Bon rendement ✅"
            elif fcf_yield > 0.04: return 6, "Correct 👍"
            elif fcf_yield > 0.02: return 4, "Rendement faible ⚠️"
            return 1, "Cash-flow négatif 🚨"

    @staticmethod
    def interpret_dividend_yield(div, sector="General"):
        if div is None:
            return 2, "Pas de dividende 🚫"
        
        sector_group = Utils._get_sector_group(sector)
        
        if sector_group in ["Utilities", "Energy", "Real Estate"]:
            if div > 10: return 8, "Rendement très élevé (risque de soutenabilité) ⚠️"
            elif div > 7: return 9, "Rendement élevé - typique du secteur 💰"
            elif div > 5: return 8, "Bon rendement ✅"
            elif div > 4: return 7, "Rendement correct 👍"
            elif div > 3: return 6, "Rendement modéré 📊"
            elif div > 2: return 5, "Rendement modeste 😐"
            elif div > 1: return 4, "Rendement faible ⬇️"
            elif div > 0: return 3, "Rendement symbolique 🔴"
            return 1, "Dividende nul - atypique 🚫"

        elif sector_group in ["Technology", "Healthcare"]:
            if div > 4: return 8, "Rendement élevé pour la croissance ⚠️"
            elif div > 2.5: return 7, "Bon rendement - rare dans le secteur ✅"
            elif div > 1.5: return 6, "Rendement modéré 👍"
            elif div > 0.8: return 5, "Rendement symbolique 📊"
            elif div > 0.3: return 4, "Très faible 😐"
            elif div > 0: return 3, "Minimal ⬇️"
            return 5, "Aucun dividende - normal pour la croissance 📈"

        else:  # General et autres secteurs
            if div > 8: return 10, "Rendement très élevé (risque) ⚠️"
            elif div > 6: return 9, "Rendement élevé 💰"
            elif div > 4.5: return 8, "Bon rendement ✅"
            elif div > 4: return 7, "Rendement correct 👍"
            elif div > 3: return 6, "Rendement modéré 📊"
            elif div > 2: return 5, "Rendement modeste 📊"
            elif div > 1: return 4, "Rendement faible 😐"
            elif div > 0.5: return 3, "Rendement très faible ⬇️"
            elif div > 0: return 2, "Rendement symbolique 🔴"
            return 1, "Dividende nul 🚫"

    @staticmethod
    def interpret_payout_ratio(payout, sector="General"):
        if payout is None:
            return 4, "Données indisponibles"
        
        sector_group = Utils._get_sector_group(sector)
        
        if sector_group in ["Utilities", "Real Estate"]:
            if 0.60 <= payout <= 0.80: return 10, "Distribution idéale pour le secteur 💎"
            elif 0.50 <= payout < 0.60: return 9, "Distribution équilibrée 🚀"
            elif 0.80 < payout <= 0.95: return 8, "Distribution élevée mais acceptable ✅"
            elif payout > 0.95: return 4, "Distribution très élevée ⚠️"
            elif 0.30 <= payout < 0.50: return 7, "Distribution conservatrice 👍"
            elif payout < 0.30: return 6, "Distribution faible 📊"
            else: return 5, "Hors normes 😐"

        elif sector_group in ["Technology", "Healthcare"]:
            if payout < 0.20: return 10, "Conservation des profits idéale pour la R&D 💎"
            elif payout < 0.35: return 9, "Distribution faible - bon pour la croissance 🚀"
            elif payout < 0.50: return 8, "Distribution modérée ✅"
            elif payout < 0.70: return 6, "Distribution élevée - limite pour la croissance 📊"
            elif payout >= 0.70: return 3, "Distribution très élevée - pénalise l'innovation ⚠️"
            else: return 5, "Distribution nulle - normal 📈"

        else:  # General et autres secteurs
            if 0.25 <= payout <= 0.45: return 10, "Distribution idéale 💎"
            elif 0.45 < payout <= 0.60: return 8, "Distribution équilibrée ✅"
            elif 0.60 < payout <= 0.75: return 6, "Distribution élevée 📊"
            elif 0.75 < payout <= 0.90: return 3, "Distribution très élevée ⚠️"
            elif payout > 0.90: return 1, "Non soutenable 🚨"
            elif payout < 0.25: return 7, "Distribution conservatrice 👍"
            elif payout < 0.10: return 6, "Distribution faible 📊"
            return 5, "Distribution nulle 😐"

    # === Position 52 semaines ===
    @staticmethod
    def interpret_52w_position(current_price, low_52w, high_52w, sector="General"):
        if not (current_price and low_52w and high_52w) or high_52w == low_52w:
            return None, 5, "Données insuffisantes"

        position = (current_price - low_52w) / (high_52w - low_52w) * 100
        sector_group = Utils._get_sector_group(sector)

        if sector_group in ["Technology", "Healthcare"]:
            if position < 20: note, interp = 10, "Exceptionnellement proche du plus bas - opportunité croissance 💎"
            elif position < 35: note, interp = 9, "Très proche du plus bas 🚀"
            elif position < 50: note, interp = 8, "Dans le bas du range ✅"
            elif position < 65: note, interp = 7, "Légèrement sous la moyenne 👍"
            elif position < 75: note, interp = 6, "Proche de la moyenne 📊"
            elif position < 85: note, interp = 5, "Légèrement au-dessus 😐"
            elif position < 92: note, interp = 4, "Dans le haut du range ⚠️"
            elif position < 97: note, interp = 3, "Proche du plus haut 🔴"
            else: note, interp = 2, "Exceptionnellement proche du plus haut - surévalué 🚨"

        elif sector_group in ["Energy", "Financial Services"]:
            if position < 15: note, interp = 10, "Exceptionnellement proche du plus bas - cycle favorable 💎"
            elif position < 25: note, interp = 9, "Très proche du plus bas 🚀"
            elif position < 40: note, interp = 8, "Dans le bas du range ✅"
            elif position < 55: note, interp = 7, "Légèrement sous la moyenne 👍"
            elif position < 65: note, interp = 6, "Proche de la moyenne 📊"
            elif position < 75: note, interp = 5, "Légèrement au-dessus 😐"
            elif position < 85: note, interp = 4, "Dans le haut du range ⚠️"
            elif position < 95: note, interp = 3, "Proche du plus haut 🔴"
            else: note, interp = 2, "Exceptionnellement proche du plus haut 🚨"

        else:  # General et autres secteurs
            if position < 10: note, interp = 10, "Exceptionnellement proche du plus bas 💎"
            elif position < 20: note, interp = 9, "Très proche du plus bas 🚀"
            elif position < 30: note, interp = 8, "Proche du plus bas ✅"
            elif position < 40: note, interp = 7, "Dans le bas du range 👍"
            elif position < 50: note, interp = 6, "Légèrement sous la moyenne 📊"
            elif position < 60: note, interp = 5, "Proche de la moyenne 😐"
            elif position < 70: note, interp = 4, "Légèrement au-dessus ⚠️"
            elif position < 80: note, interp = 3, "Dans le haut du range 🔴"
            elif position < 90: note, interp = 2, "Proche du plus haut 💀"
            else: note, interp = 1, "Exceptionnellement proche du plus haut 🚨"

        return position, note, interp

    @staticmethod
    def interpret_analyst_rating(rec_mean, num_analysts, sector="General"):
        if rec_mean is None:
            return "N/A", 3, "Données indisponibles"

        sector_group = Utils._get_sector_group(sector)
        
        # Base sur la note moyenne
        if rec_mean <= 1.2:
            note, base_interp = 10, "Achat fort exceptionnel 💎"
        elif rec_mean <= 1.5:
            note, base_interp = 9, "Achat fort 🚀"
        elif rec_mean <= 1.7:
            note, base_interp = 8, "Achat fort 🚀"
        elif rec_mean <= 2.0:
            note, base_interp = 7, "Achat ✅"
        elif rec_mean <= 2.5:
            note, base_interp = 6, "Achat modéré 👍"
        elif rec_mean <= 3.0:
            note, base_interp = 5, "Neutre positif 📊"
        elif rec_mean <= 3.3:
            note, base_interp = 4, "Neutre 😐"
        elif rec_mean <= 3.7:
            note, base_interp = 3, "Neutre négatif ⚠️"
        elif rec_mean <= 4.2:
            note, base_interp = 2, "Vente modérée 🔴"
        elif rec_mean <= 4.5:
            note, base_interp = 1, "Vente 💀"
        else:
            note, base_interp = 0, "Vente forte 🚨"

        # Ajustement selon le nombre d'analystes et le secteur
        if num_analysts < 2:
            note = max(1, note - 3)
            interp = f"{base_interp} ⚠️ Très peu d'avis ({num_analysts})"
        elif num_analysts < 4:
            note = max(1, note - 2)
            interp = f"{base_interp} ⚠️ Peu d'avis ({num_analysts})"
        elif num_analysts < 8:
            note = max(1, note - 1)
            interp = f"{base_interp} Avis limités ({num_analysts})"
        elif num_analysts < 15:
            interp = f"{base_interp} ({num_analysts} analystes)"
        else:
            note = min(10, note + 1)
            interp = f"{base_interp} ✅ Consensus fort ({num_analysts} analystes)"

        # Ajout du contexte sectoriel
        if sector_group in ["Technology", "Healthcare"] and note >= 7:
            interp += " - Soutien fort pour la croissance"
        elif sector_group in ["Financial Services", "Energy"] and note >= 7:
            interp += " - Confiance sectorielle"
        elif note <= 3 and sector_group in ["Consumer Defensive", "Utilities"]:
            interp += " - Inhabituel pour ce secteur défensif"

        grade_str = f"{rec_mean:.1f}/5"
        return grade_str, note, interp