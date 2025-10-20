import yfinance as yf
import pandas as pd
from colorama import Fore
from Formatter import Formatter  # <-- Assure-toi d’avoir la classe Formatter définie ou importée

class FundamentalAnalysis:
    """
    Classe réalisant une analyse fondamentale complète sur un ticker boursier.
    Calcule différents indicateurs (ROE, PER, PEG, etc.) et renvoie un DataFrame avec un score global.
    """

    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol
        self.ticker = yf.Ticker(ticker_symbol)
        self.info = self.ticker.info
        self.formatter = Formatter()

    def run(self):
        info = self.info
        f = self.formatter
        data = []

        def add(nom, val, note, interp, defn, poids):
            data.append({
                "Indicateur": nom,
                "Valeur": val,
                "Note (/10)": note,
                "Poids (%)": poids,
                "Interprétation": interp,
                "Définition": defn
            })

        # === ROE ===
        roe = info.get("returnOnEquity")
        if roe:
            if roe > 0.20: note, interp = 9, "Excellente rentabilité"
            elif roe > 0.12: note, interp = 7, "Bonne rentabilité"
            elif roe > 0.07: note, interp = 5, "Rentabilité moyenne"
            else: note, interp = 3, "Rentabilité faible"
        else:
            note, interp = 3, "Données indisponibles"
        add("ROE", f.format_pourcentage(roe), note, interp, "Rentabilité du capital", 18)

        # === PEG Ratio ===
        peg = info.get("pegRatio")
        if peg:
            if peg < 1: note, interp = 9, "Croissance sous-évaluée 🚀"
            elif peg < 1.5: note, interp = 7, "Croissance correcte"
            elif peg < 2: note, interp = 5, "Croissance chère"
            else: note, interp = 3, "Surévaluation par rapport à la croissance"
        else:
            note, interp = 4, "Données insuffisantes"
        add("PEG Ratio", f"{peg:.2f}" if peg else "N/A", note, interp, "Valorisation ajustée à la croissance", 8)

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
            note, interp = 3, "Données insuffisantes"
        add("Croissance attendue (Fwd PE)", f.format_pourcentage(ratio), note, interp,
            "Estimation croissance via Forward PE", 15)

        # === PER ===
        if pe:
            if pe < 8: note, interp = 9, "Très sous-évaluée 💎"
            elif pe < 12: note, interp = 8, "Sous-évaluée ✅"
            elif pe < 20: note, interp = 6, "Valorisation correcte 👌"
            elif pe < 25: note, interp = 4, "Légèrement chère ⚠️"
            else: note, interp = 2, "Surévaluée 🚨"
        else:
            note, interp = 3, "Données indisponibles"
        add("PER", f"{pe:.2f}" if pe else "N/A", note, interp, "Prix par rapport au bénéfice", 10)

        # === Dette / Equity ===
        debt = info.get("debtToEquity")
        if debt is not None:
            if debt < 40: note, interp = 9, "Faible endettement 🛡️"
            elif debt < 100: note, interp = 6, "Endettement raisonnable 🙂"
            elif debt < 150: note, interp = 4, "Endettement élevé 😟"
            else: note, interp = 2, "Très endettée 🛑"
        else:
            note, interp = 3, "Données indisponibles"
        add("Dette/Equity", f"{debt:.2f}" if debt else "N/A", note, interp, "Niveau d’endettement", 8)

        # === Marge nette ===
        marg = info.get("profitMargins")
        if marg:
            if marg > 0.15: note, interp = 9, "Marge élevée ✨"
            elif marg > 0.08: note, interp = 6, "Marge correcte 👍"
            elif marg > 0.05: note, interp = 4, "Marge faible 🤏"
            else: note, interp = 2, "Marge très faible 😥"
        else:
            note, interp = 3, "Données indisponibles"
        add("Marge nette", f.format_pourcentage(marg), note, interp, "Bénéfice sur ventes", 10)

        # === Free Cash Flow Margin ===
        fcf = info.get("freeCashflow")
        revenue = info.get("totalRevenue")
        if fcf and revenue and revenue != 0:
            fcf_margin = fcf / revenue
            if fcf_margin > 0.15: note, interp = 9, "Très bonne génération de cash 🔥"
            elif fcf_margin > 0.08: note, interp = 7, "Bonne génération de cash"
            elif fcf_margin > 0.04: note, interp = 5, "Moyenne"
            else: note, interp = 3, "Faible flux de trésorerie"
            add("Free Cash Flow Margin", f.format_pourcentage(fcf_margin), note, interp, "Rentabilité du cash flow", 10)

        # === Dividend Yield ===
        div = info.get("dividendYield")
        if div:
            if div > 0.06: note, interp = 6, "Rendement élevé (attention soutenabilité)"
            elif div > 0.03: note, interp = 8, "Bon rendement 💰"
            elif div > 0.01: note, interp = 5, "Rendement modeste"
            else: note, interp = 3, "Rendement faible"
        else:
            note, interp = 3, "Pas de dividende 🚫"
        add("Dividend Yield", f.format_pourcentage(div), note, interp, "Dividende annuel", 6)

        # === Payout Ratio ===
        payout = info.get("payoutRatio")
        if payout is not None:
            if 0.3 <= payout <= 0.6: note, interp = 9, "Distribution équilibrée ✅"
            elif payout <= 0.9: note, interp = 6, "Distribution élevée ⬆️"
            elif payout > 1: note, interp = 2, "Non soutenable 🚨"
            else: note, interp = 4, "Distribution trop faible ⬇️"
        else:
            note, interp = 3, "Données indisponibles"
        add("Payout ratio", f.format_pourcentage(payout), note, interp, "Part du bénéfice versé", 5)

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
            add("Position 52W", f"{position:.2f}%", note, interp, "Cours relatif à son range annuel", 10)

        # === Score global ===
        df = pd.DataFrame(data)
        df["Score pondéré"] = df["Note (/10)"] * df["Poids (%)"] / 10
        score_total = df["Score pondéré"].sum()

        return df, score_total
