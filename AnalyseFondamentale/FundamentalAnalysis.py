import yfinance as yf
import pandas as pd
from colorama import Fore
from Formatter import Formatter 
from AnalyseFondamentale.IndicatorInterpreter import IndicatorInterpreter
from AnalyseFondamentale.Utils import Utils

import warnings
warnings.filterwarnings('ignore')

class FundamentalAnalysis:
    """
    Classe réalisant une analyse fondamentale complète sur un ticker boursier.
    Calcule différents indicateurs avec des poids adaptés au secteur d'activité.
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
        data = []

################### PRINT BRUT DATA #########################
        # Utils.print_yfinance_brut_data(self.info)
#############################################################


################### PRINT COMPANY DATA ###########################
        Utils.print_company_info(self.info, self.ticker_symbol)
##################################################################
        
        # Récupère les poids selon le secteur
        weights = Utils.get_sector_weights(self.sector)

        # === ROE === (PLUS DE CATÉGORIES)
        roe = info.get("returnOnEquity")
        note, interp = self.interpreter.interpret_roe(roe, self.sector)
        Utils.add_indicator(data, weights, "ROE", f.format_pourcentage(roe), note, interp, 
            "Return on Equity - Mesure combien de profit une entreprise génère pour chaque euro investi par les actionnaires",
            "Rentabilité des capitaux propres")

        # === ROA === (PLUS DE CATÉGORIES)
        roa = info.get("returnOnAssets")
        note, interp = self.interpreter.interpret_roa(roa, self.sector)
        Utils.add_indicator(data, weights,"ROA", f.format_pourcentage(roa), note, interp, 
            "Return on Assets - Indique l'efficacité de l'entreprise à utiliser ses actifs pour générer du profit",
            "Rentabilité par rapport aux actifs")

        # === Forward P/E === (PLUS DE CATÉGORIES)
        forward_pe = info.get("forwardPE")
        note, interp = self.interpreter.interpret_forward_pe(forward_pe, self.sector)
        if(forward_pe == None) : forward_pe = "N/A"
        else: forward_pe = f"{forward_pe:.1f}x"
        Utils.add_indicator(data, weights,"Forward P/E",forward_pe,note,interp,
            "Ratio cours/bénéfices anticipé pour l'année suivante",
            "Valorisation future anticipée de l'action"
        )
        
        # === Trailing PE === (PLUS DE CATÉGORIES)
        trailing_pe = info.get("trailingPE")
        note, interp = self.interpreter.interpret_trailing_pe(trailing_pe, self.sector)
        Utils.add_indicator(data, weights,"Trailing PE", f"{trailing_pe:.2f}" if trailing_pe else "N/A", note, interp,
            "Price to Earnings Ratio basé sur les bénéfices des 12 derniers mois - Mesure la valorisation actuelle par rapport aux performances passées",
            "PER sur 12 mois")

        # === Beta === (PLUS DE CATÉGORIES)
        beta = info.get("beta")
        note, interp = self.interpreter.interpret_beta(beta, self.sector)
        Utils.add_indicator(data, weights,"Beta", f"{beta:.2f}" if beta else "N/A", note, interp,
            "Beta - Mesure la volatilité de l'action par rapport au marché (indice de référence S&P 500). "
            "Un beta de 1 signifie une volatilité égale au marché, <1 moins volatile, >1 plus volatile",
            "Volatilité par rapport au marché")

        # === Price to Book === (PLUS DE CATÉGORIES)
        pb = info.get("priceToBook")
        note, interp = self.interpreter.interpret_price_to_book(pb, self.sector)
        Utils.add_indicator(data, weights,"Price to Book", f"{pb:.2f}" if pb else "N/A", note, interp, 
            "Price to Book Ratio - Compare la valeur de marché de l'entreprise à sa valeur comptable",
            "Prix vs valeur comptable")

        # === Dette / Equity === (PLUS DE CATÉGORIES)
        debt = info.get("debtToEquity")
        note, interp = self.interpreter.interpret_debt_to_equity(debt, self.sector)
        Utils.add_indicator(data, weights,"Dette/Equity", f"{debt:.2f}" if debt else "N/A", note, interp, 
            "Debt to Equity Ratio - Mesure le niveau d'endettement par rapport aux capitaux propres",
            "Niveau d'endettement")

        # === Current Ratio === (PLUS DE CATÉGORIES)
        current_ratio = info.get("currentRatio")
        note, interp = self.interpreter.interpret_current_ratio(current_ratio, self.sector)
        Utils.add_indicator(data, weights,"Current Ratio", f"{current_ratio:.2f}" if current_ratio else "N/A", note, interp, 
            "Ratio de liquidité générale - Capacité de l'entreprise à rembourser ses dettes à court terme avec ses actifs à court terme",
            "Liquidité à court terme")

        # === Marge nette === (PLUS DE CATÉGORIES)
        marg = info.get("profitMargins")
        note, interp = self.interpreter.interpret_profit_margin(marg, self.sector)
        Utils.add_indicator(data, weights,"Marge nette", f.format_pourcentage(marg), note, interp, 
            "Profit Margin - Pourcentage du chiffre d'affaires qui reste en bénéfice net après toutes les dépenses",
            "Profit sur les ventes")

        # === Free Cash Flow Yield === (PLUS DE CATÉGORIES)
        fcf = info.get("freeCashflow")
        market_cap = info.get("marketCap")
        if fcf and market_cap and market_cap > 0:
            fcf_yield = fcf / market_cap
            note, interp = self.interpreter.interpret_fcf_yield(fcf_yield, self.sector)
            Utils.add_indicator(data, weights,"FCF Yield", f.format_pourcentage(fcf_yield), note, interp, 
                "Free Cash Flow Yield - Rendement du flux de trésorerie libre par rapport à la capitalisation boursière, indicateur de cash disponible",
                "Rendement du cash disponible")

        # === Avis des Analystes === (PLUS DE CATÉGORIES)
        rec_mean = info.get("recommendationMean")
        num_analysts = info.get("numberOfAnalystOpinions", 0)
        grade_str, note, interp = self.interpreter.interpret_analyst_rating(rec_mean, num_analysts, self.sector)
        Utils.add_indicator(data, weights,"Avis Analystes",grade_str,note,interp,
            "Note moyenne des recommandations des analystes",
            "Recommandation des experts")

        # === Dividend Yield === (PLUS DE CATÉGORIES)
        div = info.get("dividendYield")
        div_value = div if isinstance(div, (int, float)) else None
        note, interp = self.interpreter.interpret_dividend_yield(div_value, self.sector)
        Utils.add_indicator(data, weights,"Dividend Yield", f"{div_value:.2f}%" if div else "N/A", note, interp, 
            "Rendement du dividende - Dividende annuel divisé par le prix de l'action, montre le revenu généré par l'investissement",
            "Rendement annuel du dividende")

        # === Payout Ratio === (PLUS DE CATÉGORIES)
        payout = info.get("payoutRatio")
        note, interp = self.interpreter.interpret_payout_ratio(payout, self.sector)
        Utils.add_indicator(data, weights,"Payout ratio", f.format_pourcentage(payout), note, interp, 
            "Pourcentage des bénéfices distribués aux actionnaires sous forme de dividendes, indique la soutenabilité des paiements",
            "Part des bénéfices distribuée")

        # === Position 52 semaines === (PLUS DE CATÉGORIES)
        current_price = info.get("regularMarketPrice")
        low_52w = info.get("fiftyTwoWeekLow")
        high_52w = info.get("fiftyTwoWeekHigh")
        if current_price and low_52w and high_52w and high_52w != low_52w:
            position, note, interp = self.interpreter.interpret_52w_position(current_price, low_52w, high_52w, self.sector)
            Utils.add_indicator(data, weights,"Position 52W", f"{position:.1f}%", note, interp, 
                "Position du prix actuel par rapport aux plus haut et plus bas sur 52 semaines, indique si l'action est chère ou bon marché",
                "Cours par rapport au range annuel")

        # === Score global ===
        df = pd.DataFrame(data)
        df["Score pondéré"] = df["Note (/10)"] * df["Poids (%)"] / 10
        score_total = df["Score pondéré"].sum()

        return df, score_total