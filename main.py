import argparse
from StockAnalyzer import StockAnalyzer

if __name__ == "__main__":
    # Liste par défaut si aucun ticker n'est fourni
    default_tickers = ["CS.PA", "ALV.DE"]

    parser = argparse.ArgumentParser(description="Analyse des actions.")
    parser.add_argument(
        "tickers",
        nargs="*",  # 0 ou plusieurs tickers
        default=default_tickers,
        help="Liste des tickers à analyser"
    )
    args = parser.parse_args()
    
    app = StockAnalyzer(args.tickers)
    app.run()