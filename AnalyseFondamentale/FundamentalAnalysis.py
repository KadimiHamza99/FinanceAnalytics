import yfinance as yf
import pandas as pd
from colorama import Fore
from Formatter import Formatter 
from AnalyseFondamentale.IndicatorInterpreter import IndicatorInterpreter
from AnalyseFondamentale.Utils import Utils
import math

import warnings
warnings.filterwarnings('ignore')

class FundamentalAnalysis:
    """
    Classe réalisant une analyse fondamentale complète sur un ticker boursier.
    Calcule différents indicateurs classés par catégories :
    - Rentabilité
    - Liquidité
    - Solvabilité
    - Valorisation
    - Risque & Marché
    """

    def __init__(self, ticker_symbol):
        self.ticker_symbol = ticker_symbol
        self.ticker = yf.Ticker(ticker_symbol)
        self.info = self.ticker.info
        self.formatter = Formatter()
        self.sector = self.info.get('sector', 'Général')
        self.interpreter = IndicatorInterpreter()

    def run(self):
        info = self.info
        f = self.formatter
        
        # Dictionnaire pour stocker les données par catégorie
        data_by_category = {
            "Rentabilité": [],
            "Liquidité": [],
            "Solvabilité": [],
            "Valorisation": [],
            "Risque & Marché": []
        }

################### PRINT BRUT DATA #########################
        # Utils.print_yfinance_brut_data(self.info)
#############################################################

################### PRINT COMPANY DATA ###########################
        Utils.print_company_info(self.info, self.ticker_symbol)
