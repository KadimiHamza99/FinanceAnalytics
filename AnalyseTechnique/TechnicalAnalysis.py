import pandas as pd
import numpy as np
from AnalyseTechnique.IndicatorEvaluator import IndicatorEvaluator
from AnalyseTechnique.Utils import Utils
import os


class TechnicalAnalysis:
    """Analyse technique des points d'entrée avec évaluation pondérée."""

    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol
        self.evaluator = IndicatorEvaluator()

    def calculate_fibonacci_levels(self, data, period=50):
        """
        Calcule les niveaux de Fibonacci basés sur le plus haut et le plus bas de la période.
        
        Args:
            data: DataFrame avec les données de prix
            period: Nombre de jours pour calculer le range (défaut: 50)
            
        Returns:
            dict: Dictionnaire contenant les niveaux de Fibonacci et l'analyse
        """
        recent_data = data.tail(period)
        high = float(recent_data["High"].max())
        low = float(recent_data["Low"].min())
        diff = high - low
        current_price = float(data.iloc[-1]["Close"])
        
        # Niveaux de retracement de Fibonacci
        levels = {
            "High (100%)": high,
            "Fib 78.6%": high - (diff * 0.214),
            "Fib 61.8%": high - (diff * 0.382),
            "Fib 50%": high - (diff * 0.5),
            "Fib 38.2%": high - (diff * 0.618),
            "Fib 23.6%": high - (diff * 0.764),
            "Low (0%)": low,
        }
        
        # Extensions de Fibonacci (pour les objectifs de sortie)
        extensions = {
            "Ext 161.8%": high + (diff * 0.618),
            "Ext 138.2%": high + (diff * 0.382),
            "Ext 127.2%": high + (diff * 0.272),
            "Ext 100%": high,
        }
        
        # Déterminer les zones clés
        analysis = self._analyze_fibonacci_position(current_price, levels, extensions, diff)
        
        return {
            "levels": levels,
            "extensions": extensions,
            "high": high,
            "low": low,
            "range": diff,
            "current_price": current_price,
            "analysis": analysis
        }
    
    def _analyze_fibonacci_position(self, price, levels, extensions, range_size):
        """
        Analyse la position du prix par rapport aux niveaux de Fibonacci.
        
        Returns:
            dict: Dictionnaire avec supports, résistances, entrée, sortie, stop loss
        """
        # Identifier le niveau le plus proche en dessous (support)
        support = None
        support_name = None
        for name, level in sorted(levels.items(), key=lambda x: x[1], reverse=True):
            if level < price:
                support = level
                support_name = name
                break
        
        # Identifier le niveau le plus proche au dessus (résistance)
        resistance = None
        resistance_name = None
        for name, level in sorted(levels.items(), key=lambda x: x[1]):
            if level > price:
                resistance = level
                resistance_name = name
                break
        
        # Calcul du niveau d'entrée optimal
        if support and resistance:
            # Zone d'entrée entre le support et 20% vers la résistance
            entry_zone_low = support
            entry_zone_high = support + (resistance - support) * 0.2
        else:
            entry_zone_low = price * 0.98
            entry_zone_high = price * 1.02
        
        # Calcul du stop loss (2-3% sous le support ou niveau Fib inférieur)
        if support:
            stop_loss = support * 0.97  # 3% sous le support
        else:
            stop_loss = price * 0.95  # 5% sous le prix actuel par défaut
        
        # Objectifs de sortie basés sur les extensions et résistances
        targets = []
        if resistance:
            targets.append({
                "level": resistance,
                "name": resistance_name,
                "type": "Résistance Fibonacci",
                "gain_potential": ((resistance - price) / price) * 100
            })
        
        # Ajouter les extensions comme objectifs si le prix est dans la partie haute
        for ext_name, ext_level in sorted(extensions.items(), key=lambda x: x[1]):
            if ext_level > price:
                targets.append({
                    "level": ext_level,
                    "name": ext_name,
                    "type": "Extension Fibonacci",
                    "gain_potential": ((ext_level - price) / price) * 100
                })
        
        # Évaluation de la position (note sur 10) - délégation à IndicatorEvaluator
        position_score, interpretation = self.evaluator.evaluate_fibonacci(price, levels, support, resistance)
        
        return {
            "support": support,
            "support_name": support_name,
            "resistance": resistance,
            "resistance_name": resistance_name,
            "entry_zone": (entry_zone_low, entry_zone_high),
            "stop_loss": stop_loss,
            "targets": targets[:3],  # Top 3 objectifs
            "score": position_score,
            "interpretation": interpretation,
            "risk_reward": self._calculate_risk_reward(price, stop_loss, targets)
        }
    
    def _calculate_risk_reward(self, entry, stop_loss, targets):
        """Calcule le ratio risque/récompense."""
        if not targets:
            return None
        
        risk = entry - stop_loss
        if risk <= 0:
            return None
        
        # Prendre le premier objectif
        reward = targets[0]["level"] - entry
        ratio = reward / risk if risk > 0 else 0
        
        return {
            "risk": risk,
            "reward": reward,
            "ratio": ratio
        }

    def run(self):
        try:
            data = Utils.fetch_data(self.ticker_symbol)
            data = Utils.compute_indicators(data)
        except Exception as e:
            return pd.DataFrame(), 0, f"❌ {e}", None

        last = data.iloc[-1]
        ev = self.evaluator
        results = []

        # --- Conversion explicite en float ---
        rsi = float(last["RSI"].iloc[0])
        stoch_k = float(last["STOCH_K"].iloc[0])
        stoch_d = float(last["STOCH_D"].iloc[0])
        close = float(last["Close"].iloc[0])
        bb_l = float(last["BB_L"].iloc[0])
        bb_m = float(last["BB_M"].iloc[0])
        bb_h = float(last["BB_H"].iloc[0])
        macd_val = float(last["MACD"].iloc[0])
        signal_val = float(last["Signal"].iloc[0])
        obv = float(last["OBV"].iloc[0])
        ema200 = float(last["EMA200"].iloc[0])
        adx = float(last["ADX"].iloc[0])

        # Calcul de Fibonacci
        fib_data = self.calculate_fibonacci_levels(data, period=50)
        fib_analysis = fib_data["analysis"]

        # Évaluations
        results.append(self._make_row("RSI (14)", rsi, *ev.evaluate_rsi(rsi), ev.weights["RSI"]))
        results.append(self._make_row("Stochastique K/D", f"{stoch_k:.2f}/{stoch_d:.2f}",
                                    *ev.evaluate_stoch(stoch_k, stoch_d), ev.weights["Stochastique"]))
        results.append(self._make_row("Bandes de Bollinger", close,
                                    *ev.evaluate_bollinger(close, bb_l, bb_m, bb_h), ev.weights["Bollinger"]))
        results.append(self._make_row("MACD", macd_val,
                                    *ev.evaluate_macd(macd_val, signal_val), ev.weights["MACD"]))
        results.append(self._make_row("OBV", obv,
                                    *ev.evaluate_obv(data["OBV"].iloc[-5:].mean(), data["OBV"].iloc[-20:-5].mean()), ev.weights["OBV"]))
        results.append(self._make_row("Décote vs EMA200", f"{(close - ema200) / ema200 * 100:.2f}%",
                                    *ev.evaluate_ema200(close, ema200), ev.weights["EMA200"]))
        results.append(self._make_row("ADX (14)", adx,
                                    *ev.evaluate_adx(adx), ev.weights["ADX"]))
        
        # Ajout de l'analyse Fibonacci
        results.append(self._make_row("Niveaux Fibonacci", f"{close:.2f}",
                                    fib_analysis["score"], fib_analysis["interpretation"], 10.0))

        df = pd.DataFrame(results)
        df["Score pondéré"] = df["Note (/10)"] * df["Poids (%)"] / 10
        score_total = df["Score pondéré"].sum()

        reco = IndicatorEvaluator._global_interpretation(df, score_total)

        # Ajout des informations Fibonacci à la recommandation
        fib_info = self._format_fibonacci_info(fib_data)

        # if os.getenv('GITHUB_ACTIONS') == 'true':
        #     llm_reco = Utils.askMistralTechnicalAnalysis("mistral:7b", rsi, macd_val, ema200, bb_l, bb_m, bb_h, stoch_k, stoch_d, obv, adx, close) + f"\nPrix Actuel en bourse : {close}"
        # else:
        #     llm_reco = "Analyse technique LLM non disponible en local."
        llm_reco = ""
        print(f"Prix Actuel en bourse : {close}")
        print(fib_info)
        
        return df, score_total, reco, llm_reco, fib_data

    def _format_fibonacci_info(self, fib_data):
        """Formate les informations Fibonacci pour l'affichage."""
        analysis = fib_data["analysis"]
        
        info = "\n" + "="*60
        info += "\n📊 ANALYSE FIBONACCI (50 jours)\n"
        info += "="*60 + "\n"
        
        info += f"\n📍 Prix actuel : {fib_data['current_price']:.2f}€"
        info += f"\n📈 Plus haut (50j) : {fib_data['high']:.2f}€"
        info += f"\n📉 Plus bas (50j) : {fib_data['low']:.2f}€"
        info += f"\n📏 Range : {fib_data['range']:.2f}€"
        
        info += "\n\n🎯 NIVEAUX DE RETRACEMENT FIBONACCI :"
        for name, level in fib_data["levels"].items():
            marker = " ← PRIX ACTUEL" if abs(level - fib_data['current_price']) < fib_data['range'] * 0.05 else ""
            info += f"\n  {name:15} : {level:.2f}€{marker}"
        
        info += "\n\n🚀 EXTENSIONS FIBONACCI (Objectifs) :"
        for name, level in fib_data["extensions"].items():
            gain = ((level - fib_data['current_price']) / fib_data['current_price']) * 100
            info += f"\n  {name:15} : {level:.2f}€ (+{gain:.1f}%)"
        
        info += "\n\n" + "-"*60
        info += "\n💡 RECOMMANDATIONS DE TRADING :"
        info += "\n" + "-"*60
        
        if analysis["support"]:
            info += f"\n🛡️  Support : {analysis['support']:.2f}€ ({analysis['support_name']})"
        if analysis["resistance"]:
            info += f"\n⚔️  Résistance : {analysis['resistance']:.2f}€ ({analysis['resistance_name']})"
        
        entry_low, entry_high = analysis["entry_zone"]
        info += f"\n\n✅ Zone d'entrée optimale : {entry_low:.2f}€ - {entry_high:.2f}€"
        info += f"\n🛑 Stop Loss recommandé : {analysis['stop_loss']:.2f}€"
        
        info += "\n\n🎯 Objectifs de sortie :"
        for i, target in enumerate(analysis["targets"], 1):
            info += f"\n   Objectif {i} : {target['level']:.2f}€ ({target['name']}) - Gain potentiel: +{target['gain_potential']:.1f}%"
        
        if analysis["risk_reward"]:
            rr = analysis["risk_reward"]
            info += f"\n\n⚖️  Ratio Risque/Récompense : 1:{rr['ratio']:.2f}"
            info += f"\n   Risque : {rr['risk']:.2f}€ | Récompense : {rr['reward']:.2f}€"
        
        info += f"\n\n📝 Interprétation : {analysis['interpretation']}"
        info += f"\n⭐ Score Fibonacci : {analysis['score']:.1f}/10"
        
        info += "\n" + "="*60 + "\n"
        
        return info

    def _make_row(self, name, value, note, interp, weight):
        return {
            "Indicateur": name,
            "Valeur": f"{value:.2f}" if isinstance(value, (int, float, np.floating)) else str(value),
            "Note (/10)": note,
            "Poids (%)": weight,
            "Interprétation": interp,
        }