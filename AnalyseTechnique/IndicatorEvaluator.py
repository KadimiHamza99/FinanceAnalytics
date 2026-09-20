from colorama import Fore, Style

class IndicatorEvaluator:
    """
    Évalue les indicateurs techniques avec une approche prudente adaptée aux
    actions liquides cotées en France et à un horizon de plusieurs semaines à
    plusieurs mois. Un indicateur isolé ne suffit jamais à justifier un achat.
    """

    def __init__(self):
        self.weights = {
            "RSI": 14,
            "Stochastique": 5,
            "Bollinger": 11,
            "MACD": 17,
            "OBV": 9,
            "EMA200": 17,
            "ADX": 9,
            "Tendance": 10,
            "Fibonacci": 8,
        }

    # --- RSI ---
    def evaluate_rsi(self, rsi: float):
        if rsi < 22:
            return 10, "🟢 RSI < 20 → Marché en panique totale 😱. Niveau historiquement bas, opportunité exceptionnelle 💎."
        elif rsi < 28:
            return 9, "🟢 RSI 20–28 → Forte sous-évaluation, marché dominé par la peur. Signal d'entrée solide ✅."
        elif rsi < 30:
            return 8, "🟢 RSI 28–35 → Sous-évaluation technique claire, zone d'achat intéressante 👀."
        elif rsi < 35:
            return 7, "🟢 RSI 28–35 → Sous-évaluation technique claire, zone d'achat intéressante 👀."
        elif rsi < 45:
            return 6, "🟡 RSI 35–45 → Faiblesse modérée, surveiller une reprise confirmée."
        elif rsi < 50:
            return 5, "🟡 RSI 35–45 → Faiblesse modérée, surveiller une reprise confirmée."
        elif rsi < 55:
            return 4, "⚪ RSI 45–55 → Marché neutre, patience recommandée ⏳."
        elif rsi < 65:
            return 3, "🟠 RSI 55–65 → Légère surévaluation, prudence."
        else:
            return 1, "🔴 RSI > 65 → Surachat, risque de repli 🚨."

    # --- Stochastique ---
    def evaluate_stoch(self, k: float, d: float):
        if k < 15 and k > d:
            return 9, "🟢 Croisement haussier sous 15 → Signal fort de redressement potentiel ⚡."
        elif k < 25:
            return 8, "🟢 Stochastique < 25 → Marché survendu, probabilité élevée de rebond 📈."
        elif 25 <= k <= 40:
            return 6, "🟡 Stochastique bas mais stabilisé → zone d'observation."
        elif 40 < k <= 65:
            return 4, "⚪ Stochastique neutre → peu exploitable."
        elif 65 < k <= 80:
            return 3, "🟠 Stochastique haut → possible essoufflement."
        else:
            return 1, "🔴 Stochastique > 80 → Surachat confirmé 🚨."

    # --- Bandes de Bollinger ---
    def evaluate_bollinger(self, close, bb_low, bb_mid, bb_high):
        if close < bb_low * 0.97:
            return 10, "🟢 Cours très en dessous de la bande basse → excès de vente exceptionnel 💎."
        elif close < bb_low:
            return 8, "🟢 Cours sous la bande basse → marché survendu, rebond probable ⚡."
        elif close < bb_mid:
            return 6, "🟡 Cours sous la moyenne → phase de repli, bonne zone d'accumulation progressive 📊."
        elif close < bb_high:
            return 4, "⚪ Cours entre moyenne et bande haute → marché équilibré."
        else:
            return 2, "🔴 Cours au-dessus de la bande haute → euphorie du marché 🚨."

    # --- MACD ---
    def evaluate_macd(self, macd_val, signal_val):
        """
        Interprétation du MACD centrée sur la détection de retournements haussiers précoces.
        L'accent est mis sur les croisements haussiers sous zéro, et non sur les phases déjà haussières.
        """
        if macd_val > signal_val and macd_val < -0.6:
            return 10, "🟢 Croisement haussier profond sous zéro → retournement majeur probable, signal rare 🔄✨."
        elif macd_val > signal_val and macd_val < -0.3:
            return 9, "🟢 Croisement haussier sous zéro → très bon signal de redressement 💪📈."
        elif macd_val > signal_val and macd_val < 0:
            return 7, "🟢 MACD haussier proche de zéro → reprise en cours, encore un peu de prudence 👀."
        elif macd_val > signal_val:
            return 5, "🟡 MACD haussier positif → tendance déjà engagée, peu de marge d'entrée 🏁."
        elif macd_val < signal_val and macd_val < -0.3:
            return 3, "🟠 MACD baissier sous zéro → marché toujours sous pression, patience 🕰️."
        else:
            return 2, "🔴 MACD positif mais en affaiblissement → risque de retournement baissier ⚠️."

    # --- OBV ---
    def evaluate_obv(self, recent, previous):
        variation = (recent - previous) / previous * 100 if previous != 0 else 0
        if variation > 8:
            return 9, "🟢 OBV en forte hausse → accumulation claire 📦. Acheteurs discrets en action."
        elif variation > 3:
            return 7, "🟢 OBV légèrement haussier → flux acheteurs modérés mais réguliers ✅."
        elif abs(variation) <= 1:
            return 4, "⚪ OBV stable → marché attentiste ⏸️."
        elif variation < -3:
            return 3, "🟠 OBV en baisse → sortie légère de capitaux."
        else:
            return 1, "🔴 OBV en forte baisse → distribution nette 💸."

    # --- EMA200 ---
    def evaluate_ema200(self, close, ema200, ema50=None):
        discount = (close - ema200) / ema200 * 100
        if discount < -18:
            return 10, f"🟢 Prix {abs(discount):.1f}% sous EMA200 → décote exceptionnelle 💎."
        elif discount < -10:
            return 9, f"🟢 Prix {abs(discount):.1f}% sous EMA200 → forte sous-évaluation, opportunité sérieuse ✅."
        elif discount < -5:
            return 7, f"🟢 Prix {abs(discount):.1f}% sous EMA200 → décote intéressante, zone d'accumulation potentielle."
        elif discount < -2.5:
            return 6, f"🟡 Prix légèrement sous EMA200 → neutre à légèrement favorable."
        elif discount < 0:
            return 5, f"🟡 Prix légèrement sous EMA200 → neutre à légèrement favorable."
        elif discount < 2.5:
            return 4, f"🟡 Prix légèrement sous EMA200 → neutre à légèrement favorable."
        elif discount < 5:
            return 3, f"🟠 Prix légèrement au-dessus EMA200 → valorisation intégrée, prudence."
        else:
            return 1, f"🔴 Prix {abs(discount):.1f}% au-dessus EMA200 → surévaluation du titre 🚨."

    def evaluate_trend_alignment(self, close, ema50, ema200):
        """Score la structure de tendance, sans confondre hausse et décote."""
        if close > ema50 > ema200:
            return 8, "🟢 Cours au-dessus des EMA50 et EMA200 : tendance haussière confirmée."
        if close > ema200 and ema50 <= ema200:
            return 5, "🟡 Reprise possible, mais les moyennes ne sont pas encore alignées."
        if close < ema50 < ema200:
            return 2, "🔴 Cours sous les EMA50 et EMA200 : tendance baissière confirmée."
        return 4, "⚪ Structure neutre : attendre une confirmation avant d'entrer."

    # --- ADX ---
    def evaluate_adx(self, adx):
        if adx < 10:
            return 8, "🟢 ADX < 10 → marché très calme, souvent proche d'un plancher ⏳."
        elif 10 <= adx < 20:
            return 7, "🟢 ADX 10–20 → tendance faible mais en formation 🌱."
        elif 20 <= adx < 30:
            return 5, "⚪ ADX 20–30 → tendance moyenne, rien de marqué."
        elif 30 <= adx < 40:
            return 3, "🟠 ADX 30–40 → tendance forte, possible entrée tardive."
        else:
            return 1, "🔴 ADX > 40 → tendance violente, peu de marge pour un achat."

    # --- FIBONACCI ---
    def evaluate_fibonacci(self, price, levels, support, resistance):
        """
        Évalue la position du prix par rapport aux niveaux de Fibonacci.
        Philosophie moyen-terme : privilégier les zones de retracement 38.2%-50% pour des entrées 
        progressives avec bon ratio risque/récompense sur 6-24 mois.
        
        Args:
            price: Prix actuel
            levels: Dictionnaire des niveaux de Fibonacci
            support: Niveau de support identifié
            resistance: Niveau de résistance identifié
            
        Returns:
            tuple: (note sur 10, interprétation)
        """
        if not support or not resistance:
            return 4.0, "⚪ Fibonacci non exploitable : support ou résistance absent."
        
        # Calcul de la position relative dans le range
        total_range = resistance - support
        price_position = (price - support) / total_range if total_range > 0 else 0.5
        
        # Identification du niveau Fibonacci le plus proche
        fib_levels_sorted = [
            ("Fib 23.6%", 0.236),
            ("Fib 38.2%", 0.382),
            ("Fib 50%", 0.5),
            ("Fib 61.8%", 0.618),
            ("Fib 78.6%", 0.786),
        ]
        
        # Déterminer le niveau le plus proche
        closest_level = None
        min_distance = float('inf')
        for level_name, level_value in fib_levels_sorted:
            distance = abs(price_position - level_value)
            if distance < min_distance:
                min_distance = distance
                closest_level = level_name
        
        # Évaluation optimisée pour investisseur moyen-terme
        if price_position <= 0.20:
            return 6, "🟡 Prix très bas dans le range : potentiel rebond, mais risque de poursuite baissière élevé."
        
        elif price_position <= 0.30:  # Proche de Fib 23.6% - 30%
            return 7, f"🟢 Prix à {closest_level} : zone intéressante uniquement avec confirmation du volume et du momentum."
        
        elif price_position <= 0.382:  # Au niveau Fib 38.2%
            return 7, f"🟢 Prix à {closest_level} : retracement surveillable pour une entrée progressive."
        
        elif price_position <= 0.45:  # Entre 38.2% et 50%
            return 6, f"🟡 Prix vers {closest_level} : zone intermédiaire, attendre une réaction haussière."
        
        elif price_position <= 0.55:  # Au niveau Fib 50%
            return 5, f"🟡 Prix à {closest_level} : point médian sans avantage clair."
        
        elif price_position <= 0.618:  # Vers Fib 61.8%
            return 4, f"🟡 Prix à {closest_level} : attendre un meilleur point d'entrée."
        
        elif price_position <= 0.75:  # Entre 61.8% et 78.6%
            return 3, f"🟠 Prix vers {closest_level} : marge de sécurité limitée, prudence."
        
        else:  # Au dessus de 78.6%
            return 2, f"🔴 Prix au-dessus de Fib 78.6% : entrée tardive, risque de correction."

    # --- INTERPRÉTATION GLOBALE ---
    def _global_interpretation(df, score):
        """Interprétation globale affinée du score total, adaptée à la détection de sous-évaluation."""
        bullish_signals = sum(df["Note (/10)"] >= 7)

        if score >= 90:
            msg = Fore.GREEN + "💎 Configuration technique très favorable, mais à confirmer par le volume et le contexte."
        elif score >= 80:
            msg = Fore.GREEN + "🟢 Configuration favorable : tendance et momentum cohérents, entrée progressive uniquement."
        elif score >= 70:
            msg = Fore.CYAN + "🔵 Configuration plutôt favorable : attendre une confirmation par le volume ou le MACD."
        elif score >= 60:
            msg = Fore.LIGHTBLUE_EX + "🔷 Neutre-haussier : signaux mitigés, attendre confirmation d'un retournement clair."
        elif score >= 50:
            msg = Fore.YELLOW + "🟠 Marché équilibré : peu de marge de sécurité, à surveiller sans se précipiter."
        elif score >= 40:
            msg = Fore.MAGENTA + "🟣 Signaux techniques fragiles : possible consolidation, prudence."
        else:
            msg = Fore.RED + "🔴 Configuration défavorable : tendance ou momentum faibles, pas de signal d'entrée."

        # ✅ Renforcement du message si plusieurs indicateurs convergent
        if bullish_signals >= 3 and score >= 70:
            msg += Fore.GREEN + "\n✅ Plusieurs indicateurs convergent → signal fort de retournement probable."

        elif bullish_signals <= 1 and score < 50:
            msg += Fore.RED + "\n⚠️ Peu ou pas de signaux positifs → risque élevé de poursuite baissière."

        return msg + Style.RESET_ALL

    @staticmethod
    def integrated_interpretation(score, fibonacci_data):
        """Combine technical momentum and Fibonacci context into one decision.

        Fibonacci is already one weighted component of ``score``. It is used
        here as a confirmation and risk filter, not counted a second time.
        """
        if not fibonacci_data or not fibonacci_data.get("valid", False):
            return (
                Fore.YELLOW
                + "🟠 Analyse technique partielle : Fibonacci n'est pas exploitable, "
                "aucune entrée agressive."
                + Style.RESET_ALL
            )

        analysis = fibonacci_data["analysis"]
        trend = fibonacci_data.get("trend", "indéterminé")
        fibonacci_score = analysis.get("score", 0)
        risk_reward = analysis.get("risk_reward")

        if trend == "baissier":
            return (
                Fore.RED
                + "🔴 Pas de signal d'achat : tendance baissière confirmée. "
                "Attendre un retournement et une clôture au-dessus d'une moyenne clé."
                + Style.RESET_ALL
            )

        if fibonacci_score < 4 or (risk_reward and risk_reward["ratio"] < 1):
            return (
                Fore.YELLOW
                + "🟠 Configuration défavorable : la zone Fibonacci n'offre pas "
                "assez de marge de sécurité."
                + Style.RESET_ALL
            )

        if score >= 70 and fibonacci_score >= 6 and (
            risk_reward is None or risk_reward["ratio"] >= 1.5
        ):
            return (
                Fore.GREEN
                + "🟢 Signal technique confirmé : momentum, tendance et zone "
                "Fibonacci convergent. Entrée progressive uniquement."
                + Style.RESET_ALL
            )

        if score >= 55 and fibonacci_score >= 5:
            return (
                Fore.CYAN
                + "🔵 Configuration surveillable : signaux partiellement alignés. "
                "Attendre une confirmation avant toute entrée."
                + Style.RESET_ALL
            )

        return (
            Fore.YELLOW
            + "🟠 Signal insuffisant : les indicateurs techniques et Fibonacci "
            "ne convergent pas assez."
            + Style.RESET_ALL
        )