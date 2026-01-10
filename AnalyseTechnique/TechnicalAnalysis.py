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
        Version améliorée avec validation et détection de tendance.
        
        Args:
            data: DataFrame avec les données de prix
            period: Nombre de jours pour calculer le range (défaut: 50)
            
        Returns:
            dict: Dictionnaire contenant les niveaux de Fibonacci et l'analyse
        """
        try:
            if len(data) < period:
                period = len(data)
            
            if period < 10:
                return self._create_invalid_fibonacci_result(
                    float(data.iloc[-1]["Close"]), 
                    "Pas assez de données historiques (minimum 10 jours)"
                )
            
            recent_data = data.tail(period)
            
            # Conversion robuste en float
            high_series = recent_data["High"]
            low_series = recent_data["Low"]
            close_series = data.iloc[-1]["Close"]
            
            # S'assurer qu'on a des valeurs scalaires
            if isinstance(high_series.max(), pd.Series):
                high = float(high_series.max().iloc[0])
            else:
                high = float(high_series.max())
            
            if isinstance(low_series.min(), pd.Series):
                low = float(low_series.min().iloc[0])
            else:
                low = float(low_series.min())
            
            if isinstance(close_series, pd.Series):
                current_price = float(close_series.iloc[0])
            else:
                current_price = float(close_series)
            
            diff = high - low
            
        except Exception as e:
            return self._create_invalid_fibonacci_result(
                float(data.iloc[-1]["Close"]) if len(data) > 0 else 0.0,
                f"Erreur extraction données: {str(e)}"
            )
        
        # Validation : vérifier que le range est significatif (au moins 2% du prix)
        if diff <= 0 or current_price <= 0:
            return self._create_invalid_fibonacci_result(current_price, 
                "Range invalide - prix identiques sur la période")
        
        if diff / current_price < 0.02:
            return self._create_invalid_fibonacci_result(current_price, 
                "Range trop faible sur la période - Fibonacci non applicable")
        
        # Détection de la tendance
        try:
            trend = self._detect_trend(data, period)
        except Exception as e:
            print(f"⚠️ Erreur détection tendance: {e}")
            trend = "neutre"
        
        # Niveaux de retracement de Fibonacci (corrigés)
        # Pour une tendance haussière : high = 100%, low = 0%
        # Pour une tendance baissière : high = 0%, low = 100%
        levels = {
            "High (100%)": high,
            "Fib 78.6%": high - (diff * 0.214),  # Retracement de 21.4%
            "Fib 61.8%": high - (diff * 0.382),  # Retracement de 38.2%
            "Fib 50%": high - (diff * 0.5),      # Retracement de 50%
            "Fib 38.2%": high - (diff * 0.618),  # Retracement de 61.8%
            "Fib 23.6%": high - (diff * 0.764),  # Retracement de 76.4%
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
        analysis = self._analyze_fibonacci_position(current_price, levels, extensions, diff, trend)
        
        return {
            "levels": levels,
            "extensions": extensions,
            "high": high,
            "low": low,
            "range": diff,
            "current_price": current_price,
            "trend": trend,
            "analysis": analysis,
            "valid": True
        }
    
    def _detect_trend(self, data, period):
        """
        Détecte la tendance sur la période donnée.
        
        Returns:
            str: 'haussier', 'baissier', ou 'neutre'
        """
        try:
            recent_data = data.tail(period)
            
            if len(recent_data) < 10:
                return "neutre"
            
            # Comparer les moyennes mobiles courtes et longues
            close_series = recent_data["Close"]
            sma_short = float(close_series.tail(10).mean())
            sma_long = float(close_series.mean())
            
            # Prix de début et de fin de période
            start_close = recent_data.iloc[0]["Close"]
            end_close = recent_data.iloc[-1]["Close"]
            
            # Conversion en float
            if isinstance(start_close, pd.Series):
                start_price = float(start_close.iloc[0])
            else:
                start_price = float(start_close)
            
            if isinstance(end_close, pd.Series):
                end_price = float(end_close.iloc[0])
            else:
                end_price = float(end_close)
            
            price_change_pct = ((end_price - start_price) / start_price) * 100
            
            # Détection de tendance
            if price_change_pct > 5 and sma_short > sma_long * 1.02:
                return "haussier"
            elif price_change_pct < -5 and sma_short < sma_long * 0.98:
                return "baissier"
            else:
                return "neutre"
        except Exception as e:
            print(f"⚠️ Erreur dans _detect_trend: {e}")
            return "neutre"
    
    def _create_invalid_fibonacci_result(self, current_price, reason):
        """Crée un résultat Fibonacci invalide avec message d'erreur."""
        return {
            "levels": {},
            "extensions": {},
            "high": current_price,
            "low": current_price,
            "range": 0,
            "current_price": current_price,
            "trend": "indéterminé",
            "valid": False,
            "analysis": {
                "support": None,
                "support_name": None,
                "resistance": None,
                "resistance_name": None,
                "entry_zone": (current_price, current_price),
                "stop_loss": current_price * 0.95,
                "targets": [],
                "score": 5.0,
                "interpretation": f"⚠️ {reason}",
                "risk_reward": None
            }
        }
    
    def _analyze_fibonacci_position(self, price, levels, extensions, range_size, trend):
        """
        Analyse la position du prix par rapport aux niveaux de Fibonacci.
        Version améliorée avec prise en compte de la tendance.
        
        Returns:
            dict: Dictionnaire avec supports, résistances, entrée, sortie, stop loss
        """
        # Tolérance pour considérer qu'on est "sur" un niveau (1% du range)
        tolerance = range_size * 0.01
        
        # Identifier le niveau le plus proche en dessous (support)
        support = None
        support_name = None
        support_distance = float('inf')
        
        for name, level in levels.items():
            if level < price - tolerance:
                distance = price - level
                if distance < support_distance:
                    support = level
                    support_name = name
                    support_distance = distance
        
        # Identifier le niveau le plus proche au-dessus (résistance)
        resistance = None
        resistance_name = None
        resistance_distance = float('inf')
        
        for name, level in levels.items():
            if level > price + tolerance:
                distance = level - price
                if distance < resistance_distance:
                    resistance = level
                    resistance_name = name
                    resistance_distance = distance
        
        # Déterminer la zone d'entrée selon la tendance
        if trend == "haussier":
            # En tendance haussière : chercher un retracement (38.2%, 50%, ou 61.8%)
            entry_zone_low = levels.get("Fib 61.8%", support if support else price * 0.95)
            entry_zone_high = levels.get("Fib 38.2%", price)
        elif trend == "baissier":
            # En tendance baissière : attendre un rebond vers une résistance
            entry_zone_low = price
            entry_zone_high = resistance if resistance else price * 1.05
        else:
            # Tendance neutre : zone autour du niveau 50%
            fib_50 = levels.get("Fib 50%")
            if fib_50:
                entry_zone_low = fib_50 * 0.98
                entry_zone_high = fib_50 * 1.02
            else:
                entry_zone_low = price * 0.98
                entry_zone_high = price * 1.02
        
        # Calcul du stop loss adapté à la tendance
        if trend == "haussier":
            # Stop sous le prochain niveau Fibonacci important
            if support:
                # Trouver le niveau Fibonacci en dessous du support actuel
                next_support = None
                for name, level in sorted(levels.items(), key=lambda x: x[1], reverse=True):
                    if level < support - tolerance:
                        next_support = level
                        break
                stop_loss = next_support * 0.99 if next_support else support * 0.97
            else:
                stop_loss = price * 0.95
        elif trend == "baissier":
            # En tendance baissière, stop au-dessus de la résistance
            stop_loss = resistance * 1.03 if resistance else price * 1.05
        else:
            # Tendance neutre : stop sous le support
            stop_loss = support * 0.97 if support else price * 0.95
        
        # Objectifs de sortie basés sur la tendance
        targets = []
        
        if trend == "haussier":
            # Objectifs : prochaines résistances puis extensions
            if resistance and resistance > price:
                targets.append({
                    "level": resistance,
                    "name": resistance_name,
                    "type": "Résistance Fibonacci",
                    "gain_potential": ((resistance - price) / price) * 100
                })
            
            # Ajouter les niveaux supérieurs
            for name, level in sorted(levels.items(), key=lambda x: x[1]):
                if level > price and len(targets) < 3:
                    if not any(t["level"] == level for t in targets):
                        targets.append({
                            "level": level,
                            "name": name,
                            "type": "Résistance Fibonacci",
                            "gain_potential": ((level - price) / price) * 100
                        })
            
            # Ajouter extensions (augmenté de 3 à 5 objectifs max)
            for ext_name, ext_level in sorted(extensions.items(), key=lambda x: x[1]):
                if ext_level > price and len(targets) < 5:
                    targets.append({
                        "level": ext_level,
                        "name": ext_name,
                        "type": "Extension Fibonacci",
                        "gain_potential": ((ext_level - price) / price) * 100
                    })
        
        elif trend == "baissier":
            # En baissier, objectifs = supports en dessous (augmenté à 5 objectifs)
            for name, level in sorted(levels.items(), key=lambda x: x[1], reverse=True):
                if level < price and len(targets) < 5:
                    targets.append({
                        "level": level,
                        "name": name,
                        "type": "Support Fibonacci (Short)",
                        "gain_potential": ((price - level) / price) * 100  # Gain en short
                    })
        else:
            # Neutre : objectifs modérés (augmenté à 3 objectifs)
            if resistance:
                targets.append({
                    "level": resistance,
                    "name": resistance_name,
                    "type": "Résistance Fibonacci",
                    "gain_potential": ((resistance - price) / price) * 100
                })
            
            # Ajouter d'autres niveaux au-dessus
            for name, level in sorted(levels.items(), key=lambda x: x[1]):
                if level > price and len(targets) < 3:
                    if not any(t["level"] == level for t in targets):
                        targets.append({
                            "level": level,
                            "name": name,
                            "type": "Résistance Fibonacci",
                            "gain_potential": ((level - price) / price) * 100
                        })
        
        # Évaluation de la position - score amélioré
        position_score, interpretation = self._evaluate_fibonacci_position(
            price, levels, support, resistance, trend, range_size
        )
        
        # Calcul du ratio risque/récompense
        risk_reward = self._calculate_risk_reward(price, stop_loss, targets, trend)
        
        return {
            "support": support,
            "support_name": support_name,
            "resistance": resistance,
            "resistance_name": resistance_name,
            "entry_zone": (entry_zone_low, entry_zone_high),
            "stop_loss": stop_loss,
            "targets": targets[:5],  # Top 5 objectifs au lieu de 3
            "score": position_score,
            "interpretation": interpretation,
            "risk_reward": risk_reward
        }
    
    def _evaluate_fibonacci_position(self, price, levels, support, resistance, trend, range_size):
        """
        Évalue la qualité de la position actuelle selon Fibonacci.
        
        Returns:
            tuple: (score, interpretation)
        """
        score = 5.0  # Score neutre de base
        reasons = []
        
        try:
            # Calcul de la position relative dans le range
            high = float(levels["High (100%)"])
            low = float(levels["Low (0%)"])
            
            if high == low:
                return 5.0, "Position neutre - range trop faible"
            
            position_pct = ((price - low) / (high - low)) * 100
        except Exception as e:
            print(f"⚠️ Erreur calcul position: {e}")
            return 5.0, f"Erreur évaluation position: {str(e)}"
        
        # Évaluation selon la position et la tendance
        if trend == "haussier":
            # En tendance haussière, chercher les retracements (zones d'achat)
            if 35 <= position_pct <= 65:  # Zone 38.2% - 61.8%
                score += 3
                reasons.append("✅ Prix dans zone de retracement idéale (38-62%)")
            elif position_pct < 35:
                score += 2
                reasons.append("✅ Prix proche du support - bon point d'entrée")
            elif position_pct > 80:
                score -= 2
                reasons.append("⚠️ Prix proche du plus haut - risque de correction")
            
            # Proximité d'un niveau clé
            for name, level in levels.items():
                if abs(price - level) / range_size < 0.03:  # À 3% du niveau
                    if "61.8%" in name or "50%" in name:
                        score += 1
                        reasons.append(f"✅ Prix proche du niveau clé {name}")
                        break
        
        elif trend == "baissier":
            # En tendance baissière, méfiance, attendre les rebonds
            if position_pct > 65:
                score += 2
                reasons.append("⚠️ Tendance baissière - attendre rebond vers résistance")
            else:
                score -= 1
                reasons.append("⚠️ Tendance baissière active - prudence")
        
        else:  # neutre
            if 45 <= position_pct <= 55:  # Autour de 50%
                score += 1
                reasons.append("Neutre - Prix autour du niveau 50%")
            reasons.append("📊 Marché en consolidation")
        
        # Vérifier le ratio risque/récompense potentiel
        if support and resistance:
            potential_gain = resistance - price
            potential_loss = price - support
            if potential_loss > 0:
                rr_ratio = potential_gain / potential_loss
                if rr_ratio > 2:
                    score += 1.5
                    reasons.append(f"✅ Bon ratio R/R potentiel (~{rr_ratio:.1f}:1)")
                elif rr_ratio < 1:
                    score -= 1
                    reasons.append(f"⚠️ Ratio R/R défavorable (~{rr_ratio:.1f}:1)")
        
        # Limiter le score entre 0 et 10
        score = max(0, min(10, score))
        
        # Construction de l'interprétation
        if score >= 7.5:
            interpretation = "🟢 EXCELLENTE position Fibonacci - " + " | ".join(reasons)
        elif score >= 6:
            interpretation = "🟡 BONNE position Fibonacci - " + " | ".join(reasons)
        elif score >= 4:
            interpretation = "🟠 Position MOYENNE - " + " | ".join(reasons)
        else:
            interpretation = "🔴 Position DÉFAVORABLE - " + " | ".join(reasons)
        
        return score, interpretation
    
    def _calculate_risk_reward(self, entry, stop_loss, targets, trend):
        """Calcule le ratio risque/récompense selon la tendance."""
        if not targets:
            return None
        
        if trend == "baissier":
            # En short, le risque est vers le haut
            risk = stop_loss - entry
        else:
            # En long, le risque est vers le bas
            risk = entry - stop_loss
        
        if risk <= 0:
            return None
        
        # Prendre le premier objectif
        if trend == "baissier":
            reward = entry - targets[0]["level"]  # Gain en short
        else:
            reward = targets[0]["level"] - entry  # Gain en long
        
        ratio = reward / risk if risk > 0 else 0
        
        return {
            "risk": abs(risk),
            "reward": abs(reward),
            "ratio": ratio
        }

    def run(self):
        try:
            data = Utils.fetch_data(self.ticker_symbol)
            data = Utils.compute_indicators(data)
        except Exception as e:
            return pd.DataFrame(), 0, f"❌ {e}", None, None

        if data is None or len(data) == 0:
            return pd.DataFrame(), 0, "❌ Aucune donnée disponible", None, None

        try:
            last = data.iloc[-1]
        except Exception as e:
            return pd.DataFrame(), 0, f"❌ Erreur d'accès aux données: {e}", None, None
        
        ev = self.evaluator
        results = []

        # --- Conversion robuste en float avec gestion complète des erreurs ---
        def safe_float(value, column_name="unknown", default=0.0):
            """Convertit une valeur en float de manière sécurisée."""
            try:
                if value is None:
                    print(f"⚠️ Valeur None pour {column_name}, utilisation de {default}")
                    return default
                
                if isinstance(value, pd.Series):
                    if len(value) == 0:
                        print(f"⚠️ Series vide pour {column_name}, utilisation de {default}")
                        return default
                    value = value.iloc[0]
                
                if pd.isna(value):
                    print(f"⚠️ Valeur NaN pour {column_name}, utilisation de {default}")
                    return default
                
                return float(value)
            except (ValueError, TypeError, AttributeError) as e:
                print(f"⚠️ Erreur conversion {column_name}: {e}, utilisation de {default}")
                return default
        
        try:
            rsi = safe_float(last["RSI"], "RSI", 50.0)
            stoch_k = safe_float(last["STOCH_K"], "STOCH_K", 50.0)
            stoch_d = safe_float(last["STOCH_D"], "STOCH_D", 50.0)
            close = safe_float(last["Close"], "Close")
            bb_l = safe_float(last["BB_L"], "BB_L", close * 0.98)
            bb_m = safe_float(last["BB_M"], "BB_M", close)
            bb_h = safe_float(last["BB_H"], "BB_H", close * 1.02)
            macd_val = safe_float(last["MACD"], "MACD", 0.0)
            signal_val = safe_float(last["Signal"], "Signal", 0.0)
            obv = safe_float(last["OBV"], "OBV", 0.0)
            ema200 = safe_float(last["EMA200"], "EMA200", close)
            adx = safe_float(last["ADX"], "ADX", 25.0)
        except KeyError as e:
            return pd.DataFrame(), 0, f"❌ Colonne manquante dans les données: {e}", None, None
        except Exception as e:
            return pd.DataFrame(), 0, f"❌ Erreur lors de l'extraction des indicateurs: {e}", None, None

        # Calcul de Fibonacci amélioré avec gestion d'erreur
        try:
            fib_data = self.calculate_fibonacci_levels(data, period=50)
            fib_analysis = fib_data["analysis"]
        except Exception as e:
            print(f"⚠️ Erreur lors du calcul Fibonacci: {e}")
            fib_data = self._create_invalid_fibonacci_result(close, f"Erreur calcul: {str(e)}")
            fib_analysis = fib_data["analysis"]

        # Évaluations avec gestion d'erreur
        try:
            results.append(self._make_row("RSI (14)", rsi, *ev.evaluate_rsi(rsi), ev.weights["RSI"]))
        except Exception as e:
            print(f"⚠️ Erreur évaluation RSI: {e}")
        
        try:
            results.append(self._make_row("Stochastique K/D", f"{stoch_k:.2f}/{stoch_d:.2f}",
                                        *ev.evaluate_stoch(stoch_k, stoch_d), ev.weights["Stochastique"]))
        except Exception as e:
            print(f"⚠️ Erreur évaluation Stochastique: {e}")
        
        try:
            results.append(self._make_row("Bandes de Bollinger", close,
                                        *ev.evaluate_bollinger(close, bb_l, bb_m, bb_h), ev.weights["Bollinger"]))
        except Exception as e:
            print(f"⚠️ Erreur évaluation Bollinger: {e}")
        
        try:
            results.append(self._make_row("MACD", macd_val,
                                        *ev.evaluate_macd(macd_val, signal_val), ev.weights["MACD"]))
        except Exception as e:
            print(f"⚠️ Erreur évaluation MACD: {e}")
        
        try:
            obv_recent = data["OBV"].iloc[-5:].mean() if len(data) >= 5 else obv
            obv_past = data["OBV"].iloc[-20:-5].mean() if len(data) >= 20 else obv
            results.append(self._make_row("OBV", obv,
                                        *ev.evaluate_obv(obv_recent, obv_past), ev.weights["OBV"]))
        except Exception as e:
            print(f"⚠️ Erreur évaluation OBV: {e}")
        
        try:
            results.append(self._make_row("Décote vs EMA200", f"{(close - ema200) / ema200 * 100:.2f}%",
                                        *ev.evaluate_ema200(close, ema200), ev.weights["EMA200"]))
        except Exception as e:
            print(f"⚠️ Erreur évaluation EMA200: {e}")
        
        try:
            results.append(self._make_row("ADX (14)", adx,
                                        *ev.evaluate_adx(adx), ev.weights["ADX"]))
        except Exception as e:
            print(f"⚠️ Erreur évaluation ADX: {e}")
        
        # Ajout de l'analyse Fibonacci (seulement si valide)
        try:
            if fib_data.get("valid", True):
                results.append(self._make_row("Niveaux Fibonacci", f"{close:.2f}",
                                            fib_analysis["score"], fib_analysis["interpretation"], 10.0))
        except Exception as e:
            print(f"⚠️ Erreur ajout Fibonacci: {e}")

        if len(results) == 0:
            return pd.DataFrame(), 0, "❌ Aucun indicateur n'a pu être calculé", None, None

        df = pd.DataFrame(results)
        df["Score pondéré"] = df["Note (/10)"] * df["Poids (%)"] / 10
        score_total = df["Score pondéré"].sum()

        try:
            reco = IndicatorEvaluator._global_interpretation(df, score_total)
        except Exception as e:
            reco = f"Analyse technique (score: {score_total:.1f}/10) - Erreur interprétation: {e}"

        # Ajout des informations Fibonacci à la recommandation
        try:
            fib_info = self._format_fibonacci_info(fib_data)
        except Exception as e:
            fib_info = f"\n⚠️ Erreur formatage Fibonacci: {e}\n"

        llm_reco = close
        print(f"Prix Actuel en bourse : {close}")
        print(fib_info)
        
        return df, score_total, reco, llm_reco, fib_data

    def _format_fibonacci_info(self, fib_data):
        """Formate les informations Fibonacci pour l'affichage."""
        try:
            if not fib_data.get("valid", True):
                return f"\n⚠️ FIBONACCI NON APPLICABLE\n{fib_data['analysis']['interpretation']}\n"
            
            analysis = fib_data["analysis"]
            trend_emoji = {"haussier": "📈", "baissier": "📉", "neutre": "➡️"}
            
            info = "\n" + "="*60
            info += "\n📊 ANALYSE FIBONACCI (50 jours)\n"
            info += "="*60 + "\n"
            
            info += f"\n📍 Prix actuel : {fib_data['current_price']:.2f}€"
            info += f"\n{trend_emoji.get(fib_data['trend'], '📊')} Tendance : {fib_data['trend'].upper()}"
            info += f"\n📈 Plus haut (50j) : {fib_data['high']:.2f}€"
            info += f"\n📉 Plus bas (50j) : {fib_data['low']:.2f}€"
            info += f"\n📏 Range : {fib_data['range']:.2f}€ ({(fib_data['range']/fib_data['current_price']*100):.1f}%)"
            
            # Position relative avec gestion d'erreur
            try:
                high = float(fib_data['high'])
                low = float(fib_data['low'])
                current = float(fib_data['current_price'])
                if high != low:
                    position_pct = ((current - low) / (high - low) * 100)
            except Exception as e:
                print(f"⚠️ Erreur calcul position relative: {e}")
        except Exception as e:
            return f"\n⚠️ Erreur formatage informations Fibonacci: {e}\n"
        
        info += "\n\n🎯 NIVEAUX DE RETRACEMENT FIBONACCI :"
        for name, level in fib_data["levels"].items():
            distance_pct = abs(level - fib_data['current_price']) / fib_data['range'] * 100
            marker = " ← 🎯 PRIX ACTUEL ICI" if distance_pct < 2 else ""
            info += f"\n  {name:15} : {level:.2f}€{marker}"
        
        if fib_data['trend'] == "haussier":
            info += "\n\n🚀 EXTENSIONS FIBONACCI (Objectifs haussiers) :"
            for name, level in fib_data["extensions"].items():
                gain = ((level - fib_data['current_price']) / fib_data['current_price']) * 100
                info += f"\n  {name:15} : {level:.2f}€ (+{gain:.1f}%)"
        
        info += "\n\n" + "-"*60
        info += "\n💡 RECOMMANDATIONS DE TRADING :"
        info += "\n" + "-"*60
        
        if analysis["support"]:
            distance = ((fib_data['current_price'] - analysis['support']) / analysis['support']) * 100
            info += f"\n🛡️  Support proche : {analysis['support']:.2f}€ ({analysis['support_name']}) [-{distance:.1f}%]"
        if analysis["resistance"]:
            distance = ((analysis['resistance'] - fib_data['current_price']) / fib_data['current_price']) * 100
            info += f"\n⚔️  Résistance proche : {analysis['resistance']:.2f}€ ({analysis['resistance_name']}) [+{distance:.1f}%]"
        
        entry_low, entry_high = analysis["entry_zone"]
        info += f"\n\n✅ Zone d'entrée recommandée : {entry_low:.2f}€ - {entry_high:.2f}€"
        
        # Indiquer si on est dans la zone
        if entry_low <= fib_data['current_price'] <= entry_high:
            info += " ✓ (DANS LA ZONE)"
        elif fib_data['current_price'] < entry_low:
            info += f" (attendre {((entry_low - fib_data['current_price'])/fib_data['current_price']*100):.1f}% de hausse)"
        else:
            info += f" (attendre {((fib_data['current_price'] - entry_high)/fib_data['current_price']*100):.1f}% de baisse)"
        
        info += f"\n🛑 Stop Loss recommandé : {analysis['stop_loss']:.2f}€"
        stop_distance = abs(fib_data['current_price'] - analysis['stop_loss']) / fib_data['current_price'] * 100
        info += f" ({stop_distance:.1f}% {'au-dessus' if analysis['stop_loss'] > fib_data['current_price'] else 'en dessous'})"
        
        if analysis["targets"]:
            info += "\n\n🎯 Objectifs de sortie :"
            for i, target in enumerate(analysis["targets"], 1):
                info += f"\n   Objectif {i} : {target['level']:.2f}€ ({target['name']})"
                info += f" | {target['type']} | Potentiel: {'+' if target['gain_potential'] > 0 else ''}{target['gain_potential']:.1f}%"
        
        if analysis["risk_reward"] and analysis["risk_reward"]["ratio"] > 0:
            rr = analysis["risk_reward"]
            info += f"\n\n⚖️  Ratio Risque/Récompense : 1:{rr['ratio']:.2f}"
            info += f"\n   💸 Risque : {rr['risk']:.2f}€ | 💰 Récompense : {rr['reward']:.2f}€"
            if rr['ratio'] >= 2:
                info += " ✅ Excellent"
            elif rr['ratio'] >= 1.5:
                info += " ✓ Bon"
            elif rr['ratio'] >= 1:
                info += " ~ Acceptable"
            else:
                info += " ⚠️ Défavorable"
        
        info += f"\n\n📝 {analysis['interpretation']}"
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