from colorama import Fore, Style

class IndicatorEvaluator:
    """
    Évalue les indicateurs techniques avec une approche équilibrée orientée détection d'opportunités
    moyen-terme (2 ans). Combine prudence et flexibilité pour capter les retournements naissants.
    """

    def __init__(self):
        self.weights = {
            "RSI": 22,
            "Stochastique": 5,
            "Bollinger": 20,
            "MACD": 22,
            "OBV": 5,
            "EMA200": 21,
            "ADX": 5,
        }

    # --- RSI ---
    def evaluate_rsi(self, rsi: float):
        if rsi < 22:
            return 10, "🟢 RSI < 20 → Marché en panique totale 😱. Niveau historiquement bas, opportunité exceptionnelle 💎."
        elif rsi < 28:
            return 9, "🟢 RSI 20–28 → Forte sous-évaluation, marché dominé par la peur. Signal d’entrée solide ✅."
        elif rsi < 30:
            return 8, "🟢 RSI 28–35 → Sous-évaluation technique claire, zone d’achat intéressante 👀."
        elif rsi < 35:
            return 7, "🟢 RSI 28–35 → Sous-évaluation technique claire, zone d’achat intéressante 👀."
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
            return 6, "🟡 Stochastique bas mais stabilisé → zone d’observation."
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
            return 6, "🟡 Cours sous la moyenne → phase de repli, bonne zone d’accumulation progressive 📊."
        elif close < bb_high:
            return 4, "⚪ Cours entre moyenne et bande haute → marché équilibré."
        else:
            return 2, "🔴 Cours au-dessus de la bande haute → euphorie du marché 🚨."

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
            return 5, "🟡 MACD haussier positif → tendance déjà engagée, peu de marge d’entrée 🏁."
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
            return 7, f"🟢 Prix {abs(discount):.1f}% sous EMA200 → décote intéressante, zone d’accumulation potentielle."
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

    # --- ADX ---
    def evaluate_adx(self, adx):
        if adx < 10:
            return 8, "🟢 ADX < 10 → marché très calme, souvent proche d’un plancher ⏳."
        elif 10 <= adx < 20:
            return 7, "🟢 ADX 10–20 → tendance faible mais en formation 🌱."
        elif 20 <= adx < 30:
            return 5, "⚪ ADX 20–30 → tendance moyenne, rien de marqué."
        elif 30 <= adx < 40:
            return 3, "🟠 ADX 30–40 → tendance forte, possible entrée tardive."
        else:
            return 1, "🔴 ADX > 40 → tendance violente, peu de marge pour un achat."
        


    def _global_interpretation(df, score):
        """Interprétation globale affinée du score total, adaptée à la détection de sous-évaluation."""
        bullish_signals = sum(df["Note (/10)"] >= 7)

        if score >= 90:
            msg = Fore.GREEN + "💎 Exceptionnel : forte sous-évaluation confirmée 🔥 — opportunité rare à saisir."
        elif score >= 80:
            msg = Fore.GREEN + "🟢 Très bon niveau : marché nettement en décote, configuration favorable à l’achat."
        elif score >= 70:
            msg = Fore.CYAN + "🔵 Sous-évaluation modérée : tendance de reprise à confirmer par le volume ou le MACD."
        elif score >= 60:
            msg = Fore.LIGHTBLUE_EX + "🔷 Neutre-haussier : signaux mitigés, attendre confirmation d’un retournement clair."
        elif score >= 50:
            msg = Fore.YELLOW + "🟠 Marché équilibré : peu de marge de sécurité, à surveiller sans se précipiter."
        elif score >= 40:
            msg = Fore.MAGENTA + "🟣 Légère surévaluation : prudence, possible consolidation avant reprise."
        else:
            msg = Fore.RED + "🔴 Surévaluation marquée : tendance défavorable, aucun signal d’entrée."

        # ✅ Renforcement du message si plusieurs indicateurs convergent
        if bullish_signals >= 3 and score >= 70:
            msg += Fore.GREEN + "\n✅ Plusieurs indicateurs convergent → signal fort de retournement probable."

        elif bullish_signals <= 1 and score < 50:
            msg += Fore.RED + "\n⚠️ Peu ou pas de signaux positifs → risque élevé de poursuite baissière."

        return msg + Style.RESET_ALL

