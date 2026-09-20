import argparse
import os
import sys

from StockAnalyzer import StockAnalyzer


DEFAULT_TICKERS = ("CS.PA",)


def configure_console_encoding():
    """Configure UTF-8 when the current terminal supports ``reconfigure``."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            pass


def build_parser():
    """Create the command-line parser used by the application."""
    parser = argparse.ArgumentParser(
        description="Analyse fondamentale et technique d'actions."
    )
    parser.add_argument(
        "tickers",
        nargs="*",
        default=list(DEFAULT_TICKERS),
        help="Liste des tickers à analyser",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="Fichier contenant un ticker par ligne (les lignes # sont ignorées)",
    )
    return parser


def load_tickers_from_file(path):
    """Read non-empty ticker symbols from ``path``."""
    with open(path, "r", encoding="utf-8") as ticker_file:
        return [
            line.strip()
            for line in ticker_file
            if line.strip() and not line.lstrip().startswith("#")
        ]


def resolve_tickers(cli_tickers, file_path=None):
    """Resolve CLI/file input while preserving the default fallback."""
    if not file_path:
        return cli_tickers

    if not os.path.exists(file_path):
        print(
            f"⚠️ Fichier '{file_path}' introuvable, "
            "utilisation des tickers fournis par défaut."
        )
        return cli_tickers

    tickers = load_tickers_from_file(file_path)
    return tickers or cli_tickers


def main():
    """Parse arguments and launch the portfolio analysis."""
    configure_console_encoding()
    args = build_parser().parse_args()
    StockAnalyzer(resolve_tickers(args.tickers, args.file)).run()


if __name__ == "__main__":
    main()