##################################################################
        
        # Récupère les poids selon le secteur
        weights = Utils.get_sector_weights(self.sector)

        # ==================== RENTABILITÉ ====================
        
        # === ROE ===
        roe = info.get("returnOnEquity")
        note, interp = self.interpreter.interpret_roe(roe, self.sector)
        Utils.add_indicator(data_by_category["Rentabilité"], weights, "ROE", 
            f.format_pourcentage(roe), note, interp, 
            "Return on Equity - Rentabilité des capitaux propres",
            "Profit généré par euro investi")

        # === ROA ===
        roa = info.get("returnOnAssets")
        note, interp = self.interpreter.interpret_roa(roa, self.sector)
        Utils.add_indicator(data_by_category["Rentabilité"], weights, "ROA", 
            f.format_pourcentage(roa), note, interp, 
            "Return on Assets - Efficacité d'utilisation des actifs",
            "Rentabilité par rapport aux actifs")

        # === Marge nette ===
        marg = info.get("profitMargins")
        note, interp = self.interpreter.interpret_profit_margin(marg, self.sector)
        Utils.add_indicator(data_by_category["Rentabilité"], weights, "Marge nette", 
            f.format_pourcentage(marg), note, interp, 
            "Pourcentage du CA restant en bénéfice net",
            "Profit sur les ventes")

        # === Marge opérationnelle ===
        op_margin = info.get("operatingMargins")
        note, interp = self.interpreter.interpret_operating_margin(op_margin, self.sector)
        Utils.add_indicator(data_by_category["Rentabilité"], weights, "Marge opérationnelle", 
            f.format_pourcentage(op_margin), note, interp, 
            "Rentabilité avant charges financières et impôts",
            "Efficacité opérationnelle")

        # === Marge brute === (surtout pour Energy)
        if self.sector in ['Energy', 'Consumer Cyclical', 'Consumer Defensive', 'Basic Materials']:
            gross_margin = info.get("grossMargins")
            note, interp = self.interpreter.interpret_gross_margin(gross_margin, self.sector)
            Utils.add_indicator(data_by_category["Rentabilité"], weights, "Marge brute", 
                f.format_pourcentage(gross_margin), note, interp, 
                "Profit brut après coût des ventes",
                "Marge avant frais d'exploitation")

        # === Croissance des bénéfices ===
        earnings_growth = info.get("earningsGrowth")
        note, interp = self.interpreter.interpret_earnings_growth(earnings_growth, self.sector)
        Utils.add_indicator(data_by_category["Rentabilité"], weights, "Croissance bénéfices", 
            f.format_pourcentage(earnings_growth), note, interp, 
            "Évolution des bénéfices sur 1 an",
            "Dynamique de croissance")

        # === Free Cash Flow Yield ===
        fcf = info.get("freeCashflow")
        market_cap = info.get("marketCap")
        if fcf and market_cap and market_cap > 0:
            fcf_yield = fcf / market_cap
            note, interp = self.interpreter.interpret_fcf_yield(fcf_yield, self.sector)
            Utils.add_indicator(data_by_category["Rentabilité"], weights, "FCF Yield", 
                f.format_pourcentage(fcf_yield), note, interp, 
                "Rendement du cash-flow libre",
                "Cash disponible vs valorisation")

        # ==================== LIQUIDITÉ ====================
        
        # === Current Ratio ===
        current_ratio = info.get("currentRatio")
        note, interp = self.interpreter.interpret_current_ratio(current_ratio, self.sector)
        Utils.add_indicator(data_by_category["Liquidité"], weights, "Current Ratio", 
            f"{current_ratio:.2f}" if current_ratio else "N/A", note, interp, 
            "Capacité à rembourser dettes court terme",
            "Liquidité générale")

        # === Quick Ratio ===
        quick_ratio = info.get("quickRatio")
        note, interp = self.interpreter.interpret_quick_ratio(quick_ratio, self.sector)
        Utils.add_indicator(data_by_category["Liquidité"], weights, "Quick Ratio", 
            f"{quick_ratio:.2f}" if quick_ratio else "N/A", note, interp, 
            "Liquidité immédiate (sans stocks)",
            "Test de liquidité stricte")

        # === Operating Cash Flow ===
        op_cashflow = info.get("operatingCashflow")
        current_liabilities = info.get("totalCurrentLiabilities")
        if op_cashflow and current_liabilities and current_liabilities > 0:
            ocf_ratio = op_cashflow / current_liabilities
            note, interp = self.interpreter.interpret_ocf_ratio(ocf_ratio, self.sector)
            Utils.add_indicator(data_by_category["Liquidité"], weights, "Operating Cash Flow", 
                f"{ocf_ratio:.2f}" if ocf_ratio else "N/A", note, interp, 
                "Cash opérationnel vs dettes court terme",
                "Flux de trésorerie opérationnel")

                # ==================== SOLVABILITÉ ====================
        
        # === Dette / Equity ===
        debt = info.get("debtToEquity")
        note, interp = self.interpreter.interpret_debt_to_equity(debt, self.sector)
        Utils.add_indicator(data_by_category["Solvabilité"], weights, "Dette/Equity", 
            f"{debt:.2f}" if debt else "N/A", note, interp, 
            "Endettement vs capitaux propres",
            "Levier financier")

        # === Dette / EBITDA ===
        total_debt = info.get("totalDebt")
        ebitda = info.get("ebitda")
        if total_debt and ebitda and ebitda > 0:
            debt_ebitda = total_debt / ebitda
            note, interp = self.interpreter.interpret_debt_ebitda(debt_ebitda, self.sector)
            Utils.add_indicator(data_by_category["Solvabilité"], weights, "Dette/EBITDA", 
                f"{debt_ebitda:.2f}x" if debt_ebitda else "N/A", note, interp, 
                "Années nécessaires pour rembourser la dette",
                "Capacité de remboursement")

        # === Total Debt / Total Assets (Ratio d'endettement) ===
        total_assets = info.get("totalAssets")
        if total_debt and total_assets and total_assets > 0:
            debt_to_assets = total_debt / total_assets
            note, interp = self.interpreter.interpret_debt_to_assets(debt_to_assets, self.sector)
            Utils.add_indicator(data_by_category["Solvabilité"], weights, "Dette/Actifs", 
                f"{debt_to_assets*100:.1f}%" if debt_to_assets else "N/A", note, interp, 
                "Part des actifs financée par la dette",
                "Taux d'endettement global")

        # === Book Value (Valeur comptable par action) ===
        book_value = info.get("bookValue")
        current_price = info.get("currentPrice") or info.get("regularMarketPrice")
        if book_value and current_price and book_value > 0:
            note, interp = self.interpreter.interpret_book_value(book_value, current_price, self.sector)
            Utils.add_indicator(data_by_category["Solvabilité"], weights, "Valeur comptable", 
                f"{book_value:.2f}€" if book_value else "N/A", note, interp, 
                "Valeur nette par action",
                "Matelas de sécurité")

        # === Interest Coverage (Couverture des intérêts) ===
        ebit = info.get("ebit")
        interest_expense = info.get("interestExpense")
        if ebit and interest_expense and interest_expense != 0:
            # interestExpense est souvent négatif dans yfinance, on prend la valeur absolue
            interest_coverage = ebit / abs(interest_expense)
            note, interp = self.interpreter.interpret_interest_coverage(interest_coverage, self.sector)
            Utils.add_indicator(data_by_category["Solvabilité"], weights, "Couverture intérêts", 
                f"{interest_coverage:.2f}x" if interest_coverage else "N/A", note, interp, 
                "Capacité à payer les intérêts de la dette",
                "Solvabilité à court terme")

        # === Equity Ratio (Ratio de capitaux propres) ===
        total_assets = info.get("totalAssets")
        stockholder_equity = info.get("totalStockholderEquity")
        if total_assets and stockholder_equity and total_assets > 0:
            equity_ratio = stockholder_equity / total_assets
            note, interp = self.interpreter.interpret_equity_ratio(equity_ratio, self.sector)
            Utils.add_indicator(data_by_category["Solvabilité"], weights, "Equity Ratio", 
                f"{equity_ratio*100:.1f}%" if equity_ratio else "N/A", note, interp, 
                "Part des actifs financée par capitaux propres",
                "Indépendance financière")

        # ==================== VALORISATION ====================
        
        # === Forward P/E ===
        sector = self.sector
        forward_pe = info.get("forwardPE")
        if forward_pe is None:
            current_price = info.get("currentPrice")
            trailing_eps = info.get("trailingEps")
            earnings_growth = info.get("earningsGrowth")
            if (current_price is not None and trailing_eps is not None and earnings_growth is not None
                and trailing_eps != 0 and (current_price > 0)):                
                try:
                    forward_eps_estimated = trailing_eps * (1 + earnings_growth)
                    if forward_eps_estimated > 0:
                        forward_pe = current_price / forward_eps_estimated
                    else:
                        forward_pe = None 
                except (TypeError, ZeroDivisionError):
                    forward_pe = None 
        note = 3
        interp = "Donnée non disponible ou non calculable."

        if forward_pe is not None and isinstance(forward_pe, (int, float)) and math.isfinite(forward_pe) and forward_pe > 0:
            note, interp = self.interpreter.interpret_forward_pe(forward_pe, sector)
            forward_pe_display = f"{forward_pe:.1f}x"
        else:
            forward_pe_display = "N/A"

        Utils.add_indicator(data_by_category["Valorisation"], weights, "Forward P/E", 
            forward_pe_display, note, interp,
            "Valorisation future anticipée",
            "PER prévisionnel")
        
        # === Trailing PE ===
        trailing_pe = info.get("trailingPE")
        note, interp = self.interpreter.interpret_trailing_pe(trailing_pe, self.sector)
        Utils.add_indicator(data_by_category["Valorisation"], weights, "Trailing PE", 
            f"{trailing_pe:.2f}" if trailing_pe else "N/A", note, interp,
            "Valorisation sur bénéfices passés",
            "PER sur 12 mois")

        # === Price to Book ===
        pb = info.get("priceToBook")
        note, interp = self.interpreter.interpret_price_to_book(pb, self.sector)
        Utils.add_indicator(data_by_category["Valorisation"], weights, "Price to Book", 
            f"{pb:.2f}" if pb else "N/A", note, interp, 
            "Prix vs valeur comptable",
            "Valorisation des actifs")

        # === PEG Ratio ===
        peg = info.get("trailingPegRatio")
        note, interp = self.interpreter.interpret_peg_ratio(peg, self.sector)
        Utils.add_indicator(data_by_category["Valorisation"], weights, "PEG Ratio", 
            f"{peg:.2f}" if peg else "N/A", note, interp, 
            "PER ajusté de la croissance",
            "Valorisation vs croissance")

        # === Dividend Yield ===
        div = info.get("dividendYield")
        div_value = div if isinstance(div, (int, float)) else None
        note, interp = self.interpreter.interpret_dividend_yield(div_value, self.sector)
        Utils.add_indicator(data_by_category["Valorisation"], weights, "Dividend Yield", 
            f"{div_value:.2f}%" if div_value else "N/A", note, interp, 
            "Rendement du dividende annuel",
            "Revenu passif")

        # === Payout Ratio ===
        payout = info.get("payoutRatio")
        note, interp = self.interpreter.interpret_payout_ratio(payout, self.sector)
        Utils.add_indicator(data_by_category["Valorisation"], weights, "Payout ratio", 
            f.format_pourcentage(payout), note, interp, 
            "Part des bénéfices distribuée",
            "Soutenabilité du dividende")

        # ==================== RISQUE & MARCHÉ ====================
        
        # === Beta ===
        beta = info.get("beta")
        note, interp = self.interpreter.interpret_beta(beta, self.sector)
        Utils.add_indicator(data_by_category["Risque & Marché"], weights, "Beta", 
            f"{beta:.2f}" if beta else "N/A", note, interp,
            "Volatilité vs marché",
            "Risque systématique")

        # === Position 52 semaines ===
        current_price = info.get("regularMarketPrice")
        low_52w = info.get("fiftyTwoWeekLow")
        high_52w = info.get("fiftyTwoWeekHigh")
        if current_price and low_52w and high_52w and high_52w != low_52w:
            position, note, interp = self.interpreter.interpret_52w_position(current_price, low_52w, high_52w, self.sector)
            Utils.add_indicator(data_by_category["Risque & Marché"], weights, "Position 52W", 
                f"{position:.1f}%", note, interp, 
                "Position dans le range annuel",
                "Momentum prix")

        # === Avis des Analystes ===
        rec_mean = info.get("recommendationMean")
        num_analysts = info.get("numberOfAnalystOpinions", 0)
        grade_str, note, interp = self.interpreter.interpret_analyst_rating(rec_mean, num_analysts, self.sector)
        Utils.add_indicator(data_by_category["Risque & Marché"], weights, "Avis Analystes",
            grade_str, note, interp,
            "Consensus des analystes",
            "Recommandation moyenne")

        # === Calcul du score global par catégorie et total ===
        scores_by_category = {}
        all_data = []
        
        for category, data in data_by_category.items():
            if data:
                df_cat = pd.DataFrame(data)
                df_cat["Score pondéré"] = df_cat["Note (/10)"] * df_cat["Poids (%)"] / 10
                score_cat = df_cat["Score pondéré"].sum()
                
                # Normalisation sur 100 : (score obtenu / poids total de la catégorie) * 100
                total_weight_category = df_cat["Poids (%)"].sum()
                if total_weight_category > 0:
                    score_cat_normalized = (score_cat / total_weight_category) * 100
                else:
                    score_cat_normalized = 0
                
                scores_by_category[category] = score_cat_normalized
                all_data.extend(data)
        
        # Calcul du score total normalisé
        df_complete = pd.DataFrame(all_data)
        df_complete["Score pondéré"] = df_complete["Note (/10)"] * df_complete["Poids (%)"] / 10
        
        # Normalisation du score total sur 100
        total_weight_used = df_complete["Poids (%)"].sum()
        score_total_brut = df_complete["Score pondéré"].sum()
        
        if total_weight_used > 0:
            score_total = (score_total_brut / total_weight_used) * 100
        else:
            score_total = 0

        return data_by_category, df_complete, score_total, info.get("shortName") or info.get("longName"), info.get("marketCap", None), scores_by_category