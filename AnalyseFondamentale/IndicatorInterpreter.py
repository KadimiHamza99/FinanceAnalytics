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
        """
        Interprète le current ratio avec contexte sectoriel
        
        Règle générale:
        - CR > 2.0 : Excellente liquidité
        - CR 1.5-2.0 : Bonne liquidité
        - CR 1.0-1.5 : Liquidité acceptable
        - CR < 1.0 : Risque de liquidité
        """
        if cr is None:
            return 4, "Données indisponibles"
        
        sector_group = Utils._get_sector_group(sector)
        
        # Secteurs spéciaux
        if sector_group == "Financial Services":
            # Banques/Assurances : structure bilancielle unique
            if cr > 1.3: return 10, "Liquidité très forte 💎"
            elif cr > 1.1: return 9, "Forte liquidité 🚀"
            elif cr > 0.9: return 8, "Bonne liquidité ✅"
            elif cr > 0.7: return 6, "Correcte 👍"
            elif cr > 0.5: return 4, "Faible ⚠️"
            elif cr > 0.3: return 3, "Problème grave 🔴"
            else: return 2, "Critique 🚨"
        
        elif sector_group == "Retail":
            # Commerce : rotation rapide, stocks élevés
            if cr > 2.5: return 10, "Liquidité exceptionnelle 💎"
            elif cr > 2.0: return 9, "Excellente 🚀"
            elif cr > 1.5: return 8, "Très bonne ✅"
            elif cr > 1.2: return 7, "Bonne 👍"
            elif cr > 1.0: return 6, "Correcte 📊"
            elif cr > 0.8: return 4, "Faible ⚠️"
            else: return 3, "Critique 🔴"
        
        elif sector_group in ["Technology", "Healthcare"]:
            # Tech/Pharma : liquidité élevée normale
            if cr > 3.0: return 10, "Liquidité exceptionnelle 💎"
            elif cr > 2.5: return 9, "Excellente 🚀"
            elif cr > 2.0: return 8, "Très bonne ✅"
            elif cr > 1.5: return 7, "Bonne 👍"
            elif cr > 1.2: return 6, "Correcte 📊"
            elif cr > 1.0: return 5, "Acceptable 😐"
            elif cr > 0.8: return 4, "Faible ⚠️"
            else: return 3, "Critique 🔴"
        
        elif sector_group in ["Utilities", "Telecom"]:
            # Services publics : cash-flows prévisibles
            if cr > 2.0: return 10, "Liquidité très forte 💎"
            elif cr > 1.5: return 9, "Excellente 🚀"
            elif cr > 1.2: return 8, "Bonne ✅"
            elif cr > 1.0: return 7, "Correcte 👍"
            elif cr > 0.8: return 6, "Acceptable 📊"
            elif cr > 0.6: return 4, "Faible ⚠️"
            else: return 3, "Critique 🔴"
        
        else:  # Manufacturing, Services, etc.
            if cr > 3.0: return 10, "Liquidité exceptionnelle 💎"
            elif cr > 2.5: return 9, "Excellente 🚀"
            elif cr > 2.0: return 8, "Très bonne ✅"
            elif cr > 1.5: return 7, "Bonne 👍"
            elif cr > 1.2: return 6, "Correcte 📊"
            elif cr > 1.0: return 5, "Acceptable 😐"
            elif cr > 0.8: return 4, "Faible ⚠️"
            elif cr > 0.6: return 3, "Problème grave 🔴"
            else: return 2, "Critique 🚨"


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
    

    @staticmethod
    def interpret_operating_margin(op_margin, sector="General"):
        """Interprète la marge opérationnelle"""
        if op_margin is None:
            return 5, "Données indisponibles"
        
        margin_pct = op_margin * 100
        sector_group = Utils._get_sector_group(sector)
        
        if sector_group == "Technology":
            if margin_pct > 25: return 10, f"Marge opérationnelle exceptionnelle ({margin_pct:.1f}%) 💎"
            elif margin_pct > 18: return 9, f"Excellente efficacité opérationnelle ({margin_pct:.1f}%) 🚀"
            elif margin_pct > 12: return 8, f"Bonne marge opérationnelle ({margin_pct:.1f}%) ✅"
            elif margin_pct > 8: return 7, f"Marge correcte ({margin_pct:.1f}%) 👍"
            elif margin_pct > 4: return 6, f"Marge faible ({margin_pct:.1f}%) 📊"
            elif margin_pct > 0: return 4, f"Marge très faible ({margin_pct:.1f}%) ⚠️"
            return 2, f"Pertes opérationnelles ({margin_pct:.1f}%) 🔴"
        
        elif sector_group == "Healthcare":
            if margin_pct > 22: return 10, f"Marge exceptionnelle pharma ({margin_pct:.1f}%) 💎"
            elif margin_pct > 15: return 9, f"Excellente marge ({margin_pct:.1f}%) 🚀"
            elif margin_pct > 10: return 8, f"Bonne marge ({margin_pct:.1f}%) ✅"
            elif margin_pct > 6: return 7, f"Marge correcte ({margin_pct:.1f}%) 👍"
            elif margin_pct > 3: return 5, f"Marge faible ({margin_pct:.1f}%) ⚠️"
            elif margin_pct > 0: return 3, f"Marge très faible ({margin_pct:.1f}%) 🔴"
            return 1, f"Pertes opérationnelles ({margin_pct:.1f}%) 🚨"
        
        elif sector_group == "Financial Services":
            if margin_pct > 40: return 10, f"Marge exceptionnelle ({margin_pct:.1f}%) 💎"
            elif margin_pct > 30: return 9, f"Excellente efficacité ({margin_pct:.1f}%) 🚀"
            elif margin_pct > 22: return 8, f"Bonne marge ({margin_pct:.1f}%) ✅"
            elif margin_pct > 15: return 7, f"Marge correcte ({margin_pct:.1f}%) 👍"
            elif margin_pct > 10: return 5, f"Marge faible ({margin_pct:.1f}%) 📊"
            elif margin_pct > 0: return 3, f"Marge très faible ({margin_pct:.1f}%) ⚠️"
            return 1, f"Pertes ({margin_pct:.1f}%) 🔴"
        
        elif sector_group == "Energy":
            if margin_pct > 18: return 10, f"Marge exceptionnelle ({margin_pct:.1f}%) 💎"
            elif margin_pct > 12: return 9, f"Excellente marge ({margin_pct:.1f}%) 🚀"
            elif margin_pct > 8: return 8, f"Bonne marge ({margin_pct:.1f}%) ✅"
            elif margin_pct > 5: return 7, f"Marge correcte ({margin_pct:.1f}%) 👍"
            elif margin_pct > 2: return 5, f"Marge faible ({margin_pct:.1f}%) ⚠️"
            elif margin_pct > 0: return 3, f"Marge très faible ({margin_pct:.1f}%) 🔴"
            return 1, f"Pertes ({margin_pct:.1f}%) 🚨"
        
        else:  # General
            if margin_pct > 20: return 10, f"Marge exceptionnelle ({margin_pct:.1f}%) 💎"
            elif margin_pct > 14: return 9, f"Excellente marge ({margin_pct:.1f}%) 🚀"
            elif margin_pct > 10: return 8, f"Bonne marge ({margin_pct:.1f}%) ✅"
            elif margin_pct > 6: return 7, f"Marge correcte ({margin_pct:.1f}%) 👍"
            elif margin_pct > 3: return 5, f"Marge faible ({margin_pct:.1f}%) 📊"
            elif margin_pct > 0: return 3, f"Marge très faible ({margin_pct:.1f}%) ⚠️"
            return 1, f"Pertes ({margin_pct:.1f}%) 🔴"


    @staticmethod
    def interpret_gross_margin(gross_margin, sector="General"):
        """Interprète la marge brute"""
        if gross_margin is None:
            return 5, "Données indisponibles"
        
        margin_pct = gross_margin * 100
        sector_group = Utils._get_sector_group(sector)
        
        if sector_group == "Energy":
            if margin_pct > 45: return 10, f"Marge brute exceptionnelle ({margin_pct:.1f}%) 💎"
            elif margin_pct > 35: return 9, f"Excellente marge brute ({margin_pct:.1f}%) 🚀"
            elif margin_pct > 28: return 8, f"Bonne marge brute ({margin_pct:.1f}%) ✅"
            elif margin_pct > 20: return 7, f"Marge correcte ({margin_pct:.1f}%) 👍"
            elif margin_pct > 15: return 5, f"Marge faible ({margin_pct:.1f}%) 📊"
            elif margin_pct > 0: return 3, f"Marge très faible ({margin_pct:.1f}%) ⚠️"
            return 1, f"Marge négative ({margin_pct:.1f}%) 🔴"
        
        elif sector_group in ["Consumer Cyclical", "Consumer Defensive"]:
            if margin_pct > 50: return 10, f"Marge brute exceptionnelle ({margin_pct:.1f}%) 💎"
            elif margin_pct > 40: return 9, f"Excellente marge ({margin_pct:.1f}%) 🚀"
            elif margin_pct > 32: return 8, f"Bonne marge ({margin_pct:.1f}%) ✅"
            elif margin_pct > 25: return 7, f"Marge correcte ({margin_pct:.1f}%) 👍"
            elif margin_pct > 18: return 5, f"Marge faible ({margin_pct:.1f}%) 📊"
            elif margin_pct > 0: return 3, f"Marge très faible ({margin_pct:.1f}%) ⚠️"
            return 1, f"Marge négative ({margin_pct:.1f}%) 🔴"
        
        else:  # General et Basic Materials
            if margin_pct > 45: return 10, f"Marge brute exceptionnelle ({margin_pct:.1f}%) 💎"
            elif margin_pct > 35: return 9, f"Excellente marge ({margin_pct:.1f}%) 🚀"
            elif margin_pct > 28: return 8, f"Bonne marge ({margin_pct:.1f}%) ✅"
            elif margin_pct > 20: return 7, f"Marge correcte ({margin_pct:.1f}%) 👍"
            elif margin_pct > 15: return 5, f"Marge faible ({margin_pct:.1f}%) 📊"
            elif margin_pct > 0: return 3, f"Marge très faible ({margin_pct:.1f}%) ⚠️"
            return 1, f"Marge négative ({margin_pct:.1f}%) 🔴"


    @staticmethod
    def interpret_earnings_growth(growth, sector="General"):
        """Interprète la croissance des bénéfices"""
        if growth is None:
            return 5, "Données indisponibles"
        
        growth_pct = growth * 100
        
        if growth_pct < -30:
            return 1, f"Effondrement des bénéfices ({growth_pct:.1f}%) 🚨"
        elif growth_pct < -20:
            return 2, f"Forte baisse des bénéfices ({growth_pct:.1f}%) 🔴"
        elif growth_pct < -10:
            return 3, f"Baisse importante ({growth_pct:.1f}%) ⚠️"
        elif growth_pct < -5:
            return 4, f"Baisse modérée ({growth_pct:.1f}%) 📊"
        elif growth_pct < 0:
            return 5, f"Légère baisse ({growth_pct:.1f}%) 😐"
        elif growth_pct < 5:
            return 6, f"Croissance faible ({growth_pct:.1f}%) 👍"
        elif growth_pct < 15:
            return 7, f"Croissance modérée ({growth_pct:.1f}%) ✅"
        elif growth_pct < 25:
            return 8, f"Bonne croissance ({growth_pct:.1f}%) 🚀"
        elif growth_pct < 50:
            return 9, f"Forte croissance ({growth_pct:.1f}%) 💎"
        else:
            return 10, f"Croissance exceptionnelle ({growth_pct:.1f}%) 🔥"


    @staticmethod
    def interpret_quick_ratio(ratio, sector="General"):
        """
        Interprète le quick ratio (liquidité immédiate sans stocks)
        
        Règle générale:
        - QR > 1.5 : Excellente liquidité immédiate
        - QR 1.0-1.5 : Bonne liquidité
        - QR 0.7-1.0 : Liquidité acceptable
        - QR < 0.7 : Risque de liquidité court terme
        
        Note: Quick Ratio est plus strict que Current Ratio (exclut stocks)
        """
        if ratio is None:
            return 5, "Données indisponibles"
        
        sector_group = Utils._get_sector_group(sector)
        
        if sector_group == "Financial Services":
            # Banques/Assurances : liquidité immédiate critique
            if ratio > 1.0: 
                return 10, f"Excellente liquidité immédiate ({ratio:.2f}) 💎"
            elif ratio > 0.8: 
                return 9, f"Très bonne liquidité ({ratio:.2f}) 🚀"
            elif ratio > 0.6: 
                return 8, f"Bonne liquidité ({ratio:.2f}) ✅"
            elif ratio > 0.5: 
                return 6, f"Liquidité correcte ({ratio:.2f}) 👍"
            elif ratio > 0.4: 
                return 4, f"Liquidité faible ({ratio:.2f}) ⚠️"
            elif ratio > 0.3: 
                return 3, f"Liquidité préoccupante ({ratio:.2f}) 🔴"
            else: 
                return 2, f"Liquidité critique ({ratio:.2f}) 🚨"
        
        elif sector_group in ["Retail", "Manufacturing"]:
            # Commerce/Industrie : Stocks importants, quick ratio naturellement plus bas
            if ratio > 1.5: 
                return 10, f"Excellente liquidité immédiate ({ratio:.2f}) 💎"
            elif ratio > 1.0: 
                return 9, f"Très bonne liquidité ({ratio:.2f}) 🚀"
            elif ratio > 0.8: 
                return 8, f"Bonne liquidité ({ratio:.2f}) ✅"
            elif ratio > 0.6: 
                return 7, f"Liquidité correcte ({ratio:.2f}) 👍"
            elif ratio > 0.5: 
                return 6, f"Liquidité acceptable ({ratio:.2f}) 📊"
            elif ratio > 0.4: 
                return 4, f"Liquidité faible ({ratio:.2f}) ⚠️"
            elif ratio > 0.3: 
                return 3, f"Liquidité préoccupante ({ratio:.2f}) 🔴"
            else: 
                return 2, f"Liquidité critique ({ratio:.2f}) 🚨"
        
        elif sector_group in ["Technology", "Healthcare"]:
            # Tech/Pharma : Peu de stocks, quick ratio élevé attendu
            if ratio > 2.5: 
                return 10, f"Excellente liquidité immédiate ({ratio:.2f}) 💎"
            elif ratio > 2.0: 
                return 9, f"Très bonne liquidité ({ratio:.2f}) 🚀"
            elif ratio > 1.5: 
                return 8, f"Bonne liquidité ({ratio:.2f}) ✅"
            elif ratio > 1.0: 
                return 7, f"Liquidité correcte ({ratio:.2f}) 👍"
            elif ratio > 0.8: 
                return 6, f"Liquidité acceptable ({ratio:.2f}) 📊"
            elif ratio > 0.6: 
                return 5, f"Liquidité faible ({ratio:.2f}) 😐"
            elif ratio > 0.4: 
                return 4, f"Liquidité préoccupante ({ratio:.2f}) ⚠️"
            else: 
                return 3, f"Liquidité critique ({ratio:.2f}) 🔴"
        
        elif sector_group in ["Services", "Consulting"]:
            # Services : Quasi pas de stocks, quick ≈ current ratio
            if ratio > 2.0: 
                return 10, f"Excellente liquidité immédiate ({ratio:.2f}) 💎"
            elif ratio > 1.5: 
                return 9, f"Très bonne liquidité ({ratio:.2f}) 🚀"
            elif ratio > 1.2: 
                return 8, f"Bonne liquidité ({ratio:.2f}) ✅"
            elif ratio > 1.0: 
                return 7, f"Liquidité correcte ({ratio:.2f}) 👍"
            elif ratio > 0.8: 
                return 6, f"Liquidité acceptable ({ratio:.2f}) 📊"
            elif ratio > 0.6: 
                return 4, f"Liquidité faible ({ratio:.2f}) ⚠️"
            else: 
                return 3, f"Liquidité critique ({ratio:.2f}) 🔴"
        
        elif sector_group in ["Utilities", "Telecom"]:
            # Services publics : Cash-flows stables, seuils modérés
            if ratio > 1.5: 
                return 10, f"Excellente liquidité immédiate ({ratio:.2f}) 💎"
            elif ratio > 1.2: 
                return 9, f"Très bonne liquidité ({ratio:.2f}) 🚀"
            elif ratio > 1.0: 
                return 8, f"Bonne liquidité ({ratio:.2f}) ✅"
            elif ratio > 0.8: 
                return 7, f"Liquidité correcte ({ratio:.2f}) 👍"
            elif ratio > 0.6: 
                return 6, f"Liquidité acceptable ({ratio:.2f}) 📊"
            elif ratio > 0.5: 
                return 4, f"Liquidité faible ({ratio:.2f}) ⚠️"
            else: 
                return 3, f"Liquidité critique ({ratio:.2f}) 🔴"
        
        else:  # General / Default
            if ratio > 2.0: 
                return 10, f"Excellente liquidité immédiate ({ratio:.2f}) 💎"
            elif ratio > 1.5: 
                return 9, f"Très bonne liquidité ({ratio:.2f}) 🚀"
            elif ratio > 1.2: 
                return 8, f"Bonne liquidité ({ratio:.2f}) ✅"
            elif ratio > 1.0: 
                return 7, f"Liquidité correcte ({ratio:.2f}) 👍"
            elif ratio > 0.8: 
                return 6, f"Liquidité acceptable ({ratio:.2f}) 📊"
            elif ratio > 0.6: 
                return 5, f"Liquidité faible ({ratio:.2f}) 😐"
            elif ratio > 0.5: 
                return 4, f"Liquidité préoccupante ({ratio:.2f}) ⚠️"
            else: 
                return 3, f"Liquidité critique ({ratio:.2f}) 🔴"


    @staticmethod
    def interpret_ocf_ratio(ratio, sector="General"):
        """Interprète le ratio Operating Cash Flow / Current Liabilities"""
        if ratio is None:
            return 5, "Données indisponibles"
        
        if ratio > 2.5: return 10, f"Excellent flux de trésorerie ({ratio:.2f}x) 💎"
        elif ratio > 2.0: return 9, f"Très bon flux ({ratio:.2f}x) 🚀"
        elif ratio > 1.5: return 8, f"Bon flux de trésorerie ({ratio:.2f}x) ✅"
        elif ratio > 1.0: return 7, f"Flux correct ({ratio:.2f}x) 👍"
        elif ratio > 0.7: return 6, f"Flux acceptable ({ratio:.2f}x) 📊"
        elif ratio > 0.5: return 5, f"Flux faible ({ratio:.2f}x) 😐"
        elif ratio > 0.3: return 3, f"Flux très faible ({ratio:.2f}x) ⚠️"
        return 1, f"Flux insuffisant ({ratio:.2f}x) 🔴"


    @staticmethod
    def interpret_debt_ebitda(ratio, sector="General"):
        """Interprète le ratio Dette/EBITDA"""
        if ratio is None:
            return 5, "Données indisponibles"
        
        sector_group = Utils._get_sector_group(sector)
        
        if sector_group in ["Technology", "Healthcare"]:
            if ratio < 1.0: return 10, f"Endettement très faible ({ratio:.1f}x) 💎"
            elif ratio < 2.0: return 9, f"Endettement faible ({ratio:.1f}x) 🚀"
            elif ratio < 3.0: return 8, f"Endettement modéré ({ratio:.1f}x) ✅"
            elif ratio < 4.0: return 7, f"Endettement correct ({ratio:.1f}x) 👍"
            elif ratio < 5.5: return 5, f"Endettement élevé ({ratio:.1f}x) 📊"
            elif ratio < 7.0: return 3, f"Endettement très élevé ({ratio:.1f}x) ⚠️"
            return 1, f"Endettement critique ({ratio:.1f}x) 🔴"
        
        elif sector_group in ["Utilities", "Real Estate"]:
            if ratio < 3.0: return 10, f"Endettement faible ({ratio:.1f}x) 💎"
            elif ratio < 4.5: return 9, f"Endettement modéré ({ratio:.1f}x) 🚀"
            elif ratio < 6.0: return 8, f"Endettement acceptable ({ratio:.1f}x) ✅"
            elif ratio < 7.5: return 7, f"Endettement correct ({ratio:.1f}x) 👍"
            elif ratio < 9.0: return 5, f"Endettement élevé ({ratio:.1f}x) 📊"
            elif ratio < 11.0: return 3, f"Endettement très élevé ({ratio:.1f}x) ⚠️"
            return 1, f"Endettement critique ({ratio:.1f}x) 🔴"
        
        elif sector_group == "Energy":
            if ratio < 1.5: return 10, f"Endettement très faible ({ratio:.1f}x) 💎"
            elif ratio < 2.5: return 9, f"Endettement faible ({ratio:.1f}x) 🚀"
            elif ratio < 3.5: return 8, f"Endettement modéré ({ratio:.1f}x) ✅"
            elif ratio < 5.0: return 7, f"Endettement correct ({ratio:.1f}x) 👍"
            elif ratio < 6.5: return 5, f"Endettement élevé ({ratio:.1f}x) 📊"
            elif ratio < 8.0: return 3, f"Endettement très élevé ({ratio:.1f}x) ⚠️"
            return 1, f"Endettement critique ({ratio:.1f}x) 🔴"
        
        else:  # General
            if ratio < 1.5: return 10, f"Endettement très faible ({ratio:.1f}x) 💎"
            elif ratio < 2.5: return 9, f"Endettement faible ({ratio:.1f}x) 🚀"
            elif ratio < 3.5: return 8, f"Endettement modéré ({ratio:.1f}x) ✅"
            elif ratio < 5.0: return 7, f"Endettement correct ({ratio:.1f}x) 👍"
            elif ratio < 6.5: return 5, f"Endettement élevé ({ratio:.1f}x) 📊"
            elif ratio < 8.0: return 3, f"Endettement très élevé ({ratio:.1f}x) ⚠️"
            return 1, f"Endettement critique ({ratio:.1f}x) 🔴"


    @staticmethod
    def interpret_peg_ratio(peg, sector="General"):
        """Interprète le PEG ratio (PE / croissance)"""
        if peg is None:
            return 5, "Données indisponibles"
        
        if peg <= 0:
            return 2, f"PEG invalide ({peg:.2f}) - croissance négative ⚠️"
        elif peg < 0.5:
            return 10, f"Action très sous-évaluée (PEG: {peg:.2f}) 💎"
        elif peg < 0.8:
            return 9, f"Action sous-évaluée (PEG: {peg:.2f}) 🚀"
        elif peg < 1.0:
            return 8, f"Bonne valorisation (PEG: {peg:.2f}) ✅"
        elif peg < 1.3:
            return 7, f"Valorisation correcte (PEG: {peg:.2f}) 👍"
        elif peg < 1.7:
            return 6, f"Valorisation acceptable (PEG: {peg:.2f}) 📊"
        elif peg < 2.0:
            return 5, f"Légèrement surévaluée (PEG: {peg:.2f}) 😐"
        elif peg < 2.5:
            return 4, f"Surévaluée (PEG: {peg:.2f}) ⚠️"
        elif peg < 3.0:
            return 3, f"Très surévaluée (PEG: {peg:.2f}) 🔴"
        else:
            return 1, f"Excessivement surévaluée (PEG: {peg:.2f}) 🚨"
        
    @staticmethod
    def interpret_debt_to_assets(ratio, sector="General"):
        """Interprète le ratio Dette / Actifs totaux"""
        if ratio is None:
            return 5, "Données indisponibles"
        
        ratio_pct = ratio * 100
        sector_group = Utils._get_sector_group(sector)
        
        # Secteurs financiers (leverage élevé normal)
        if sector_group == "Financial Services":
            if ratio_pct < 30: return 10, f"Endettement très faible ({ratio_pct:.1f}%) 💎"
            elif ratio_pct < 45: return 9, f"Endettement faible ({ratio_pct:.1f}%) 🚀"
            elif ratio_pct < 60: return 8, f"Endettement modéré ({ratio_pct:.1f}%) ✅"
            elif ratio_pct < 70: return 7, f"Endettement acceptable ({ratio_pct:.1f}%) 👍"
            elif ratio_pct < 80: return 5, f"Endettement élevé ({ratio_pct:.1f}%) 📊"
            elif ratio_pct < 88: return 3, f"Endettement très élevé ({ratio_pct:.1f}%) ⚠️"
            return 1, f"Endettement excessif ({ratio_pct:.1f}%) 🔴"
        
        # Utilities, Real Estate (leverage modéré à élevé normal)
        elif sector_group in ["Utilities", "Real Estate"]:
            if ratio_pct < 25: return 10, f"Endettement très faible ({ratio_pct:.1f}%) 💎"
            elif ratio_pct < 40: return 9, f"Endettement faible ({ratio_pct:.1f}%) 🚀"
            elif ratio_pct < 55: return 8, f"Endettement modéré ({ratio_pct:.1f}%) ✅"
            elif ratio_pct < 65: return 7, f"Endettement acceptable ({ratio_pct:.1f}%) 👍"
            elif ratio_pct < 75: return 5, f"Endettement élevé ({ratio_pct:.1f}%) 📊"
            elif ratio_pct < 82: return 3, f"Endettement très élevé ({ratio_pct:.1f}%) ⚠️"
            return 1, f"Endettement excessif ({ratio_pct:.1f}%) 🔴"
        
        # Technology, Healthcare (faible endettement attendu)
        elif sector_group in ["Technology", "Healthcare"]:
            if ratio_pct < 15: return 10, f"Endettement très faible ({ratio_pct:.1f}%) 💎"
            elif ratio_pct < 25: return 9, f"Endettement faible ({ratio_pct:.1f}%) 🚀"
            elif ratio_pct < 35: return 8, f"Endettement modéré ({ratio_pct:.1f}%) ✅"
            elif ratio_pct < 45: return 7, f"Endettement acceptable ({ratio_pct:.1f}%) 👍"
            elif ratio_pct < 55: return 5, f"Endettement élevé ({ratio_pct:.1f}%) 📊"
            elif ratio_pct < 65: return 3, f"Endettement très élevé ({ratio_pct:.1f}%) ⚠️"
            return 1, f"Endettement excessif ({ratio_pct:.1f}%) 🔴"
        
        # Autres secteurs (General)
        else:
            if ratio_pct < 20: return 10, f"Endettement très faible ({ratio_pct:.1f}%) 💎"
            elif ratio_pct < 30: return 9, f"Endettement faible ({ratio_pct:.1f}%) 🚀"
            elif ratio_pct < 40: return 8, f"Endettement modéré ({ratio_pct:.1f}%) ✅"
            elif ratio_pct < 50: return 7, f"Endettement acceptable ({ratio_pct:.1f}%) 👍"
            elif ratio_pct < 60: return 6, f"Endettement moyen ({ratio_pct:.1f}%) 📊"
            elif ratio_pct < 70: return 5, f"Endettement élevé ({ratio_pct:.1f}%) 😐"
            elif ratio_pct < 80: return 3, f"Endettement très élevé ({ratio_pct:.1f}%) ⚠️"
            return 1, f"Endettement excessif ({ratio_pct:.1f}%) 🔴"


    @staticmethod
    def interpret_book_value(book_value, current_price, sector="General"):
        """Interprète la valeur comptable par action (book value)"""
        if book_value is None or current_price is None:
            return 5, "Données indisponibles"
        
        # Calculer le ratio Prix / Valeur comptable
        pb_ratio = current_price / book_value if book_value > 0 else None
        
        if pb_ratio is None:
            return 2, f"Valeur comptable négative ({book_value:.2f}) 🚨"
        
        sector_group = Utils._get_sector_group(sector)
        
        # Pour les secteurs financiers et immobilier, le P/B est plus pertinent
        if sector_group in ["Financial Services", "Real Estate"]:
            if pb_ratio < 0.5:
                return 10, f"Forte décote vs actifs ({book_value:.2f}€, P/B: {pb_ratio:.2f}) 💎"
            elif pb_ratio < 0.8:
                return 9, f"Décote significative ({book_value:.2f}€, P/B: {pb_ratio:.2f}) 🚀"
            elif pb_ratio < 1.0:
                return 8, f"Légère décote ({book_value:.2f}€, P/B: {pb_ratio:.2f}) ✅"
            elif pb_ratio < 1.3:
                return 7, f"Proche de la valeur comptable ({book_value:.2f}€, P/B: {pb_ratio:.2f}) 👍"
            elif pb_ratio < 1.7:
                return 6, f"Légère prime ({book_value:.2f}€, P/B: {pb_ratio:.2f}) 📊"
            elif pb_ratio < 2.5:
                return 5, f"Prime modérée ({book_value:.2f}€, P/B: {pb_ratio:.2f}) 😐"
            else:
                return 3, f"Prime élevée ({book_value:.2f}€, P/B: {pb_ratio:.2f}) ⚠️"
        
        # Pour les autres secteurs (notamment tech)
        else:
            if pb_ratio < 0.7:
                return 10, f"Forte marge de sécurité ({book_value:.2f}€, P/B: {pb_ratio:.2f}) 💎"
            elif pb_ratio < 1.0:
                return 9, f"Bonne marge de sécurité ({book_value:.2f}€, P/B: {pb_ratio:.2f}) 🚀"
            elif pb_ratio < 1.5:
                return 8, f"Marge de sécurité correcte ({book_value:.2f}€, P/B: {pb_ratio:.2f}) ✅"
            elif pb_ratio < 2.5:
                return 7, f"Valorisation raisonnable ({book_value:.2f}€, P/B: {pb_ratio:.2f}) 👍"
            elif pb_ratio < 4.0:
                return 6, f"Valorisation élevée ({book_value:.2f}€, P/B: {pb_ratio:.2f}) 📊"
            elif pb_ratio < 6.0:
                return 5, f"Valorisation très élevée ({book_value:.2f}€, P/B: {pb_ratio:.2f}) 😐"
            else:
                return 3, f"Valorisation excessive ({book_value:.2f}€, P/B: {pb_ratio:.2f}) ⚠️"
            
    @staticmethod
    def interpret_interest_coverage(coverage, sector="General"):
        """Interprète le ratio de couverture des intérêts (EBIT / Interest Expense)"""
        if coverage is None:
            return 5, "Données indisponibles"
        
        sector_group = Utils._get_sector_group(sector)
        
        # Secteurs à forte intensité capitalistique (endettement normal)
        if sector_group in ["Utilities", "Real Estate", "Energy"]:
            if coverage > 8.0: return 10, f"Excellente couverture des intérêts ({coverage:.1f}x) 💎"
            elif coverage > 5.0: return 9, f"Très bonne couverture ({coverage:.1f}x) 🚀"
            elif coverage > 3.5: return 8, f"Bonne couverture ({coverage:.1f}x) ✅"
            elif coverage > 2.5: return 7, f"Couverture correcte ({coverage:.1f}x) 👍"
            elif coverage > 2.0: return 6, f"Couverture acceptable ({coverage:.1f}x) 📊"
            elif coverage > 1.5: return 5, f"Couverture faible ({coverage:.1f}x) 😐"
            elif coverage > 1.0: return 3, f"Couverture très faible ({coverage:.1f}x) ⚠️"
            elif coverage > 0: return 2, f"Couverture critique ({coverage:.1f}x) 🔴"
            return 1, f"Incapacité à couvrir les intérêts 🚨"
        
        # Secteurs Technology, Healthcare (endettement faible attendu)
        elif sector_group in ["Technology", "Healthcare"]:
            if coverage > 15.0: return 10, f"Excellente couverture ({coverage:.1f}x) 💎"
            elif coverage > 10.0: return 9, f"Très bonne couverture ({coverage:.1f}x) 🚀"
            elif coverage > 7.0: return 8, f"Bonne couverture ({coverage:.1f}x) ✅"
            elif coverage > 5.0: return 7, f"Couverture correcte ({coverage:.1f}x) 👍"
            elif coverage > 3.0: return 6, f"Couverture acceptable ({coverage:.1f}x) 📊"
            elif coverage > 2.0: return 5, f"Couverture faible ({coverage:.1f}x) 😐"
            elif coverage > 1.2: return 3, f"Couverture très faible ({coverage:.1f}x) ⚠️"
            elif coverage > 0: return 2, f"Couverture critique ({coverage:.1f}x) 🔴"
            return 1, f"Incapacité à couvrir les intérêts 🚨"
        
        # Autres secteurs (General)
        else:
            if coverage > 10.0: return 10, f"Excellente couverture des intérêts ({coverage:.1f}x) 💎"
            elif coverage > 6.0: return 9, f"Très bonne couverture ({coverage:.1f}x) 🚀"
            elif coverage > 4.0: return 8, f"Bonne couverture ({coverage:.1f}x) ✅"
            elif coverage > 3.0: return 7, f"Couverture correcte ({coverage:.1f}x) 👍"
            elif coverage > 2.0: return 6, f"Couverture acceptable ({coverage:.1f}x) 📊"
            elif coverage > 1.5: return 5, f"Couverture faible ({coverage:.1f}x) 😐"
            elif coverage > 1.0: return 3, f"Couverture très faible ({coverage:.1f}x) ⚠️"
            elif coverage > 0: return 2, f"Couverture critique ({coverage:.1f}x) 🔴"
            return 1, f"Incapacité à couvrir les intérêts 🚨"


    @staticmethod
    def interpret_equity_ratio(ratio, sector="General"):
        """Interprète le ratio de capitaux propres (Equity / Total Assets)"""
        if ratio is None:
            return 5, "Données indisponibles"
        
        ratio_pct = ratio * 100
        sector_group = Utils._get_sector_group(sector)
        
        # Secteurs financiers et immobilier (leverage élevé normal)
        if sector_group in ["Financial Services", "Real Estate"]:
            if ratio_pct > 20: return 10, f"Excellente indépendance financière ({ratio_pct:.1f}%) 💎"
            elif ratio_pct > 15: return 9, f"Très bonne structure ({ratio_pct:.1f}%) 🚀"
            elif ratio_pct > 12: return 8, f"Bonne structure financière ({ratio_pct:.1f}%) ✅"
            elif ratio_pct > 10: return 7, f"Structure correcte ({ratio_pct:.1f}%) 👍"
            elif ratio_pct > 8: return 6, f"Structure acceptable ({ratio_pct:.1f}%) 📊"
            elif ratio_pct > 6: return 5, f"Capitaux propres faibles ({ratio_pct:.1f}%) 😐"
            elif ratio_pct > 4: return 3, f"Structure fragile ({ratio_pct:.1f}%) ⚠️"
            elif ratio_pct > 0: return 2, f"Structure très fragile ({ratio_pct:.1f}%) 🔴"
            return 1, f"Capitaux propres négatifs 🚨"
        
        # Utilities et Energy (leverage modéré normal)
        elif sector_group in ["Utilities", "Energy"]:
            if ratio_pct > 50: return 10, f"Excellente indépendance ({ratio_pct:.1f}%) 💎"
            elif ratio_pct > 40: return 9, f"Très bonne structure ({ratio_pct:.1f}%) 🚀"
            elif ratio_pct > 35: return 8, f"Bonne structure ({ratio_pct:.1f}%) ✅"
            elif ratio_pct > 30: return 7, f"Structure correcte ({ratio_pct:.1f}%) 👍"
            elif ratio_pct > 25: return 6, f"Structure acceptable ({ratio_pct:.1f}%) 📊"
            elif ratio_pct > 20: return 5, f"Capitaux propres faibles ({ratio_pct:.1f}%) 😐"
            elif ratio_pct > 15: return 3, f"Structure fragile ({ratio_pct:.1f}%) ⚠️"
            elif ratio_pct > 0: return 2, f"Structure très fragile ({ratio_pct:.1f}%) 🔴"
            return 1, f"Capitaux propres négatifs 🚨"
        
        # Autres secteurs (General, Tech, Healthcare, etc.)
        else:
            if ratio_pct > 65: return 10, f"Excellente indépendance financière ({ratio_pct:.1f}%) 💎"
            elif ratio_pct > 55: return 9, f"Très bonne structure ({ratio_pct:.1f}%) 🚀"
            elif ratio_pct > 45: return 8, f"Bonne structure financière ({ratio_pct:.1f}%) ✅"
            elif ratio_pct > 40: return 7, f"Structure correcte ({ratio_pct:.1f}%) 👍"
            elif ratio_pct > 35: return 6, f"Structure acceptable ({ratio_pct:.1f}%) 📊"
            elif ratio_pct > 30: return 5, f"Capitaux propres faibles ({ratio_pct:.1f}%) 😐"
            elif ratio_pct > 25: return 4, f"Dépendance élevée à la dette ({ratio_pct:.1f}%) ⚠️"
            elif ratio_pct > 20: return 3, f"Structure fragile ({ratio_pct:.1f}%) 🔴"
            elif ratio_pct > 0: return 2, f"Structure très fragile ({ratio_pct:.1f}%) 🚨"
            return 1, f"Capitaux propres négatifs - insolvabilité 💀"