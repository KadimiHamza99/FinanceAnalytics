import argparse
from StockAnalyzer import StockAnalyzer
import os
from SendNotification import SendNotification

if __name__ == "__main__":

    # Liste par défaut si aucun ticker n'est fourni
    default_tickers = [
        "CS.PA"
    ]

    parser = argparse.ArgumentParser(description="Analyse des actions.")
    parser.add_argument(
        "tickers",
        nargs="*",
        default=default_tickers,
        help="Liste des tickers à analyser"
    )
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="Fichier contenant une liste de tickers (un par ligne)"
    )

    args = parser.parse_args()

    tickers = args.tickers

    # Si un fichier est fourni, on lit les tickers à partir de ce fichier
    if args.file:
        if os.path.exists(args.file):
            with open(args.file, "r", encoding="utf-8") as f:
                file_tickers = [
                    line.strip() for line in f.readlines()
                    if line.strip() and not line.startswith("#")
                ]
                tickers = file_tickers
        else:
            print(f"⚠️ Fichier '{args.file}' introuvable, utilisation des tickers par défaut.")

    app = StockAnalyzer(tickers)

    app.run()
    